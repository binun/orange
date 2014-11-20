/**
 * section: Scheduling
 * synopsis: Suspend a domain and then resume its execution
 * purpose: Demonstrate the basic use of the library to suspend and
 *          resume a domain. If no id is given on the command line
 *          this script will suspend and resume the first domain found
 *          which is not Domain 0.
 * usage: suspend [id]
 * test: suspend
 * author: Daniel Veillard
 * copy: see Copyright for the status of this software.
 */
#define _GNU_SOURCE
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <signal.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <memory.h>
#include <dirent.h>
#include <unistd.h>

#include <libvirt/libvirt.h>
#include <libxml/parser.h>
#include <libxml/tree.h>
#include <libvmi/libvmi.h>

#define SIG_VMREBOOT 33
#define SIG_VMUPDATE 34

#define LINUX_OS "Linux"
#define CONFFILE "/etc/libvmi.conf"
#define MAX_DOMAINS 10

typedef struct tagVMPID
{
	int pid;
	virDomainPtr dom;
	char ip[20];
} VMPID;

static virConnectPtr conn = NULL; /* the hypervisor connection */
static char *sm_drv = "/dev/sm_channel";
static char *guestdir="/var/run/libvirt/qemu";
static int sm_channel;
static VMPID vms[MAX_DOMAINS];
static int pid;
static int numDomains;

static int runShell(char *cmd, char *result, int limitResult)
{
	FILE *fp;
	int status;

	fp = popen(cmd, "r");
	if (fp == NULL)
	{
		printf("The pipe to %s cannot be opened\n", cmd);
		return -1;
	}

	while (fgets(result, limitResult, fp) != NULL)
	    printf("%s", result);

	status = pclose(fp);
	if (status == -1)
	{
		printf("The pipe to %s cannot be closed\n", cmd);
	    return -1;
	}
	else
	{
		printf("%d,%d,%d\n",status, WIFEXITED(status), WEXITSTATUS(status));
	    /* Use macros described under wait() to inspect `status' in order
	       to determine success/failure of command executed by popen() */

	}
	return 0;
}

static int initVMIFile(int numDomains, char *sysmapName)
{
	FILE *confFile;
	int i;

	confFile = fopen(CONFFILE, "wt");
	if (!confFile)
	{
		printf("Cannot set up the VMI configuration file");
		return 0;
	}

	for (i=0;i<numDomains;i++)
	{
	   VMPID *vmEntry = vms + i;
	   int nb, pid = vmEntry->pid;
	   char *vmName = virDomainGetName(vmEntry->dom);
       char command[30] = "", vmdata[200] = "";

	   fprintf(confFile, "%s {\n",vmName);                      //vmname
	   fprintf(confFile,"    sysmap = \"%s\";\n", sysmapName); //system map file
	   fprintf(confFile,"    ostype = \"%s\";\n", LINUX_OS);   //OS Type

	   sprintf(command, "VMPid:%d", pid);
	   nb = write(sm_channel, command, strlen(command));
	   printf("Requesting parameters for VM %s -  written %d bytes\n", command, nb);

	   if (read(sm_channel,vmdata,200)!=0)
	   	{
		   printf("Got parameters for VM %s\n", vmdata);
		   fprintf(confFile, "%s", vmdata);
		   //fprintf(confFile, "   pid = %d\n", pid);
	   	}
	   fprintf(confFile, "}\n");
	}

	fclose(confFile);
	return 1;
}

static void find_pid(xmlNode * a_node)
{
    xmlNode *cur_node = NULL;
    xmlChar *uri;

    for (cur_node = a_node; cur_node; cur_node = cur_node->next) 
    {
      if (cur_node->type == XML_ELEMENT_NODE && !strcmp((char*)cur_node->name, "vcpu"))
        {      
          uri = xmlGetProp(cur_node, (xmlChar*)"pid");
          //printf("uri: %s\n", uri);
          if (!pid)
            pid=atoi((char*)uri);
	      xmlFree(uri);
	    }
      find_pid(cur_node->children); 
    }
}

static void parseVM(char*vmname)
{
	xmlDoc *doc = NULL;
	xmlNode *root_element = NULL;
	doc = xmlReadFile(vmname, NULL, 0);

	if (doc == NULL)
	{
	  printf("Could not parse VM metamodel %s\n", vmname);
	  return;
	}

	root_element = xmlDocGetRootElement(doc);
	find_pid(root_element);
    //if (pid>0) printf("Found pid %d\n", pid);
	xmlFreeDoc(doc);
	xmlCleanupParser();
}

static void examineVM(char *vmname)
{
	char fullname[100] = "";
	struct stat sts;

	strcpy(fullname,guestdir);
	strcat(fullname,"/");
	strcat(fullname,vmname);
	strcat(fullname, ".xml");

	if (stat(fullname, &sts) == -1)
	{
	   printf ("The VM runtime file %s doesn't exist\n", fullname);
	   return;
	}

	//printf("Examining the VM runtime file %s \n", fullname);
	parseVM(fullname);
}

static int isActiveDomain(virDomainPtr dom)
{
    virDomainInfo info;        /* the information being fetched */
    int ret;

    ret = virDomainGetInfo(dom, &info);
    if (ret < 0)
        return -1;
    //if (ret==VIR_DOMAIN_RUNNING)
    if ((ret == VIR_DOMAIN_RUNNING) || (ret == VIR_DOMAIN_NOSTATE) || (ret == VIR_DOMAIN_BLOCKED))
     return 1;
    else
    return 0;
}

static void refreshDomains(void)
{
	int i,*activeDomains;
	char *domName;
	char shc[50];

	for (i=0; i<MAX_DOMAINS;i++)
	{
		vms[i].dom = NULL;
        vms[i].pid = -1;
        memset(vms[i].ip,0,20*sizeof(char));
	}

	numDomains = virConnectNumOfDomains(conn);
    activeDomains = malloc(sizeof(int) * numDomains);
    numDomains = virConnectListDomains(conn, activeDomains, numDomains);

	if (numDomains==0)
	{
		printf("No active VMs\n");
		return -1;
	}

	for (i = 0 ; i < numDomains ; i++)
	{
		memset(shc,0,50*sizeof(char));

	    vms[i].dom = virDomainLookupByID(conn, activeDomains[i]);
	    domName = virDomainGetName(vms[i].dom);
	    sprintf(shc,"./vm-ip.sh %s", domName);
        pid=0;
	    examineVM(domName);
        vms[i].pid=pid;
        runShell(shc, vms[i].ip, 20);
        printf("Process %d runs the virtual machine %s on IP %s\n ", vms[i].pid, domName, vms[i].ip);
	}
	printf("\n");
    //initVMIFile(numDomains, sysmap);
	free(activeDomains);
}

static void rebootVM(virDomainPtr dom)
{
    int ret = virDomainReset(dom,0);
    if (ret < 0)
     {
       virDomainFree(dom);
    }
}

static void rebootAll(void)
{
	int i = 0;
	for (i=0; i<MAX_DOMAINS && vms[i].dom!=NULL && vms[i].pid>=0;i++)
	  rebootVM(vms[i].dom);
}

static void receiveData(int signal)
{
	int n,guest_pid;
	char msg[20] = "";

	if (n = read(sm_channel,msg,10)!=0)
	{
		sscanf(msg,"%d",&guest_pid);
		//printf("Targeted guest: %d\n",guest_pid);
	}
	else
		printf("Error: obtained invalid guest pid %d , %s\n", n,msg);

	if (guest_pid==-1)
	{
		printf("The Stabilization manager is attacked - resetting... \n");
		printf("All virtual machines are being rebooted... \n");
		rebootAll();
	}
	else
	{
       for (n=0; vms[n].pid>0;n++)
	      if (vms[n].pid==guest_pid)
            break;
       printf("Virtual Machine %s on process %d is attacked - rebooting... \n",
    		   virDomainGetName(vms[n].dom), vms[n].pid);
       if(vms[n].dom!=NULL && isActiveDomain(vms[n].dom)==1)
    	   rebootVM(vms[n].dom);

	}
}

static void updateVMList(int signal)
{
	printf("VM List updated\n");
	//refreshDomains();
}

int main(int argc, char **argv)
{
  int ret;
  char command[100] = "";
  struct sigaction sig,sig1;
  vmi_instance_t vmi;
  LIBXML_TEST_VERSION

  /* Connect to the hypervisor - NULL means connect to default hypervisor Qemu */
  conn = virConnectOpen(NULL);
  if (conn == NULL)
    {
        fprintf(stderr, "Failed to connect to hypervisor\n");
        return 0;
    }
    else
    	printf("Successfully connected to the KVM hypervisor\n");

  if (argc==1)
    {
     printf("Stabilization driver and QEMU runtime directory are not supplied,use defaults %s - %s\n",
       sm_drv,guestdir);

    }

  if (argc==2)
   {
	  printf("QEMU runtime directory is not still supplied,use default %s\n", guestdir);
       sm_drv = argv[1];
   }

  if (argc==3)
   {
      printf("QEMU runtime directory is not still supplied,use default %s\n",
        guestdir);
      sm_drv = argv[1];
      guestdir = argv[2];
  }

  sig.sa_sigaction = receiveData;
  sig.sa_flags = SA_SIGINFO;
  sigaction(SIG_VMREBOOT, &sig, NULL);

  sig1.sa_sigaction = updateVMList;
  sig1.sa_flags = SA_SIGINFO;
  sigaction(SIG_VMUPDATE, &sig1, NULL);

  //refreshDomains();

  sm_channel = open(sm_drv,O_RDWR);
  if(sm_channel==-1)
    {
       printf("Device %s not found, error is %s\n", sm_drv, strerror(errno));
       virConnectClose(conn);
       return -1;
    }

  memset(command, 0, 100);
  sprintf(command, "Usrpid:%d",getpid());
  write(sm_channel, command, strlen(command));

  //initVMIFile(numDomains, argv[1]);
  //if (vmi_init(&vmi, VMI_AUTO | VMI_INIT_COMPLETE, "fedora64") == VMI_FAILURE)
  //{
	//  printf("Failed to init LibVMI library.\n");
	 // return -1;
  //}
  //else
  //{
//	  printf("LibVMI is ready to introspect VM %s\n", "fedora64");
 // }


  // -------------------------  Main loop, getting commands from a user

   for (;;)
    {
    	memset(command,0,100);
    	if (fgets(command,99,stdin)!=NULL)
    	{
    		//printf("Next command is %s\n", command);

    		if (!strcmp(command, "exit"))
    			break;

    		//if (write(sm_channel, command, strlen(command))!=strlen(command))
    		//{
    			//printf("Cannot send data, error is %s\n",strerror(errno));
    		//}
    	}

    }
    //vmi_destroy(vmi);
    ret = virConnectClose(conn);
    close(sm_channel);

    return ret;
}

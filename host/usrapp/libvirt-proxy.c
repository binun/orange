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

#define SIG_VM 0x0f //maximal is 32
#define LINUX_OS "Linux"
#define CONFFILE "/etc/libvmi.conf"
#define MAX_DOMAINS 10

typedef struct tagVMPID
{
	int pid;
	virDomainPtr dom;
} VMPID;

static virConnectPtr conn = NULL; /* the hypervisor connection */
static char *sm_drv = "/dev/sm_channel";
static char *guestdir="/var/run/libvirt/qemu";
static int sm_channel;
static VMPID vms[MAX_DOMAINS];
static int pid;

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
	   //vm-name{
	       //sysmap = "/boot/System.map-3.5.0-24-generic";
	       //ostype = "Linux";
	       //linux_name = 0x460;
	       //linux_tasks = 0x240;
	       //linux_mm = 0x278;
	       //linux_pid = 0x2b4;
	       //linux_pgd = 0x48;
	       //linux_addr = 0xe8;
	   //}

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

static int processDomains(char *sysmap)
{
	int i,numDomains,*activeDomains;
	char *domName;

	for (i=0; i<MAX_DOMAINS;i++)
	{
		vms[i].dom = NULL;
        vms[i].pid = -1;
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
	    vms[i].dom = virDomainLookupByID(conn, activeDomains[i]);
	    domName = virDomainGetName(vms[i].dom);
        pid=0;
	    examineVM(domName);
        vms[i].pid=pid;
        printf("Process %d runs the virtual machine %s \n ", vms[i].pid, domName);
	}
	printf("\n");
    //initVMIFile(numDomains, sysmap);
	free(activeDomains);
	return numDomains;
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

int main(int argc, char **argv)
{
  int ret,numDomains;
  char command[100] = "";
  struct sigaction sig;
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

  if (argc<=1 || (argc>=1 && access(argv[1], F_OK)==-1))
  {
	  printf("No system map is delivered or the system map does not exist\n");
	  return 0;
  }

  if (argc==2)
  {
	  //printf("Stabilization driver and QEMU runtime directory are not supplied,use defaults %s - %s\n",  sm_drv,guestdir);
      printf("System map is in %s\n", argv[1]);
  }
  if (argc==3)
  {
	  //printf("QEMU runtime directory is not still supplied,use default %s\n", guestdir);
	  sm_drv = argv[2];
  }

  if (argc==4)
  {
  	  //printf("QEMU runtime directory is not still supplied,use default %s\n", guestdir);
  	  sm_drv = argv[2];
  	  guestdir = argv[3];
  }

  sig.sa_sigaction = receiveData;
  sig.sa_flags = SA_SIGINFO;
  sigaction(SIG_VM, &sig, NULL);

  numDomains = processDomains(argv[1]);

  sm_channel = open(sm_drv,O_RDWR);
  if(sm_channel==-1)
    {
       printf("Device %s not found, error is %s\n", sm_drv, strerror(errno));
       virConnectClose(conn);
       return -1;
    }

  initVMIFile(numDomains, argv[1]);

  memset(command, 0, 100);
  sprintf(command, "Usrpid:%d",getpid());
  write(sm_channel, command, strlen(command));

  if (vmi_init(&vmi, VMI_AUTO | VMI_INIT_COMPLETE, "fedora64") == VMI_FAILURE)
  {
	  printf("Failed to init LibVMI library.\n");
	  return -1;
  }
  else
  {
	  printf("LibVMI is ready to introspect VM %s\n", "fedora64");
  }


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

    ret = virConnectClose(conn);
    close(sm_channel);
    vmi_destroy(vmi);
    return ret;
}

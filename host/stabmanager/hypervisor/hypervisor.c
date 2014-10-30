// Defining __KERNEL__ and MODULE allows us to access kernel-level code not usually available to userspace programs.
#undef __KERNEL__
#define __KERNEL__
 
#undef MODULE
#define MODULE
 
// Linux Kernel/LKM headers: module.h is needed by all modules and kernel.h is needed for KERN_INFO.
#include <linux/module.h>    // included for all kernel modules
#include <linux/kernel.h>	// included for KERN_INFO
#include <linux/init.h>		// included for __init and __exit macros
#include <linux/kallsyms.h>
#include <linux/string.h>
#include <linux/kvm.h>
#include <linux/kvm_host.h>
#include <linux/slab.h>
#include <linux/async.h>

#include <linux/proc_fs.h>
#include <asm/uaccess.h>

#define MAX_POSSIBLE_IDTS 2
#define MIN_DOS_PERCENTAGE 1
#define MIN_DOS_ATTACKS 5000
#define DOS_ATTENUATION 0.1

#include "../definitions.h"
#include "stabdrv.h"
#include "utils.h"

extern void *infected_cpu;

extern int tracer_init(void);
extern void tracer_destroy(void);

MODULE_LICENSE("GPL");

struct list_head* vms_list;
raw_spinlock_t* vm_lock;
static char message[MSGLEN] = "";

bool isHVUnderDDOS(void)
{
	bool unsafe = 0;
	int i = 0;
	int total_dos_requests=0;	
	
	for (i = 0; i < num_vcpus; i++) 
		total_dos_requests+=(int)(atomic_read(&states[i].dos_requests));
	
	    memset (message, 0, sizeof(char)*MSGLEN);
        sprintf (message, "%d requests from %d VCPUs", total_dos_requests,num_vcpus);
        debugPrint(message);	

	if (total_dos_requests==0) 
	{
		debugPrint("DDOS attacks absent");
		return 0;
		//no dos attacks at all, assume all is safe
	}
		
	
	for (i = 0; i < num_vcpus; i++)
	{
		int curr_requests = (int)atomic_read(&states[i].dos_requests);
		//printk("DDOS statistics: state %d total %d\n", curr_requests, total_dos_requests);
		if ( (int)(100*curr_requests/total_dos_requests) > MIN_DOS_PERCENTAGE &&
				curr_requests > MIN_DOS_ATTACKS
		   )
		{
		    debugPrint("Prepare for CPU reset - DOS attacks...\n");
		    unsafe = 1;
		    states[i].toReset = 1;
		}
	}
	
	return unsafe;
}

bool isHVDeadVMs(void)
{
  bool dead=0,enough_running = 0;
  int live, i;
  char msg[30] = "";
  //printk("Searching for dead VMs among %d cpus\n", num_vcpus);
  for (i = 0; i < num_vcpus; i++)
  {
	  live = (int)(atomic_read(&(states[i].alive)));
      if (states[i].last_rebooted<=0) //first reboot
    	  enough_running = 1;
      else //runs during a long time...
	      enough_running = ((msecs_to_jiffies(jiffies)-states[i].last_rebooted)>recovery_period);

	  printk("CPU %d Status: live %d enough running %d\n", i, live,enough_running);
	  if (!live && enough_running)
	  {
		  dead = 1;
		  states[i].toReset= 1;
	  }
          
      if (dead)
	    sprintf(msg," WD: CPU %d DEAD",i);
      else
        sprintf(msg," WD: CPU %d LIVE",i);
	  debugPrint(msg);
  }
  return dead;
}

bool isHVUnsafeState(void)
{
  bool unsafe = 0;
  int i;

  debugPrint("Verifying VCPU states... ");
  if (infected_cpu==NULL)
  {
	  debugPrint("No rootkits");
	  return false;
  }

  for (i = 0; i < num_vcpus; i++)
  {
	  if (states[i].cpu==infected_cpu)
	  {
		  //debugPrint("Prepare for CPU reset --- rootkits\n");
		  unsafe = 1;
		  states[i].toReset=1;
	  }
  }
  return unsafe;
}

void enforceHVSafeState(void *_data, async_cookie_t c)
{
   int i = 0;
   VMAlarm vma;

   debugPrint("	Make the HV consistent");

   for (i = 0; i < num_vcpus; i++)
    {
      if (states[i].toReset)
       {
	      printk(KERN_INFO " !!Reset CPU %d", i);
	      states[i].toReset = 0;
          vma.pid = states[i].pid;
          states[i].last_rebooted = msecs_to_jiffies(jiffies);
          signalError(&vma);
       }
   }
}

void enforceHVDOSProtection(void *_data, async_cookie_t c)
{
	int i = 0;
	void *vcpu_to_reset;

	debugPrint(" Enforce DOS protection");
	    
	for (i = 0; i < num_vcpus; i++) 
	{ 
	    
	 if (states[i].toReset)
	  {
	  	 vcpu_to_reset = (void*)states[i].cpu;
	  	 states[i].toReset = 0;
	  	 atomic_set(&states[i].dos_requests, 0);
	  	 states[i].cpu = 0;
		 killVM(vcpu_to_reset);	
	  }
	  else
	  {
         atomic_set(&states[i].dos_requests, 0);
	  }
	}
}

void refreshHVState(void)
{
  int i = 0;

  for (i = 0; i < num_vcpus; i++)
    {
       states[i].toReset = 0;
       //atomic_set(&(states[i].alive), 0);
       atomic_set(&(states[i].dos_requests), 0);
    }      
  
  //memset (message, 0, sizeof(char)*MSGLEN);
  //sprintf (message, "HV state refreshed - %d VCPUs", num_vcpus);
  //debugPrint(message);
}

void registerDOSHit(void *vcpu)
{
	int i;
	struct kvm_vcpu *sender = (struct kvm_vcpu*)vcpu;
	
    memset (message, 0, sizeof(char)*MSGLEN);
    sprintf (message, "CPUID from %d",sender->pid->numbers[0].nr);
    debugPrint(message);
	
	for (i = 0; i < num_vcpus; i++)
	{
		struct kvm_vcpu *at = (struct kvm_vcpu*)(states[i].cpu);
		if (sender->pid->numbers[0].nr==at->pid->numbers[0].nr) //better to compare following sender processes
		{
			atomic_inc(&states[i].dos_requests);
            memset (message, 0, sizeof(char)*MSGLEN);
            sprintf (message, "CPUID from %d results in overall %d requests",
            	       sender->pid->numbers[0].nr,
            	       (int)(atomic_read(&(states[i].dos_requests)))
            	    );
            debugPrint(message);

			break;
		}
			
	}
}

void backupHVState(void*data, async_cookie_t c)
{
	debugPrint("Backup the hypervisor state");
}

int initHypervisor(void)
{   
	int i=0;
	struct kvm*kvm;
    struct kvm_vcpu *vcpu;
    num_vcpus = 0;
    vms_list = (struct list_head*)kallsyms_lookup_name("vm_list");
    //vm_lock =(raw_spinlock_t*)kallsyms_lookup_name("kvm_lock");

    if (tracer_init() < 0)
    {
    	debugPrint("ERROR - Function tracing is out");
    	return -1;
    }

    //spin_lock(&kvm_lock);
    list_for_each_entry(kvm, vms_list, vm_list)
      {
    	 kvm_for_each_vcpu(i, vcpu, kvm)
          {
           states[num_vcpus].cpu = (void*)vcpu;
           states[num_vcpus].toReset = 0;
           states[num_vcpus].pid = vcpu->pid->numbers[0].nr;
           states[num_vcpus].last_rebooted = -1;
           atomic_set(&(states[num_vcpus].alive), 0);
           atomic_set(&(states[num_vcpus].dos_requests), 0);
           printk("Attaching new CPU %d PID %d\n", num_vcpus, states[num_vcpus].pid);
           num_vcpus++;
          }
      }

    memset (message, 0, sizeof(char)*MSGLEN);
    sprintf (message, "There are %d VCPUs", num_vcpus);
    debugPrint(message);
    //spin_unlock(vm_lock);

    debugPrint("INIT - Hypervisor initialized");
    return 0;
}

void cleanupHypervisor(void)
{
     memset ((void*)states, 0, MAX_VCPUS*sizeof(VCPUState));
     tracer_destroy();
     debugPrint("CLEANUP - Hypervisor destroyed");
}



#include <linux/kernel.h>
#include <linux/kvm.h>
#include <linux/kvm_host.h>
#include <linux/string.h>
#include <linux/kvm.h>
#include <linux/kvm_host.h>
#include <linux/pid.h>
#include <asm/siginfo.h>
#include <linux/sched.h>
#include "../definitions.h"

bool debugMode = 1;
static struct task_struct *task;

extern struct list_head* vms_list;
extern raw_spinlock_t* vm_lock;

void debugPrint(char *message)
{
	if (debugMode)
		printk(KERN_INFO "%s\n",message);
}

void* current_vcpu(void)
{
  int i = 0;
  struct kvm* kvm;
  raw_spin_lock(vm_lock);
  list_for_each_entry(kvm, vms_list, vm_list) 
   {
     for (i = 0; i < kvm->online_vcpus.counter; i++) 
      {
       if (current->pid == kvm->vcpus[i]->pid->numbers[0].nr) 
        {
          raw_spin_unlock(vm_lock);
          return (void*)(kvm->vcpus[i]);
        }
      }  
   }
   raw_spin_unlock(vm_lock);
   return NULL;
}

bool current_is_vcpu_pid(void)
{
	return (current_vcpu()!=NULL);
}

void killVM(void *vcpu)
{
	struct siginfo info;
	int ret;
	
	rcu_read_lock();
	task = pid_task(((struct kvm_vcpu*)vcpu)->pid,PIDTYPE_PID);
	rcu_read_unlock();
	
	if (task==NULL)
	{
		debugPrint("Failed killing a malfunctioning VM");
		return;
	}
	
	memset(&info, 0, sizeof(struct siginfo));
	info.si_signo =
			SIGKILL;
	info.si_code = 0;
	info.si_errno = 0;
	
	ret = send_sig_info(
                        SIGKILL,
			&info, task);
	
	if (ret <0)
		debugPrint("Failed killing a malfunctioning VM");
}


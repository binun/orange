#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/sched.h>

int get_vm_characteristics(int pid,char *message)
{
    struct task_struct *p = NULL;
    unsigned long commOffset;
    unsigned long tasksOffset;
    unsigned long mmOffset;
    unsigned long pidOffset;
    unsigned long pgdOffset;
    unsigned long addrOffset;

    printk(KERN_ALERT "Getting parameters of PID %d \n\n", pid);
    //p = current;

    //rcu_read_lock();
    p = pid_task(find_vpid(pid),PIDTYPE_PID);
    //rcu_read_unlock();

    if (p==NULL)
    {
        printk(KERN_ALERT "Found no process structure for PID %d\n",pid);
        return -1;
    }

    printk("Starting examine the task structure for PID %d\n", pid);

    commOffset = (unsigned long) (&(p->comm)) - (unsigned long) (p);
    tasksOffset = (unsigned long) (&(p->tasks)) - (unsigned long) (p);
    mmOffset = (unsigned long) (&(p->mm)) - (unsigned long) (p);
    pidOffset = (unsigned long) (&(p->pid)) - (unsigned long) (p);
    pgdOffset = (unsigned long) (&(p->mm->pgd)) - (unsigned long) (p->mm);
    addrOffset = (unsigned long) (&(p->mm->start_code)) - (unsigned long) (p->mm);

    /*sprintf(message,
    		//"    linux_name=0x%x;\n"
    		"    linux_tasks=%d;\n"
    		"    linux_mm=%d;\n"
    		"    linux_pid=%d;\n"
    		"    linux_pgid=%d;\n"
    		//"    linux_addr=0x%x;\n",

    		//	 (unsigned int) commOffset,
    			 (unsigned int)tasksOffset,
    			 (unsigned int)mmOffset,
    			 (unsigned int)pidOffset,
    			 (unsigned int)pgdOffset
    		//	 (unsigned int) addrOffset
    	);
    	*/

    sprintf(message,
    	 "    linux_name=0x%x;\n"
         "    linux_tasks = %d;\n"
         "    linux_mm = %d;\n"
         "    linux_pid = %d;\n"
         "    linux_pgd = %d;\n",
        (unsigned int)commOffset,
        (unsigned int)tasksOffset,
        (unsigned int)mmOffset,
        (unsigned int)pidOffset,
        (unsigned int)pgdOffset
        	);

    return 0;
}

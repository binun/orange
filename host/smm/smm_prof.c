#undef __KERNEL__
#define __KERNEL__

#undef MODULE
#define MODULE

#include <linux/version.h>
#include <linux/module.h>    // included for all kernel modules
#include <linux/kernel.h>    // included for KERN_INFO
#include <linux/init.h>        // included for __init and __exit macros
#include <linux/timer.h>
#include <linux/jiffies.h>
#include <linux/async.h>
#include <linux/string.h>
#include <linux/kallsyms.h>
#include <linux/perf_event.h>
#include <linux/hw_breakpoint.h>

#define SM_DATA_SIZE 24 // 6*sizeof(int) + 10*21 (13 is the sizeof ofVMState
MODULE_LICENSE("GPL");

void (*f)(unsigned long);
void (*reboot)(void);
struct perf_event * __percpu *sample_hbp;

static char *ksym_name = "stab_timer_period";
static char *reboot_name = "rebootAll";

int original_timer_period;
void *data;

static void hbp_handler(struct perf_event *bp,struct perf_sample_data *psd,
                                 struct pt_regs *regs)
{
   printk(KERN_INFO "%s value is changed. Restoring to the default %d\n",
		   ksym_name,original_timer_period);
   *((int*)data)=original_timer_period;

   if (f!=NULL)
	   f(0);

   if (reboot!=NULL)
	   reboot();
}

static int __init smm_init(void)
{
    int ret = 0;
	struct perf_event_attr attr;

	printk(KERN_INFO "INIT - SMM ");

	data=(void*)kallsyms_lookup_name("stab_timer_period"); //global data starts from this variable
	if (data == NULL)
	 {
	   printk(KERN_INFO "ERROR - SM data is not found");
	   return -1;
	 }
	else
	{
		printk(KERN_INFO "SM data value %d at %lu\n", *((int*)data), (unsigned long)data);
	}

	f=(void *)kallsyms_lookup_name("stabilization_timer_callback");
    if (f == NULL)
    {
    	printk(KERN_INFO "ERROR - SM callback is not found");
    	return -1;
    }
    else
    {
    	printk("SM callback found\n");
    }

    reboot=(void *)kallsyms_lookup_name(reboot_name);
    if (reboot == NULL)
     {
       printk(KERN_INFO "ERROR - Rebooter is not found");
       return -1;
     }
    else
     {
       printk("Rebooter found\n");
     }


    hw_breakpoint_init(&attr);
    attr.bp_addr = kallsyms_lookup_name(ksym_name);
    attr.bp_len = sizeof(int);

    attr.bp_type = HW_BREAKPOINT_W;// | HW_BREAKPOINT_R;

    sample_hbp = register_wide_hw_breakpoint(&attr, hbp_handler, NULL);
    if (IS_ERR((void __force *)sample_hbp))
    {
      ret = PTR_ERR((void __force *)sample_hbp);
      printk(KERN_INFO "Breakpoint registration failed\n");
      return -1;
    }

    printk(KERN_INFO "HW Breakpoint for %s write installed\n", ksym_name);

    original_timer_period = *((int*)data);
    printk(KERN_INFO "INIT - SMM initialized with the original data %d\n: ",original_timer_period);
    return 0;
}

static void __exit smm_exit(void)
{
	unregister_wide_hw_breakpoint(sample_hbp);
    printk(KERN_INFO "CLEANUP - SMM\n");
}

module_init(smm_init);
module_exit(smm_exit);

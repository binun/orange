#include <linux/kernel.h>
#include <linux/module.h>
#include <asm/uaccess.h>	
#include <linux/timer.h>
#include <linux/jiffies.h>
#include <linux/async.h>
#include <linux/string.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("The BGU Orange Team");
MODULE_DESCRIPTION("Intra-VM Agent");

static char *mapFile = "";
module_param(mapFile, charp, 0);
MODULE_PARM_DESC(mapFile,"The Linux map file");

#define KVM_HYPERCALL ".byte 0x0f,0x01,0xc1"
#define HC_ALARM 10
#define HC_ALIVE 11
#define HC_VMUP 12
#define HC_VMDOWN 13

#define HCP_RK_ATTACK 0

static struct timer_list orch_timer;
static int orch_timer_period = 500;
static int ip_passed = 0;

static long run_hypercall(unsigned int command, unsigned long param)
 {
	long ret = 0;
	char msg[50] = "";
	sprintf(msg,"Running hypercall %d with param %lu\n",command,param);
	printk(msg);
	asm volatile(KVM_HYPERCALL
		: "=a"(ret)
		: "a"(command), "b"(param)
		: "memory");
	return ret;
}

static void orch_timer_callback( unsigned long data )
{
    unsigned int command;
    command=ip_passed?HC_ALIVE:HC_VMUP;
 
	run_hypercall(command, 0);
    ip_passed = 1;

    if (orch_timer_period>0)
     mod_timer( &orch_timer, jiffies + msecs_to_jiffies(orch_timer_period) );
}

int initExternalChannel(void)
{
	int ret = 0;
	setup_timer( &orch_timer, orch_timer_callback, 0 );

	ret = mod_timer( &orch_timer, jiffies + msecs_to_jiffies(orch_timer_period) );
	if (ret!=0)
	{
      printk("Error in orchestration timer\n");
      return ret;
	}

	printk(KERN_INFO "System map file is = %s",mapFile);

	return 0;
}

void cleanupExternalChannel(void)
{
	int ret = 1;
	ret = del_timer( &orch_timer );
	if (ret==0)
      printk("The orchestration timer is still in use...");
}

module_init(initExternalChannel);
module_exit(cleanupExternalChannel);

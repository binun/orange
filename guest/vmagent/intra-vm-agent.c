#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/fs.h>
#include <asm/uaccess.h>	
#include <linux/timer.h>
#include <linux/jiffies.h>
#include <linux/async.h>

MODULE_LICENSE("GPL");

#define KVM_HYPERCALL ".byte 0x0f,0x01,0xc1"
#define HC_ALARM 10
#define HC_ALIVE 11

#define HCP_RK_ATTACK 0

static struct timer_list orch_timer;
static int orch_timer_period = 500;

static long run_hypercall(unsigned int command, unsigned long param)
 {
	long ret = 0;
	char msg[50] = "";
	sprintf(msg,"Running hypercall %d\n",command);
	printk(msg);
	asm volatile(KVM_HYPERCALL
		: "=a"(ret)
		: "a"(command), "b"(param)
		: "memory");
	return ret;
}

static void orch_timer_callback( unsigned long data )
{
	unsigned int hc_command = HC_ALIVE;

    run_hypercall(hc_command, HCP_RK_ATTACK);

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

	return 0;
}

void cleanupExternalChannel(void)
{
	int ret = del_timer( &orch_timer );
	if (!ret)
      printk("The orchestration timer is still in use...");
}

module_init(initExternalChannel);
module_exit(cleanupExternalChannel);

#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/fs.h>
#include <linux/mutex.h>
#include <asm/uaccess.h>	
#include <linux/miscdevice.h>
#include <linux/kfifo.h>
#include <linux/timer.h>
#include <linux/jiffies.h>
#include <linux/async.h>

MODULE_LICENSE("GPL");

#define BUFFER_SIZE 4096
#define MSG_SIZE 200
#define DEVICE_NAME "stabdrv"
#define MAX_ALLOWED_TOOLS 10

#define KVM_HYPERCALL ".byte 0x0f,0x01,0xc1"
#define HC_ALARM 10
#define HC_ALIVE 11

#define HCP_RK_ATTACK 0

typedef struct tagrootkitStat
{
	char* name;
	bool present;
} rootkitStat;

typedef struct tagtoolStat
{
	void *alias; //obtained from device_open, maintained in read, write...
	bool status;
} toolStat;

static struct timer_list orch_timer;
static int orch_timer_period = 500;
static toolStat toolStatistics[MAX_ALLOWED_TOOLS];
static int numTools;
static char message[MSG_SIZE] = "";

static DEFINE_MUTEX(rk_lock);
static DEFINE_MUTEX(toolstat_lock);

static bool add_tool(void *al)
{
	int i;

	if (mutex_lock_interruptible(&toolstat_lock)!=0)
		{
		  printk("Error in blocking\n");
		  return false;
	    }

	if (numTools > MAX_ALLOWED_TOOLS-1)
	{
	   printk("Tool limit exceeded\n");
	   mutex_unlock(&toolstat_lock);
	   return false;
	}

	for (i = 0; i < numTools; i++)
	   if (toolStatistics[i].alias==al)
	   {
		   printk("Tool exists\n");
		   mutex_unlock(&toolstat_lock);
		   return false;
	   }

	toolStatistics[numTools].alias = al;
	toolStatistics[numTools].status = false;
	numTools++;
	mutex_unlock(&toolstat_lock);
	return true;
}

static bool rem_tool(void *al)
{
	toolStat bck_toolStatistics[MAX_ALLOWED_TOOLS];
	int i,num_tools = 0;

	if (mutex_lock_interruptible(&toolstat_lock)!=0)
			{
			  printk("Error in blocking\n");
			  return false;
		    }

	memset (bck_toolStatistics, 0, sizeof(toolStat)*MAX_ALLOWED_TOOLS);
	memmove (bck_toolStatistics,toolStatistics, sizeof(toolStat)*MAX_ALLOWED_TOOLS);
	memset (toolStatistics, 0, sizeof(toolStat)*MAX_ALLOWED_TOOLS);

	for (i = 0; i < numTools; i++)
	{
		if (toolStatistics[i].alias && toolStatistics[i].alias == al)
		{
			memmove(bck_toolStatistics + num_tools,toolStatistics+i,sizeof(toolStat));
			num_tools++;
		}
	}

	memmove (toolStatistics,bck_toolStatistics, sizeof(toolStat)*MAX_ALLOWED_TOOLS);
	numTools = num_tools;
	mutex_unlock(&toolstat_lock);
	return true;
}

static bool updateToolStatus (void *al, bool newStatus)
{
	int i = 0;

	if (mutex_lock_interruptible(&toolstat_lock)!=0)
				{
				  printk("Error in blocking\n");
				  return false;
			    }

	for (i = 0; i < numTools; i++)
	  if (toolStatistics[i].alias && toolStatistics[i].alias == al)
	  {
	     toolStatistics[i].status = newStatus;
	  }
	mutex_unlock(&toolstat_lock);
	return true;
}

static bool checkToolStats(void)
{
	int i = 0;
    bool status = false;
	if (mutex_lock_interruptible(&toolstat_lock)!=0)
				{
				  printk("Error in blocking\n");
				  return false;
			    }

	for (i = 0; i < numTools; i++)
	  status = status || toolStatistics[i].status;

	mutex_unlock(&toolstat_lock);

	return status;
}


static long run_hypercall(unsigned int command, unsigned long param)
 {
	long ret = 0;
	char msg[30] = "";
	sprintf(msg,"Running hypercall %d\n",command);
	printk(msg);
	asm volatile(KVM_HYPERCALL
		: "=a"(ret)
		: "a"(command), "b"(param)
		: "memory");
	return ret;
}

void resetExternalChannel(void)
{
	memset(message,0,MSG_SIZE);
	memset (toolStatistics, 0, sizeof(toolStat)*MAX_ALLOWED_TOOLS);
	numTools = 0;
}

static bool examineToolOutput(char *msg)
{

	if (strstr (msg, "installed")!=NULL &&
		(strstr (msg, "Worm")!=NULL || strstr (msg, "Trojan")!=NULL || strstr (msg, "rootkit")!=NULL)
	   )
	{
		run_hypercall(HC_ALARM, HCP_RK_ATTACK);
		return true;
	}

	return false;
}

static void orch_timer_callback( unsigned long data )
{
	unsigned int hc_command;
    if (checkToolStats()==true)
    	hc_command = HC_ALARM;
    else
    	hc_command = HC_ALIVE;

    run_hypercall(hc_command, HCP_RK_ATTACK);

    if (&orch_timer!=NULL && orch_timer_period>0)
     mod_timer( &orch_timer, jiffies + msecs_to_jiffies(orch_timer_period) );
}

static int device_open(struct inode *inode, struct file *file)
{
	add_tool(file->private_data);
	printk("Tool %ld added: now %d tools\n", (unsigned long)(file->private_data), numTools);
	return 0;
}

static int device_release(struct inode *inode, struct file *file)
{
	rem_tool(file->private_data);
	printk("Tool %ld removed: now %d tools\n", (unsigned long)(file->private_data), numTools);
	return 0;
}

static ssize_t device_read(struct file *file, char *buffer, size_t count, loff_t *offset)
{
	return count;
}

static ssize_t device_write(struct file *filp, const char *buffer, size_t count, loff_t *off)
{
	int remain = copy_from_user(message, buffer, count);
    bool malw_check_result = false;
	if (!remain)
	{
		malw_check_result = examineToolOutput(message);
	}
	else
	{
		printk("Problems in getting data\n");
	}

    memset(message,0,MSG_SIZE);
    if (malw_check_result)
    {
    	updateToolStatus (filp->private_data, true);
    	printk("Status changed to %d from tool %ld\n", 1, (unsigned long)(filp->private_data));
    	run_hypercall(HC_ALARM, HCP_RK_ATTACK);
    }
	return count;
}

static const struct file_operations fops = {
	.owner = THIS_MODULE,
	.read = device_read,
	.write = device_write,
	.open = device_open,
	.release = device_release
};

static struct miscdevice stab_dev = {
	.minor = MISC_DYNAMIC_MINOR,
	.name = DEVICE_NAME,
	.fops = &fops,
};


int initExternalChannel(void)
{
	int ret = misc_register(&stab_dev);
	if (ret)
	{
		printk("Device register failed\n");
		return ret;
	}
	printk("Device register succeeded\n");

	memset (toolStatistics, 0, sizeof(toolStat)*MAX_ALLOWED_TOOLS);
	numTools = 0;

	resetExternalChannel();

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
	misc_deregister(&stab_dev);
}

module_init(initExternalChannel);
module_exit(cleanupExternalChannel);

#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/fs.h>
#include <linux/kfifo.h>
#include <asm/uaccess.h>
#include <linux/miscdevice.h>
#include <linux/pid.h>
#include <linux/sched.h>
#include "utils.h"
#include "definitions.h"

#define FIFO_SIZE 1000
#define MSGSIZE 200
#define MSGCOUNT 200

static char message[MSGSIZE] = "COMMAND", param[MSGSIZE] = "";

static DEFINE_MUTEX(sent_command_lock);
static int usr_pid;
static struct task_struct *usr_task;

extern int get_vm_characteristics(int,char*);

void rebootAll(void)
{
	struct siginfo info;

	memset(param,0, sizeof(char)*MSGSIZE);
	sprintf(param, "%d", -1);

	info.si_signo = SIG_VM;
	info.si_code = 0;
	info.si_errno = 0;
	printk("Sending alarm signal to all VMs\n");

	send_sig_info(SIG_VM,&info, usr_task);
}

void signalError(void* sigp)
{
	struct siginfo info;
	VMAlarm *vma = (VMAlarm*)sigp;
	memset(param,0, sizeof(char)*MSGSIZE);
	sprintf(param, "%d", vma->pid);

	info.si_signo = SIG_VM;
	info.si_code = 0;
	info.si_errno = 0;
	printk("Sending alarm signal to %d\n", vma->pid);

	send_sig_info(SIG_VM,&info, usr_task);
}

static int device_open(struct inode *inode, struct file *file)
{
	debugPrint("Stabman device opened");
	return 0;
}

static int device_release(struct inode *inode, struct file *file)
{
	debugPrint("Stabman device released");
	return 0;
}

//Used for transferring parameters
static ssize_t device_read(struct file *file, char *buffer, size_t count, loff_t *offset)
{
	int remain;
	char command[100] = "";

	mutex_lock(&sent_command_lock);
	remain = copy_to_user(buffer, param, strlen(param));
	//remain = copy_to_user(buffer, message, count);
	mutex_unlock(&sent_command_lock);

    sprintf(command, "Sent %s to userspace", message);
    debugPrint(command);
	return strlen(param);
}

static ssize_t device_write(struct file *filp, const char *buffer, size_t count, loff_t *off)
{
	char command[100] = "";
	int vm_pid,remain;

	//sprintf(command, "Arrived %d bytes from userspace", count);
	//debugPrint(command);

	mutex_lock(&sent_command_lock);
	memset(message,0,MSGSIZE*sizeof(char));
    remain = copy_from_user(message, buffer, count);
    mutex_unlock(&sent_command_lock);

    memset(command,0,100);
    if (!remain)
    {
    	sprintf(command, "Got %s from userspace", message);
    	debugPrint(command);
    }
    else
    {
    	printk("Problems in getting data\n");
    }

    if (!strncmp(message, "Usrpid:",strlen("Usrpid:")))
    {
    	sscanf(message,"Usrpid:%d",&usr_pid);
    	printk("User pid %d obtained", usr_pid);
    	usr_task = pid_task(find_vpid(usr_pid), PIDTYPE_PID);
    	if (usr_task==NULL)
    		{
    			debugPrint("Failed connecting to userspace");
    		}
    }

    if (!strncmp(message, "VMPid:",strlen("VMPid:")))
        {
        	sscanf(message,"VMPid:%d",&vm_pid);
        	printk("VM pid %d obtained", vm_pid);
        	memset(param,0,MSGSIZE*sizeof(char));
        	if (get_vm_characteristics(vm_pid, param)<0)
        	{
        		debugPrint("Cannot retrieve VM params");
        	}
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

int initStabmanDevice(void)
{
	int ret = misc_register(&stab_dev);
	if (ret)
	{
		debugPrint("ERROR - Stabman device registration failed\n");
		return ret;
	}


	debugPrint("INIT - Stabman device registered successfully\n");

	return 0;
}

void cleanupStabmanDevice(void)
{
	misc_deregister(&stab_dev);

}





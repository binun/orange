// Defining __KERNEL__ and MODULE allows us to access kernel-level code not usually available to userspace programs.
#undef __KERNEL__
#define __KERNEL__

#undef MODULE
#define MODULE

// Linux Kernel/LKM headers: module.h is needed by all modules and kernel.h is needed for KERN_INFO.
#include <linux/version.h>
#include <linux/module.h>	// included for all kernel modules
#include <linux/kernel.h>	// included for KERN_INFO
#include <linux/init.h>		// included for __init and __exit macros
#include <linux/fs.h>
#include <linux/kallsyms.h>
#include <linux/uio.h>
#include <linux/highmem.h>
#include <asm/unistd.h>
#include <linux/sched.h>
#include <linux/string.h>
#include <linux/async.h>

#include <linux/kvm.h>
#include <linux/kvm_host.h>
#include "utils.h"

MODULE_LICENSE("GPL");

// Address of syscall table
unsigned long* sys_call_table_address;

asmlinkage int (*real_open)(const char* __user, int, int);
asmlinkage int custom_open(const char* __user file_name, int flags, int mode) 
{
	if (current_is_vcpu_pid()) {
		printk("Traffic interceptor: pid<%d, %d> open(\"%s\", %X, %X)\n", 
												current->pid, 
												current->tgid, 
												file_name,
												flags, 
												mode);
	}
	return real_open(file_name, flags, mode);
}

asmlinkage int (*real_read)(unsigned int, char* __user, size_t);
asmlinkage int custom_read(unsigned int fd, char* __user buf, size_t count) 
{
	if (current_is_vcpu_pid()) {
		printk("Traffic interceptor: pid<%d, %d> read(%d, %lu)\n",
												current->pid,
												current->tgid,
												fd,
												count);
	}
	return real_read(fd, buf, count);
}

asmlinkage long (*real_ioctl)(unsigned int fd, unsigned int cmd, unsigned long arg);
asmlinkage long custom_ioctl(unsigned int fd, unsigned int cmd, unsigned long arg)
{
	if (current_is_vcpu_pid()) {
		switch (cmd){
					case KVM_RUN:
						/**
							there is nothing we want to print if it's KVM_RUN
						**/
						break;
#ifdef __KVM_HAVE_IRQ_LINE
					case KVM_IRQ_LINE_STATUS:
					case KVM_IRQ_LINE: {
						printk(KERN_INFO "pid(%d) - The irq is: %u\n",current->pid,((struct kvm_irq_level*)arg)->irq);
						break;
					}

#endif				
					default:
						printk("interceptor: pid<%d> ioctl(fd: %d, cmd: %d, arg: %lu)\n",
																current->pid,
																fd,
																cmd,
																arg);
		}
	}
	return real_ioctl(fd, cmd, arg);
}

bool pingPacket(const struct iovec __user *vec){
	unsigned long i=0;
	if (vec->iov_len<8)
		return false;
	for (i=0;i<7;i++){
		if (((char*)(vec->iov_base))[vec->iov_len-1-i] != (0x37-(char)i)){
			return false;
		}
	}
	return true;
}
asmlinkage long (*real_writev)(unsigned long fd,
                            const struct iovec __user *vec,
                            unsigned long vlen);
asmlinkage long custom_writev(unsigned long fd,
                            const struct iovec __user *vec,
                            unsigned long vlen) 
{
	if (current_is_vcpu_pid()) {
	
		printk("interceptor: pid<%d> writev(fd: %lu, vec.base = %p vec.len = %lu: XXX, vlen: %lu)\n", 
			current->pid,
			fd,
			vec->iov_base, vec->iov_len,
			vlen);
		if (pingPacket(vec)){
			printk("Found a ping packet\n");
			printk("Destination ip is: %u.%u.%u.%u",((unsigned char*)(vec->iov_base))[30],
											((unsigned char*)(vec->iov_base))[31],
											((unsigned char*)(vec->iov_base))[32],
											((unsigned char*)(vec->iov_base))[33]);

		}
	}
	return real_writev(fd, vec, vlen);
}


/* Make the page writeable */
static int make_rw(unsigned long address) {
	unsigned int level;
	pte_t *pte = lookup_address(address, &level);
	if (pte->pte &~ _PAGE_RW) {
		pte->pte |= _PAGE_RW;
	}
	return 0;
}

/* Make the page write protected */
static int make_ro(unsigned long address) {
	unsigned int level;
	pte_t *pte = lookup_address(address, &level);
	pte->pte = pte->pte &~ _PAGE_RW;
	return 0;
}

static void patchSCTable(void)
{
	    debugPrint("ioctl: Patch table");
		make_rw((unsigned long)sys_call_table_address);
		debugPrint("ioctl: block memory");
		
		// swap open
		real_open = (void*)(*(sys_call_table_address + __NR_open));
		*(sys_call_table_address + __NR_open) = (unsigned long)custom_open;
		
		// swap read
		real_read = (void*)(*(sys_call_table_address + __NR_read));
		*(sys_call_table_address + __NR_read) = (unsigned long)custom_read;
		
		// swap ioctl
		real_ioctl = (void*)(*(sys_call_table_address + __NR_ioctl));
		*(sys_call_table_address + __NR_ioctl) = (unsigned long)custom_ioctl;
		
		// swap writev
		real_writev = (void*)(*(sys_call_table_address + __NR_writev));
		*(sys_call_table_address + __NR_writev) = (unsigned long)custom_writev;

		make_ro((unsigned long)sys_call_table_address);
}

static void restoreSCTable(void)
{
	    debugPrint("ioctl: Restore table");
		make_rw((unsigned long)sys_call_table_address);
		
		// fix open
		*(sys_call_table_address + __NR_open) = (unsigned long)real_open;
		
		// fix read
		*(sys_call_table_address + __NR_read) = (unsigned long)real_read;
		
		// fix ioctl
		*(sys_call_table_address + __NR_ioctl) = (unsigned long)real_ioctl;
		
		// fix writev
		*(sys_call_table_address + __NR_writev) = (unsigned long)real_writev;

		make_ro((unsigned long)sys_call_table_address);
}

//Traffic state --------------------------------------------------------------------------
bool isTrafficSafeState(void)
{
	return 1;
}

void enforceTrafficSafeState(void *_data, async_cookie_t c)
{
	debugPrint("	Make the traffic consistent");
}

void backupTrafficState(void*data, async_cookie_t c)
{
	debugPrint("       Backup the traffic state");
}

void refreshTrafficState(void)
{

}

int initTrafficManager(void)
{ 
	debugPrint("INIT - Initializing Traffic Manager");
    sys_call_table_address = (void*)kallsyms_lookup_name("sys_call_table");
    printk(KERN_INFO "Syscall table resides at  %p\n", sys_call_table_address);
    patchSCTable();
 	
    return 0;
}

void cleanupTrafficManager(void)
{
	debugPrint("CLEANUP - Cleaning up traffic manager");
   
    restoreSCTable();
}

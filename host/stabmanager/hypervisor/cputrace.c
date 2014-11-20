#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/init.h> 
#include <linux/kprobes.h>
#include <linux/kallsyms.h>
#include <linux/kvm_host.h>

#include "../definitions.h"
#include "utils.h"
#define HCALL_COMMAND 0 //1,2,3 and so on are registers , see include/asm/kvm_host.h

static char *cpuid_point = "kvm_cpuid";
static char *hcall_point = "kvm_emulate_hypercall";

void *infected_cpu;
static struct jprobe cpuid_jpr,hcall_jpr;

extern int num_vcpus;
extern VCPUState states[MAX_VCPUS];

extern void registerDOSHit(void*);
extern void refreshVMList(void);

static int cpuid_handler(struct kvm_vcpu *vcpu, u32 *eax, u32 *ebx, u32 *ecx, u32 *edx)
{		
	//registerDOSHit((void*)vcpu);
	
	jprobe_return();
	return 0;
}

static int hcall_handler(struct kvm_vcpu *vcpu)
{
	char msg[50] = "";
    int i = 0;
    unsigned int command = vcpu->arch.regs[0];

	if (vcpu==NULL)
	{
		debugPrint("Illegal Hypercall");
		jprobe_return();
	}

	if (command==HC_ALARM)
	{
		infected_cpu = vcpu;
		debugPrint("CPU ATTACKED");
		jprobe_return();
	}

	if (command==HC_VMUP)
	{
		debugPrint("Hypercall updating VM List");
		refreshVMList();
		jprobe_return();

	}

    if (command==HC_ALIVE)
    {
    	debugPrint("Hypercall updating VM List");

    	for (i = 0; i < num_vcpus; i++)
    	 if (states[i].pid == vcpu->pid->numbers[0].nr)
    	 {
    	  atomic_set(&(states[i].alive), 1);
    	  sprintf(msg, "Hypercall accepted from VCPU ID %d Status %d",i,(int)(atomic_read(&(states[i].alive))));
    	  debugPrint(msg);
    	 }

    	jprobe_return();
    }
	return 0;
}

int tracer_init(void)
{
	int ret;

	// --------------------- Planting CPUID interceptor... -----------------
	cpuid_jpr.entry = cpuid_handler;
	cpuid_jpr.kp.addr = (kprobe_opcode_t *)kallsyms_lookup_name(cpuid_point);
	if (!cpuid_jpr.kp.addr) 
	{
	   debugPrint("ERROR - Couldn't find entry to attach CPUID sniffer to");
	   return -1;
	}

	ret = register_jprobe(&cpuid_jpr);
	if (ret < 0) 
	{
		debugPrint("ERROR - CPUID Sniffer planting failed");
		return ret;
	}
	debugPrint("INIT - CPUID sniffer successfully planted");
	
	// ---------------------Planting hypercall interceptor... ------------------------------
	hcall_jpr.entry = hcall_handler;
	hcall_jpr.kp.addr = (kprobe_opcode_t *)kallsyms_lookup_name(hcall_point);
	if (!hcall_jpr.kp.addr)
	{
		debugPrint("ERROR - Couldn't find entry to attach hypercall sniffer to");
		return -1;
	}

	ret = register_jprobe(&hcall_jpr);
	if (ret < 0)
	{
		debugPrint("ERROR - Hypercall sniffer planting failed");
		return ret;
	}
	debugPrint("INIT - Hypercall sniffer successfully planted");

	return 0;
}

void tracer_destroy(void)
{
	unregister_jprobe(&cpuid_jpr);
	debugPrint("CLEANUP - CPUID Sniffer unregistered");

	unregister_jprobe(&hcall_jpr);
	debugPrint("CLEANUP - Hypercall Sniffer unregistered");
}




#ifndef __SMDEFS

#include <linux/async.h>
#include <asm/atomic.h>

// Constants ...............

#define DIGEST_LENGTH 10
#define MAX_VCPUS 10
#define MAX_CPU_REQUESTS 200
#define MSGLEN 50
#define HC_ALARM 10
#define HC_ALIVE 11
#define DEVICE_NAME "sm_channel"
#define SIG_VM 0x0f

// Structure definitions

typedef bool (*Guard)(void);
typedef void (*Action)(void*,async_cookie_t);

typedef struct tagGuardedCommand
{
  bool periodic;
  Guard guard_func;
  Action action_func;
} GuardedCommand;

typedef struct tagVCPUState
{
 unsigned int bytes;
 void *cpu;
 atomic_t alive;
 bool toReset;
 pid_t pid;
 unsigned long last_rebooted;
 atomic_t dos_requests; //number of CPUID, RDTSC etc for this VCPU
 
} VCPUState;

typedef struct tagVMAlarm
{
	int pid;
} VMAlarm;

// External data....

extern int old_backup_phase;
extern int backup_phase;
extern int backup_period;
extern int stab_timer_period;
extern int watchdog_period;
extern int num_vcpus;

extern unsigned long recovery_period;

extern VCPUState states[MAX_VCPUS];

#define __SMDEFS
#endif

#ifndef __SMDEFS

#include <linux/async.h>
#include <asm/atomic.h>

// Constants ...............

#define DIGEST_LENGTH 10
#define MAX_VCPUS 10
#define MAX_CPU_REQUESTS 200
#define MSGLEN 50
#define DEVICE_NAME "sm_channel"

#define SIG_VMREBOOT 33
#define SIG_VMUPDATE 34

#define HC_ALARM 10
#define HC_ALIVE 11
#define HC_VMUP 12
#define HC_VMDOWN 13

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
 unsigned short ip[4];
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

extern unsigned long silence_period;

extern VCPUState states[MAX_VCPUS];

#define __SMDEFS
#endif

// Defining __KERNEL__ and MODULE allows us to access kernel-level code not usually available to userspace programs.
#undef __KERNEL__
#define __KERNEL__
 
#undef MODULE
#define MODULE
 
// Linux Kernel/LKM headers: module.h is needed by all modules and kernel.h is needed for KERN_INFO.
#include <linux/version.h>
#include <linux/module.h>    // included for all kernel modules
#include <linux/kernel.h>    // included for KERN_INFO
#include <linux/init.h>        // included for __init and __exit macros
#include <linux/timer.h>
#include <linux/jiffies.h>
#include <linux/async.h>
#include <linux/string.h>

#include "utils.h"
#include "guard_commands.h"
#include "sched.h"
#include "hypervisor.h"
#include "trafficman.h"
#include "watchdog.h"
#include "stabdrv.h"

MODULE_LICENSE("GPL");

/* Stabilization timers*/
static struct timer_list stabilization_timer;

static void runBackup(void)
{
  backup_phase = msecs_to_jiffies(jiffies) / backup_period;
	
  if (backup_phase > old_backup_phase) //backup period passed 
    {
     async_schedule(backupHVState,NULL);
     async_schedule(backupSchedulerState,NULL);
     async_schedule(backupTrafficState,NULL);
    }
	
  old_backup_phase = backup_phase;
}

static void refreshCurrentState(void)
{
  refreshHVState();
  refreshTrafficState();
  refreshSchedulerState();
}


//Callbacks for watchdog and timer
static void stabilization_timer_callback( unsigned long data )
{ 	
	//printk("Next SM phase in %d msecs\n", stab_timer_period);

	refreshCurrentState();

	runAllGuardedCommands();
	
    //runBackup();
    if (stab_timer_period > 0)
    	mod_timer( &stabilization_timer, jiffies + msecs_to_jiffies(stab_timer_period) );
	
}

int initStabilizationManager(void)
{
  int ret = 0;
  
  old_backup_phase = 0;
  backup_phase = 0;
  
  setup_timer( &stabilization_timer, stabilization_timer_callback, 0 );
  debugPrint("INIT - Setting up stabilization timer");
  ret = mod_timer( &stabilization_timer, jiffies + msecs_to_jiffies(stab_timer_period) );
  if (ret!=0) 
    { 
	  debugPrint("ERROR - Error in stabilization timer");
    }
  
  return ret;
}

static void cleanupStabilizationManager(void)
{
  int ret;
  
  debugPrint("CLEANUP - Main module uninstalling");
  ret = del_timer( &stabilization_timer );
  if (!ret) 
	  debugPrint("ERROR - The stabilization timer is still in use...");
  
}

//Module entry and exit  
static int __init main_init(void)
{     
  int ret = 0;
  debugPrint("INIT - Starting to load main");

  //ret |= initStabmanDevice();
  //ret |= initWatchdog();
  //ret |= initHypervisor();
  //ret |= initStabilizationManager();
  //ret |= initTrafficManager();
  //ret |= initScheduler();
  
  return ret;
}
 
static void __exit main_cleanup(void)
{   
  debugPrint("CLEANUP - Cleaning up main module");
  
  //cleanupHypervisor();
  //cleanupStabilizationManager();
  //cleanupTrafficManager();
  //cleanupScheduler();
  //cleanupWatchdog();
  //cleanupStabmanDevice();

  return;
}
 
module_init(main_init);
module_exit(main_cleanup);

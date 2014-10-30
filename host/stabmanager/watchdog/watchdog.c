#include <linux/timer.h>
#include <linux/jiffies.h>
#include <linux/reboot.h>

#include "../definitions.h"
#include "utils.h"
#include "guard_commands.h"

static struct timer_list watchdog_timer;

static void watchdog_callback(unsigned long data)
{
    int i = 0;
    //printk("Watchdog runs on %d CPUs\n", num_vcpus);

    runGuardedCommand(GC_HANDLE_DEAD_VMS);

    for (i = 0; i < num_vcpus; i++)
      {
    	atomic_set(&(states[i].alive), 0);
    	printk("CPU %d Status cleared %d\n", i, (int)(atomic_read(&(states[i].alive)))
    		  );
      }
    
    mod_timer( &watchdog_timer, jiffies + msecs_to_jiffies(watchdog_period) );
}

int initWatchdog(void)
{
  int ret;

  setup_timer( &watchdog_timer, watchdog_callback, 0 );  
  
  ret = mod_timer( &watchdog_timer, jiffies + msecs_to_jiffies(watchdog_period) );
  if (ret!=0) 
    { 
	  debugPrint("ERROR - Error in watchdog timer");
    }
  debugPrint("INIT - Watchdog");
  return ret;
}

void cleanupWatchdog(void)
{
  int ret;
  debugPrint("CLEANUP - Watchdog");
  
  ret = del_timer( &watchdog_timer );
  if (!ret) 
	  debugPrint("The watchdog timer is still in use...");
  
}

void kickWatchdog(void)
{
  mod_timer(&watchdog_timer, jiffies+msecs_to_jiffies(watchdog_period));
}

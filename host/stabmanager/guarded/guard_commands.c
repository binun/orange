
#include "../definitions.h"
#include <linux/async.h>

#include "utils.h"
#include "sched.h"
#include "hypervisor.h"
#include "trafficman.h"
#include "watchdog.h"

static GuardedCommand guarded_commands[] =
{
   {1, isHVUnsafeState,enforceHVSafeState},
   {0, isHVDeadVMs,enforceHVSafeState},
   {1, isSchedulerSafeState,enforceSchedulerSafeState},
   {1, isTrafficSafeState,enforceTrafficSafeState}
};

void runGuardedCommand(int index)
{
	if (guarded_commands[index].guard_func())
	      async_schedule(guarded_commands[index].action_func,NULL);
}

void runAllGuardedCommands(void)
{
  int i = 0;
  for (i = 0; i < (int)(sizeof(guarded_commands)/sizeof(GuardedCommand)); i++)
  {
    if (guarded_commands[i].periodic && guarded_commands[i].guard_func())
      async_schedule(guarded_commands[i].action_func,NULL);
  }
}



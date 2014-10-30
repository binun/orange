
#include <linux/kernel.h>
#include <linux/string.h>
#include <linux/async.h>
#include "utils.h"

bool isSchedulerSafeState(void)
{
	return 1;
}

void enforceSchedulerSafeState(void *_data, async_cookie_t c)
{
	debugPrint("	Make the Scheduler consistent");
}

void backupSchedulerState(void*data, async_cookie_t c)
{
	debugPrint("       Backup the scheduler state");
}

void refreshSchedulerState(void)
{
}

int initScheduler(void)
{
  debugPrint("INIT - Initialize the scheduler");
  return 0;
}

void cleanupScheduler(void)
{
  debugPrint("CLEANUP - Cleanup the scheduler");
}

#include "../definitions.h"


int initScheduler(void);
void cleanupScheduler(void);

bool isSchedulerSafeState(void);
void enforceSchedulerSafeState(void *_data, async_cookie_t c);
void backupSchedulerState(void *data,async_cookie_t c);
void refreshSchedulerState(void);

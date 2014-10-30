#include "../definitions.h"

int initTrafficManager(void);
void cleanupTrafficManager(void);

bool isTrafficSafeState(void);
void enforceTrafficSafeState(void *_data, async_cookie_t c);
void backupTrafficState(void *data, async_cookie_t c);
void refreshTrafficState(void);

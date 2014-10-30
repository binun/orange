#include "../definitions.h"

void registerDOSHit(void*);
int initHypervisor(void);
void cleanupHypervisor(void);

bool isHVUnsafeState(void);
bool isHVDeadVMs(void);
void enforceHVSafeState(void *_data, async_cookie_t c);

bool isHVUnderDDOS(void);
void enforceHVDOSProtection(void *_data, async_cookie_t c);

void backupHVState(void *data,async_cookie_t c);
void refreshHVState(void);

int tracer_init(void);
void tracer_destroy(void);

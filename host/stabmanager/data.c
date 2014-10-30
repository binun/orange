#include "definitions.h"

int stab_timer_period = 1000;
int watchdog_period = 2000;
int backup_period = 500;
int old_backup_phase=-1;
int backup_phase = 0;

int num_vcpus = 0;

unsigned long recovery_period = 60000; //1 minutes=5*60*1000 milliseconds

VCPUState states[MAX_VCPUS];




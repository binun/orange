extern bool debugMode;

bool current_is_vcpu_pid(void);
void* current_vcpu(void);
void debugPrint(char*);
void killVM(void*);

The Self-Stabilization Manager (abbrv. SSM) - An Overview

                                                Assembling

Go to the folder integrated. SSM is represented by a LKM (Loadable Kernel Module) named stabman.ko. Assembling the module is performed by executing 
the command 

make clean; make 

in this case the Makefile deletes the (outdated) object files and creates the module stabman.ko. After compiling, add the module to the running kernel 
(insmod ./stabman.ko) and see its output (watch -n 0.4 "dmesg | tail -n 20").


                                               Setting up the execution environment
                                               
The execution parameters are (so far) hardcoded into the implementation and kept in the following global variables in the consistency.h file:

 
* int stab_timer_period = 100 - the SSM executes every stab_timer_period milliseconds. 
* int   watchdog_period = 600 - the watchdog timer is delayed on watchdog_period milliseconds after a successful SSM run 
bool  reboot = false -   if reboot=true then the system reboots upon a watchdog signal
bool  kernel_panic = false - if kernel_panic=true the system panics upon a watchdog signal
int   backup_period = 500;   //the system state is saved every backup_period milliseconds


                                               Output
                                               
The output consists of the following messages:
 * Startup messages issued once during the module initialization:
 
     --- "Starting to load self-stabilizer!" 
     --- "Setting up stabilization timer"
     --- "There are ... VCPUs in the system"
     
 * The messages that illustrate the running process. These are:
     --- "Reporting the VCPU states" - followed by the IDTs for every VCPU. Issued at every SSM iteration
     --- "Make the HV driver/Scheduler/Traffic Manager". Issued at every SSM iteration.
     --- "Backup the scheduler/hypervisor/traffic manager state". Issued at every backup state iteration (so far every 500 msec).
    
 * The messages that illustrate the watchdog are issued by the watchdog signal handler: 
    --- "Watchdog fired!" - issued every time when the watchdog signal handler executed
    --- "Initiating system reboot"  - when the handler decides to reboot the system
    --- "Initiating panic"  - when the handler decides to make the system panic
    

                                                

   

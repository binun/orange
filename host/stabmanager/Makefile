CC := gcc
MODULE_NAME := stabman
KDIR  := /lib/modules/$(shell uname -r)/build
PWD   := $(shell pwd)
CFILES := data.c chardrv/stabdrv.c chardrv/findoffsets.c hypervisor/hypervisor.c hypervisor/cpuid_trace.c trafficman/trafficman.c watchdog/watchdog.c scheduler/sched.c utils/utils.c guarded/guard_commands.c main_stm.c
OBJS := $(CFILES:%.c=%.o)

obj-m := $(MODULE_NAME).o
$(MODULE_NAME)-objs := $(OBJS)
ccflags-y := -g
ccflags-y += -Wall
ccflags-y += -I$(src)/.
ccflags-y += -I$(src)/chardrv
ccflags-y += -I$(src)/hypervisor
ccflags-y += -I$(src)/trafficman
ccflags-y += -I$(src)/watchdog
ccflags-y += -I$(src)/scheduler
ccflags-y += -I$(src)/guarded
ccflags-y += -I$(src)/utils

default:
	$(MAKE) -C $(KDIR) M=$(PWD) modules

clean:
	rm -rf *.ko *.cmd Module.symvers modules.order
	find . -name "*.c~" -delete
	find . -name "*.o" -delete
	find . -name "*.cmd" -delete
	find . -name "*.mod.c" -delete

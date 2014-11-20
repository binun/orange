#include <config.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <inttypes.h>

#include <libvirt/libvirt.h>
#include <libvirt/virterror.h>
#include "vector/vector.h"

#include "defs.h"

#ifndef ATTRIBUTE_UNUSED
# define ATTRIBUTE_UNUSED __attribute__((__unused__))
#endif

int callback1ret = -1;
int callback2ret = -1;
int callback3ret = -1;
int callback4ret = -1;
int callback5ret = -1;
int callback6ret = -1;
int callback7ret = -1;
int callback8ret = -1;
int callback9ret = -1;
int callback10ret = -1;
int callback11ret = -1;
int callback12ret = -1;
int callback13ret = -1;

vector VMs;

extern int run ;
extern const char *eventToString(int);
extern const char *eventDetailToString(int, int);
extern int runShell(char*, char*, int);

int myEventAddHandleFunc  (int fd, int event,
                           virEventHandleCallback cb,
                           void *opaque,
                           virFreeCallback ff);
void myEventUpdateHandleFunc(int watch, int event);
int  myEventRemoveHandleFunc(int watch);

int myEventAddTimeoutFunc(int timeout,
                          virEventTimeoutCallback cb,
                          void *opaque,
                          virFreeCallback ff);
void myEventUpdateTimeoutFunc(int timer, int timout);
int myEventRemoveTimeoutFunc(int timer);

int myEventHandleTypeToPollEvent(virEventHandleType events);
virEventHandleType myPollEventToEventHandleType(int events);


static void connectClose(virConnectPtr conn ATTRIBUTE_UNUSED,
                         int reason,
                         void *opaque ATTRIBUTE_UNUSED)
{
    switch (reason) {
    case VIR_CONNECT_CLOSE_REASON_ERROR:
        fprintf(stderr, "Connection closed due to I/O error\n");
        break;
    case VIR_CONNECT_CLOSE_REASON_EOF:
        fprintf(stderr, "Connection closed due to end of file\n");
        break;
    case VIR_CONNECT_CLOSE_REASON_KEEPALIVE:
        fprintf(stderr, "Connection closed due to keepalive timeout\n");
        break;
    case VIR_CONNECT_CLOSE_REASON_CLIENT:
        fprintf(stderr, "Connection closed due to client request\n");
        break;
    default:
        fprintf(stderr, "Connection closed due to unknown reason\n");
        break;
    };
    run = 0;
}

static int myDomainEventCallback1(virConnectPtr conn ATTRIBUTE_UNUSED,
                                  virDomainPtr dom,
                                  int event,
                                  int detail,
                                  void *opaque ATTRIBUTE_UNUSED)
{
	VMStruct *vm1, *vm;
	char command[100] = "",spid[10] = "",ip[20] = "";
	int pid;

    printf("EVENT: Domain %s , Event %s Detail %s\n",virDomainGetName(dom),eventToString(event),eventDetailToString(event, detail));

    if (
         (virDomainEventType)event==VIR_DOMAIN_EVENT_STARTED &&
          (
            (virDomainEventStartedDetailType)detail==VIR_DOMAIN_EVENT_STARTED_BOOTED ||
            (virDomainEventStartedDetailType)detail==VIR_DOMAIN_EVENT_STARTED_MIGRATED
          )
       )
        {
          sprintf(command, "./vcpu-pid.sh %s",virDomainGetName(dom));
          runShell(command,spid,strlen(command)-1);
          pid = atoi(spid);

          memset(command,0,100);
          sprintf(command, "./vm-ip.sh %s",virDomainGetName(dom));
          runShell(command,ip,strlen(command)-1);

          vm1 = (VMStruct*)malloc(sizeof(VMStruct));
          memset(vm1,0, sizeof(VMStruct));
          vm1->pid = pid;
          strcpy(vm1->name,virDomainGetName(dom));
          strcpy(vm1->ip,ip);
          vm1->suspended = 0;
          vector_add(&VMs, vm1);

          printf(" Added VM: PID %d,Name %s, IP %s - Total %d VMs\n",
        		  vm1->pid, vm1->name,vm1->ip,vector_total(&VMs));
        }

    if ((virDomainEventType)event==VIR_DOMAIN_EVENT_SUSPENDED)
    {
    	vm1->suspended = 1;
    }

    if ((virDomainEventType)event==VIR_DOMAIN_EVENT_RESUMED)
    {
        vm1->suspended = 0;
    }

    if ((virDomainEventType)event==VIR_DOMAIN_EVENT_STOPPED ||
        (virDomainEventType)event==VIR_DOMAIN_EVENT_SHUTDOWN)
    {
        vector_remove(&VMs, virDomainGetName(dom));
        printf("VM %s to be removed; %d VMs remain\n", virDomainGetName(dom),vector_total(&VMs));
    }

    return 0;
}

static int myDomainEventRebootCallback(virConnectPtr conn ATTRIBUTE_UNUSED,
                                       virDomainPtr dom,
                                       void *opaque ATTRIBUTE_UNUSED)
{
    printf("%s EVENT: Domain %s(%d) rebooted\n", __func__, virDomainGetName(dom),
           virDomainGetID(dom));

    return 0;
}

static int myDomainEventRTCChangeCallback(virConnectPtr conn ATTRIBUTE_UNUSED,
                                          virDomainPtr dom,
                                          long long offset,
                                          void *opaque ATTRIBUTE_UNUSED)
{
    /* HACK: use asprintf since we have gnulib's wrapper for %lld on Win32
     * but don't have a printf() replacement with %lld */
    printf("EVENT: Domain %s RTC change %lld\n",
                 virDomainGetName(dom),
                 offset);
    return 0;
}

static int myDomainEventBalloonChangeCallback(virConnectPtr conn ATTRIBUTE_UNUSED,
                                              virDomainPtr dom,
                                              unsigned long long actual,
                               	               void *opaque ATTRIBUTE_UNUSED)
{
    printf("%s EVENT: Domain %s(%d) balloon change %" PRIuMAX "KB\n",
           __func__, virDomainGetName(dom), virDomainGetID(dom), (uintmax_t)actual);

    return 0;
}

static int myDomainEventWatchdogCallback(virConnectPtr conn ATTRIBUTE_UNUSED,
                                         virDomainPtr dom,
                                         int action,
                                         void *opaque ATTRIBUTE_UNUSED)
{
    printf("%s EVENT: Domain %s(%d) watchdog action=%d\n", __func__, virDomainGetName(dom),
           virDomainGetID(dom), action);

    return 0;
}

static int myDomainEventIOErrorCallback(virConnectPtr conn ATTRIBUTE_UNUSED,
                                        virDomainPtr dom,
                                        const char *srcPath,
                                        const char *devAlias,
                                        int action,
                                        void *opaque ATTRIBUTE_UNUSED)
{
    printf("%s EVENT: Domain %s(%d) io error path=%s alias=%s action=%d\n", __func__, virDomainGetName(dom),
           virDomainGetID(dom), srcPath, devAlias, action);

    return 0;
}

static int myDomainEventGraphicsCallback(virConnectPtr conn ATTRIBUTE_UNUSED,
                                         virDomainPtr dom,
                                         int phase,
                                         virDomainEventGraphicsAddressPtr local,
                                         virDomainEventGraphicsAddressPtr remote,
                                         const char *authScheme,
                                         virDomainEventGraphicsSubjectPtr subject,
                                         void *opaque ATTRIBUTE_UNUSED)
{
    int i;
    printf("%s EVENT: Domain %s(%d) graphics ", __func__, virDomainGetName(dom),
           virDomainGetID(dom));

    switch (phase) {
    case VIR_DOMAIN_EVENT_GRAPHICS_CONNECT:
        printf("connected ");
        break;
    case VIR_DOMAIN_EVENT_GRAPHICS_INITIALIZE:
        printf("initialized ");
        break;
    case VIR_DOMAIN_EVENT_GRAPHICS_DISCONNECT:
        printf("disconnected ");
        break;
    }

    printf("local: family=%d node=%s service=%s ",
           local->family, local->node, local->service);
    printf("remote: family=%d node=%s service=%s ",
           remote->family, remote->node, remote->service);

    printf("auth: %s ", authScheme);
    for (i = 0 ; i < subject->nidentity ; i++) {
        printf(" identity: %s=%s",
               subject->identities[i].type,
               subject->identities[i].name);
    }
    printf("\n");

    return 0;
}

static int myDomainEventControlErrorCallback(virConnectPtr conn ATTRIBUTE_UNUSED,
                                             virDomainPtr dom,
                                             void *opaque ATTRIBUTE_UNUSED)
{
    printf("%s EVENT: Domain %s(%d) control error\n", __func__, virDomainGetName(dom),
           virDomainGetID(dom));

    return 0;
}


static const char *diskChangeReasonStrings[] =
{
    "startupPolicy", /* 0 */
    /* add new reason here */
};
static int myDomainEventDiskChangeCallback(virConnectPtr conn ATTRIBUTE_UNUSED,
                                           virDomainPtr dom,
                                           const char *oldSrcPath,
                                           const char *newSrcPath,
                                           const char *devAlias,
                                           int reason,
                                           void *opaque ATTRIBUTE_UNUSED)
{

    printf("%s EVENT: Domain %s(%d) disk change oldSrcPath: %s newSrcPath: %s devAlias: %s reason: %s\n",
           __func__, virDomainGetName(dom), virDomainGetID(dom),
           oldSrcPath, newSrcPath, devAlias, diskChangeReasonStrings[reason]);
    return 0;
}

const char *trayChangeReasonStrings[] = {
    "open",
    "close",
};

static int myDomainEventTrayChangeCallback(virConnectPtr conn ATTRIBUTE_UNUSED,
                                           virDomainPtr dom,
                                           const char *devAlias,
                                           int reason,
                                           void *opaque ATTRIBUTE_UNUSED)
{
    printf("%s EVENT: Domain %s(%d) removable disk's tray change devAlias: %s reason: %s\n",
           __func__, virDomainGetName(dom), virDomainGetID(dom),
           devAlias, trayChangeReasonStrings[reason]);
    return 0;
}

static int myDomainEventPMWakeupCallback(virConnectPtr conn ATTRIBUTE_UNUSED,
                                         virDomainPtr dom,
                                         int reason ATTRIBUTE_UNUSED,
                                         void *opaque ATTRIBUTE_UNUSED)
{
    printf("%s EVENT: Domain %s(%d) system pmwakeup",
           __func__, virDomainGetName(dom), virDomainGetID(dom));
    return 0;
}

static int myDomainEventPMSuspendCallback(virConnectPtr conn ATTRIBUTE_UNUSED,
                                          virDomainPtr dom,
                                          int reason ATTRIBUTE_UNUSED,
                                          void *opaque ATTRIBUTE_UNUSED)
{
    printf("%s EVENT: Domain %s(%d) system pmsuspend",
           __func__, virDomainGetName(dom), virDomainGetID(dom));
    return 0;
}

static void myFreeFunc(void *opaque)
{
    char *str = (char*)opaque;
    //printf("%s: Freeing [%s]\n", __func__, str);
    free(str);
}

void registerLVSniffers(virConnectPtr dconn)
{
	printf("Registering handlers\n");

	vector_init(&VMs);

	virConnectRegisterCloseCallback(dconn, connectClose, NULL, NULL);

	callback1ret = virConnectDomainEventRegister(dconn, myDomainEventCallback1,
	                                                 strdup("Basic VM Events"), myFreeFunc);

	/*callback3ret = virConnectDomainEventRegisterAny(dconn,
	                                                    NULL,
	                                                    VIR_DOMAIN_EVENT_ID_REBOOT,
	                                                    VIR_DOMAIN_EVENT_CALLBACK(myDomainEventRebootCallback),
	                                                    strdup("callback reboot"), myFreeFunc);
    callback4ret = virConnectDomainEventRegisterAny(dconn,
	                                                    NULL,
	                                                    VIR_DOMAIN_EVENT_ID_RTC_CHANGE,
	                                                    VIR_DOMAIN_EVENT_CALLBACK(myDomainEventRTCChangeCallback),
	                                                    strdup("callback rtcchange"), myFreeFunc);
    callback5ret = virConnectDomainEventRegisterAny(dconn,
	                                                    NULL,
	                                                    VIR_DOMAIN_EVENT_ID_WATCHDOG,
	                                                    VIR_DOMAIN_EVENT_CALLBACK(myDomainEventWatchdogCallback),
	                                                    strdup("callback watchdog"), myFreeFunc);
    callback6ret = virConnectDomainEventRegisterAny(dconn,
	                                                    NULL,
	                                                    VIR_DOMAIN_EVENT_ID_IO_ERROR,
	                                                    VIR_DOMAIN_EVENT_CALLBACK(myDomainEventIOErrorCallback),
	                                                    strdup("callback io error"), myFreeFunc);
    callback7ret = virConnectDomainEventRegisterAny(dconn,
	                                                    NULL,
	                                                    VIR_DOMAIN_EVENT_ID_GRAPHICS,
	                                                    VIR_DOMAIN_EVENT_CALLBACK(myDomainEventGraphicsCallback),
	                                                    strdup("callback graphics"), myFreeFunc);
    callback8ret = virConnectDomainEventRegisterAny(dconn,
	                                                    NULL,
	                                                    VIR_DOMAIN_EVENT_ID_CONTROL_ERROR,
	                                                    VIR_DOMAIN_EVENT_CALLBACK(myDomainEventControlErrorCallback),
	                                                    strdup("callback control error"), myFreeFunc);
	callback9ret = virConnectDomainEventRegisterAny(dconn,
	                                                    NULL,
	                                                    VIR_DOMAIN_EVENT_ID_DISK_CHANGE,
	                                                    VIR_DOMAIN_EVENT_CALLBACK(myDomainEventDiskChangeCallback),
	                                                    strdup("disk change"), myFreeFunc);
	callback10ret = virConnectDomainEventRegisterAny(dconn,
	                                                     NULL,
	                                                     VIR_DOMAIN_EVENT_ID_TRAY_CHANGE,
	                                                     VIR_DOMAIN_EVENT_CALLBACK(myDomainEventTrayChangeCallback),
	                                                     strdup("tray change"), myFreeFunc);
	callback11ret = virConnectDomainEventRegisterAny(dconn,
	                                                     NULL,
	                                                     VIR_DOMAIN_EVENT_ID_PMWAKEUP,
	                                                     VIR_DOMAIN_EVENT_CALLBACK(myDomainEventPMWakeupCallback),
	                                                     strdup("pmwakeup"), myFreeFunc);
	callback12ret = virConnectDomainEventRegisterAny(dconn,
	                                                     NULL,
	                                                     VIR_DOMAIN_EVENT_ID_PMSUSPEND,
	                                                     VIR_DOMAIN_EVENT_CALLBACK(myDomainEventPMSuspendCallback),
	                                                     strdup("pmsuspend"), myFreeFunc);
	callback13ret = virConnectDomainEventRegisterAny(dconn,
	                                                     NULL,
	                                                     VIR_DOMAIN_EVENT_ID_BALLOON_CHANGE,
	                                                     VIR_DOMAIN_EVENT_CALLBACK(myDomainEventBalloonChangeCallback),
	                                                     strdup("callback balloonchange"), myFreeFunc);
    */
	if (
			(callback1ret != -1)
	        /*&& (callback3ret != -1) &&
	        (callback4ret != -1) &&
	        (callback5ret != -1) &&
	        (callback6ret != -1) &&
	        (callback7ret != -1) &&
	        (callback9ret != -1) &&
	        (callback10ret != -1) &&
	        (callback11ret != -1) &&
	        (callback12ret != -1) &&
	        (callback13ret != -1) */
	        )

	        if (virConnectSetKeepAlive(dconn, 5, 3) < 0)
	        {
	            virErrorPtr err = virGetLastError();
	            fprintf(stderr, "Failed to start keepalive protocol: %s\n",
	                    err && err->message ? err->message : "Unknown error");
	            run = 0;
	        }
}

void deregisterSniffers(virConnectPtr dconn)
{
	printf("Deregistering event handlers");

	virConnectDomainEventDeregister(dconn, myDomainEventCallback1);

	/*virConnectDomainEventDeregisterAny(dconn, callback3ret);
	virConnectDomainEventDeregisterAny(dconn, callback4ret);
	virConnectDomainEventDeregisterAny(dconn, callback5ret);
	virConnectDomainEventDeregisterAny(dconn, callback6ret);
	virConnectDomainEventDeregisterAny(dconn, callback7ret);
	virConnectDomainEventDeregisterAny(dconn, callback9ret);
	virConnectDomainEventDeregisterAny(dconn, callback10ret);
	virConnectDomainEventDeregisterAny(dconn, callback11ret);
	virConnectDomainEventDeregisterAny(dconn, callback12ret);
	virConnectDomainEventDeregisterAny(dconn, callback13ret);*/
}

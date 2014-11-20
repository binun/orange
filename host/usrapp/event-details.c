#include <config.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <inttypes.h>

#include <libvirt/libvirt.h>
#include <libvirt/virterror.h>


const char *eventToString(int event)
{
    const char *ret = "";
    switch ((virDomainEventType) event)
    {
        case VIR_DOMAIN_EVENT_DEFINED:
            ret ="Defined";
            break;
        case VIR_DOMAIN_EVENT_UNDEFINED:
            ret ="Undefined";
            break;
        case VIR_DOMAIN_EVENT_STARTED:
            ret ="Started";
            break;
        case VIR_DOMAIN_EVENT_SUSPENDED:
            ret ="Suspended";
            break;
        case VIR_DOMAIN_EVENT_RESUMED:
            ret ="Resumed";
            break;
        case VIR_DOMAIN_EVENT_STOPPED:
            ret ="Stopped";
            break;
        case VIR_DOMAIN_EVENT_SHUTDOWN:
            ret = "Shutdown";
            break;
    }
    return ret;
}

const char *eventDetailToString(int event, int detail)
{
    const char *ret = "";
    switch ((virDomainEventType) event) {
        case VIR_DOMAIN_EVENT_DEFINED:
            if (detail == VIR_DOMAIN_EVENT_DEFINED_ADDED)
                ret = "Added";
            else if (detail == VIR_DOMAIN_EVENT_DEFINED_UPDATED)
                ret = "Updated";
            break;
        case VIR_DOMAIN_EVENT_UNDEFINED:
            if (detail == VIR_DOMAIN_EVENT_UNDEFINED_REMOVED)
                ret = "Removed";
            break;
        case VIR_DOMAIN_EVENT_STARTED:
            switch ((virDomainEventStartedDetailType) detail) {
            case VIR_DOMAIN_EVENT_STARTED_BOOTED:
                ret = "Booted";
                break;
            case VIR_DOMAIN_EVENT_STARTED_MIGRATED:
                ret = "Migrated";
                break;
            case VIR_DOMAIN_EVENT_STARTED_RESTORED:
                ret = "Restored";
                break;
            case VIR_DOMAIN_EVENT_STARTED_FROM_SNAPSHOT:
                ret = "Snapshot";
                break;
            case VIR_DOMAIN_EVENT_STARTED_WAKEUP:
                ret = "Event wakeup";
                break;
            }
            break;
        case VIR_DOMAIN_EVENT_SUSPENDED:
            switch ((virDomainEventSuspendedDetailType) detail) {
            case VIR_DOMAIN_EVENT_SUSPENDED_PAUSED:
                ret = "Paused";
                break;
            case VIR_DOMAIN_EVENT_SUSPENDED_MIGRATED:
                ret = "Migrated";
                break;
            case VIR_DOMAIN_EVENT_SUSPENDED_IOERROR:
                ret = "I/O Error";
                break;
            case VIR_DOMAIN_EVENT_SUSPENDED_WATCHDOG:
                ret = "Watchdog";
                break;
            case VIR_DOMAIN_EVENT_SUSPENDED_RESTORED:
                ret = "Restored";
                break;
            case VIR_DOMAIN_EVENT_SUSPENDED_FROM_SNAPSHOT:
                ret = "Snapshot";
                break;
            }
            break;
        case VIR_DOMAIN_EVENT_RESUMED:
            switch ((virDomainEventResumedDetailType) detail) {
            case VIR_DOMAIN_EVENT_RESUMED_UNPAUSED:
                ret = "Unpaused";
                break;
            case VIR_DOMAIN_EVENT_RESUMED_MIGRATED:
                ret = "Migrated";
                break;
            case VIR_DOMAIN_EVENT_RESUMED_FROM_SNAPSHOT:
                ret = "Snapshot";
                break;
            }
            break;
        case VIR_DOMAIN_EVENT_STOPPED:
            switch ((virDomainEventStoppedDetailType) detail) {
            case VIR_DOMAIN_EVENT_STOPPED_SHUTDOWN:
                ret = "Shutdown";
                break;
            case VIR_DOMAIN_EVENT_STOPPED_DESTROYED:
                ret = "Destroyed";
                break;
            case VIR_DOMAIN_EVENT_STOPPED_CRASHED:
                ret = "Crashed";
                break;
            case VIR_DOMAIN_EVENT_STOPPED_MIGRATED:
                ret = "Migrated";
                break;
            case VIR_DOMAIN_EVENT_STOPPED_SAVED:
                ret = "Saved";
                break;
            case VIR_DOMAIN_EVENT_STOPPED_FAILED:
                ret = "Failed";
                break;
            case VIR_DOMAIN_EVENT_STOPPED_FROM_SNAPSHOT:
                ret = "Snapshot";
                break;
            }
            break;
        case VIR_DOMAIN_EVENT_SHUTDOWN:
            switch ((virDomainEventShutdownDetailType) detail) {
            case VIR_DOMAIN_EVENT_SHUTDOWN_FINISHED:
                ret = "Finished";
                break;
            }
            break;
    }
    return ret;
}

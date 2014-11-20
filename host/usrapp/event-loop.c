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

int run = 1;

extern void registerLVSniffers(virConnectPtr);
extern void deregisterSniffers(virConnectPtr);

static void stop(int sig)
{
    printf("Exiting on signal %d\n", sig);
    run = 0;
    exit(0);
}

int main(int argc, char **argv)
{
	struct sigaction action_stop;

    memset(&action_stop, 0, sizeof(action_stop));
    action_stop.sa_handler = stop;
    sigaction(SIGTERM, &action_stop, NULL);
    sigaction(SIGINT, &action_stop, NULL);

    virEventRegisterDefaultImpl();

    virConnectPtr dconn = virConnectOpen(NULL);
    if (!dconn)
    {
        printf("Error connecting to Qemu\n");
        return -1;
    }

    registerLVSniffers(dconn);

    while (run)
     {
       if (virEventRunDefaultImpl() < 0)
          {
            virErrorPtr err = virGetLastError();
            fprintf(stderr, "Failed to run event loop: %s\n",
                        err && err->message ? err->message : "Unknown error");
          }
     }

    deregisterSniffers(dconn);

    printf("Closing connection");
    if (dconn && virConnectClose(dconn) < 0)
    {
        printf("Error closing Qemu connection\n");
    }

    printf("Done\n");
    return 0;
}

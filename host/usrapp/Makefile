TARGET = client
CC = gcc
VMIDIR = /usr/share/libvmi
XMLDIR = /usr/include/libxml2

CFLAGS = -g -Wall -I$(XMLDIR) -I$(VMIDIR)
LIBPATHS = -L$(VMIDIR)/libvmi/.libs
LDFLAGS = -lvirt -lxml2 -lvmi
CFILES = libvirt-proxy.c
OBJECTS = $(CFILES:%.c=%.o)


client: $(OBJECTS)
	$(CC) $(CFLAGS) $(LIBPATHS) $(OBJECTS) -o $(TARGET) $(LDFLAGS)

clean:
	rm -f *~ *.o client

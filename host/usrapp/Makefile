TARGET = client
CC = gcc
VMIDIR = /usr/share/libvmi
# XMLDIR = /usr/include/libxml2

CFLAGS = -g -Wall -I$(VMIDIR)
LIBPATHS = -L$(VMIDIR)/libvmi/.libs
LDFLAGS = -lvirt -lvmi
CFILES = event-loop.c event-details.c callbacks.c utils.c vector/vector.c
OBJECTS = $(CFILES:%.c=%.o)

client: $(OBJECTS)
	$(CC) $(CFLAGS) $(LIBPATHS) $(OBJECTS) -o $(TARGET) $(LDFLAGS)

clean:
	rm -f *~ *.o client
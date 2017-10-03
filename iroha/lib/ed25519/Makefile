LIBDIR := lib

all: $(LIBDIR) $(LIBDIR)/libed25519.a $(LIBDIR)/libed25519.so 

CC := gcc
CFLAGS := -fPIC -O2 -pipe
CFLAGS += -Wall -pedantic
LDFLAGS += -Led25519
LIBDIR := lib

$(LIBDIR):
	mkdir -p $(LIBDIR)

SRCS = $(wildcard src/*.c)
OBJS = $(SRCS:.c=.o)

%.o: %.c
	$(CC) -c -o $@ $< $(CFLAGS)

$(LIBDIR)/libed25519.a: $(OBJS)
	ls $(OBJS)
	ar rcs $@ $^

$(LIBDIR)/libed25519.so: $(OBJS)
	$(CC) $(CFLAGS) -shared $(OBJS) -o $@

.PHONY: test
test: $(LIB)
	$(CC) $(CFLAGS) -o $@ test.c $(LDFLAGS) -L$(LIBDIR) -led25519

.PHONY: clean
clean:
	rm -fr $(LIBDIR)  test test.o $(OBJS)



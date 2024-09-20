CC = gcc
CFLAGS = -Wall -Wextra -Wpedantic -m64

TARGET = note

all: $(TARGET)

$(TARGET): $(TARGET).c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)

.PHONY: all clean

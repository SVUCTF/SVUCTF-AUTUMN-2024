#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void init() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void vuln() {
    char message[64];
    while (1) {
        memset(message, 0, sizeof(message));
        system("echo -n \"Enter your message (type 'exit' to quit): \"");
        read(0, message, 0x100);
        if (strncmp(message, "exit", 4) == 0) {
            break;
        }
        printf("You entered: %s\n", message);
    }
}

int main() {
    init();
    vuln();
    return EXIT_SUCCESS;
}

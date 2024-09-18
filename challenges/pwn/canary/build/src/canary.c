#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void init() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void banner() {
    printf(" ___  _  _  __  __  ___  ____  ____ \n");
    printf("/ __)( \\/ )(  )(  )/ __)(_  _)( ___)\n");
    printf("\\__ \\ \\  /  )(__)(( (__   )(   )__) \n");
    printf("(___/  \\/  (______)\\___) (__) (__) \n");
    printf("\n");
    printf("Welcome to the SVUCTF AUTUMN 2024!\n");
    printf("\n");
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
    banner();
    vuln();
    return EXIT_SUCCESS;
}

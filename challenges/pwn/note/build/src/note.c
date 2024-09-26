#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAX_NOTES 20
#define MAX_SIZE 0x100

char* notes[MAX_NOTES];
int note_count = 0;

void add_note() {
    if (note_count >= MAX_NOTES) {
        puts("Maximum number of notes reached.");
        return;
    }

    int size;
    printf("Enter note size (max %d): ", MAX_SIZE);
    scanf("%d", &size);
    if (size > MAX_SIZE) {
        puts("Size too large.");
        return;
    }

    notes[note_count] = (char*)malloc(size);

    printf("Enter note content: ");
    read(0, notes[note_count], size);

    note_count++;
    puts("Note added successfully.");
}

void delete_note() {
    int index;
    printf("Enter note index to delete: ");
    scanf("%d", &index);

    if (index < 0 || index >= note_count) {
        puts("Invalid index.");
        return;
    }

    free(notes[index]);
    puts("Note deleted successfully.");
}

void print_note() {
    int index;
    printf("Enter note index to print: ");
    scanf("%d", &index);

    if (index < 0 || index >= note_count) {
        puts("Invalid index.");
        return;
    }

    printf("Note content: ");
    puts(notes[index]);
}

void edit_note() {
    int index;
    printf("Enter note index to edit: ");
    scanf("%d", &index);

    if (index < 0 || index >= note_count) {
        puts("Invalid index.");
        return;
    }

    printf("Enter new content: ");
    read(0, notes[index], sizeof(notes[index]));
}

void menu() {
    puts("1. Add note");
    puts("2. Delete note");
    puts("3. Print note");
    puts("4. Edit note");
    puts("5. Exit");
    printf("Choice: ");
}

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

int main() {
    init();
    banner();

    int choice;
    while (1) {
        menu();
        scanf("%d", &choice);
        getchar();

        switch (choice) {
            case 1:
                add_note();
                break;
            case 2:
                delete_note();
                break;
            case 3:
                print_note();
                break;
            case 4:
                edit_note();
                break;
            case 5:
                exit(0);
            default:
                puts("Invalid choice.");
        }
    }

    return EXIT_SUCCESS;
}

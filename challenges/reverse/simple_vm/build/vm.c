#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_STACK 1000
#define MAX_MEMORY 1000
#define MAX_INPUT 100

typedef enum {
    PUSH,
    POP,
    ADD,
    SUB,
    MUL,
    DIV,
    AND,
    OR,
    XOR,
    NOT,
    ROL,
    ROR,
    JMP,
    JZ,
    JNZ,
    CMP,
    OUT,
    IN,
    HALT
} OpCode;

typedef struct {
    OpCode opcode;
    int operand;
} Instruction;

int stack[MAX_STACK];
int sp = -1;  // Stack pointer
Instruction memory[MAX_MEMORY];
int pc = 0;  // Program counter
char input[MAX_INPUT];
int input_index = 0;

void push(int x) {
    if (sp < MAX_STACK - 1) {
        stack[++sp] = x;
    } else {
        printf("Stack overflow\n");
        exit(1);
    }
}

int pop() {
    if (sp >= 0) {
        return stack[sp--];
    } else {
        printf("Stack underflow\n");
        exit(1);
    }
}

int rol(int value, int shift) {
    shift &= 7;
    return ((value << shift) | (value >> (8 - shift))) & 0xFF;
}

int ror(int value, int shift) {
    shift &= 8;
    return ((value >> shift) | (value << (8 - shift))) & 0xFF;
}

void execute(Instruction* program, int program_size) {
    while (pc < program_size) {
        Instruction instr = program[pc++];
        int a, b, result;

        switch (instr.opcode) {
            case PUSH:
                push(instr.operand);
                break;
            case POP:
                pop();
                break;
            case ADD:
                push(pop() + pop());
                break;
            case SUB:
                b = pop();
                a = pop();
                push(a - b);
                break;
            case MUL:
                push(pop() * pop());
                break;
            case DIV:
                b = pop();
                a = pop();
                if (b != 0)
                    push(a / b);
                else {
                    printf("Division by zero\n");
                    exit(1);
                }
                break;
            case AND:
                push(pop() & pop());
                break;
            case OR:
                push(pop() | pop());
                break;
            case XOR:
                push(pop() ^ pop());
                break;
            case NOT:
                push(~pop());
                break;
            case ROL:
                b = pop();
                a = pop();
                push(rol(a, b));
                break;
            case ROR:
                b = pop();
                a = pop();
                push(ror(a, b));
                break;
            case JMP:
                pc = instr.operand;
                break;
            case JZ:
                if (pop() == 0)
                    pc = instr.operand;
                break;
            case JNZ:
                if (pop() != 0)
                    pc = instr.operand;
                break;
            case CMP:
                b = pop();
                a = pop();
                result = (a == b) ? 0 : (a < b ? -1 : 1);
                push(result);
                break;
            case OUT:
                printf("%c", (char)pop());
                break;
            case IN:
                if (input_index < strlen(input)) {
                    push((int)input[input_index++]);
                } else {
                    push(-1);  // EOF
                }
                break;
            case HALT:
                return;
            default:
                printf("Unknown instruction\n");
                exit(1);
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        printf("Usage: %s <encoded_flag_file>\n", argv[0]);
        return 1;
    }

    FILE* file = fopen(argv[1], "rb");
    if (file == NULL) {
        printf("Cannot open file\n");
        return 1;
    }

    int program_size = 0;
    while (fread(&memory[program_size], sizeof(Instruction), 1, file) == 1) {
        program_size++;
    }
    fclose(file);

    printf("Enter the flag: ");
    if (fgets(input, MAX_INPUT, stdin) == NULL) {
        printf("Error reading input\n");
        return 1;
    }
    input[strcspn(input, "\n")] = 0;

    execute(memory, program_size);
    return 0;
}

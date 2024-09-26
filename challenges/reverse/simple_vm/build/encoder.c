#include <stdio.h>
#include <string.h>

#define MAX_FLAG_LENGTH 100
#define MAX_INSTRUCTIONS 10000

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

Instruction program[MAX_INSTRUCTIONS];
int program_size = 0;

unsigned char rol(unsigned char value, int shift) {
    shift &= 7;
    return (value << shift) | (value >> (8 - shift));
}

unsigned char ror(unsigned char value, int shift) {
    shift &= 7;
    return (value >> shift) | (value << (8 - shift));
}

void add_instruction(OpCode opcode, int operand) {
    program[program_size].opcode = opcode;
    program[program_size].operand = operand;
    program_size++;
}

void encode_char(char c) {
    add_instruction(IN, 0);  // 读取输入

    add_instruction(PUSH, 0xA5);
    add_instruction(XOR, 0);  // 异或 10100101

    add_instruction(PUSH, 3);
    add_instruction(ROL, 0);  // 循环左移 3 位

    add_instruction(PUSH, 0x33);
    add_instruction(XOR, 0);  // 异或 00110011

    add_instruction(PUSH, 5);
    add_instruction(ROR, 0);  // 循环右移 5 位

    add_instruction(PUSH, 0xF0);
    add_instruction(XOR, 0);  // 异或 11110000

    // 将结果与预期值比较
    unsigned char expected = ror(rol(c ^ 0xA5, 3) ^ 0x33, 5) ^ 0xF0;

    add_instruction(PUSH, expected);
    add_instruction(XOR, 0);  // 异或操作：如果相等，结果为0
    add_instruction(PUSH, 1);
    add_instruction(ADD, 0);  // 如果字符匹配，栈顶将是1；否则大于1
}

void add_result_messages() {
    // 成功消息
    add_instruction(PUSH, 'C');
    add_instruction(OUT, 0);
    add_instruction(PUSH, 'o');
    add_instruction(OUT, 0);
    add_instruction(PUSH, 'r');
    add_instruction(OUT, 0);
    add_instruction(PUSH, 'r');
    add_instruction(OUT, 0);
    add_instruction(PUSH, 'e');
    add_instruction(OUT, 0);
    add_instruction(PUSH, 'c');
    add_instruction(OUT, 0);
    add_instruction(PUSH, 't');
    add_instruction(OUT, 0);
    add_instruction(PUSH, '!');
    add_instruction(OUT, 0);
    add_instruction(PUSH, '\n');
    add_instruction(OUT, 0);
    add_instruction(HALT, 0);

    // 失败消息
    add_instruction(PUSH, 'W');
    add_instruction(OUT, 0);
    add_instruction(PUSH, 'r');
    add_instruction(OUT, 0);
    add_instruction(PUSH, 'o');
    add_instruction(OUT, 0);
    add_instruction(PUSH, 'n');
    add_instruction(OUT, 0);
    add_instruction(PUSH, 'g');
    add_instruction(OUT, 0);
    add_instruction(PUSH, '!');
    add_instruction(OUT, 0);
    add_instruction(PUSH, '\n');
    add_instruction(OUT, 0);
    add_instruction(HALT, 0);
}

void encode_flag(const char* flag) {
    int flag_length = strlen(flag);

    // 初始化累加器为1
    add_instruction(PUSH, 1);

    // 编码每个字符
    for (int i = 0; i < flag_length; i++) {
        encode_char(flag[i]);
        add_instruction(MUL, 0);  // 将结果与累加器相乘
    }

    // 检查最终结果
    add_instruction(PUSH, 1);
    add_instruction(CMP, 0);
    add_instruction(JZ, program_size + 2);  // 如果相等（结果为1），跳到正确消息
    add_instruction(JMP, program_size + 20);  // 否则，跳到错误消息

    // 添加结果消息
    add_result_messages();
}

int main() {
    char flag[MAX_FLAG_LENGTH];
    printf("Enter the flag: ");
    fgets(flag, sizeof(flag), stdin);
    flag[strcspn(flag, "\n")] = 0;

    encode_flag(flag);

    FILE* file = fopen("flag.bin", "wb");
    fwrite(program, sizeof(Instruction), program_size, file);
    fclose(file);

    printf("Encoded flag has been written to 'flag.bin'\n");
    return 0;
}

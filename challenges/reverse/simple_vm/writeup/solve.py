import struct
from enum import Enum


class OpCode(Enum):
    PUSH = 0
    POP = 1
    ADD = 2
    SUB = 3
    MUL = 4
    DIV = 5
    AND = 6
    OR = 7
    XOR = 8
    NOT = 9
    ROL = 10
    ROR = 11
    JMP = 12
    JZ = 13
    JNZ = 14
    CMP = 15
    OUT = 16
    IN = 17
    HALT = 18


def parse_flag_bin(filename):
    with open(filename, "rb") as f:
        data = f.read()

    instructions = []
    for i in range(0, len(data), 8):
        op, operand = struct.unpack("<II", data[i : i + 8])
        instructions.append((OpCode(op), operand))

    return instructions


def print_instructions(instructions):
    for i, (op, operand) in enumerate(instructions):
        if op in [OpCode.PUSH, OpCode.JMP, OpCode.JZ, OpCode.JNZ]:
            print(f"{i:04d}: {op.name:<4} {operand}")
        elif op == OpCode.IN:
            print("-" * 15)
            print(f"{i:04d}: {op.name}")
        else:
            print(f"{i:04d}: {op.name}")


def extract_expected_chars(instructions):
    expected_chars = []
    for i in range(len(instructions)):
        op, operand = instructions[i]
        if (
            op == OpCode.PUSH
            and instructions[i - 1][0] == OpCode.XOR
            and instructions[i + 1][0] == OpCode.XOR
        ):
            expected_chars.append(operand)

    return expected_chars


def rol(value, shift):
    return ((value << shift) | (value >> (8 - shift))) & 0xFF


def ror(value, shift):
    return ((value >> shift) | (value << (8 - shift))) & 0xFF


def decode_flag(expected_chars):
    flag = ""
    for char in expected_chars:
        char ^= 0xF0
        char = rol(char, 5)
        char ^= 0x33
        char = ror(char, 3)
        char ^= 0xA5
        flag += chr(char)

    return flag


instructions = parse_flag_bin("flag.bin")
print_instructions(instructions)

expected_chars = extract_expected_chars(instructions)
print(f"expected_chars: {expected_chars}")

flag = decode_flag(expected_chars)
print(f"flag: {flag}")

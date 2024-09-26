import struct

# fmt: off
# [0x0000129b]> pcp 0x1f @ obj.encrypted_flag
encrypted_flag = struct.pack("45B", *[
    0xc8, 0xcf, 0xce, 0x38, 0xc9, 0x3f, 0xf0, 0xc8, 0xc6, 0x38, 0xd4, 
    0x2a, 0xe8, 0xd4, 0x29, 0xd4, 0xc6, 0x29, 0xdc, 0x2a, 0xd8, 0x29, 
    0xe1, 0xd4, 0xc8, 0x28, 0xe1, 0xdf, 0xd4, 0xc6, 0x25, 0xd9, 0x2a, 
    0xdf, 0xf2, 0x2a, 0xe7, 0xdc, 0xd4, 0x38, 0x25, 0xd9, 0x28, 0x1a, 
    0xf6])
# fmt: on

flag = []
for char in encrypted_flag:
    char ^= 0x42
    char -= 0x37
    flag.append(chr(char))

print("".join(flag))

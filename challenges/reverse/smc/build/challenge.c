#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>

const unsigned char encrypted_flag[] = {
    0xC8, 0xCF, 0xCE, 0x38, 0xC9, 0x3F, 0xF0, 0xC8, 0xC6, 0x38, 0xD4, 0x2A,
    0xE8, 0xD4, 0x29, 0xD4, 0xC6, 0x29, 0xDC, 0x2A, 0xD8, 0x29, 0xE1, 0xD4,
    0xC8, 0x28, 0xE1, 0xDF, 0xD4, 0xC6, 0x25, 0xD9, 0x2A, 0xDF, 0xF2, 0x2A,
    0xE7, 0xDC, 0xD4, 0x38, 0x25, 0xD9, 0x28, 0x1A, 0xF6};

// radare2 -AA -w challenge
// [0x000011c9]> s sym.encrypt_data
// [0x000011c9]> afi
// [0x000011c9]> b 117
// [0x000011c9]> woa 0x73
// [0x000011c9]> wox 0x24
void encrypt_data(char* data, size_t len) {
    const char xor_key = 0x42;
    const char add_key = 0x37;
    for (size_t i = 0; i < len; i++) {
        data[i] += add_key;
        data[i] ^= xor_key;
    }
}

void decrypt_func(unsigned char* func, size_t func_size) {
    const unsigned char xor_key = 0x24;
    const unsigned char sub_key = 0x73;

    for (size_t i = 0; i < func_size; i++) {
        func[i] ^= xor_key;
        func[i] -= sub_key;
    }
}

int main() {
    char input[100];

    long page_size = sysconf(_SC_PAGESIZE);
    uintptr_t page_start = (uintptr_t)encrypt_data & ~(page_size - 1);
    if (mprotect((void*)page_start, page_size,
                 PROT_READ | PROT_WRITE | PROT_EXEC) == -1) {
        perror("mprotect failed");
        return 1;
    }

    size_t func_size = 117;
    decrypt_func((unsigned char*)encrypt_data, func_size);

    printf("Enter your flag: ");
    if (fgets(input, sizeof(input), stdin) == NULL) {
        printf("Error reading input\n");
        return 1;
    }

    encrypt_data(input, strlen(input));

    if (memcmp(input, encrypted_flag, sizeof(encrypted_flag)) == 0) {
        printf("Congratulations! You've solved the challenge!\n");
    } else {
        printf("Sorry, that's not correct. Try again!\n");
    }

    return 0;
}

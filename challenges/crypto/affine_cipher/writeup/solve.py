import math
import string
from itertools import permutations


def affine_decrypt(ciphertext, a, b, charset):
    m = len(charset)
    a_inv = pow(a, -1, m)
    plaintext = []
    for char in ciphertext:
        if char in charset:
            c = charset.index(char)
            p = (a_inv * (c - b)) % m
            plaintext.append(charset[p])
        else:
            plaintext.append(char)
    return "".join(plaintext)


ciphertext = "P6XNy4{4Wbh-PhvAA-oIJAGGAGJ5-NbhBI-dWIvy-ysAGJ5}"

for charset_perm in permutations(
    [string.ascii_uppercase, string.ascii_lowercase, string.digits]
):
    charset = "".join(charset_perm)
    m = len(charset)
    print(f"charset = {charset}")

    for a in range(1, m):
        if math.gcd(a, m) != 1:
            continue
        for b in range(m):
            decrypted_text = affine_decrypt(ciphertext, a, b, charset)
            if decrypted_text and "SVUCTF" in decrypted_text:
                print(f"a = {a}, b = {b} -> {decrypted_text}")

    print("-" * 72)

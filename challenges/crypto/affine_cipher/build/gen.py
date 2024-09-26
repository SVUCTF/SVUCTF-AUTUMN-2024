import string
import math

charset = string.digits + string.ascii_uppercase + string.ascii_lowercase
m = len(charset)


def affine_encrypt(plaintext, a, b, charset):
    if not math.gcd(a, m) == 1:
        return None
    ciphertext = []
    for char in plaintext:
        if char in charset:
            p = charset.index(char)
            c = (a * p + b) % m
            ciphertext.append(charset[c])
        else:
            ciphertext.append(char)
    return "".join(ciphertext)


def main():
    plaintext = "SVUCTF{Fr0m-Sma11-B3g1nn1ngs-C0me3-Gr3aT-Th1ngs}"
    a = 35
    b = 37

    encrypted_text = affine_encrypt(plaintext, a, b, charset)
    print(f"Plaintext: {plaintext}")
    print(f"Encrypted (a={a}, b={b}): {encrypted_text}")


if __name__ == "__main__":
    main()

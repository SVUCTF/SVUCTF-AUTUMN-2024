flag = "SVUCTF{SMC_1s_4_M4g1c4l_S3lf_M0d1fy1ng_C0d3!}"

hex_values = []
for char in flag:
    char_code = ord(char)
    char_code += 0x37
    char_code ^= 0x42
    hex_values.append(f"0x{(char_code):02X}")

print(f"const unsigned char encrypted_flag[] = {{{', '.join(hex_values)}}};")

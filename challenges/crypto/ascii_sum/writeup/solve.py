encrypted = [
    169,
    171,
    152,
    151,
    154,
    193,
    210,
    191,
    225,
    170,
    159,
    158,
    164,
    211,
    201,
    223,
    232,
    231,
    161,
    113,
    116,
    143,
    144,
    133,
    209,
]

flag = ["S"]

for num in encrypted:
    next_char = num - ord(flag[-1])
    flag.append(chr(next_char))

print("".join(flag))

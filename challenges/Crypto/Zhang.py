
# 233,235,216,215,218,225,210,191,225,170,159,158,164,211,201,223,232,231,161,113,116,143,144,133,209,


from secrets import flag
size = len(flag)
for i in range(size - 1):
    print(ord(flag[i]) + ord(flag[i + 1]), end=",")





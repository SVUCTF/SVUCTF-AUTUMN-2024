# 169,171,152,151,154,193,210,191,225,170,159,158,164,211,201,223,232,231,161,113,116,143,144,133,209,

from secrets import flag

for i in range(len(flag) - 1):
    print(ord(flag[i]) + ord(flag[i + 1]), end=",")

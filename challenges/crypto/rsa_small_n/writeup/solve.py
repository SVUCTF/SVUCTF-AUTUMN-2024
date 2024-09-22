from Crypto.Util.number import inverse, long_to_bytes, bytes_to_long
import math


c = 957698255151384368606624936473822523773515635988447837939657
p = 1138974730065136957261200778603
q = 1203220651376767521371118453437
n = p * q
e = 65537

# 计算私钥 d 并进行初始解密
# 得到的 m 是原始消息模 n 的结果，即 m ≡ original_m (mod n)
d = inverse(e, (p - 1) * (q - 1))
m = pow(c, d, n)

prefix = b"SVUCTF{"
suffix = b"}"

# 首先调整m，使其以 '}' (0x7d) 结尾
while m % 256 != ord(suffix):
    m += n

# 估计 Flag 的总长度
# math.log(m, 256) 计算得出 m 的字节数，减去前缀长度，得到 Flag 内容部分的估计长度
# target = b"SVUCTF{0000000..."
target_length = math.floor(math.log(m, 256))
target = prefix.ljust(target_length, b"0")

# 定义跳跃步长
# n * 256 确保每次跳跃不会改变最后一个字节
# 加 jump 实际上是在最低有效字节之前插入一个新字节
jump = n * 256

# 定义有效字符集
valid_chars = set(b"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_{}")

while True:
    md = long_to_bytes(m)

    # 检查是否找到有效的Flag
    if set(md) <= valid_chars:
        print(md.decode())
        break

    if md.startswith(prefix):
        # 如果以正确前缀开始，尝试下一个可能的值
        m += jump
    else:
        # 一旦 md 不再以 prefix 开头，继续添加 jump 不会使它重新以 prefix 开头
        # 因为如果失去了正确前缀，意味着发生了"进位"，影响了 prefix 所在的高位字节
        # 继续添加 jump 只会影响更低位的字节，不会撤销这个进位效果

        # 当前长度下无法找到正确的 Flag，需要增加 Flag 长度
        # 快速调整 m 到新的目标范围
        distance = bytes_to_long(target) - m
        m += jump * math.ceil(distance / jump)

        # 更新目标长度，为下一轮搜索做准备
        target += b"0"

from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes, inverse

p = getPrime(100)
q = getPrime(100)
n = p * q
e = 65537

message = b"SVUCTF{关于flag为什么不能是中文的这件事我也不是很清楚}"
m = bytes_to_long(message)
c = pow(m, e, n)

print(f"c = {c}")
print(f"p = {p}")
print(f"q = {q}")
#  c = 957698255151384368606624936473822523773515635988447837939657
#  p = 1138974730065136957261200778603
#  q = 1203220651376767521371118453437

d = inverse(e, (p - 1) * (q - 1))
newm = pow(c, d, n)

print(long_to_bytes(newm))
#  b'\xbfs\x93\xd0\n\x8a\xc8\xc6\xab\xedBvS\x1f\xbeKe\xf7r:SQ>n\xc3'

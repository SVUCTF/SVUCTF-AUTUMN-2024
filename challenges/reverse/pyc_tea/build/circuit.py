import struct


class LogicGate:
    @staticmethod
    def AND(a, b):
        return (a & b) & 0xFFFFFFFF

    @staticmethod
    def OR(a, b):
        return a | b

    @staticmethod
    def XOR(a, b):
        return a ^ b

    @staticmethod
    def NOT(a):
        return ~a & 0xFFFFFFFF

    @staticmethod
    def ADD(a, b):
        return (a + b) & 0xFFFFFFFF

    @staticmethod
    def NAND(a, b):
        return LogicGate.NOT(LogicGate.AND(a, b))

    @staticmethod
    def NOR(a, b):
        return LogicGate.NOT(LogicGate.OR(a, b))


class Circuit:
    def __init__(self):
        self.logic = LogicGate()

    def left_shift(self, value, shift):
        return (value << shift) & 0xFFFFFFFF

    def right_shift(self, value, shift):
        return (value >> shift) & 0xFFFFFFFF

    def processing_cycle(self, v0, v1, sum, k0, k1, k2, k3):
        temp1 = self.logic.ADD(self.left_shift(v1, 4), k0)
        temp2 = self.logic.ADD(v1, sum)
        temp3 = self.logic.ADD(self.right_shift(v1, 5), k1)
        new_v0 = self.logic.ADD(v0, self.logic.XOR(temp1, self.logic.XOR(temp2, temp3)))

        temp4 = self.logic.ADD(self.left_shift(new_v0, 4), k2)
        temp5 = self.logic.ADD(new_v0, sum)
        temp6 = self.logic.ADD(self.right_shift(new_v0, 5), k3)
        new_v1 = self.logic.ADD(v1, self.logic.XOR(temp4, self.logic.XOR(temp5, temp6)))

        return new_v0, new_v1

    def process_data_block(self, v, k):
        v0, v1 = struct.unpack("II", v)
        k0, k1, k2, k3 = struct.unpack("IIII", k)
        sum = 0x4B1D
        delta = 0xDEADBEEF
        for _ in range(32):
            sum = self.logic.ADD(sum, delta)
            v0, v1 = self.processing_cycle(v0, v1, sum, k0, k1, k2, k3)
        return struct.pack("II", v0, v1)

    def process_data(self, input_data, key):
        padded_data = input_data + b"\x00" * (8 - len(input_data) % 8)

        processed_data = b""
        for i in range(0, len(padded_data), 8):
            block = padded_data[i : i + 8]
            processed_block = self.process_data_block(block, key)
            processed_data += processed_block

        return processed_data


def verify_secret_message(user_input):
    key = b"SVUCTF_K3Y_2024!"
    encoded_secret = b"I\xc0T\xee?~1\x08-\x9fy\xdd\x12\xb7z\x19(\xb7\xd2\xcbY1~YI\x89\xb0\x08\xf7EXh@'S\x96Cp0\x03"
    circuit = Circuit()
    user_encoded = circuit.process_data(user_input.encode(), key)
    return user_encoded == encoded_secret


def main():
    user_input = input("请输入秘密信息: ")
    if verify_secret_message(user_input):
        print("验证成功！")
    else:
        print("验证失败！")


if __name__ == "__main__":
    main()

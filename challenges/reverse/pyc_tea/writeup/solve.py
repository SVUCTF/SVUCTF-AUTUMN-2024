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
    def SUB(a, b):
        return (a - b) & 0xFFFFFFFF

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
        temp4 = self.logic.ADD(self.left_shift(v0, 4), k2)
        temp5 = self.logic.ADD(v0, sum)
        temp6 = self.logic.ADD(self.right_shift(v0, 5), k3)
        bew_v1 = self.logic.SUB(v1, self.logic.XOR(temp4, self.logic.XOR(temp5, temp6)))

        temp1 = self.logic.ADD(self.left_shift(bew_v1, 4), k0)
        temp2 = self.logic.ADD(bew_v1, sum)
        temp3 = self.logic.ADD(self.right_shift(bew_v1, 5), k1)
        new_v0 = self.logic.SUB(v0, self.logic.XOR(temp1, self.logic.XOR(temp2, temp3)))

        return new_v0, bew_v1

    def process_data_block(self, v, k):
        v0, v1 = struct.unpack("II", v)
        k0, k1, k2, k3 = struct.unpack("IIII", k)
        delta = 0xDEADBEEF
        sum = (0x4B1D + (delta * 32)) & 0xFFFFFFFF
        for _ in range(32):
            v0, v1 = self.processing_cycle(v0, v1, sum, k0, k1, k2, k3)
            sum = self.logic.SUB(sum, delta)
        return struct.pack("II", v0, v1)

    def process_data(self, input_data, key):
        processed_data = b""
        for i in range(0, len(input_data), 8):
            block = input_data[i : i + 8]
            processed_block = self.process_data_block(block, key)
            processed_data += processed_block

        return processed_data.rstrip(b"\x00")


def main():
    key = b"SVUCTF_K3Y_2024!"
    encoded_secret = b"I\xc0T\xee?~1\x08-\x9fy\xdd\x12\xb7z\x19(\xb7\xd2\xcbY1~YI\x89\xb0\x08\xf7EXh@'S\x96Cp0\x03"
    circuit = Circuit()
    flag = circuit.process_data(encoded_secret, key)
    print(flag)


if __name__ == "__main__":
    main()

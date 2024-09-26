import random
from scapy.layers.usb import USBpcap
from scapy.packet import Raw
from scapy.utils import wrpcap

message = "SVUCTF{此杯人岂独骚人事_三百篇中半是愁}"
message = "".join(f"\\u{ord(c):04x}" for c in message)
print(message)

KEY_CODES = {
    "a": 0x04,
    "b": 0x05,
    "c": 0x06,
    "d": 0x07,
    "e": 0x08,
    "f": 0x09,
    "g": 0x0A,
    "h": 0x0B,
    "i": 0x0C,
    "j": 0x0D,
    "k": 0x0E,
    "l": 0x0F,
    "m": 0x10,
    "n": 0x11,
    "o": 0x12,
    "p": 0x13,
    "q": 0x14,
    "r": 0x15,
    "s": 0x16,
    "t": 0x17,
    "u": 0x18,
    "v": 0x19,
    "w": 0x1A,
    "x": 0x1B,
    "y": 0x1C,
    "z": 0x1D,
    "A": 0x04,
    "B": 0x05,
    "C": 0x06,
    "D": 0x07,
    "E": 0x08,
    "F": 0x09,
    "G": 0x0A,
    "H": 0x0B,
    "I": 0x0C,
    "J": 0x0D,
    "K": 0x0E,
    "L": 0x0F,
    "M": 0x10,
    "N": 0x11,
    "O": 0x12,
    "P": 0x13,
    "Q": 0x14,
    "R": 0x15,
    "S": 0x16,
    "T": 0x17,
    "U": 0x18,
    "V": 0x19,
    "W": 0x1A,
    "X": 0x1B,
    "Y": 0x1C,
    "Z": 0x1D,
    "1": 0x1E,
    "2": 0x1F,
    "3": 0x20,
    "4": 0x21,
    "5": 0x22,
    "6": 0x23,
    "7": 0x24,
    "8": 0x25,
    "9": 0x26,
    "0": 0x27,
    "\n": 0x28,
    " ": 0x2C,
    "-": 0x2D,
    "=": 0x2E,
    "[": 0x2F,
    "]": 0x30,
    "\\": 0x31,
    ";": 0x33,
    "'": 0x34,
    "`": 0x35,
    ",": 0x36,
    ".": 0x37,
    "/": 0x38,
}


def get_keycode_and_modifier(char):
    if char in KEY_CODES:
        if char.isupper():
            return KEY_CODES[char], 0x02  # Shift modifier for uppercase
        else:
            return KEY_CODES[char], 0x00
    else:
        print(
            f"Warning: Character '{char}' not found in KEY_CODES, using space instead."
        )
        return KEY_CODES[" "], 0x00


packets = []
for char in message:
    key_code, modifier = get_keycode_and_modifier(char)

    # 添加按键数据包 (URB_SUBMIT)
    press_pkt = USBpcap(
        headerLen=80,
        res=0,
        irpId=random.getrandbits(32),
        usbd_status=0x0,
        function=0x0009,
        info=0x01,  # URB_SUBMIT
        bus=1,
        device=1,
        endpoint=0x81,
        transfer=0x01,
        dataLength=8,
    )
    press_pkt /= Raw(
        load=bytes([modifier, 0x00, key_code, 0x00, 0x00, 0x00, 0x00, 0x00])
    )
    packets.append(press_pkt)

    # 添加释放数据包 (URB_COMPLETE)
    release_pkt = USBpcap(
        headerLen=80,
        res=0,
        irpId=random.getrandbits(32),
        usbd_status=0x0,
        function=0x0009,
        info=0x02,  # URB_COMPLETE
        bus=1,
        device=1,
        endpoint=0x81,
        transfer=0x01,
        dataLength=8,
    )
    release_pkt /= Raw(load=bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
    packets.append(release_pkt)

wrpcap("song.pcap", packets)

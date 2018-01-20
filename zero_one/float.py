"""
float

    V = (-1)^s * M * 2^E



Show bits of a float in c language


c float: 4 bytes

---------------------------------------------------------------
|sign(1 byte)|    exponent(8 bytes)   |  mantissa(23 bytes)   |
---------------------------------------------------------------

exponent: store as an unsigned integer
mantissa: value between 1.0 and (almost) 2.0


References:
1. https://stackoverflow.com/q/7644699
2. http://www.oxfordmathcenter.com/drupal7/node/43
"""

import struct


def float_to_bytes(num: float) -> str:
    binary = []
    for c in struct.pack('!f', num):
        byte = bin(c).replace('0b', '').rjust(8, '0')
        binary.append(byte)
    return ''.join(binary)


x = float_to_bytes(1.23)
print(x)

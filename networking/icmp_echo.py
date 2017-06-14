# -*- coding: utf-8 -*-

import random
import socket


def int_to_binary(num):
    if num >= 256:
        binary = "{:0>16b}".format(num)
        return [binary[:8], binary[8:]]
    else:
        return ["{:0>8b}".format(num)]


def int_shift(num, ensure_odd=False):
    result = [int(x, base=2) for x in int_to_binary(num)]
    if ensure_odd and len(result) == 1:
        result = [0, result[0]]
    return result


def send_ip_packet(host, port, payload):
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    s.connect((host, port))
    return s.send(payload)

class ICMP(object):
    def __init__(self, _type, code, _id, seq, data):
        self._type = _type
        self.code = code
        self._id = _id
        self.seq = seq
        self.data = data
        self.checksum = 0
        self.packet = self.assemble_packet()
        self.binary = ['{:0>8}'.format(format(c, 'b'))
                       for c in self.packet]
        self.raw = ''.join(self.binary)

    def assemble_packet(self):
        packet = [self._type, self.code, self.checksum, self.checksum]
        for x in (self._id, self.seq):
            packet.extend(int_shift(x, ensure_odd=True))
        packet.extend([ord(c) for c in self.data])
        self.checksum = self.genernate_checksum(packet)
        checksum_shift = int_shift(self.checksum, ensure_odd=True)
        packet[2], packet[3] = checksum_shift[1], checksum_shift[0]
        return packet

    def genernate_checksum(self, packet):
        last = 0
        for i in range(len(packet) // 2):
            last += (packet[i*2+1] << 8) + packet[i*2]
        if len(packet) % 2:
            last += packet[-1]
        while (last >> 16):
            last = (last & 0xffff) + (last >> 16)
        return ~last & 0xffff

    @property
    def pretty(self):
        head = (
            '+-----------------------------------+\n'
            '|          ICMP - {: <18}|\n'
            '+--------+--------+-----------------+\n'
            '|  Type  |  Code  |    chechsum     |\n'
            '+--------+--------+-----------------+\n'
            '|{}|{}|{}|\n'
            '+-----------------+-----------------+\n'
            '|       ID        |    sequence     |\n'
            '+-----------------+-----------------+\n'
            '|{}|{}|\n'
            '+-----------------+-----------------+\n'
            '|                Data               |\n'
            '+-----------------------------------+\n'
            .format(self.__class__.__name__,
                    self.binary[0],
                    self.binary[1],
                    ' '.join(self.binary[2:4]),
                    ' '.join(self.binary[4:6]),
                    ' '.join(self.binary[6:8]))
        )
        binary_data = self.binary[8:]
        data = []
        pattern = '|{: <35}|\n+-----------------------------------+\n'
        for i in range(len(binary_data) // 4):
            line = ' '.join(binary_data[i*4: (i+1) * 4])
            data.append(pattern.format(line))
        rest = ' '.join(binary_data[-(len(binary_data) % 4):])
        data.append(pattern.format(rest))
        data = ''.join(data)
        return head + data

    def __str__(self):
        return ''.join([chr(x) for x in self.packet])

    def __repr__(self):
        return '{}(id={}, seq={}, data="{}", checksum={})'.format(
            self.__class__.__name__, self._id, self.seq,
            self.data, self.checksum,
        )

class Echo(ICMP):
    TYPE = 8
    CODE = 0

    def __init__(self, _id=None, seq=None, data=''):
        _id = _id or random.randint(0, 0xffff)
        seq = seq or random.randint(0, 0xffff)
        super(Echo, self).__init__(self.TYPE, self.CODE, _id, seq, data)


e = Echo(10086, 1, data="hello world")
print(repr(e))
print(e.pretty)
print(send_ip_packet('10.10.10.10', 1, str(e)))


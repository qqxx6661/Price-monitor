#!/usr/bin/env python
# coding: utf-8
# author: frk

import struct
from socket import inet_aton
import os


class IPL:
    def __init__(self, file):
        self.offset = 0
        self.index = 0
        self.binary = ""
        self._unpack_V = lambda b: struct.unpack("<L", b)
        self._unpack_N = lambda b: struct.unpack(">L", b)
        self._unpack_C = lambda b: struct.unpack("B", b)
        self.load(file)

    def load(self, file):
        try:
            path = os.path.abspath(file)
            with open(path, "rb") as f:
                self.binary = f.read()
                self.offset, = self._unpack_N(self.binary[:4])
                self.index = self.binary[4:self.offset]
        except Exception as ex:
            print "cannot open file %s" % file
            print ex.message
            exit(0)

    def find(self, ip):
        index = self.index
        offset = self.offset
        binary = self.binary
        nip = inet_aton(ip)
        ipdot = ip.split('.')
        if int(ipdot[0]) < 0 or int(ipdot[0]) > 255 or len(ipdot) != 4:
            return "N/A"

        tmp_offset = int(ipdot[0]) * 4
        start, = self._unpack_V(index[tmp_offset:tmp_offset + 4])

        index_offset = index_length = 0
        max_comp_len = offset - 1028
        start = start * 8 + 1024
        while start < max_comp_len:
            if index[start:start + 4] >= nip:
                index_offset, = self._unpack_V(index[start + 4:start + 7] + chr(0).encode('utf-8'))
                index_length, = self._unpack_C(index[start + 7])
                break
            start += 8

        if index_offset == 0:
            return "N/A"

        res_offset = offset + index_offset - 1024
        return binary[res_offset:res_offset + index_length].decode('utf-8')

if __name__ == '__main__':
    IPL = IPL('17monipdb.dat')
    ip = '59.64.234.174'
    try:
        area = IPL.find(ip).rstrip().replace('\t', '.')
    except:
        area = 'None.None.None'
    print area

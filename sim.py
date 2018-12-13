# Required for handling files in Instabase
import os
IB = os.environ.get('INSTABASE_URI',None) is not None
open = ib.open if IB else open

def hex2bin(hex_v):
    base = 16
    # truncating 13 bits from left (2 for '0b' and rest to make it 32 bit)
    return bin(int(hex_v, base))[13:]


command = []
offset = []
addr = []
with open('small.memtrace','r') as trace:
    for line in trace:
        for count, word in enumerate(line.split()):
            print(count, word)
            command.append(word) if count == 0
            offset.append(word) if count == 1





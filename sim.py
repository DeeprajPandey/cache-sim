# Required for handling files in Instabase
import os
IB = os.environ.get('INSTABASE_URI',None) is not None
open = ib.open if IB else open

def hex2bin(hex_v):
    base = 16
    # truncating 13 bits from left (2 for '0b' and rest to make it 32 bit)
    return bin(int(hex_v, base))[13:]

def bin2dec(bin_index):
    base = 2
    return int(bin_index,base)


command = []
offset = []
addr = []
with open('small.memtrace','r') as trace:
    for line in trace:
        for count, word in enumerate(line.split()):
            print(count, word)
            command.append(word) if count == 0
            offset.append(word) if count == 1

# For L1 Cache
# Cache size = 32 kB
# Block size = 16 B
# Num sets = 2048
L1_limit = 2048
L1_tag_array = []
L1_set_array = []
for address in addr:
    # 16 = 2^4. offset is 4 bits from right
    offset = address[28:32]
    # 2048 = 2^11. index is 11 bits from right
    index = address[17:28]
    # rest of the bits to left of index is the tag
    tag = address[0:17]
    



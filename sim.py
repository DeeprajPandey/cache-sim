# Required for handling files in Instabase
import os
import itertools

IB = os.environ.get('INSTABASE_URI',None) is not None
open = ib.open if IB else open

def hex2bin(hex_v):
    base = 16
    bits = 32
    # truncating 13 bits from left (2 for '0b' and rest to make it 32 bit)
    return bin(int(hex_v, base))[13:].zfill(bits)

def bin2dec(bin_index):
    base = 2
    return int(bin_index,base)

instructions = []
offset = []
addr = []
with open('small.memtrace','r') as trace:
    for line in trace:
        for count, word in enumerate(line.split()):
            if count == 0:
                instructions.append(word)
            if count == 1:
                offset.append(word)
            if count == 2:
                addr.append(hex2bin(word))
hits = 0
misses = 0
# For L1 Cache
# Cache size = 32 kB
# Block size = 16 B
# Num sets = 2048
L1_limit = 2048
L1_tag_array = [-1]*L1_limit
L1_set_array = [-1]*L1_limit

# Using itertools to go through the instruction and address lists in parallel
# and wrapping them with enumerate to keep track of the index

for indx, (instruction, address) in enumerate(itertools.izip(instructions, addr)):
    # 16 = 2^4. offset is 4 bits from right
    adr_offset = address[28:32]
    # 2048 = 2^11. index is 11 bits from right
    i = address[17:28]
    adr_index = bin2dec(i)
    # rest of the bits to left of index is the tag
    adr_tag = address[0:17]
    
    # When the instruction is load
    if instruction == 'L':
        if L1_tag_array[adr_index] == adr_tag:
            hits += 1
        else:
            # increment misses
            misses += 1
    if instruction == 'S':
        if L1_tag_array[adr_index] == adr_tag:
            hits += 1
        else:
            misses += 1
            # add the tag to that index to simulate the data being added to block in set array
            L1_tag_array[adr_index] = adr_tag
            L1_set_array[adr_index] = bin2dec(address)
    
#calculating hit rate, miss rate, average time per instruction
hit_rate=(float(hits)/10001) * 100
miss_rate=(float(misses)/10001)*100
avg_time_per_Instruction=(hit_rate/100*1)+(miss_rate/100*301)hit_rate=(float(hits)/10001) * 100
miss_rate=(float(misses)/10001)*100
avg_cycles_per_Instruction=(hit_rate/100*1)+(miss_rate/100*301)
print "Average cycles per Instruction: ",avg_cycles_per_Instruction
print "Hit Rate:",hit_rate
print "Miss Rate: ",miss_rate
    

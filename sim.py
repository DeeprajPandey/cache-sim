# cache-simulator.py
# python2
#
# Implements a trace driven L1 cache simulator.
#
# Nandini Agrawal, Deepraj Pandey
import os
import itertools

IB = os.environ.get('INSTABASE_URI',None) is not None
open = ib.open if IB else open

# Converts hexadecimal to binary
def hex2bin(hex_v):
    base = 16
    bits = 32
    # truncating 13 bits from left (2 for '0b' and rest to make it 32 bit)
    binary = bin(int(hex_v, base))[2:]
    if len(binary) > 32:
        diff = len(binary)-32
        binary = binary[diff:].zfill(bits)
    
    return binary

# Converts binary to decimal
def bin2dec(bin_index):
    base = 2
    return int(bin_index,base)

# Extract data from the memtrace and store in relevant DSs
instructions = []
offset = []
addr = []
# Open mode is 'rU' for cross-OS compatibility
with open('small.memtrace','rU') as trace:
    for line in trace:
        for count, word in enumerate(line.split()):
            if count == 0:
                instructions.append(word)
            if count == 1:
                offset.append(word)
            if count == 2:
                addr.append(hex2bin(word))

# Counters for the number of hits and misses
hits = 0
L_hits = 0
S_hits = 0
misses = 0
comp_misses = 0

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
            L_hits += 1
        else:
            # increment misses
            misses += 1
            if L1_tag_array[adr_index] == -1:
                comp_misses += 1
            # add the tag to that index to simulate the data being added to block in set array
            L1_tag_array[adr_index] = adr_tag
            L1_set_array[adr_index] = bin2dec(address)
            
    if instruction == 'S':
        if L1_tag_array[adr_index] == adr_tag:
            hits += 1
            S_hits += 1
        else:
            misses += 1
            if L1_tag_array[adr_index] == -1:
                comp_misses += 1
            # add the tag to that index to simulate the data being added to block in set array
            L1_tag_array[adr_index] = adr_tag
            L1_set_array[adr_index] = bin2dec(address)

# Calculating hit rate, miss rate, average cycles per instruction & printing
hit_rate=(float(hits)/10000) * 100
miss_rate=(float(misses)/10000)*100
avg_cycles_per_Instruction=(hit_rate/100*1)+(miss_rate/100*301)
print "Hits:", hits
print "Read Hits:", L_hits
print "Write Hits:", S_hits
print("\n")
print "Misses:", misses
print "Compulsory Misses:", comp_misses
print("\n")
print "Hit Rate:",hit_rate
print "Read Hit Rate:", float(L_hits)/hits*100
print "Write Hit Rate:", float(S_hits)/hits*100
print "Miss Rate:",miss_rate

# Required for handling files in Instabase
import os
IB = os.environ.get('INSTABASE_URI',None) is not None
open = ib.open if IB else open

with open('small.memtrace','r') as trace:
    for line in trace:
        for word in line.split():
            print(word)   





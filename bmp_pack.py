import os
import sys

from header import write_header
from crc import Crc

# https://www2.cs.duke.edu/csed/curious/compression/lzw.html
def lzw_compress(data):
    out = []
    dic = {}
    next_id = 257
    
    prev = bytes([data[0]])
    for byte in data[1:]:
        byte = bytes([byte])
        sequence = prev + byte
        if sequence in dic:
            prev += byte
        else:
            out.append(dic[prev] if len(prev) > 1 else prev[0])
            if next_id < 4096:
                dic[sequence] = next_id
                next_id += 1
            prev = byte
    out.append(dic[prev] if len(prev) > 1 else prev[0])
    return out

def lzw_write(data):
    phase = True
    buf = 0
    res = bytearray()
    for code in data:
        if phase:
            res.append(code >> 4)
            buf = code & 0xF
        else:
            res.append((buf << 4) | (code >> 8))
            res.append(code & 0xFF)
        phase = not phase
        
    if len(data) % 2 != 0:
        res.append(buf << 4)
    return res

def compress_folder(root):
    items = []
    for dirName, subdirList, fileList in os.walk(root):
        for fname in fileList:
            path = os.path.join(dirName, fname)
            rel  = os.path.relpath(path, root)
            print(rel)
            
            with open(path, 'rb') as f:
                data = f.read()
            
            comp = lzw_write(lzw_compress(data))
            items.append((rel, len(data), comp))
    return items
    
if __name__ == '__main__':
    if len(sys.argv) == 3:
        root = sys.argv[1]
        filename = sys.argv[2]
        items = compress_folder(root)
        header = write_header(items, 84)
        crc = Crc(header)
        with open(filename, 'wb') as outf:
            outf.write(header)
            for name, full_size, data in items:
                crc.update(data)
                outf.write(data)
            outf.write(crc.bruteforce(0x21DC))
    else:
        print('Usage: python bmp_pack.py FOLDER_TO_PACK PATH_TO_OUTPUT_FILE')

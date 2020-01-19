import os
import sys

from header import read_header

def lzw_decompress(data):    
    out = bytearray()
    dic = [None] * 3839
    dict_size = 0
    prev_code = 0
    
    def get(idx):
        if idx < 256:
            return bytes([idx])
        elif idx - 257 == dict_size:
            res = get(prev_code)
            return res + bytes([res[0]])
        else:
            return dic[idx - 257]

    prev_code = data[0]
    out.append(prev_code)
    for code in data[1:]:
        if code == 256:
            dict_size = 0
            continue
        temp = get(code)    
        out.extend(temp)
        
        if dict_size < 3839:
            dic[dict_size] = get(prev_code) + bytes([temp[0]])
            dict_size += 1
        
        prev_code = code
    return out

def lzw_read(data):
    phase = 0
    buf = 0
    res = []
    for code in data:
        if phase == 0:
            buf = code << 4
        elif phase == 1:
            res.append(buf | (code >> 4))
            buf = (code & 0xF) << 8
        else:
            res.append(buf | code)
        
        phase = (phase + 1) % 3
    return res

def bmp_unpack(bmp, folder):
    data = bmp.read()
    length = bmp.tell()
    # change to 20 for Ele Paper Action
    name_len = 84
    entry_len = name_len + 3 * 4

    items = read_header(data, name_len)

    print(f'{"Filename":<40} {"Offset":>11} {"Size":>7} {"Actual":>8}')
    print('=' * (40 + 11 + 7 + 8 + 3))
    for name, offset, size, dsize in items:
        print(f'{name:<40} {offset:>11} {size:>7} {dsize:>8}')
        
        if size == 0:
            continue
        
        bmp.seek(4 + len(items) * entry_len + offset)
        data = bmp.read(size)
        decompressed = lzw_decompress(lzw_read(data))
        
        filename = os.path.join(folder, name)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'wb') as outf:
            outf.write(decompressed)
            
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python bmp_unpack.py PATH_TO_BMPDATA.BIN FOLDER_TO_UNPACK_TO')
    else:
        with open(sys.argv[1], 'rb') as bmp:
            bmp_unpack(bmp, sys.argv[2])

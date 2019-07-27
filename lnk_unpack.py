import struct
import os
import sys
from header import read_header

BIN_SIZE = 10485760

def lzss_decompress(data):
    data = iter(data)
    out = bytearray()
    ctrl = 0
    
    while True:
        ctrl = next(data)
        for i in range(7, -1, -1):
            if ctrl & (1 << i) == 0:
                out.append(next(data))
            else:
                temp = next(data)
                back = ((temp & 0xF0) << 4) | next(data)
                if back == 0:
                    return out
                back_idx = len(out) - back
                length = temp & 0x0F
                if length == 0:
                    length = next(data) + 16
                for idx in range(back_idx, back_idx + length + 1):
                    out.append(out[idx])
                    
def open_data_file(game_root, idx):
    path = os.path.join(game_root, 'bin', f'data{idx:03}.bin')
    return open(path, 'rb')

def lnk_unpack(items, game_root, folder):
    data_idx = 0
    data_file = open_data_file(game_root, data_idx)
    print(f'{"Filename":<40} {"Offset":>11} {"Size":>7} {"Actual":>8}')
    print('=' * (40 + 11 + 7 + 8 + 3))
    for name, offset, size, dsize in items:
        print(f'{name:<40} {offset:>11} {size:>7} {dsize:>8}')
        
        data_to_read = size
        start_file = offset // BIN_SIZE
        data = bytes()
        if data_idx != start_file:
            data_file.close()
            data_idx = start_file
            data_file = open_data_file(game_root, data_idx)
        data_file.seek(offset % BIN_SIZE)
        while True:
            from_this = min(data_to_read, BIN_SIZE - data_file.tell())
            data += data_file.read(from_this)
            data_to_read -= from_this
            if data_to_read > 0:
                data_file.close()
                data_idx += 1
                data_file = open_data_file(game_root, data_idx)
            else:
                break
        decompressed = lzss_decompress(data)
        
        if len(decompressed) != dsize:
            print('File size mismatch!', file=sys.stderr)
        
        filename = os.path.join(folder, name)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'wb') as outf:
            outf.write(decompressed)
    data_file.close()
            
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python lnk_unpack.py PATH_TO_GAME_ROOT FOLDER_TO_UNPACK_TO')
    else:
        game_root = sys.argv[1]
        unpack_folder = sys.argv[2]
        lnkpath = os.path.join(game_root, 'lnkdatas.bin')
        with open(lnkpath, 'rb') as lnk:
            items = read_header(lnk.read(), 128)
        lnk_unpack(items, game_root, unpack_folder)

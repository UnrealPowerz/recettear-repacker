import sys
import hashlib

known_crc = { 0x8BAA: ('lnkdatas.bin EN',       b'\xf6q\xf8\x08\xbe^\xfahz\xbf1J\xa1\xadU-'),
              0xC5E1: ('lnkdata.bin EN',        None),
              0x7CE7: ('bmpdata.bin v1.106 EN', b'\xeax\x0el}\xe7\x9b\x831\xa0sq#9\xc5\x94'),
              0x21DC: ('bmpdata.bin v1.108 EN', b'\xa8\x8a\xcb\x1c\x81\x1aNr\x84_\xc0\x07m\x10J\x8b'),
              0xCCB3: ('lnkdata.bin JP',        b'\xee!\x04\x92\xd5@\x15\xc2A\xc9\x01\xa7\xdb6\x8c\xb2'),
              0x286C: ('bmpdata.bin v1.126 JP', b'\xac`\xa5\x9b\xce\x9f\xaf*\xaf\x9e\xb44I\xd4\x90\x8f') }

class Crc:
    def __init__(self, buf):
        self.crc = 0xFFFF
        self.update(buf)
        
    def _finalize(crc):
        return ~crc & 0xFFFF
    
    def _calculate(self, buf):
        res = self.crc
        for byte in buf:
            res ^= byte << 8
            for i in range(8):
                if res & 0x8000 == 0:
                    res = ((res << 1) & 0xFFFFFFFF)
                else:
                    res = ((res << 1) & 0xFFFFFFFF)  - 4129
        return res        
    
    def get(self):
        return Crc._finalize(self.crc)
    
    def update(self, buf):
        self.crc = self._calculate(buf)
        
    def bruteforce(self, desired):
        for i in range(1 << 16):
            buf = [i >> 8, i & 0xFF]
            crc = Crc._finalize(self._calculate(buf))
            if crc == desired:
                return bytes(buf)
        return False

if __name__ == '__main__':
    if len(sys.argv) in [2, 3]:
        path = sys.argv[1]
        with open(path, 'rb') as f:
            data = f.read()
        crc = Crc(data).get()
        
        if crc in known_crc:
            desc, md5hash = known_crc[crc]
            note = desc
            if md5hash is not None:
                md5 = hashlib.md5(data).digest()
                note += ' original' if md5 == md5hash else ' modified'
            print(f'CRC for {path}: {crc:X} [{note}]')
        else:
            print(f'CRC for {path}: {crc:X}')
        
        if len(sys.argv) == 3:
            want  = int(sys.argv[2], 16)
            padding = crc.bruteforce(want)
            print(f'{crc:X} -> {want:X}: Pad with {padding}')
    else:
        print('Usage:')
        print('python crc.py FILE')
        print('python crc.py FILE DESIRED_CRC_HEX')

import sys

# lnkdatas: 0x8BAA   lnkdata: 0xC5E1    bmpdata: 0x21DC

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
        print(f'CRC for {path}: {crc:X}')
        
        if len(sys.argv) == 3:
            want  = int(sys.argv[2], 16)
            padding = crc.bruteforce(want)
            print(f'{crc.get():X} -> {want:X}: Pad with {padding}')
    else:
        print('Usage:')
        print('python crc.py FILE')
        print('python crc.py FILE DESIRED_CRC_HEX')

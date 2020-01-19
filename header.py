import struct

def read_header(data, name_len):
    num_items = struct.unpack('>i', data[:4])[0]
    step = 3 * 4 + name_len
    items = []
    for i in range(4, 4 + step * num_items, step):
        (name, dsize, offset, size) = struct.unpack('>' + str(name_len) + 'siii', data[i:i+step])
        try:
            name = name[:name.index(0)]
        except:
            pass
        name = name.decode('ascii')
        items.append((name, offset, size, dsize))
    return items

def write_header(items, name_len):
    out = bytearray()
    form = struct.Struct('>' + str(name_len) + 'siii')
    
    out.extend(struct.pack('>i', len(items)))
    
    offset = 0
    for name, full_size, data in items:
        if len(name) > name_len:
            raise ValueError('File path too long!')
        
        size = len(data)
        entry = form.pack(name.encode('ascii'), full_size, offset, size)
        out.extend(entry)
        offset += size
    return out

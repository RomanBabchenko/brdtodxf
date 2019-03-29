with open("A1286_k18.brd", "rb") as f:
    buffer = bytearray(f.read())

newbuf = bytearray()

for x in buffer:
    if not (chr(x) == '\r' or chr(x) == '\n' or chr(x) == 0):
        newbuf.append((~(x>>6 & 3 | x<<2))%256)
        # newbuf.append(255)
    else:
        newbuf.append(x)


with open('var.brd', mode='wb') as f:
    f.write(bytes(newbuf))

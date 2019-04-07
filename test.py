import time

with open("A1286_k18.brd", "rb") as f:
    buffer = bytearray(f.read())

newbuf = bytearray()

for x in buffer:
    if not (chr(x) == '\r' or chr(x) == '\n' or chr(x) == 0):
        newbuf.append((~(x >> 6 & 3 | x << 2)) % 256)
    else:
        newbuf.append(x)

with open('var.brd', mode='wb') as f:
    f.write(bytes(newbuf))


def func2():
    start = time.perf_counter()
    with open("A1286_k18.brd", "rb") as f:
        buffer2 = list(f.read())

    chars = ''
    for i in range(len(buffer2)):
        if not (chr(buffer2[i]) == '\r' or chr(buffer2[i]) == '\n' or chr(buffer2[i]) == 0):
            buffer2[i] = (~(buffer2[i] >> 6 & 3 | buffer2[i] << 2)) % 256
        chars += chr(buffer2[i])
    lines = chars.split('\r\n')
    # print(lines)
    with open('var2.brd', mode='wb') as f:
        f.write(bytes(newbuf))

    with open('var2.brd', "r") as read_file:
        lines = read_file.readlines()
    # print(lines)


class Brdfile_2(object):
    def __init__(self, path):
        with open(path, "rb") as f:
            buffer = list(f.read())
        chars = ''
        for i in range(len(buffer)):
            if not (chr(buffer[i]) == '\r' or chr(buffer[i]) == '\n' or chr(buffer[i]) == 0):
                buffer[i] = (~(buffer[i] >> 6 & 3 | buffer[i] << 2)) % 256
            chars += chr(buffer[i])
        self.lines = chars.split('\r\n')
        self.parts = {}
        self.pins = []
        for i in range(len(self.lines)):
            if self.lines[i][:5] == 'Parts':
                print('Найден')
                for n in range(i + 1, len(self.lines)):
                    if self.lines[n] != '':
                        part = self.lines[n].split()
                        self.parts[part[0]] = part[1:7]
                        try:
                            self.parts[part[0]].append(int(self.lines[n - 1].split()[-1]))
                        except ValueError:
                            self.parts[part[0]].append('0')
                    else:
                        break

            if self.lines[i][:4] == 'Pins':
                for n in range(i + 1, len(self.lines)):
                    if self.lines[n] != '':
                        self.pins.append(self.lines[n])
                    else:
                        break

    def range_xy(self, part):
        x = []
        y = []
        print(range(int(self.parts[part][2]), int(self.parts[part][1])))
        print(self.parts[part][1])
        print(self.pins[int(self.parts[part][2])])
        print(self.pins[int(self.parts[part][1])-1])
        for n in range(int(self.parts[part][2]), int(self.parts[part][1])):
            side = self.pins[n].split()[3]
            x.append(int(self.pins[n].split()[0]))
            y.append(int(self.pins[n].split()[1]))
        return [min(x), min(y), max(x), max(y), side]

print
file = Brdfile_2('A1286_k18.brd')
print(file.range_xy('U1000'))
# print(file.parts['U8000'])
print(func2())

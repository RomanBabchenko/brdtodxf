from dxfwrite import DXFEngine as dxf
from colorama import Fore, Back, Style

with open("LA-E911P.brd", "r") as read_file:
    data = read_file.readlines()

pins = []
for i in range(len(data)):
    if data[i][:4] == 'PINS':
        for n in range(i + 1, len(data)):
            if data[n] != '\n':
                pins.append(data[n][:-1])
            else:
                break

drawing = dxf.drawing('test.dxf')
width = float(input('Введите ширину подложки, мм: '))
distance = float(input('Введите растояние между крайними пинами, мм: '))
diameter = float(input('Введите диаметр отверствия в трафарете: '))

for line in data:
    try:
        target = line.split()
        if target[0] == 'UC1':
            print(Fore.WHITE + 'Выбран элемент:' + Fore.GREEN +' '+ target[0] + Fore.WHITE)
            offset = (width - distance)/2
            rangex = range(int(target[1]), int(target[3]) + 1)
            rangey = range(int(target[2]), int(target[4]) + 1)
            scale = distance / (max(rangex) - min(rangex))
            print(Fore.WHITE + 'Количество контактов:' + Fore.GREEN + ' ' + str(len(pins)) + Fore.WHITE)
            print(rangex, rangey)
            drawing.add(dxf.line((min(rangex) * scale - offset, min(rangey) * scale - offset),
                                 (max(rangex) * scale + offset, min(rangey) * scale - offset),
                                 color=1))
            drawing.add(dxf.line((max(rangex) * scale + offset, min(rangey) * scale - offset),
                                 (max(rangex) * scale + offset, max(rangey) * scale + offset),
                                 color=1))
            drawing.add(dxf.line((max(rangex) * scale + offset, max(rangey) * scale + offset),
                                 (min(rangex) * scale - offset, max(rangey) * scale + offset),
                                 color=1))
            drawing.add(dxf.line((min(rangex) * scale - offset, max(rangey) * scale + offset),
                                 (min(rangex) * scale - offset, min(rangey) * scale - offset),
                                 color=1))
            break
    except:
        continue

for line in pins:
    pin = line.split()
    try:
        if int(pin[0]) in rangex and int(pin[1]) in rangey and int(pin[3]) == int(target[-1]):
            # x = int(target[0]) - min(rangex)
            # y = int(target[1]) - min(rangey)

            x = int(pin[0]) * scale
            y = int(pin[1]) * scale
            drawing.add(dxf.circle(diameter / 2, (x, y)))
            print('circle added', x, y)
    except:
        continue

# drawing.add(dxf.line((0, 0), (10, 0), color=7))
# drawing.add(dxf.circle(10,(10,10)))
# drawing.add_layer('TEXTLAYER', color=2)
# drawing.add(dxf.text('Test', insert=(0, 0.2), layer='TEXTLAYER'))
drawing.save()

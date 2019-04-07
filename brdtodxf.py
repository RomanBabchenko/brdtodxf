# coding: utf-8
from dxfwrite import DXFEngine as dxf
from colorama import init, Fore, Back
import sys

class Brdfile_1(object):
    def __init__(self, path):
        found = False
        with open(path, "r") as read_file:
            self.type = 'brd1'
            self.lines = read_file.readlines()
            self.parts = {}
            self.pins = []
            for i in range(len(self.lines)):
                if self.lines[i][:5] == 'PARTS':
                    found = True
                    for n in range(i + 1, len(self.lines)):
                        if self.lines[n] != '\n':
                            part = self.lines[n][:-1].split()
                            self.parts[part[0]] = part[1:7]
                        else:
                            break
                if self.lines[i][:4] == 'PINS':
                    for n in range(i + 1, len(self.lines)):
                        if self.lines[n] != '\n':
                            self.pins.append(self.lines[n][:-1])
                        else:
                            break
            if not found:
                raise BufferError

class Brdfile_2(object):
    def __init__(self, path):
        with open(path, "rb") as f:
            buffer = list(f.read())
            if buffer[0:4] != [35, 226, 99, 40]:
                raise BufferError
        chars = ''
        for i in range(len(buffer)):
            if not (chr(buffer[i]) == '\r' or chr(buffer[i]) == '\n' or chr(buffer[i]) == 0):
                buffer[i] = (~(buffer[i] >> 6 & 3 | buffer[i] << 2)) % 256
            chars += chr(buffer[i])
        self.type = 'brd2'
        self.lines = chars.split('\r\n')
        self.parts = {}
        self.pins = []
        found = False
        for i in range(len(self.lines)):
            if self.lines[i][:5] == 'Parts':
                found = True
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
        if not found:
            raise BufferError

    def range_xy(self, part):
        x = []
        y = []
        for n in range(int(self.parts[part][2]), int(self.parts[part][1])):
            side = self.pins[n].split()[3]
            x.append(int(self.pins[n].split()[0]))
            y.append(int(self.pins[n].split()[1]))
        return [min(x), min(y), max(x), max(y), side]



class Part(object):
    def __init__(self, name, part_data, pins):
        self.rangex = range(int(part_data[0]), int(part_data[2]) + 1)
        self.rangey = range(int(part_data[1]), int(part_data[3]) + 1)
        self.name = name
        self.pins = []
        for line in pins:
            pin = line.split()
            if int(pin[0]) in self.rangex and int(pin[1]) in self.rangey and int(pin[3]) == int(part_data[-1]):
                self.pins.append(pin)

    def build_dxf(self, scale, offset, diameter):
        drawing = dxf.drawing('Drawing.dxf')
        print('\n' + Fore.RESET + 'Выполняется построение объекта...')
        counter = 0
        for pin in self.pins:
            x = int(pin[0]) * scale
            y = int(pin[1]) * scale
            drawing.add(dxf.circle(diameter / 2, (x, y)))
            counter += 1
            print('item added', x, y)
        drawing.add(dxf.line((min(self.rangex) * scale - offset, min(self.rangey) * scale - offset),
                             (max(self.rangex) * scale + offset, min(self.rangey) * scale - offset),
                             color=1))
        drawing.add(dxf.line((max(self.rangex) * scale + offset, min(self.rangey) * scale - offset),
                             (max(self.rangex) * scale + offset, max(self.rangey) * scale + offset),
                             color=1))
        drawing.add(dxf.line((max(self.rangex) * scale + offset, max(self.rangey) * scale + offset),
                             (min(self.rangex) * scale - offset, max(self.rangey) * scale + offset),
                             color=1))
        drawing.add(dxf.line((min(self.rangex) * scale - offset, max(self.rangey) * scale + offset),
                             (min(self.rangex) * scale - offset, min(self.rangey) * scale - offset),
                             color=1))
        print('Построение завершено.')
        printtable()
        try:
            drawing.save()
            print('Результат сохранен в файл ' + Fore.CYAN + 'Drawing.dxf' + Fore.RESET)
        except PermissionError:
            print(Fore.RED + 'ФАЙЛ ЗАНЯТ ДРУГИМ ПРИЛОЖЕНИЕМ.' + Fore.RESET)

def printtable():
    print(Fore.RESET)
    print('+' + '-' * 49 + '+')
    print('|{0:^8}|{1:^18}|{2:^10}|{3:^10}|'.format("Объект", "Количество пинов", "Ширина", "Димаметр"))
    print('+' + '-' * 49 + '+')
    print(('|' + Fore.GREEN + '{0:^8}' + Fore.RESET +
           '|' + Fore.GREEN + '{1:^18}' + Fore.RESET +
           '|' + Fore.GREEN + '{2:^10}' + Fore.RESET +
           '|' + Fore.GREEN + '{3:^10}' + Fore.RESET + '|').format(part.name, len(part.pins), width, diameter))
    print('+' + '-' * 49 + '+')
    print()

def main():
    global part, width, diameter
    try:
        if sys.argv[1][-3:] != 'brd':
            print('Неподдерживаемое разрешение файла.')
            return
        else:
            try:
                file = Brdfile_1(sys.argv[1])
            except BufferError:
                try:
                    file = Brdfile_2(sys.argv[1])
                except BufferError:
                    print('Неподдерживаемый формат файла')
                    return

    except FileNotFoundError:
        print('file.brd не найден в папке с программой.')
        return
    except IndexError:
        print('Файл не указан.')
        return


    print(Back.BLUE + Fore.WHITE + ' BRDTODXF BY SERVICE CORE :) ' + Fore.RESET + Back.RESET)
    while True:
        try:
            print(Fore.RESET + 'Выберите позиционный номер объекта: ' + Fore.LIGHTRED_EX, end='')
            target = input()
            if file.type == 'brd1':
                part = Part(target, file.parts[target], file.pins)
            if file.type == 'brd2':
                part = Part(target, file.range_xy(target), file.pins)
            break
        except KeyError:
            print('Нет такого элемента')
        except KeyboardInterrupt:
            return
    while True:
        try:
            print(Fore.RESET + 'Введите ширину подложки, мм: ' + Fore.LIGHTRED_EX, end='')
            width = float(input())
            break
        except ValueError:
            print('Принимаются только числовые значения')
        except KeyboardInterrupt:
            return
    while True:
        try:
            print(Fore.RESET + 'Введите растояние между крайними пинами, мм: ' + Fore.LIGHTRED_EX, end='')
            distance = float(input())
            break
        except ValueError:
            print('Принимаются только числовые значения')
        except KeyboardInterrupt:
            return
    while True:
        try:
            print(Fore.RESET + 'Введите диаметр отверствия в трафарете: ' + Fore.LIGHTRED_EX, end='')
            diameter = float(input())
            break
        except ValueError:
            print('Принимаются только числовые значения')
        except KeyboardInterrupt:
            return
    scale = distance / (max(part.rangex) - min(part.rangex))
    offset = (width - distance) / 2
    part.build_dxf(scale, offset, diameter)


init(convert=True)
main()

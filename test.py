import dxfwrite
from dxfwrite import DXFEngine as dxf
from random import random

name="rectangle.dxf"
drawing = dxf.drawing(name)

polyline= dxf.polyline(linetype='DOT')
polyline.add_vertices( [(0,20), (3,20), (6,23), (9,23)] )
drawing.add(polyline)
drawing.save()
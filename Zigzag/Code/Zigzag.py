import math

from GenDpPath import *
from Utility import *
from VtkAdaptor import *
import numpy as np
import os
import copy
# this inputed contours must be closed and this contour must be anticlockwise
inner_path = "\Data\inner_contour.txt"
out_path = "\Data\out_contour.txt"
out_offset_path = "\Data\out_contour_path.txt"

#path = "C:/Users/Hang/Desktop/ANN/Zigzag/Path/cluster_contour.txt"
save_path = "\Data/zigzag.txt"

cofficient = 10000.0
interval = 0.4
angle = 90

angle = degToRad(angle)
pathes = []
dirpath = os.path.abspath(os.path.dirname(os.getcwd()))

inner_path = dirpath + inner_path
out_path = dirpath + out_path
out_offset_path = dirpath + out_offset_path
save_path = dirpath + save_path

inner_points = np.loadtxt(inner_path)
out_points = np.loadtxt(out_path)

contours = []
temp_contour = []
temp_contour1 = []
temp_contour2 = []

for point in out_points:
    var_tuple = (round(point[0] * cofficient), round(point[1] * cofficient))
    temp_contour1.append(var_tuple)
for point in inner_points:
    var_tuple = (round(point[0] * cofficient), round(point[1] * cofficient))
    temp_contour2.append(var_tuple)

temp_contour.append(temp_contour1)
temp_contour.append(temp_contour2)
flag = -1

for i in range(len(temp_contour)):
    if(i == 1) :flag = 1
    var_temp_tuple = tuple(temp_contour[i])
    pco = pyclipper.PyclipperOffset()
    pco.AddPath(var_temp_tuple, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)
    solution = pco.Execute(flag * interval * cofficient / 2.0)
    solution = np.array(solution) / cofficient
    contours.append(solution)
layer = Layer(0)
polygon = Polyline()
for i in range (len(contours)):
    polygon = Polyline()
    for j in range (contours[i].shape[0]):
        for k in range (contours[i].shape[1]):
            polygon.addPoint(Point3D(contours[i][j][k][0], contours[i][j][k][1]))
        polygon.addPoint(Point3D(contours[i][j][0][0], contours[i][j][0][1]))
    if(i == 1): polygon.points.reverse()
    layer.contours.append(polygon)

paths = genDpPath(layer.contours, interval, angle)
pathes.append(paths)

layer_hight = [0.2,0.4]
with open(save_path, 'w') as f:
    for z in range(len(layer_hight)):
        for i in range(len(pathes)):
            for fill in pathes[i]:
                for j in fill.points:
                    f.write(str(j.x) + "    " + str(j.y) + "    " + str(layer_hight [z]) + '\n')
                f.write("1111" + "    " + "1111" + "    " + "1111" + '\n')
                print("this is split contours")
    f.write("11" +"    " + "1111" + "    " + "0.6")
f.close()

out_contour_path = np.loadtxt(out_offset_path)
layer_out = Layer(0)
polygon_out = Polyline()
for point in out_contour_path:
    if(point[0] == 1111):
        polygon_out_copy = copy.deepcopy(polygon_out)
        layer_out.contours.append(polygon_out_copy)
        polygon_out.points.clear()
        continue
    polygon_out.addPoint(Point3D(point[0],point[1]))

va = VtkAdaptor()

for coutour in layer_out.contours:
    va.drawPolyline(coutour).GetProperty().SetColor(0, 0, 1)

#for coutour in  layer.contours:
    #va.drawPolyline(coutour).GetProperty().SetColor(0,0,0)
for paths in  pathes:
    for path in paths:
        va.drawPolyline(path).GetProperty().SetColor(0,0,1)
va.display()

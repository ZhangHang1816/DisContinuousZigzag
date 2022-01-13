from GenDpPath import *
from Utility import *
from VtkAdaptor import *
import numpy as np
import os
import copy
# this inputed contours must be closed and this contour must be anticlockwise
path = "\Data\cluster_contour_first.txt"
save_path = "C:/Users/Hang/Desktop/ANN/Zigzag/NoContinuiousZigzag/Data/zigzag.txt"
cofficient = 10000.0
interval = 0.4
angle = 0
pathes = []
dirpath = os.path.abspath(os.path.dirname(os.getcwd()))
path = dirpath + path
points = np.loadtxt(path)

contours = []
temp_contours = []
temp_contour = []
angles = []

for point in points:
    if(point[0] == 111111111111):
        copy_temp_contour = copy.deepcopy(temp_contour)
        temp_contours.append(copy_temp_contour)
        angles.append(point[2])
        temp_contour.clear()
        continue
    var_tuple = (round(point[0] * cofficient), round(point[1] * cofficient))
    temp_contour.append(var_tuple)
for i in range(len(temp_contours)):
    var_temp_tuple = tuple(temp_contours[i])
    pco = pyclipper.PyclipperOffset()
    pco.AddPath(var_temp_tuple, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)
    solution = pco.Execute(-interval * cofficient / 2.0)
    solution = np.array(solution) / cofficient
    contours.append(solution)

polygon =Polyline()
polygon1 =Polyline()
layer = Layer(0)
layer_contours = []
for i in range (len(contours)):
    layer = Layer(0)
    polygon = Polyline()
    for j in range (contours[i].shape[0]):
        for k in range (contours[i].shape[1]):
            polygon.addPoint(Point3D(contours[i][j][k][0], contours[i][j][k][1]))
        polygon.addPoint(Point3D(contours[i][j][0][0], contours[i][j][0][1]))
        layer.contours.append(polygon)
    layer_contours.append(layer)
    paths = genDpPath(layer.contours, interval, angles[i])
    pathes.append(paths)
#with open(save_path, 'w') as f:
    #for i in range(len(pathes)):
        #for fill in pathes[i]:
            #for j in fill.points:
                #.write(str(j.x) + "    " + str(j.y) + "    " + "0.2000"'\n')
            #f.write("1111" + "    " + "1111" + "    " + "1111" + '\n')
            #print("this is split contours")
#f.close()
va = VtkAdaptor()
for i in range(len(layer_contours)):
    for countour in  layer_contours[i].contours:
        va.drawPolyline(countour).GetProperty().SetColor(0,0,0)
index = 0
for paths in  pathes:
    for path in paths:
        va.drawPolyline(path).GetProperty().SetColor(1,0,0)
va.display()

import math

from GenDpPath import *
from Utility import *
from VtkAdaptor import *
import numpy as np
import os
import copy
from PathOp import *

# this inputed contours must be closed and this contour must be anticlockwise
path = "\Data\cluster_contour.txt"
out_offset_path = "\Data\out_contour_path.txt"

#path = "C:/Users/Hang/Desktop/ANN/Zigzag/Path/cluster_contour.txt"
save_path = "C:/Users/Hang/Desktop/ANN/Zigzag/DisContinuousZigzag/IICP/Data/zigzag.txt"
cofficient = 10000
interval = 0.4
pathes = []
dirpath = os.path.abspath(os.path.dirname(os.getcwd()))

path = dirpath + path
out_offset_path = dirpath + out_offset_path

points = np.loadtxt(path)

contours_no_offset = []
contours_offset = []
temp_contours = []
temp_contour = []
angles = []
jiaocuoangle = 0.0
jiaocuoflag = False
if(jiaocuoflag) : jiaocuoangle = math.pi / 2.0
for point in points:
    if(point[0] == 111111111111):
        copy_temp_contour = copy.deepcopy(temp_contour)
        temp_contours.append(copy_temp_contour)
        angle = point[2] + jiaocuoangle
        #if((angle - jiaocuoangle) >= 1e-14) : angle = angle - math.pi
        angles.append(angle)
        temp_contour.clear()
        continue
    var_tuple = (round(point[0] * cofficient), round(point[1] * cofficient))
    temp_contour.append(var_tuple)
for i in range(len(temp_contours)):
    var_temp_tuple = tuple(temp_contours[i])
    pco = pyclipper.PyclipperOffset()
    pco.AddPath(var_temp_tuple, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)
    solution = pco.Execute(-interval * cofficient / 4)
    solution = np.array(solution) / cofficient
    contours_offset.append(solution)

polygon =Polyline()
layer_contours = []
for i in range (len(contours_offset)):
    layer = Layer(0)
    polygon = Polyline()
    for j in range (contours_offset[i].shape[0]):
        for k in range (contours_offset[i].shape[1]):
            polygon.addPoint(Point3D(contours_offset[i][j][k][0], contours_offset[i][j][k][1]))
        polygon.addPoint(Point3D(contours_offset[i][j][0][0], contours_offset[i][j][0][1]))
        layer.contours.append(polygon)
    layer_contours.append(layer)
    paths = genDpPath(layer.contours, interval, angles[i])
    for path in paths:
        path.points.reverse()
    pathes.append(paths)

# this is to optimize the printing time only for discontinuous printing paths
optimal_pathes = sample_printing_time(pathes)

layer = [0.2,0.4]
with open(save_path, 'w') as f:
    for z in range(len(layer)):
        for i in range(len(pathes)):
            for fill in pathes[i]:
                for j in fill.points:
                    f.write(str(j.x) + "    " + str(j.y) + "    " + str(layer[z]) + '\n')
                f.write("1111" + "    " + "1111" + "    " + "1111" + '\n')
                print("this is split contours")
    f.write("11" + "    " + "1111" + "    " + "0.6")
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
for contour in layer_out.contours:
    va.drawPolyline(contour).GetProperty().SetColor(0, 0, 1)

for i in range(len(layer_contours)):
    for countour in  layer_contours[i].contours:
        va.drawPolyline(countour).GetProperty().SetColor(1,0,1)

for paths in  optimal_pathes:
    for path in paths:
        va.drawPolyline(path).GetProperty().SetColor(1,0,1)
        va.drawPolyline(path).GetProperty().SetColor(0,0,1)



va.display()

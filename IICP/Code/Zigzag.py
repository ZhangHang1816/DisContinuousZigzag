import math

from GenDpPath import *
from Utility import *
from VtkAdaptor import *
import numpy as np
import os
import copy
from PathOp import *
from RegionOffsetting import *
from WritePaths import *
from MergePath import *

# this inputed contours must be closed and this contour must be anticlockwise
path = "\Data\cluster_contour.txt"
out_offset_path = "\Data\out_contour_path.txt"

#path = "C:/Users/Hang/Desktop/ANN/Zigzag/Path/cluster_contour.txt"
save_path = "C:/Users/Hang/Desktop/ANN/Zigzag/DisContinuousZigzag/IICP/Data/zigzag.txt"
cofficient = 10000
interval = 0.4
first_layer = 0.2

dirpath = os.path.abspath(os.path.dirname(os.getcwd()))
path = dirpath + path
out_offset_path = dirpath + out_offset_path


points = np.loadtxt(path)
pathes = []
contours_offset = []
temp_contours = []
temp_contour = []
angles = []

z_layer = first_layer
for point in points:
    if(z_layer != point[2] and point[0] != 111111111111):
        pathes.append(region_offset(z_layer, interval, cofficient, angles, temp_contours))
        angles = []
        temp_contours = []
    if(point[0] == 111111111111):
        temp_contours.append(temp_contour)
        angles.append(point[2])
        temp_contour = []
        continue
    z_layer = point[2]
    var_tuple = (round(point[0] * cofficient), round(point[1] * cofficient))
    temp_contour.append(var_tuple)

pathes.append(region_offset(z_layer, interval, cofficient, angles, temp_contours))

## the next is to add the contour-parallel paths
pathes = mergepath(out_offset_path, first_layer, pathes)
write_paths(save_path,pathes)

va = VtkAdaptor()

for single_layer_paths in pathes:
    for paths in  single_layer_paths:
        for path in paths:
            va.drawPolyline(path).GetProperty().SetColor(1,0,0)
va.display()

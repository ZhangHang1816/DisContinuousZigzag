import math

from GenDpPath import *
from Utility import *
from VtkAdaptor import *
import numpy as np
import os
import copy
from Angle import *
from WritePath import *
from MergePath import *

# this inputed contours must be closed and this contour must be anticlockwise
inner_path = "\Data\inner_contour.txt"
out_path = "\Data\out_contour.txt"
out_offset_path = "\Data\out_contour_path.txt"

#path = "C:/Users/Hang/Desktop/ANN/Zigzag/Path/cluster_contour.txt"
save_path = "\Data\zigzag.txt"
first_layer = 0.2
H = 0.2
Height = 2.0
angles = []
pathes = []
cofficient = 10000.0
interval = 0.4

layer_num = round((Height - first_layer) / H) + 1

angleone = degToRad(1e-12)
angletwo = degToRad(1e-12)

dirpath = os.path.abspath(os.path.dirname(os.getcwd()))
inner_path = dirpath + inner_path
out_path = dirpath + out_path
out_offset_path = dirpath + out_offset_path
save_path = dirpath + save_path


for layer_num_index in range(0, layer_num, 2):
    angles.append(angleone)
    angles.append(angletwo)
pathes = angel(inner_path, out_path, first_layer, cofficient, H, interval, angles)

## the next is to add the contour-parallel paths

pathes = mergepath(out_offset_path, first_layer, pathes)

write_paths(save_path,pathes)

va = VtkAdaptor()

for paths in  pathes:
    for path in paths:
        va.drawPolyline(path).GetProperty().SetColor(0,0,1)
va.display()

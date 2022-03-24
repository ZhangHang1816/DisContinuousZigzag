#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from GenDpPath import *
import numpy as np

def mergepath(out_offset_path, first_layer, pathes):
    out_contour_path = np.loadtxt(out_offset_path)
    single_layer_out = Layer(first_layer)
    layer_out = []
    polygon_out = Polyline()
    z_layer = first_layer
    index_out = 0
    index_inner = 0
    paths = []
    for point in out_contour_path:
        if (point[0] == 1111):
            single_layer_out.contours.append(polygon_out)
            pathes[index_out].insert(index_inner, polygon_out)
            index_inner = index_inner + 1
            polygon_out = Polyline()
            paths = []
            if (point[2] != z_layer):
                layer_out.append(single_layer_out)
                single_layer_out = Layer(z_layer)
                index_out = index_out + 1
                index_inner = 0
            continue
        z_layer = point[2]
        polygon_out.addPoint(Point3D(point[0], point[1], point[2]))
    return pathes
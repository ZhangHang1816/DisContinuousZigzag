#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from PathOp import *
from GenDpPath import *

def region_offset(z_layer, interval, cofficient, angles, temp_contours):
    contours_offset = []
    single_pathes = []
    show_times = 0
    for i in range(len(temp_contours)):
        var_temp_tuple = tuple(temp_contours[i])
        pco = pyclipper.PyclipperOffset()
        pco.AddPath(var_temp_tuple, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)
        solution = pco.Execute(-interval * cofficient / 4)
        solution = np.array(solution) / cofficient
        contours_offset.append(solution)

    layer_contours = []
    for i in range (len(contours_offset)):
        layer = Layer(z_layer)
        polygon = Polyline()
        for j in range (contours_offset[i].shape[0]):
            for k in range (contours_offset[i].shape[1]):
                polygon.addPoint(Point3D(contours_offset[i][j][k][0], contours_offset[i][j][k][1], z_layer))
            polygon.addPoint(Point3D(contours_offset[i][j][0][0], contours_offset[i][j][0][1], z_layer))
            layer.contours.append(polygon)
        layer_contours.append(layer)
        paths = genDpPath(layer.contours, interval, angles[i])
        for path in paths:
            path.points.reverse()
        single_pathes.append(paths)
    if (show_times == 1):
        va = VtkAdaptor()
        for region_contour in layer_contours:
            for contour in region_contour.contours:
                va.drawPolyline(contour).GetProperty().SetColor(0, 0, 1)
        va.display()
    # this is to optimize the printing time only for discontinuous printing paths
    return sample_printing_time(single_pathes)
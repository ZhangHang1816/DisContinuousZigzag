#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from GenDpPath import *
import numpy as np

def angel(inner_path, out_path, first_layer, cofficient, H, interval, angles):
    pathes = []
    show_times = 0
    inner_points = np.loadtxt(inner_path)
    out_points = np.loadtxt(out_path)

    single_layer_contour = []
    layer_contour = []

    single_layer_out_contour = []
    single_layer_inner_contour = []

    z_layer = first_layer

    ## read the out contous
    for point in out_points:
        if (z_layer != point[2]):
            single_layer_contour.append(single_layer_out_contour)
            layer_contour.append(single_layer_contour)
            single_layer_contour = []
            single_layer_out_contour = []
        var_tuple = (round(point[0] * cofficient), round(point[1] * cofficient))
        z_layer = point[2]
        single_layer_out_contour.append(var_tuple)

    single_layer_contour.append(single_layer_out_contour)
    layer_contour.append(single_layer_contour)

    ## read the inner contours
    z_layer = first_layer
    for point in inner_points:
        if (z_layer != point[2]):
            index = round((z_layer - first_layer) / H)
            layer_contour[index].append(single_layer_inner_contour)
            single_layer_inner_contour = []
        var_tuple = (round(point[0] * cofficient), round(point[1] * cofficient))
        z_layer = point[2]
        single_layer_inner_contour.append(var_tuple)
    index = round((z_layer - first_layer) / H)
    layer_contour[index].append(single_layer_inner_contour)

    z_layer = first_layer
    for num in range(len(layer_contour)):
        flag = -1
        contours = []
        for size in range(len(layer_contour[num])):
            if (size == 1): flag = 1
            var_temp_tuple = tuple(layer_contour[num][size])
            pco = pyclipper.PyclipperOffset()
            pco.AddPath(var_temp_tuple, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)
            solution = pco.Execute(flag * interval * cofficient / 2.0)
            solution = np.array(solution) / cofficient
            contours.append(solution)
        layer = Layer(z_layer)
        polygon = Polyline()
        for i in range(len(contours)):
            polygon = Polyline()
            for j in range(contours[i].shape[0]):
                for k in range(contours[i].shape[1]):
                    polygon.addPoint(Point3D(contours[i][j][k][0], contours[i][j][k][1],  z_layer))
                polygon.addPoint(Point3D(contours[i][j][0][0], contours[i][j][0][1], z_layer))
            if (i == 1): polygon.points.reverse()
            layer.contours.append(polygon)
        if (show_times == 1):
            va = VtkAdaptor()
            for contour in layer.contours:
                va.drawPolyline(contour).GetProperty().SetColor(1, 0, 1)
            va.display()
        paths = genDpPath(layer.contours, interval, angles[num])
        pathes.append(paths)
        z_layer = z_layer + H
    return pathes
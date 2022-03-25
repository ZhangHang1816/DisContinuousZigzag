#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from GenDpPath import *

def write_paths(save_path, pathes):
    with open(save_path, 'w') as f:
        for single_layer_path in pathes:
            for single_connected_region in single_layer_path:
                for point in single_connected_region.points:
                    f.write(str(point.x) + "    " + str(point.y) + "    " + str(point.z) + '\n')
                f.write("1111" + "    " + "1111" + "    " + str(point.z) + '\n')
    f.close()
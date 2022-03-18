from GenDpPath import *
from Utility import *
from VtkAdaptor import *
import numpy as np
import os
import copy
class optipath:
    @staticmethod
    def Get_Key(value, key_list, value_list):  # 反查法
        return (key_list[value_list.index(value)])

    @staticmethod
    def Get_Key_list(points):
        key_list = []
        for key, value in points.items():
            key_list.append(key)
        return key_list

    @staticmethod
    def Get_value_list(points):
        value_list = []
        for key, value in points.items():
            value_list.append(value)
        return value_list

    @staticmethod
    def init_dict_points_and_pointlist(pathes):
        points = {}
        pointlist = []
        for i in range(len(pathes)):
            temp = []
            temp.append(pathes[i][0].points[0])
            temp.append(pathes[i][-1].points[-1])
            pointlist.append(pathes[i][0].points[0])
            pointlist.append(pathes[i][-1].points[-1])
            points[i] = temp
        return points, pointlist

    @staticmethod
    def to_get_the_optimal_pointsorder(points, map):
        list2 = []
        list_of_path = []
        distance = {}
        cannot = np.ones((len(points) * 2, 1)) * np.inf
        for i in range(len(points) * 2):
            list2.clear()
            tempmap = map.copy()
            tempmap[:, [i]] = cannot
            temp = 0
            index = [i]
            list2.append(index[0])
            while (len(list2) < len(points) * 2):
                index = np.argmin(tempmap[index[0]:index[0] + 1, 0:len(points) * 2], 1)  # 先置无穷大再寻找最小值
                list2.append(index[0])
                tempmap[:, index] = cannot
            for j in range(len(list2) - 1):
                temp = temp + map[list2[j]][list2[j + 1]]
            distance[i] = temp
            templist = copy.deepcopy(list2)
            list_of_path.append(templist)
        distance = sorted(distance.items(), key=lambda x: x[1])
        return distance, list_of_path
    @staticmethod
    def get_the_optimalpath(list_of_path, distance, pathes, pointlist, key_list, value_list):
        optimal_pathes = []
        for i in range(len(pathes)):
            optimal_pathes.append([])
        a = distance[0][0]
        index_of_pathes = 0
        for i in range(0, len(list_of_path[a]), 2):
            templist = []
            if (list_of_path[a][i + 1] > list_of_path[a][i]):
                templist.append(pointlist[list_of_path[a][i]])
                templist.append(pointlist[list_of_path[a][i + 1]])

                index = optipath.Get_Key(templist, key_list, value_list)
                for k in range(len(pathes[index])):
                    optimal_pathes[index_of_pathes].append(pathes[index][k])
                index_of_pathes = index_of_pathes + 1
            elif (list_of_path[a][i + 1] < list_of_path[a][i]):
                templist.append(pointlist[list_of_path[a][i + 1]])
                templist.append(pointlist[list_of_path[a][i]])
                index = optipath.Get_Key(templist, key_list, value_list)
                for k in range(len(pathes[index]) - 1, -1, -1):
                    pathes[index][k].points.reverse()
                    optimal_pathes[index_of_pathes].append(pathes[index][k])
                index_of_pathes = index_of_pathes + 1
        return optimal_pathes
    @staticmethod
    def Get_Map(points, key_list, pointlist):
        map = np.ones((len(points) * 2, len(points) * 2)) * np.inf
        for i in range(len(pointlist)):
            for j in range(len(pointlist)):
                if (i != j):
                    map[i][j] = pointlist[i].distance(pointlist[j])
        for i in range(len(key_list)):
            map[2 * key_list[i]][2 * key_list[i] + 1] = 0
            map[2 * key_list[i] + 1][2 * key_list[i]] = 0
        return map

def sample_printing_time(pathes):
    points, pointlist = optipath.init_dict_points_and_pointlist(pathes)
    key_list = optipath.Get_Key_list(points)
    value_list = optipath.Get_value_list(points)
    map = optipath.Get_Map(points, key_list, pointlist)
    distance, list_of_path = optipath.to_get_the_optimal_pointsorder(points, map)
    optimal_pathes = optipath.get_the_optimalpath(list_of_path, distance, pathes, pointlist, key_list, value_list)
    return optimal_pathes


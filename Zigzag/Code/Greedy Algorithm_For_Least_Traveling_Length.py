#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import math
from GenDpPath import *
from Utility import *
from VtkAdaptor import *
import numpy as np
import copy

class Least_Traveing_Path:
    def __init__(self, pathes):
        self.pathes = pathes
    def distance(self, A, B):
        return math.sqrt(math.pow((A.x - B.x),2) + math.pow((A.y - B.y),2))
    #def gen_least_path(self):



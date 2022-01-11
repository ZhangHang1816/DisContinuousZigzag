from GenDpPath import *
from Utility import *
from VtkAdaptor import *
import numpy as np
# this inputed contours must be closed and this contour must be anticlockwise
points=np.loadtxt("C:/Users/Hang/Desktop/ANN/Zigzag/Path/cluster_contour.txt")

interval = 0.4
angle = 0
pathes = []


polygon =Polyline()
polygon1 =Polyline()
for point in points:
    polygon.addPoint(Point3D(point[0],point[1]))

#point1=Point3D(0,0)
#point2=Point3D(10,0)
#point3=Point3D(10,10)
#point4=Point3D(0,10)

point1 = Point3D(0, 6)
point2=Point3D(5,2)
point3=Point3D(6,3)
point4=Point3D(4,9)
point5=Point3D(6,10)
point6=Point3D(3,9)
point7=Point3D(3,7)

subj = ((-5.0, -5.0), (5.0, -5.0), (5.0, 5.0), (-5.0, 5.0))

pco = pyclipper.PyclipperOffset()
pco.AddPath(subj, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)

solution = pco.Execute(-0.5)

#polygon.addPoint(point1)
#polygon.addPoint(point2)
#polygon.addPoint(point3)
#polygon.addPoint(point4)
#polygon.addPoint(point5)
#polygon.addPoint(point6)
#polygon.addPoint(point7)

#polygon.addPoint(point1)#
polygon1.addPoint(Point3D(2,2))
polygon1.addPoint(Point3D(8,2))
polygon1.addPoint(Point3D(8,8))
polygon1.addPoint(Point3D(6.5,8))
polygon1.addPoint(Point3D(5,4))
polygon1.addPoint(Point3D(3.5,8))
polygon1.addPoint(Point3D(2,8))
polygon1.addPoint(Point3D(2,2))

layer = Layer(0)
#layer.contours.append(polygon)
layer.contours.append(polygon)


print(type(layer.contours[0]))
angle = degToRad(angle)
paths = genDpPath(layer.contours,interval,angle) ## this angle must be rad
pathes.append(paths)
for i in paths:
    for j in i.points:
        print("HHHHHHHHHHHH", j)
    print("this is split contours")
va = VtkAdaptor()
for countour in layer.contours:
    va.drawPolyline(countour).GetProperty().SetColor(0,0,0)
for paths in  pathes:
    for path in paths:
        va.drawPolyline(path).GetProperty().SetColor(1,0,0)
va.display()

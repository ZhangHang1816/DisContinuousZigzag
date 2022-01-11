from GeomAIgo import *
from Utility import *
def _findAnglePairs(polygons, adjustPolyDirs):
    if adjustPolyDirs:
        adjustPolygonDirs(polygons)
    anglePairs = []
    for poly in polygons:
        for i in range(poly.count()-1):
            pts = poly.points
            v1 = pts[-2 if(i==0) else (i-1)].pointTo(pts[i])
            v2 = pts[i].pointTo(pts[i+1])
            if v1.crossProduct(v2).dz<0:
                a = radToDeg(v1.getAngle2D())
                b = radToDeg(v2.getAngle2D())
                a, b = min(a,b), max(a,b)
                anglePairs.append((a, b))
    return anglePairs

def _initAngleTable(digit):
    angleTable ={}
    delta = math.pow(10, -digit)
    angle = 0.0
    while angle <180:
        angleTable[angle] = 0
        angle = round(angle+delta, digit)
    return angleTable
def findOptFeedDir(polygons, digit = 0, adjustPolyDirs = False):
    anglePairs = _findAnglePairs(polygons, adjustPolyDirs)
    angletable = _initAngleTable(digit)
    delta = math.pow(10,-digit)
    for a, b in anglePairs:
        if b <= 180:
            key = round(a+delta, digit)
            while key <= round(b-delta,digit):
                angletable[key] +=1
                key = round(key+delta, digit)
        elif a >= 180:
            key = round(a -180 + delta, digit)
            while key <= round(b - 180 - delta, digit):
                angletable[key] += 1
                key = round(key + delta, digit)
        elif a <=180 and b >=180:
            b=b-180
            a, b = min(a,b), max(a,b)
            key = round(delta,digit)
            while key <a:
                angletable[key] += 1
                key = round(key+delta,digit)
            key = round(b+delta,digit)
            while key <180:
                angletable[key]+=1
                key = round(key + delta, digit)
    return angletable




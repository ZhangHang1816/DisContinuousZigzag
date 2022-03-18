import pyclipper

from GeomBase import *
from Line import *
from GeomAIgo import *
from Polyline import *
from GenHatch import *
from pyclipper import *
from ClipperAdaptor import *



class SplitRegion:
    def __init__(self, polygons, adjustPolyDirs = False):
        self.polygons = polygons
        if adjustPolyDirs:
            adjustPolygonDirs(self.polygons)
        self.splitPolygons = self.split()
    def split(self):
        turnPts = self.findTurnPoints()
        if len(turnPts)!=0:
            ys=[]
            for pt in turnPts:
                ys.append(pt.y)
            ys.sort()
            hatchPtses = calcHatchPoints(self.polygons,ys)
            splitters = []
            for turnPt in turnPts:
                lPt,rPt = self.findLRPoints(turnPt,hatchPtses)
                if lPt is not None and rPt is not  None:
                    splitter= self.createSplitter(lPt,rPt)
                    splitters.append(splitter)
            if len(splitters)!=0:
                clipper, ca =Pyclipper(), ClipperAdaptor()
                clipper.AddPaths(ca.toPaths(self.polygons), pyclipper.PT_SUBJECT )##有改动
                clipper.AddPaths(ca.toPaths(splitters), pyclipper.PT_CLIP)
                sln = clipper.Execute(pyclipper.CT_DIFFERENCE)
                return ca.toPolys(sln, turnPts[0].z)
        return self.polygons

    def findTurnPoints(self):
        vx = Vector3D(1, 0, 0)
        turnPts = []
        for poly in self.polygons:
            for i in range(poly.count()-1):
                pts = poly.points
                v1 = pts[-2 if (i==0) else(i-1)].pointTo(pts[i])
                v2 = pts[i].pointTo(pts[i+1])
                if v1.crossProduct(vx).dz * v2.crossProduct(vx).dz <=0:
                    if v1.crossProduct(v2).dz <0:
                        turnPts.append(pts[i])
        return turnPts
    def findLRPoints(self,pt,ptses):
        for pts in ptses:
            if len(pts) >0 and pts[0].y == pt.y:
                for i in range(len(pts)-1):
                    if pt.x >pts[i].x and pt.x <pts[i+1].x:
                        return pts[i],pts[i+1]
        return None ,None
    def createSplitter(self,p1,p2,delta = 1e-6):
        vx, vy = Vector3D(1,0,0),Vector3D(0,1,0)
        splitter = Polyline()
        splitter.addPoint(p1 - vx.amplified(delta)-vy.amplified(delta))
        splitter.addPoint(p2 + vx.amplified(delta)- vy.amplified(delta))
        splitter.addPoint(p2+vx.amplified(delta)+vy.amplified(delta))
        splitter.addPoint(p1-vx.amplified(delta)+vy.amplified(delta))
        splitter.addPoint(splitter.startPoint())
        return splitter
def splitRegion(polygons,adjustPolyDirs = False):
        return SplitRegion(polygons, adjustPolyDirs).splitPolygons

import GeomAIgo
from SplitRegion import *
from VtkAdaptor import *

class GenDpPath:
    def __init__(self, polygons, interval, angle):
        self.polygons, self.interval, self.angle = polygons, interval, angle
        self.splitPolys = []
    def generate(self):
        rotPolys = GeomAIgo.rotatePolygons(self.polygons, -self.angle)
        self.splitPolys = splitRegion(rotPolys)#有改动
        ys = self.genScanYs(rotPolys)
        paths = []
        for poly in self.splitPolys:
            #va = VtkAdaptor()
            #va.drawPolyline(poly).GetProperty().SetColor(0, 0, 0)
            #va.display()
            ys1 = self.genScanYs([poly])  # 对于一个polyline不能构成一个list 加上[]
            if len(ys1)!=0 and abs(ys1[0]-ys[0])<=1e-5:
                ys1.insert(0,ys1[0]-self.interval + 1e-5)
            splitymax = float('-inf')
            spacing_increment = 0.0
            for point in poly.points:
                splitymax = max(splitymax, point.y)
            if (len(ys1) >= 1):
                spacing_increment = (splitymax - ys1[len(ys1) - 1]) / len(ys1)
                for i in range(len(ys1)):
                    ys1[i] = ys1[i] + i * spacing_increment
            self.interval = self.interval + spacing_increment
            segs=genHatches([poly],ys1)
            if len(segs) > 0:
                path=self.linkLocalHatches(segs,poly)
                paths.append(path)
            self.interval = self.interval - spacing_increment
        return GeomAIgo.rotatePolygons(paths, self.angle)
    def genScanYs(self, polygons):
        yuzhi = 1e-9
        ys, yMin, yMax =[], float('inf'), float('-inf')
        for poly in polygons:
            for pt in poly.points:
             yMin, yMax = min(yMin, pt.y), max(yMax, pt.y)
        y = yMin + self.interval
        while yMax - y >= 1e-12:
            ys.append(y)
            y += self.interval
        return ys

    def linkLocalHatches(self, segs, polys): ###判断最后一条线是左线还是右线
        poly = Polyline()
        for i, seg in enumerate(segs):
            poly.addPoint(seg.A if (i % 2 == 0)else seg.B)
            poly.addPoint(seg.B if(i % 2 == 0)else seg.A)
            if (i != len(segs) - 1):
                if (i % 2 == 0):
                    PeekPoints = self.IsHavePeekR(poly.points[poly.count() - 1], segs[i + 1].B, polys)
                else:
                    PeekPoints = self.IsHavePeekL(poly.points[poly.count() - 1], segs[i + 1].A, polys)
                if PeekPoints != None:
                    for PeekPoint in PeekPoints:
                        poly.addPoint(PeekPoint)

        return poly

    def IsHavePeekL(self,prep,nextp,polys):
        peeklist=[]
        peekindex=[]
        linklist1=[]
        linklist2=[]
        flag = 0
        index_prep = -1
        index_nextp = -1
        for i,point in enumerate(polys.points):
            if (i == len(polys.points) - 1):
                continue
            # 行列式求面积判断三点是否共线
            x1 = point.x
            y1 = point.y
            x2 = polys.points[i+1].x
            y2 = polys.points[i+1].y
            x3 = prep.x
            y3 = prep.y
            sprep = 0.5 * ( x1*y2+x2*y3+x3*y1-x1*y3-x2*y1-x3*y2)
            x3 = nextp.x
            y3 = nextp.y
            snextp = 0.5 * ( x1*y2+x2*y3+x3*y1-x1*y3-x2*y1-x3*y2)
            if (abs(sprep) <= 1e-12):
                index_prep = i + 1
                if(index_prep == polys.count() - 1) : index_prep = 0
            if (abs(snextp) <= 1e-12):
                index_nextp = i + 1
                if (index_nextp == polys.count() - 1): index_nextp = 0
            if( point.y <= nextp.y and point.y >= prep.y):
                if(i == 0) : flag = 1
                peeklist.append(point)
                peekindex.append(i)
        xs1min = float('inf')
        xs2min = float('inf')
        if len(peekindex) >= 1:
            linklist1.append(peeklist[0])
            link1_index = peekindex[0]
            xs1min = min(peeklist[0].x, xs1min)
            for i in range(1,len(peekindex)):
                if (abs(link1_index-peekindex[i]) == 1 or (flag == 1 and peekindex[i] == polys.count() - 2)):
                     link1_index = peekindex[i]
                     xs1min = min(peeklist[i].x,xs1min)
                     if (flag == 1 and peekindex[i] == polys.count() - 2):
                         linklist1.insert(0, peeklist[i])
                         continue
                     linklist1.append(peeklist[i])
                     continue
                if(len(linklist2) == 0):
                    linklist2.append(peeklist[i])
                elif(len(linklist2) != 0 and abs(link2_index - peekindex[i]) == 1):
                    linklist2.append(peeklist[i])
                xs2min = min(peeklist[i].x, xs2min)
                link2_index = peekindex[i]
            if(len(linklist2) == 0):
                havelinkpoint = False
                for index in peekindex:
                    if(havelinkpoint == True) :
                        linklist1.reverse()
                        return linklist1
                    if( index == index_prep or index == index_nextp) : havelinkpoint = True
                if(havelinkpoint == False) :
                    return linklist2
            if (xs1min < xs2min) :
                linklist1.reverse()
                return linklist1
            if (xs2min < xs1min) :
                linklist2.reverse()
                return linklist2
    def IsHavePeekR(self,prep,nextp,polys):
        peeklist=[]
        peekindex=[]
        linklist1=[]
        linklist2=[]
        flag = 0
        index_prep = -1
        index_nextp = -1
        for i,point in enumerate(polys.points):
            if (i == len(polys.points) - 1):
                continue
            # 行列式求面积判断三点是否共线
            x1 = point.x
            y1 = point.y
            x2 = polys.points[i + 1].x
            y2 = polys.points[i + 1].y
            x3 = prep.x
            y3 = prep.y
            sprep = 0.5 * (x1 * y2 + x2 * y3 + x3 * y1 - x1 * y3 - x2 * y1 - x3 * y2)
            x3 = nextp.x
            y3 = nextp.y
            snextp = 0.5 * (x1 * y2 + x2 * y3 + x3 * y1 - x1 * y3 - x2 * y1 - x3 * y2)
            if (abs(sprep) <= 1e-12):
                index_prep = i + 1
                if(index_prep == polys.count() - 1) : index_prep = 0
            if (abs(snextp) <= 1e-12):
                index_nextp = i + 1
                if (index_nextp == polys.count() - 1): index_nextp = 0
            if( point.y <= nextp.y and point.y >= prep.y):
                if(i == 0) : flag = 1
                peeklist.append(point)
                peekindex.append(i)
        xs1max = float('-inf')
        xs2max = float('-inf')
        if len(peekindex) >= 1:
            linklist1.append(peeklist[0])
            link1_index = peekindex[0]
            xs1max = max(peeklist[0].x, xs1max)
            for i in range(1, len(peekindex)):
                if (abs(link1_index - peekindex[i]) == 1 or (flag == 1 and peekindex[i] == polys.count() - 2)):
                    link1_index = peekindex[i]
                    xs1max = max(peeklist[i].x, xs1max)
                    if(flag == 1 and peekindex[i] == polys.count() - 2):
                        linklist1.insert(0,peeklist[i])
                        continue
                    linklist1.append(peeklist[i])
                    continue
                if (len(linklist2) == 0):
                    linklist2.append(peeklist[i])
                elif (len(linklist2) != 0 and abs(link2_index - peekindex[i]) == 1):
                    linklist2.append(peeklist[i])
                xs2max = max(peeklist[i].x, xs2max)
                link2_index = peekindex[i]
            if (len(linklist2) == 0):
                havelinkpoint = False
                for index in peekindex:
                    if (havelinkpoint == True):return linklist1
                    if (index == index_prep or index == index_nextp): havelinkpoint = True
                if (havelinkpoint == False):
                    return linklist2
            if (xs1max < xs2max) :return linklist2
            if (xs2max < xs1max) :return linklist1

def genDpPath(polygons, interval, angle):
    return GenDpPath(polygons, interval, angle).generate()
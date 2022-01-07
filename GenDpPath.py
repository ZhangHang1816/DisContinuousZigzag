import GeomAIgo
from SplitRegion import *


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
            segs=genHatches([poly],ys)
            if len(segs) > 0:
                path=self.linkLocalHatches(segs,poly)
                paths.append(path)
        return GeomAIgo.rotatePolygons(paths, self.angle)
    def genScanYs(self, polygons):
        yuzhi = 1e-9
        ys, yMin, yMax =[], float('inf'), float('-inf')
        for poly in polygons:
            for pt in poly.points:
             yMin, yMax = min(yMin, pt.y), max(yMax, pt.y)
        y = yMin + self.interval
        while yMax - y >= 1e-10:
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
                    markbp, markap, seg1 = self.IsOnthesamepolyline(poly.points[poly.count() - 1], segs[i + 1].B, polys)
                else:
                    markbp, markap, seg1 = self.IsOnthesamepolyline(poly.points[poly.count() - 1], segs[i + 1].A, polys)
                if (markbp != -1 or markap != -1):
                    # 针对不同的方向有不同的算法 上升和下降连接的时候要把符号全部写反（猜测），记得改
                    # 要记录上升的线的数目，当到下降线时候，进行不同的算法
                    while (markap != markbp):
                        if (seg1[markbp].A.y > seg1[markbp].B.y):
                            poly.addPoint(seg1[markbp].A)
                        elif (seg1[markbp].A.y < seg1[markbp].B.y):
                            poly.addPoint(seg1[markbp].B)
                        if (seg1[markbp].A.y == seg1[markbp].B.y):
                            if (markbp != 0):
                                if (seg1[markbp - 1].B.y > seg1[markbp - 1].A.y):
                                    poly.addPoint(seg1[markbp].B)
                                if (seg1[markbp - 1].B.y < seg1[markbp - 1].A.y):
                                    poly.addPoint(seg1[markbp].A)
                            if (markbp == 0):
                                if (seg1[len(seg1) - 1].B.y > seg1[len(seg1) - 1].A.y):
                                    poly.addPoint(seg1[markbp].B)
                                if (seg1[len(seg1) - 1].B.y < seg1[len(seg1) - 1].A.y):
                                    poly.addPoint(seg1[markbp].A)
                        if (i % 2 == 0):
                            markbp, markap, seg1 = self.IsOnthesamepolyline(poly.points[poly.count() - 1],
                                                                            segs[i + 1].B, polys)
                        else:
                            markbp, markap, seg1 = self.IsOnthesamepolyline(poly.points[poly.count() - 1],
                                                                            segs[i + 1].A, polys)
                            #       the next is to link the zigzag path along to the outer contours in every split region

        return poly

    def IsOnthesamepolyline(self, bp: Point3D, ap: Point3D, polys):
        segs = []
        index = 0
        markbp = -1
        markap = -1
        for i in range(polys.count() - 1):
            seg = Segment(polys.point(i), polys.point(i + 1))
            segs.append(seg)

        for i, seg in enumerate(segs):
            v1 = seg.A.pointTo(bp)
            v2 = seg.A.pointTo(ap)

            if (seg.B.y > seg.A.y and v1.dotProduct(seg.A.pointTo(seg.B)) >= 0 and v1.crossProduct(
                    seg.A.pointTo(seg.B)).isZeroVector() and seg.A.distance(bp) < seg.length()):
                markbp = index
            if (seg.B.y < seg.A.y and v1.dotProduct(seg.A.pointTo(seg.B)) > 0 and v1.crossProduct(
                    seg.A.pointTo(seg.B)).isZeroVector() and seg.A.distance(bp) <= seg.length()):
                markbp = index

            if (seg.B.y > seg.A.y and v2.dotProduct(seg.A.pointTo(seg.B)) >= 0 and v2.crossProduct(
                    seg.A.pointTo(seg.B)).isZeroVector() and seg.A.distance(ap) < seg.length()):
                markap = index
            if (seg.B.y < seg.A.y and v2.dotProduct(seg.A.pointTo(seg.B)) > 0 and v2.crossProduct(
                    seg.A.pointTo(seg.B)).isZeroVector() and seg.A.distance(ap) <= seg.length()):
                markap = index
            if (seg.A.y == seg.B.y):
                if (i != 0):
                    if (segs[i - 1].direction().dy > 0 and v1.dotProduct(seg.A.pointTo(seg.B)) >= 0 and v1.crossProduct(
                            seg.A.pointTo(seg.B)).isZeroVector() and seg.A.distance(bp) < seg.length()):
                        markbp = index
                    if (segs[i - 1].direction().dy < 0 and v1.dotProduct(seg.A.pointTo(seg.B)) > 0 and v1.crossProduct(
                            seg.A.pointTo(seg.B)).isZeroVector() and seg.A.distance(bp) <= seg.length()):
                        markbp = index
                    if (segs[i - 1].direction().dy > 0 and v2.dotProduct(seg.A.pointTo(seg.B)) >= 0 and v2.crossProduct(
                            seg.A.pointTo(seg.B)).isZeroVector() and seg.A.distance(ap) < seg.length()):
                        markap = index
                    if (segs[i - 1].direction().dy < 0 and v2.dotProduct(seg.A.pointTo(seg.B)) > 0 and v2.crossProduct(
                            seg.A.pointTo(seg.B)).isZeroVector() and seg.A.distance(ap) <= seg.length()):
                        markap = index
                elif (i == 0):
                    if (segs[len(segs) - 1].direction().dy > 0 and v1.dotProduct(
                            seg.A.pointTo(seg.B)) >= 0 and v1.crossProduct(
                            seg.A.pointTo(seg.B)).isZeroVector() and seg.A.distance(bp) < seg.length()):
                        markbp = index
                    if (segs[len(segs) - 1].direction().dy < 0 and v1.dotProduct(
                            seg.A.pointTo(seg.B)) > 0 and v1.crossProduct(
                            seg.A.pointTo(seg.B)).isZeroVector() and seg.A.distance(bp) <= seg.length()):
                        markbp = index
                    if (segs[len(segs) - 1].direction().dy > 0 and v2.dotProduct(
                            seg.A.pointTo(seg.B)) >= 0 and v2.crossProduct(
                            seg.A.pointTo(seg.B)).isZeroVector() and seg.A.distance(ap) < seg.length()):
                        markap = index
                    if (segs[len(segs) - 1].direction().dy < 0 and v2.dotProduct(
                            seg.A.pointTo(seg.B)) > 0 and v2.crossProduct(
                            seg.A.pointTo(seg.B)).isZeroVector() and seg.A.distance(ap) <= seg.length()):
                        markap = index
            index = index + 1
        return markbp, markap, segs



def genDpPath(polygons, interval, angle):
    return GenDpPath(polygons, interval, angle).generate()
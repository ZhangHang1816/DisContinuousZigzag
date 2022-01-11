from GeomBase import *
class Polyline:
    def __init__(self):
        """

        :rtype: object
        """
        self.points = []
    def __str__(self):
        if self.count()>0:
            return 'Polyline\nPoint number:%s\nStart %s\nEnd %s'% (self.count(), str(self.startPoint()),str(self.endPoint()))
        else: return 'Polyline\nPoint number:0\n'
    def clone(self):
        poly = Polyline()
        for pt in self.points:
            poly.addPoint(pt.clone())
        return poly

    def count(self):
        return len(self.points)

    def addPoint(self, pt):
        self.points.append(pt)

    def raddPoint(self, pt):
        self.points.insert(0, pt)

    def addTuple(self,tuple):
        self.points.append(Point3D(tuple[0], tuple[1], tuple[2]))
    def removePoint(self,index):
        return self.points.pop(index)
    def point(self,index):
        return self.points[index]
    def startPoint(self):
        return self.points[0]
    def endPoint(self):
        return  self.points[len(self.points)-1]
    def isClosed(self):
        if self.count() <=2:return False
        return self.startPoint().isCoincide(self.endPoint())

    def multiply(self,m):
        for pt in self.points:
            pt.multiply(m)##书中原文是multiply,但point类中没有根据意思自己建了一个
    def multiplied(self,m):
        poly=Polyline()
        for pt in self.points:
            poly.addPoint(pt * m)##有改动
        return poly








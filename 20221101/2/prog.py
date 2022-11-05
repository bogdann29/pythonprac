def dist(c1, c2):
    return ((c2[0] - c1[0]) ** 2 + (c2[1] - c1[1]) ** 2) ** 0.5


def f(self, other):
        if self.sq == 0 or other.sq == 0:
            return False
        
        l = [(other.x1, other.y1), (other.x2, other.y2),(other.x3, other.y3)] 
        res = []
        for el in l:
            a = []
            a.append((self.x1 - el[0]) * (self.y2 - self.y1) - (self.x2 - self.x1) * (self.y1 - el[1]))
            a.append((self.x2 - el[0]) * (self.y3 - self.y2) - (self.x3 - self.x2) * (self.y2 - el[1]))
            a.append((self.x3 - el[0]) * (self.y1 - self.y3) - (self.x1 - self.x3) * (self.y3 - el[1]))
            
            res.append(all(zn >= 0 for zn in a) or all(zn <= 0 for zn in a))
        
        if res[0] == True:
            return not (res[1] and res[2])
        return res[1] or res[2]
    
    
class Triangle():
    def __init__(self, c1, c2, c3):
        self.x1, self.y1 = c1
        self.x2, self.y2 = c2
        self.x3, self.y3 = c3

        d1 = dist(c1,c2)
        d2 = dist(c1,c3)
        d3 = dist(c2,c3)
        p = (d1 + d2 + d3)/2
        self.exist = (d1 < d2 + d3) and (d2 < d1 + d3) and (d3 < d1 + d2)
        self.sq = (p * (p - d1) * (p - d2) * (p - d3))**0.5 if self.exist else 0
        
    def __abs__(self):
        return self.sq
    
    def __bool__(self):
        return self.exist
    
    def __lt__(self, other):
        return self.sq < other.sq
    
    def __contains__(self, other):
        if other.sq == 0:
            return True
        l = [(other.x1, other.y1), (other.x2, other.y2),(other.x3, other.y3)] 
        res = []
        for el in l:
            a = []
            a.append((self.x1 - el[0]) * (self.y2 - self.y1) - (self.x2 - self.x1) * (self.y1 - el[1]))
            a.append((self.x2 - el[0]) * (self.y3 - self.y2) - (self.x3 - self.x2) * (self.y2 - el[1]))
            a.append((self.x3 - el[0]) * (self.y1 - self.y3) - (self.x1 - self.x3) * (self.y3 - el[1]))
            
            res.append(all(zn >= 0 for zn in a) or all(zn <= 0 for zn in a))
        
        return all(cns == True for cns in res)
    
    def __and__(self, other):
        return f(self, other) or f(other, self)
    
import sys
exec(sys.stdin.read())
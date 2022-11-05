class Grange:
    def __init__(self, start, q, bn):
        self.start = start
        self.q = q
        self.bn = bn 
        self.progr = []
        while start < bn:
            self.progr.append(start)
            start *= q
    
    def __len__(self):
        return len(self.progr)
    
    def __getitem__(self, key):
        if isinstance(key, slice):
            if not key.step:
                return Grange(key.start, self.q , key.stop)
            return Grange(key.start, self.q ** key.step , key.stop)
        if key >= len(self):
            e = self.progr[-1]
            for i in range(len(self), key + 1):
                e *= self.q
            return e
        return self.progr[key]
    
    def __iter__(self):
        return iter(self.progr)
    
    def __repr__(self):
        return f"grange({self.start}, {self.q}, {self.bn})"

    def __str__(self):
        return f"grange({self.start}, {self.q}, {self.bn})"
    

import sys
exec(sys.stdin.read())
    
import rhinoscriptsyntax as rs
import ghpythonlib.components as ghc
from contextlib import contextmanager

class EQverts(object):
    def __init__(self):
        self.x = 0
        self.y = 0

    @classmethod
    def from_Rh_points(cls, _rp):
        obj = cls()
        obj.x, obj.y = _rp.X, _rp.Y
        return obj
    


    def __repr__(self):
        return '({},{})'.format(self.x, self.y)

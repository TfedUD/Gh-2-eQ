    """Superceeeded.
    To be archived: To be archived: was a WIP space

    """
import System
from System import Object



import rhinoscriptsyntax as rs 
from collections import namedtuple

class AltSpace:
    def __init__(self, _surface=[], _name=[]):
        self.surface = _surface
        self.nam = _name
        self._spaceVerts = []

    @property
    def name(self):
        return self.nam


    @property
    def spaceVerts(self):
        for surfaces in self.surface:
            self._spaceVerts.append( self._get_spaceVerts(surfaces))
        return self._spaceVerts

    @staticmethod
    def _get_spaceVerts(_srfc):
        xy_points = []
        points = rs.SurfacePoints(_srfc)
        for point in points:
            xy_points.append( (point.X, point.Y) )
        return xy_points

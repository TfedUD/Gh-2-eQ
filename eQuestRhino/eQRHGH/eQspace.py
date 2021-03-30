"""
HUGE thanks to Ed May!
"""


import System
from System import Object
import Rhino
from vectormath.euclid import Point3, Vector3, Vector2
import rhinoscriptsyntax as rs
from collections import namedtuple
import eq_space
from eq_space import Eq_space




class Space:
    def __init__(self, _surfaces=[], _name=None):
        self.surfaces = _surfaces# Type == list
        self._nameS = _name
        self._all_space_verts = []

    @property
    def all_space_XY_verts(self):
        """ Returns list of lists [[..],[..],[..]]"""
        for surface in self.surfaces:
            self._all_space_verts.append( self._get_one_surface_XY_verts(surface) )
        return self._all_space_verts

    @staticmethod
    def _get_one_surface_XY_verts(_srfc):
        """Looks at a single surface, finds its point XY data, returns them"""
        xy_points = []
        points = rs.SurfacePoints(_srfc)

        for point in points:
            xy_points.append( (point.X, point.Y) )

        return xy_points #=> list

    @property
    def spcName(self):
        nm = self._nameS
        return nm
        
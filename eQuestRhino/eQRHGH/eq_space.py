
import rhinoscriptsyntax as rs
from functools import reduce
import operator
import math
import ghpythonlib.components as ghc
from math import atan2
import geomTools 
from geomTools import EQverts as ev



class Eq_space:
    """Space Properties for Eq_space.
    
    Args:
        spc_srf: A srfc object hosting space properties.
        spc_name: Name of the space
        spc_vrts: vertices of the space
        
    Properties:
        *spc_srf 
        *spc_name
        *spc_vrts
        *spcVrtStr
    """

    def __init__(self, spc_srf, space_name):
        self._spc_srf = spc_srf
        self._space_name = space_name
        self._spc_vrts = None
        

    @property
    def spc_srf(self):
        """Get the surface hosting the properties"""
        return self._spc_srf

    @property
    def spc_name(self):
        """Get the name of the space"""
        return self._space_name


    @property
    def spc_vrts(self):
        """Return the verts of the space"""
        x = self._get_verts(self.spc_srf)
        return x


    @staticmethod
    def _get_verts(obj):
        brp_edges = ghc.DeconstructBrep(obj).edges
        brp_perim = ghc.JoinCurves(brp_edges, True)
        brp_verts = ghc.ControlPoints(brp_perim).points
        verts = (ev.from_Rh_points(vert) for vert in brp_verts)
        return list(verts)


    """
    @staticmethod
    def _get_verts(srfc):
        pntstr = [(point.X, point.Y) for point in rs.SurfacePoints(srfc)]
        return sorted(pntstr, key=lambda point:math.atan2(point[1]-0, point[0]-0))
    """



# returns all but one correctly: (point[1]-0, point[0]-1)
    """
    @staticmethod
    def _get_verts(srfc):
        pntstr = []
        points = rs.SurfacePoints(srfc)
        for point in points:
            pt= (point.X, point.Y)
            pntstr.append(pt)
        for pt in enumerate(pntstr):
            return sorted(pntstr, key=lambda pt:math.atan2(pt[0]-0, pt[1]-0) )
    """


        #return sorted(pntstr, key=lambda pt: math.atan2(pt[1]-0, pt[0]-0))
        # Works for 2/3 return sorted(pntstr, key=lambda pt: math.atan2(pt[0]-0, pt[1]-0))
        #return sorted(pntstr, key=lambda k: [k[0], k[1]])

# https://stackoverflow.com/questions/63338000/sorting-lists-of-polygon-coordinates-in-counter-clockwise-direction-in-python
# New goodgood   https://gist.github.com/mistycheney/4f274f6c4436bda614e5

def less(center):
    def less_helper(a, b):
        if (a[0] - center[0] >= 0 and b[0] - center[0] < 0):
            return 1;
        if (a[0] - center[0] < 0 and b[0] - center[0] >= 0):
            return -1;
        if (a[0] - center[0] == 0 and b[0] - center[0] == 0):
            if (a[1] - center[1] >= 0 or b[1] - center[1] >= 0):
                return 2*int(a[1] > b[1]) - 1;
            return 2*int(b[1] > a[1]) - 1

        # compute the cross product of vectors (center -> a) x (center -> b)
        det = (a[0] - center[0]) * (b[1] - center[1]) - (b[0] - center[0]) * (a[1] - center[1])
        if (det < 0):
            return 1;
        if (det > 0):
            return -1;

        # points a and b are on the same line from the center
        # check which point is closer to the center
        d1 = (a[0] - center[0]) * (a[0] - center[0]) + (a[1] - center[1]) * (a[1] - center[1])
        d2 = (b[0] - center[0]) * (b[0] - center[0]) + (b[1] - center[1]) * (b[1] - center[1])
        return 2*int(d1 > d2) - 1
    
    return less_helper

def sort_vertices_counterclockwise(cnt):
    # http://stackoverflow.com/a/6989383
    center = cnt.mean(axis=0)
    return sorted(cnt, cmp=less(center))

def counterclockwisesort(point):
    origin = [1, 1]
    refvec = [1, 0]
        # Vector between point and the origin: v = p - o
    vector = [point[0]-origin[0], point[1]-origin[0]]
    # Length of vector: ||v||
    lenvector = math.hypot(vector[1], vector[0])
    # If length is zero there is no angle
    if lenvector == 0:
        return -math.pi, 0
    # Normalize vector: v/||v||
    normalized = [vector[0]/lenvector, vector[1]/lenvector]
    dotprod  = normalized[0]*refvec[1] + normalized[0]*refvec[1]     # x1*x2 + y1*y2
    diffprod = refvec[0]*normalized[1] - refvec[0]*normalized[1]     # x1*y2 - y1*x2
    angle = math.atan2(diffprod, dotprod)

    return angle, lenvector

    """          
    @staticmethod
    def _get_verts(_srfc):
        pntstr = []
        points = rs.SurfacePoints(_srfc)
        for point in points:
            pt = (point.X, point.Y)
            pntstr.append(pt)
        return pntstr
    """
    








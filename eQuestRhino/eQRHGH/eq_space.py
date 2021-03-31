
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
        return self._get_verts(self.spc_srf)
        

#So Rhino natively counts counter clockwise apparently!
#So the key here is the class object in geomTools.py: that constructs 
#The 'eQuest vert Object' and the below utilizing the native Rh/Gh logic to construct 
#our 'space verts list'
    """
    @staticmethod
    def _get_verts(obj):
        brp_edges = ghc.DeconstructBrep(obj).edges
        brp_perim = ghc.JoinCurves(brp_edges, True)
        brp_verts = ghc.ControlPoints(brp_perim).points
        verts = (ev.from_Rh_points(vert) for vert in brp_verts)
        return list(verts)
    """

    @staticmethod
    def _get_verts(obj):
        brp_edges = ghc.DeconstructBrep(obj).edges
        brp_perim = ghc.JoinCurves(brp_edges, True)
        brp_verts = ghc.ControlPoints(brp_perim).points
        brpC =  ghc.CullDuplicates(brp_verts, 0.0).points
        verts = (ev.from_Rh_points(vert) for vert in brpC) #brp_verts
        
        return list(verts)










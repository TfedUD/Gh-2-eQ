import System
import rhinoscriptsyntax as rs
import scriptcontext as sc
from eq_space import Eq_space
import helpers



class eQ_Floor(Eq_space):

    def __init__(self, spc_srf, space_name, floorHeight, floorName, floorVerts):
        
        Eq_space.__init__(self, spc_srf, space_name)
        self._floorHeight = floorHeight
        self._floorName = floorName
        self._floorVerts = floorVerts

    @property
    def floor_Name(self):
        return self._floorName

    @property
    def floor_Verts(self):
        flvrts = []
        flvrts.append(self._floorVerts)
        return flvrts

    @property
    def floor_Height(self):
        return self._floorHeight    





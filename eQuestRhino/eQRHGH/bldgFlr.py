import System
import rhinoscriptsyntax as rs
import scriptcontext as sc
from eq_space import Eq_space
import helpers



class eQ_Floor(Eq_space):
    """Class allowing for the creation of floors and childspaces in one shot.
        Args:
            spc_srf: The srfcs of the spaces hosting properties
            space_name: The Name of the space (data flow a template for additional properties)
            floorHeight: Height of the floor
            floorName: Name of the floor
            floorVerts: Vertices of the floor poly: currently extrernaly acquired: to be integrated natively
    """

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





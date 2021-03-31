import rhinoscriptsyntax as rs
import scriptcontext as sc
import helpers
from eq_space import Eq_space



class eQ_Floor(Eq_space):
    """ Floor class with inheritance of Eq_space Class properties.

        Args:
            spc_srf: srfc object hosting the properties.
            spc_name: Name of the space(s)
            floorHeight: Floor height of the Floor
            floorName: The name of the floor 
            floorVerts: WIP currently: import joinbrep: surfacePoints modified list of verts.
        
        Properties:
        *spc_srf
        *spc_name
        *floorHeight
        *floorName
        *floorVerts
    """

    def __init__(self, spc_srf, space_name, floorHeight, floorName, floorVerts, floorZ):
        
        Eq_space.__init__(self, spc_srf, space_name)
        self._floorHeight = floorHeight
        self._floorName = floorName
        self._floorVerts = floorVerts
        self._floorZ = floorZ

    @property
    def floor_Name(self):
        return self._floorName
        
    @property
    def floor_Verts(self):
        return self._floorVerts
        
    @property
    def floor_Height(self):
        return self._floorHeight   

    @property
    def floorZ(self):
        return self._floorZ 
     

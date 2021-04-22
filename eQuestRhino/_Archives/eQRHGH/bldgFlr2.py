import System
import rhinoscriptsyntax as rs
import scriptcontext as sc
#from eq_space import Eq_space
import helpers



class eQ_Floor:

    def __init__(self, floorHeight, floorName, floorVerts, spc_srf=[]):
        
        self._floorHeight = floorHeight
        self._floorName = floorName
        self._floorVerts = floorVerts
        self._spcsSrfcs = spc_srf

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
    def vrts(self):
        pass


    @staticmethod
    def makeNget(_srfs):
        flsrf = rs.JoinSurfaces(_srfs, delete_input=False)
        pntstr = []
        points = rs.SurfacePoints(flsrf)
        for point in points:
            pt = (point.X, point.Y)
            pntstr.append(pt)



ghenv.Component.Message ='WIP FloorMaker\nV1'

"""
    Args:
        _geos: <list> Pass in geometry from the param getter
        _names: <list> Pass in Names from the Param getter
    Return:
        eQuest_Floor_: Connect to the _floor input in the file builder
        test1_: test output
        test2_: test output
"""

"""
Plan:  pass in the geom and params from the getparams component:
    build class with @properties for room names and verts, then switch 
    statements and stuff
"""
import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino
import ghpythonlib.components as ghc

from System import Object
from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path

from imp import reload
import eQRHGH
import eQRHGH.eQspace
reload(eQRHGH)
reload(eQRHGH.eQspace)

space = eQRHGH.eQspace.Space(_geo,)
temp = space.all_space_XY_verts

all_space_verts = DataTree[Object]() 
for i, surface_points in enumerate(temp):
    all_space_verts.AddRange(surface_points, GH_Path(i))
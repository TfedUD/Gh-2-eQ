from System import Object
from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path

import rhinoscriptsyntax as rs
import eQRHGH
import eQRHGH.eq_space
from imp import reload
reload(eQRHGH)
reload(eQRHGH.eq_space)

import json

#for space in _spaces:
a = _spaces.spc_name
b = _spaces.spc_vrts
print a
print b
    
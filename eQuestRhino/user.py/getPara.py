"""
    Args:
        _srfcs: <list> Rhino Brep or Mesh geometry
    Return:
        geo_: Connect to the '_geo' input of i've not got that far yet
        name_: Name of space
"""



ghenv.Component.Message = 'WIP Get Params\nFrom Rhino'

import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino
import ghpythonlib.components as ghc
from imp import reload
import eQRHGH
import eQRHGH.surfaces
import eQRHGH.helpers

reload(eQRHGH)
reload(eQRHGH.surfaces)
reload(eQRHGH.helpers)

input_geom = eQRHGH.surfaces.get_input_geom(_srfcs, ghenv)
input_srfcs = eQRHGH.surfaces.get_rh_srfc_params(input_geom, ghenv, ghdoc)

eQ_surfaces = (eQRHGH.surfaces.eQ_surface(srfc, ghenv) for srfc in input_srfcs)

geo_= []
name_= []

for eQ_surface in eQ_surfaces:
    geo_.append(eQ_surface.geometry)
    name_.append(eQ_surface.name)
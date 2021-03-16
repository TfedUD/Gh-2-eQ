import System
import helpers
import rhinoscriptsyntax as rs
import Grasshopper.Kernel as ghk
import Rhino
import math
import ghpythonlib.treehelpers as th
from collections import namedtuple

# This is the 'interface' that reads in the 'usertext' that we use as local file specific
# File data, see for more information: https://developer.rhino3d.com/api/rhinoscript/user_data_methods/user_data_methods.htm

class Temp_surface:
    """temp holder for srfc stuff"""

    def __init__(self, _geom=None, _params=None):
        self.geom = _geom
        self.params = _params
    
    def __iter__(self):
        return (i for i in (self.geom, self.params))

class eQ_surface:
    """ A WIP class to get all the data for making eQuest *.inp files
    Args:
        _srfc: <Surface> A single 'Surface' obj with .geom and .params
        _unknown: somthing probably in the future for space activity type ect.
        _ghenv: The Gh 'ghenv' obj from the scene
    Properties:
        * geometry
        * name
        * verts 
    """
    def __init__(self, _srfc, _ghenv):
        self.geometry = _srfc.geom
        self.params = _srfc.params
        self._warn_no_name(_ghenv)
        

    def _warn_no_name(self, _ghenv):
        nm = self.params.get('Object Name', None)
        if nm is None or nm == 'None':
            warning = "AAAHHHHH line 39"
            _ghenv.Component.AddRuntimeMessage(ghk.GH_RuntimeMessageLevel.Remark, warning)
    
            

    @property
    def name(self):
        ud_val = self.params.get('Object Name', 'No Name')
        return ud_val
       
           


def get_input_geom(_input_list, _ghenv):
    """ Gets geom and guid from whatever objects are input as the '_srfcs' """

    _input_num = 0
    output = []
    Geom = namedtuple('Geom', ['geom', 'guid'])

    for i, input_obj in enumerate(_input_list):
        if not input_obj:
            continue

        input_guid = _ghenv.Component.Params.Input[_input_num].VolatileData[0][i].ReferenceID
        rh_obj = Rhino.RhinoDoc.ActiveDoc.Objects.Find( input_guid )

        if rh_obj:

            geom = rs.coercegeometry(rh_obj)
            try:
                for srfc in geom.Surfaces:
                    output.append(Geom(srfc, input_guid))
            except AttributeError as e:
                output.append(Geom(geom, input_guid))
        else:
            try:
                for srfc in input_obj.Surfaces:
                    output.append(Geom(srfc,None))
            except AttributeError as e:
                output.append(Geom(input_obj, None))
    return output

def get_rh_srfc_params(_input_geom, _ghenv, _ghdoc):
    """ Pulls geom and UserText params from the Rhino scene.
    
    Args:
        _srfc_GUIDs: <list: Guid:> A list of the surface GUID numbers.
        _ghenv: The <ghenv> object from Grasshopper component calling this function
        _ghdoc: The <ghDoc> object from Grasshopper component calling this function
    Returns: 
        surfaces: A list of surface objects. Each object has a .geom and a .param property
    """
    surfaces = []

    for item in _input_geom:

        srfc_user_text = _get_surface_rh_userText(item.guid, _ghenv, _ghdoc)

        new_srfc_obj = Temp_surface(item.geom, srfc_user_text)
        surfaces.append(new_srfc_obj)
    
    return surfaces
"""
def get_srfc_verts(_input_geom):
    srfc_verts = []
    for item in _input_geom:
        vrts = rs.SurfacePoints(item.guid)
        srfc_verts.append(vrts)
    return srfc_verts
"""




def _get_surface_rh_userText(_srfc_GUID, _ghdoc, _ghenv):
    """ Takes in an objects GUID and returns the full dictionary of
    Attribute UserText Key and Value pairs. Cleans up a bit as well.
    
    Args:
        _GUID: <Guid> the Rhino GUID of the surface object to try and read from
        _ghdoc: The Grasshopper Component 'ghdoc' object
        _ghenv: The Grasshopper Component 'ghenv' object
    Returns:
        output_dict: a dictionary object with all the keys / values found in the Object's UserText
    """
    output_dict = {}

    if not _srfc_GUID:
        return output_dict
    
    if _srfc_GUID.GetType() != System.Guid:
        remark = "Unable to get the stuff dude set _srfc input type hint to guid"
        _ghenv.Component.AddRuntimeMessage(ghk.GH_RuntimeMessageLevel.Remark, remark)
        return output_dict
    
    with helpers.context_rh_doc(_ghdoc):
        output_dict['Object Name'] = rs.ObjectName(_srfc_GUID)

        for eachKey in rs.GetUserText(_srfc_GUID):
            if 'Object Name' not in eachKey:
                val = rs.GetUserText(_srfc_GUID, eachKey)
                if val != 'None':
                    output_dict[eachKey] = val
                else:
                    output_dict[eachKey] = None

    return output_dict



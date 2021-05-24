import rhinoscriptsyntax as rs
import sys
from ladybug_rhino import fromgeometry as fg
import ghpythonlib.components as ghc
try:  # import the core honeybee dependencies
    from honeybee.boundarycondition import boundary_conditions
    from honeybee.facetype import face_types, Wall, RoofCeiling, Floor
    from honeybee.room import Room
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

try:  # import the core honeybee dependencies
    from honeybee.face import Face
    from honeybee.facetype import face_types
    from honeybee.boundarycondition import boundary_conditions
    from honeybee.typing import clean_and_id_string
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

try:  # import the ladybug_rhino dependencies
    from ladybug_rhino.togeometry import to_face3d
    from ladybug_rhino.grasshopper import all_required_inputs, longest_list, wrap_output
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_rhino:\n\t{}'.format(e))
from decimal import Decimal as dex




#---------------Space Class---------------------------------


class eQspace:

    def __init__(self, _rm):
        self.rm = _rm


#------------------------- To be used for filtering wall verts possibly?? 
#------------------------ Tho it seems lb geom can do more better 
    @property
    def spc_vrts(self):
        return self._getVrts(self.rm)

    @staticmethod
    def _getVrts(obj):
        try:
            fcs= [face for face in obj.faces]
            flr = fcs[-2]
            p3 = flr.vertices
            vrtlst=[]
            for p in p3:
                vrts = p.x, p.y
                vrtlst.append(vrts)
            return vrtlst
        except  IndexError:
            raise IndexError('No faces found on room:"{obj.name}"')
#----------------------------------------------------------------------------

#--------------Get attrs to create the output strings------------------------
    @property
    def spc_nm(self):
        return self._getSpcNm(self.rm)
    
    @staticmethod
    def _getSpcNm(obj):
        return obj.display_name

    @property
    def lvl(self):
        return self._getlvl(self.rm)
    
    @staticmethod
    def _getlvl(obj):
        return obj.story

#------------------------------------------------------------------------------

#---------------- Space Polys -------------------------------------------------

    @property
    def spcPlystr(self):
        return self._spvst(self.rm, self.spc_nm, self.lvl)

    @staticmethod
    def _spvst(obj, nm, lv):
        try:
            fcs= [face for face in obj.faces]
            flr = fcs[-2]
            p3 = flr.vertices
            vrtlst=[]
            for p in p3:
                vrts = p.x, p.y
                vrtlst.append(vrts)
            st = []
            for i, ind in enumerate(vrtlst):
                indx = i+1
                strv = '   V{}'.format(indx)+' '*14+'=  '
                st.append(prepend(ind,strv))
            c=[]
            for elem in st:
                for el in elem:
                    c.append(el)
            bdx = '\n'.join([i for i in c[0:]])
            vx = str(bdx)+'\n   ..\n'
            ttl = '"{}_L-{} Plg" = POLYGON\n'.format(nm, lv) 

            return ttl+vx

        except  IndexError:
            raise IndexError('No faces found on room:"{obj.name}"')

#-------------------------------------------------------------------

#---------------------- spaces--------------------------------------
    @property
    def spcSpace(self):
        return self._makeSpace(self.rm)

    @staticmethod
    def _makeSpace(obj):
        filtDesc = filter(str.isalpha, obj.display_name)
        bdx = '"{}_L-{}_SP" = SPACE\n   SHAPE'.format(obj.display_name, obj.story)+' '*11+'= POLYGON\n'+'   POLYGON'\
            +' '*9+'= "{}_L-{} plg"\n'.format(obj.display_name, obj.story)+'   C-ACTIVITY-DESC = *{}*\n   ..'.format(filtDesc)
        return bdx

#---------------------------------------------------------------------

#----------------------Zones------------------------------------------

    @property
    def spcZone(self):
        return self._makezone(self.rm)

    @staticmethod
    def _makezone(obj):
        sp = '"{}_L-{}_SP"\n   '.format(obj.display_name, obj.story)
        bdx = '"{}_L{}_ZN" = ZONE\n   '.format(obj.display_name, obj.story)+'TYPE'+' '*13+'= CONDITIONED\n   '\
            +'SPACE'+' '*12+'= {}\n   ..'.format(sp)
        return bdx




#---------Level/story/floor what call you's to org eQuest spaces to their parent floor---


#Need to get flr srfcs from _rms input to apply to the make face level

#THIS is how to pass in multiple objects into a single class instance
class eQfloor(eQspace):
    """ Get our rooms sorted out by story from the HB model as to write them out by:
    Floor poly.append(spacePolys)
    """
    def __init__(self, rooms=[]):
        
        self._rooms = []
        for room in rooms:
            self.add_room(room)

    @property
    def rooms(self):
        return(self._rooms)

    def add_room(self, obj):
        self._rooms.append(eQspace(obj))















def prepend(list, str):
    str += '{0}'
    list = [str.format(list)]
    return(list)

        



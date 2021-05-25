import rhinoscriptsyntax as rs
import sys
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

from ladybug_rhino import fromgeometry as fg
import itertools


#---------------Space Class---------------------------------


class eQspace:

    def __init__(self, _rm):
        self.rm = _rm

#---------------Adding floor surface property--------------------------------
    @property
    def floorSrfc(self):
        return self.getMyFloor(self.rm)
    
    @staticmethod
    def getMyFloor(obj):
        floorFace = [srfc for srfc in obj.faces if str(srfc.type)=='Floor']
        flrgeom = []
        for f in floorFace:
            flrgeom.append(fg.from_face3d(f.geometry))
        return flrgeom

    @property
    def room_story(self):
        return self._getStory(self.rm)

    @staticmethod
    def _getStory(obj):
        return obj.story
    
    @property
    def room_height(self):
        return self._getHeight(self.rm)

    @staticmethod
    def _getHeight(obj):
        return obj.average_floor_height





#------------------------- To be used for filtering wall verts possibly?? 
#------------------------ Tho it seems lb geom can do more better
#----------------This also is not being used from what I can tell lol..
    @property
    def spc_vrts(self):
        return self._getVrts(self.rm)

    @staticmethod
    def _getVrts(obj):
        try:
            fcs= [face for face in obj.faces if str(face.type)=='Floor']
            #flr = fcs[-2]
            #p3 = flr.vertices
            p3 = fcs.vertices
            vrtlst=[]
            for p in p3:
                vrts = p.x, p.y
                vrtlst.append(vrts)
            return vrtlst
        except  IndexError:
            raise IndexError('No faces found on room:"{obj.name}"')
#----------------------------------------------------------------------------
#----------------
#----------------



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



#THIS is how to pass in multiple objects into a single class instance

class eQfloor(eQspace):
    """ todo:
            Make sort: to pass individual floors/levels/storys (lets all just use one vernacular maybe)
            As to make our 'floor instances' in which to write the file out from
        todo:
            Need to pass all the strings for the rooms into the floor so can write out the inp 
            by floor:
            floor space/poly/area whatever:   create for floor: append room strs
    """
    def __init__(self, rooms=[]):

        
        self._rooms = []
        for room in rooms:
            self.add_room(room)

        self._floor_geoms = []
        for room in self.rooms:
            self.add_floorGeoms(room)

        self._floor_storyInd = []
        for room in self.rooms:
            self.add_storyInd(room)

        self._room_heights = []
        for room in self.rooms:
            self.add_height(room)

        self._room_poly_strings = []
        for room in self.rooms:
            self.add_rmPoly_str(room)

        self._room_space_strings = []
        for room in self.rooms:
            self.add_room_space_str(room)
        
        self._space_zone_strings = []
        for room in self.rooms:
            self.add_space_zone(room)

#---------
    def add_space_zone(self,obj):
        self._space_zone_strings.append(obj.spcZone)
    
    @property
    def room_inp_zone(self):
        return(self._space_zone_strings)
#---------

#---------
    def add_room_space_str(self, obj):
        self._room_space_strings.append(obj.spcSpace)

    @property
    def room_inp_space(self):
        return(self._room_space_strings)
#---------

# ---------
    def add_rmPoly_str(self, obj):
        self._room_poly_strings.append(obj.spcPlystr)

    @property
    def room_inp_poly(self):
        return(self._room_poly_strings)
#---------

#---------
    @property
    def rooms(self):
        return(self._rooms)

    def add_room(self, obj):
        self._rooms.append(eQspace(obj))
#---------

#---------
    def add_height(self, obj):
        self._room_heights.append(obj.room_height)
    
    @property
    def floor_Height(self):
        return self._getheight(self._room_heights)
    
    @staticmethod
    def _getheight(obj):
        return obj[0]
#---------

#---------
    @property
    def floor_faces(self):
        return(self._floor_geoms)

    def add_floorGeoms(self, obj):
        self._floor_geoms.append(obj.floorSrfc)
#---------

#---------
    @property
    def floor_story_ind(self):
        return(self._floor_storyInd)

    def add_storyInd(self, obj):
        self._floor_storyInd.append(obj.room_story)
#---------

#---------
    @property
    def floor_verts(self):
        return(self._floorVerts(self.floor_faces))
    
    @staticmethod
    def _floorVerts(obj):
        geomslst = [ x for n in obj for x in n]
        te = ghc.BrepJoin(geomslst).breps
        return _get_verts(te)
#---------

#---------
    @property
    def flr_z(self):
        return(self._getz(self.floor_faces))
    
    @staticmethod
    def _getz(obj):
        geomlst = [ x for n in obj for x in n]
        te = ghc.BrepJoin(geomlst).breps
        cnt = ghc.Area(te).centroid
        return cnt.Z



#---------
    @property
    def level(self):
        return self._levelGet(self.floor_story_ind)

    @staticmethod
    def _levelGet(obj):
        return obj[0]
#---------





#---------Floor inp strings time -----------------------------------------
#---------
    #----------------Polys --------------------------------
    @property
    def floor_poly_strs(self):
        return self._makeStrSet(self.floor_verts, self.level, self.room_inp_poly)

    @staticmethod
    def _makeStrSet(vrts, lvl, rminp):
        hdr = '"Level -{} Poly" = POLYGON\n'.format(lvl)
        st = []
        x = vrts
        for i, ind in enumerate(x):
            indx = i+1
            strv = '   V{}'.format(indx)+' '*14+'=  '
            st.append(prepend(ind,strv))
        c = []
        for elem in st:
            for el in elem:
                c.append(el)
        bdx = '\n'.join([i for i in c[0:]])
        ipstrs = ''.join(i for i in rminp)
        return hdr+str(bdx)+'\n   ..\n'+ipstrs
    #---------
    #---------Floors Spaces Walls WIndows Doors
    #---------

    @property
    def floor_space_strs(self):
        return self._makeSpaceSet(self.level, self.floor_Height, self.flr_z, self.room_inp_space)

    @staticmethod
    def _makeSpaceSet(lvl, hgt, flz, sinp):
        hdr = '"Level -{}" = FLOOR\n'.format(lvl)+'   Z'+' '*16+'= {}\n'.format(flz)\
            +'   POLYGON'+' '*10+'= "Level -{} Poly"\n   '.format(lvl)+'SHAPE'+' '*12\
                +'= POLYGON\n   '+'FLOOR-HEIGHT'+' '*5+'= {}\n   '.format(hgt)\
                    +'SPACE-HEIGHT'+' '*5+'= {}\n   '.format(hgt)+'C-DIAGRAM-DATA   *Level {} UI DiagData*\n   ..\n'.format(lvl)
        
        spstrs = '\n'.join(i for i in sinp)
        return hdr+spstrs

    #---------
    #---------Zones
    #---------

    @property
    def floor_zone_strs(self):
        return self._makeZoneStrSet(self.room_inp_zone)

    @staticmethod
    def _makeZoneStrSet(obj):
        place = '"AHU PLACEHOLDER"\n   ..\n'
        znstrs = '\n'.join(i for i in obj)
        return place+znstrs





    
        














def prepend(list, str):
    str += '{0}'
    list = [str.format(list)]
    return(list)

def _get_verts(obj):
        brp_edges = ghc.DeconstructBrep(obj).edges
        brp_perim = ghc.JoinCurves(brp_edges, True)
        brp_verts = ghc.ControlPoints(brp_perim).points
        brpC =  ghc.CullDuplicates(brp_verts, 0.0).points
        verts = [(point.X,point.Y) for point in brpC]
        
        return verts
        



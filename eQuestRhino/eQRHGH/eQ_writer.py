import rhinoscriptsyntax as rs
from bldgFlr import eQ_Floor 
from System import Object
from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path





class PolyStrs:
    """ A class to take all the floor objects from the model
        Parse out their data and properties ect into the:
        $ Polygons block, and the $Floors / Spaces / Walls section of the *.inp
        from srfcs to _getVrts: ignore: data flow testing.
    """
    def __init__(self, _floorObjs):
        self.floorObjs = _floorObjs
    
    @property
    def spcNm(self):
        return self._getName(self.floorObjs)
    
    @staticmethod
    def _getName(objs):
        x = objs.spc_name
        return x
        

    @property
    def srfcs(self):
        return self._getsrfs(self.floorObjs)

    @staticmethod
    def _getsrfs(objs):
        for obj in objs:
            x = obj.spc_srf
        return x

    @property
    def Vrts(self):
        return self._getVrts(self.floorObjs)

    @staticmethod
    def _getVrts(objs):
        for obj in objs:
            x = obj.spc_vrts
            y = [t for t in (set(tuple(i) for i in x))]
        
        return q
    
    @property
    def floorName(self):
        return self._getFlrNm(self.floorObjs)

    @staticmethod
    def _getFlrNm(obj):
        x = obj.floor_Name
        return x

    @property
    def floorverts(self):
        return self._getFlrVrts(self.floorObjs)

    @staticmethod
    def _getFlrVrts(obj):
        x = obj.floor_Verts
        return x

    @property
    def floorHeight(self):
        return self._getH(self.floorObjs)

    @staticmethod
    def _getH(obj):
        x = obj.floor_Height
        return x

    @property
    def flrZ(self):
        return self._getZ(self.floorObjs)
    
    @staticmethod
    def _getZ(obj):
        x = obj.floorZ
        return x
    

# ------------------------------------------------------------
#  ----------File String Generaters---------------------------
####### Poly Strs ######
    @property
    def flrstr(self):
        return self._flrstrfrm(self.floorObjs)

    @staticmethod
    def _flrstrfrm(obj):
        st = []
        x = obj.floor_Verts
        for i, ind in enumerate(x):
            indx = i+1
            strv = '   V{}'.format(indx)+' '*14+'= '
            st.append(prepend(ind,strv))
        return st
    
    @property
    def flrWrtStr(self):
        return self._flrst(self.flrstr)+'\n   ..'
    
    @staticmethod
    def _flrst(flrstr):
        c = []
        for elem in flrstr:
            for el in elem:
                c.append(el)
        bdx = '\n'.join([i for i in c[0:]])
        return str(bdx)

    @property
    def floorWriteStr(self):
        return self._florBuilder(self.floorName, self.flrWrtStr)
    
    @staticmethod
    def _florBuilder(nm, ob):
        bdx = '"{} Poly" = POLYGON\n'.format(nm)
        strs = bdx+ob
        return strs


    @property
    def polygonStr(self):
        return self._polyStrFormer(self.floorObjs)

    @staticmethod
    def _polyStrFormer(objs):
        st = []
        x = objs.spc_vrts
        for i, ind in enumerate(x):
            indx = i+1
            strv = '   V{}'.format(indx)+' '*14+'= '
            st.append(prepend(ind,strv))
        return st

    @property
    def writeStr(self):
        return self._wrtsrt(self.polygonStr)+'\n   ..'

    @staticmethod
    def _wrtsrt(plystr):
        c = []
        for elem in plystr:
            for el in elem:
                c.append(el)
        bdx = '\n'.join([i for i in c[0:]])
        return str(bdx)

    @property
    def wrtstr(self):
        return self._wrtstrfrmt(self.spcNm, self.writeStr)

    @staticmethod
    def _wrtstrfrmt(nm, ob):
        bdx = '"{} Plg" = POLYGON\n'.format(nm)
        strs = bdx+ob
        return strs

######## Floors spaces walls windows doors

    @property
    def flrFloor(self):
        return self._flrflr(self.floorName, self.floorHeight, self.flrZ)

    @staticmethod
    def _flrflr(nm,h,fz):
        bdx = '"{}1" = FLOOR\n'.format(nm)+'   Z'+' '*16+'= {}\n'.format(fz)\
            +'   POLYGON'+' '*10+'= "{} Poly"\n   '.format(nm)+'SHAPE'+' '*12\
                +'= POLYGON\n   '+'FLOOR-HEIGHT'+' '*5+'= {}'.format(h)+'\n   C-DIAGRAM-DATA   =*Level 1 UI DiagData*\n'\
                    +'   ..'
        return bdx

    @property
    def spcSpace(self):
        return self._spcspc(self.spcNm)
    
    @staticmethod
    def _spcspc(nm):
        bdx = '"{}" = SPACE\n   SHAPE'.format(nm)+' '*11+'= POLYGON\n'+'   POLYGON'+' '*9+'= "{} Plg"\n'.format(nm)\
            +'   C-ACTIVITY-DESC = *brkm*\n  ..'# Fillers to add in additional.formats
        return bdx





def cullDoop(lst):
    return [t for t in (set(tuple(i) for i in lst))]






def prepend(list, str):
    str += '{0}'
    list = [str.format(list)]
    return(list)




    
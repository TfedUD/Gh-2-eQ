# Based on honeybee_energy properties, face.py face energy properties
#Make a writer that uses space object to_inp() str


import rhinoscriptsyntax as rs

class Eq_space(object):
    """Space Properties for Eq_space.
    
    Args:
        spc_srf: A srfc object hosting space properties.
        spc_name: Name of the space
        spc_vrts: vertices of the space
        
    Properties:
        * spc_srf
        * spc_name
        * spc_vrts
    """
    __slots__ = ('_spc_srf', '_space_name', '_spc_vrts')

    def __init__(self, spc_srf, space_name, spc_vrts=None):
        self._spc_srf = spc_srf
        self._space_name = space_name
        self._spc_vrts = spc_vrts

    @property
    def spc_srf(self):
        """Get the surface hosting the properties"""
        return self._spc_srf

    @property
    def spc_name(self):
        """Get the name of the space"""
        return self._space_name
# spaceverts not yet working    
    @property
    def spc_vrts(self):
        """Get the verts of the space"""
        return self._spc_vrts

    @spc_vrts.setter
    def spc_vrts(self, value):
        value = []
        b = rs.SurfacePoints(self.spc_srf)
        value.append(b)
        self._spc_vrts = value





    def to_dict(self, abridged=False):
        """ Return Space Properties as a dictionary.
        This is where to add additional properties to each space object!
        Unless there is exist better way. But for now this is it. 
        Args: 
            abidged false: Returns full dict, True: returns abridged version
        """
        base= {'Space': {}}
        base['Space']['type'] = 'Eq_space_properties' if not \
            abridged else 'Eq_space_properties_abridged'
        if self._space_name is not None:
            base['Space']['spc_name'] = \
                self._space_name.to_dict()
        if self._spc_vrts is not None:
            base['Space']['spc_vrts'] = self._spc_vrts.to_dict()
        return base





    def duplicate(self, new_spc_srf=None):
        """Get a copy of this object.
        Args:
            new_spc_srf: A new space object to host these properties.
                If None, the properties will *HOPEFULLY* be duplicated with the same host.
        """
        _spc_srf = new_spc_srf or self._spc_srf
        return Eq_space(_spc_srf, self._space_name, self._spc_vrts)




    def ToString(self):
            return self.__repr__()

    def __repr__(self):
        return 'Space Properties: [Space: {}]'.format(self.spc_srf.spc_name)


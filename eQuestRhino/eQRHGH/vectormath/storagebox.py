"""

    def to_dict(self, abridged=False):
        # Return Space Properties as a dictionary.
        This is where to add additional properties to each space object!
        Unless there is exist better way. But for now this is it. 
        Args: 
            abidged false: Returns full dict, True: returns abridged version
        #
        base= {'Space': {}}
        base['Space']['type'] = 'Eq_space_properties' if not \
            abridged else 'Eq_space_properties_abridged'
        if self._space_name is not None:
            base['Space']['spc_name'] = \
                self._space_name.to_dict()
        if self._spc_vrts is not None:
            base['Space']['spc_vrts'] = self._spc_vrts.to_dict()
        return base
"""

"""
def counterclockwisesort(point):
    origin = [0, 1]
    refvec = [0, 1]
        # Vector between point and the origin: v = p - o
    vector = [point[0]-origin[0], point[1]-origin[1]]
    # Length of vector: ||v||
    lenvector = math.hypot(vector[0], vector[1])
    # If length is zero there is no angle
    if lenvector == 0:
        return -math.pi, 0
    # Normalize vector: v/||v||
    normalized = [vector[0]/lenvector, vector[1]/lenvector]
    dotprod  = normalized[0]*refvec[0] + normalized[1]*refvec[1]     # x1*x2 + y1*y2
    diffprod = refvec[1]*normalized[0] - refvec[0]*normalized[1]     # x1*y2 - y1*x2
    angle = math.atan2(diffprod, dotprod)
    # Negative angles represent counter-clockwise angles so we need to subtract them 
    # from 2*pi (360 degrees)
    if angle < 0:
        return 2*math.pi+angle, lenvector
    # I return first the angle because that's the primary sorting criterium
    # but if two vectors have the same angle then the shorter distance should come first.
    return angle, lenvector
"""


    #def duplicate(self, new_spc_srf=None):
        """Get a copy of this object.
        Args:
            new_spc_srf: A new space object to host these properties.
                If None, the properties will *HOPEFULLY* be duplicated with the same host.
        """
       # _spc_srf = new_spc_srf or self._spc_srf
      #  return Eq_space(_spc_srf, self._space_name, self._spc_vrts)



"""
    def ToString(self):
            return self.__repr__()

    def __repr__(self):
        return 'Space Properties: [Space: ]'.format(self.spc_srf.spc_name)
"""

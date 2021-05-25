"""
    @property
    def floor_poly_strs(self):
        return self._makeStrSet(self.floor_verts, self.level)

    @staticmethod
    def _makeStrSet(vrts, lvl):
        hdr = '"Level -{} Poly" = POLYGON\n'.format(lvl)
        st = []
        x = vrts
        for i, ind in enumerate(x):
            indx = i+1
            strv = '   V{}'.format(indx)+' '*14+'= '
            st.append(prepend(ind,strv))
        c = []
        for elem in st:
            for el in elem:
                c.append(el)
        bdx = '\n'.join([i for i in c[0:]])


        return hdr+str(bdx)+'\n   ..'
"""
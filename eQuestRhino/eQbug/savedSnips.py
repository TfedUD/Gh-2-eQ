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
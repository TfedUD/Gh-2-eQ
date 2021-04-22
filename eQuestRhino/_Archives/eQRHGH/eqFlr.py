import rhinoscriptsyntax as rs


class Floor_capsule:

    def __init__(self,flr_height, flr_name, spaces=[]):

        self._spaces = spaces
        self._flr_height = flr_height
        self._flr_name = flr_name
        


    @property
    def floorSpaces(self):
        floorSpaces = []
        floorSpaces.append(self._spaces)
        return floorSpaces


    @staticmethod
    def 
            



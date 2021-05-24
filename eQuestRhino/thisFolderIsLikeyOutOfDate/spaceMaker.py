import rhinoscriptsyntax as rs
from imp import reload
import eQRHGH
import eQRHGH.eq_space
reload(eQRHGH)
reload(eQRHGH.eq_space)
ghenv.Component.Message = 'Space Maker Test'

eqSpace = eQRHGH.eq_space.Eq_space(_geo, _name)

if _geo != None:
    a = eqSpace


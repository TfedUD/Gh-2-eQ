
# -*- coding: UTF-8 -*-
from contextlib import contextmanager
from copy import deepcopy
import scriptcontext as sc
import Rhino
import re
import Grasshopper.Kernel as ghk
import rhinoscriptsyntax as rs
from timeit import default_timer

@contextmanager
def context_rh_doc(_ghdoc):
    ''' Switches the sc.doc to the Rhino Active Doc temporarily yeah science!'''
    if not _ghdoc:
        return

    try:
        sc.doc = Rhino.RhinoDoc.ActiveDoc
        yield
    finally:
        sc.doc = _ghdoc
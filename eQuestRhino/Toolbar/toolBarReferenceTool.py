"""
This one is a reference template for toolbar functions and layout ect.
The documentation on Rhino Eto dialog is kind of sparse: https://developer.rhino3d.com/guides/rhinopython/eto-forms-python/

As is with lots of my stuff: hugely referenced https://github.com/PH-Tools
Big shout out to Jedi Master EM as always: for continual mentorship, sharing of experience and knowledge.
-

What do:  

    For running this script: in the Rhino command line: RunPython... enter: select folder path: select this script.

TF March 2021
"""


import rhinoscriptsyntax as rs
import Eto
import Rhino
import json
from collections import defaultdict
from System import Array
from System.IO import File
import System.Windows.Forms.DialogResult
import System.Drawing.Image
import os
import random
from shutil import copyfile
import clr
clr.AddReferenceByName('Microsoft.Office.Interop.Excel, Culture=neutral, PublicKeyToken=71e9bce111e9429c')
from Microsoft.Office.Interop import Excel
import re
from contextlib import contextmanager
from System.Runtime.InteropServices import Marshal
import gc
import unicodedata


class Dialog_WindowExample(Eto.forms.Dialog):
    """ Jedi Master EM may be dissapointed but lets just use one class for the moment instead of MVC ect.
        This dialog class will encompass the view, model and controller aspects hopefully simply
    """

    def __init__(self, _exgValOne): 
        # Window Title  Variables/Properties                         
        self.Title = 'Example Title'
        self.Resizeable = False

        #Group Title Variables/Properties
        self.groupLabelOne = Eto.Forms.Label(Text= 'Group One')
        self.groupOneTextBox = Eto.Forms.TextBox(Text = str(_exgValOne))

        # Window Title  Variables/Properties? I think. We shall see lol
        self.Button_OK = Eto.Forms.Button(Text='OK')
        self.Button_OK.Click += self.onOKButtonClick

        self.Button_Cancel = Eto.Forms.Button(Text='Cancel')
        self.Button_Cancel.Click += self.onCancelButtonClick

    # Layout stuff
        # The Dynamic layout is a virtual grid that can organized controls both vertically and horizontally
        # For more information on Eto Layouts see: https://developer.rhino3d.com/guides/rhinopython/eto-layouts-python/
        self.layout = Eto.Forms.DynamicLayout()
        #sets the horizontal spacing and vertical spacing of the controls to 5 pixels between the controls.
        self.layout.Spacing = Eto.Drawing.size(10,10)
        
        # Main Group Box Box can have other boxes in it ect
        self.groupbox_Main = Eto.Forms.GroupBox(Text = 'MainGroupBoxText')
        self.layout_Group_Main = Eto.Forms.DynamicLayout()
        # Main Group Box Layout Inputs
        self.layout_Group_Main.Padding = Eto.Drawing.Padding(20)
        self.layout_Group_Main.Spacing = Eto.Drawing.Size(10,10)
        self.layout_Group_Main.AddRow(self.groupLabelOne, self.groupOneTextBox)
        self.layout_Group_Main.AddRow(self.Button_OK, self.Button_Cancel)
        # Pack the content into the window
        self.groupbox_Main.Content = self.layout_Group_Main
        self.layout.Add(self.groupbox_Main)

        self.Content = self.layout


# Gets user input from groupOneTextBox
    def GetUserInput1(self):
        grp1TxtInput = self.groupOneTextBox.Text
        return grp1TxtInput
# Canx Button functions    
    def OnCancelButtonClick(self, sender, e):
        print 'Canceled.....' #Prints in Rhino Command Line 
        self.Update = False  # any inputs are not applied 
        self.Close()   # Closes the Dialog
# OK Button functions
    def onOKButtonClick(self, sender, e):
        print 'Applying user input!'
        self.Update = True
        self.Close()

    def GetUpdateStatus(self):
        return self.Update

# We use the 'User Text' as the Data Method for applying/retrieving the user input on the Rhino side and pull it
# into the grasshopper side of things https://developer.rhino3d.com/api/rhinoscript/user_data_methods/user_data_methods.htm

# Get attrs if the selected object already has them
# Reference: https://github.com/PH-Tools/LBT-2-PH PHPP_SetSurfaceParams_cmd.py

    

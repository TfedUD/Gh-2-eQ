"""
Sets and allows editing of bldg/space type libraries
"""
import Rhino
import rhinoscriptsyntax as rs
import Eto
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







class Dialog_WindowProperties(Eto.Forms.Dialog):
    """ Toolbar Dialog window to allow for the selection of workbooks for space types and activities.
    and the editing of the related properties
    """
    
    def getActivityType(self):
        return [
            'placeholder will make libs for typology'
        ]
    
    def __init__(self, _exgName):
        self.Title = 'BR+A eQuest Room Properties'
        self.Resizeable = False

        self.roomNameLabel = Eto.Forms.Label(Text= 'Room Name')
        self.roomNameTextBox = Eto.Forms.TextBox( Text = str(_exgName))
        #self.activityTypeLable = Eto.Forms.Label(Text = 'ActvType')
        #self.activityTypeTextBox = Eto.Forms.TextBox( text = str(_exgActType))

        self.Button_OK = Eto.Forms.Button(Text = 'OK')
        self.Button_OK.Click += self.onOKButtonClick
        self.Button_Cancel = Eto.Forms.Button(Text= 'Cancel')
        self.Button_Cancel.Click += self.OnCancelButtonClick

        self.layout = Eto.Forms.DynamicLayout()

        self.layout.Spacing = Eto.Drawing.Size(10,10)
        self.layout.Padding = Eto.Drawing.Padding(15)

        self.groupbox_Main = Eto.Forms.GroupBox(Text = 'Room Information')
        self.layout_Group_Main = Eto.Forms.DynamicLayout()

        self.layout_Group_Main.Padding = Eto.Drawing.Padding(20)
        self.layout_Group_Main.Spacing = Eto.Drawing.Size(10,10)
        self.layout_Group_Main.AddRow(self.roomNameLabel, self.roomNameTextBox)
        self.layout_Group_Main.AddRow(self.Button_OK, self.Button_Cancel)

        self.groupbox_Main.Content = self.layout_Group_Main
        self.layout.Add(self.groupbox_Main)

        self.Content = self.layout

    def GetUserInput(self):
        name = self.roomNameTextBox.Text
        return name

    def OnCancelButtonClick(self, sender, e):
        print 'Canceled...'
        self.Update = False
        self.Close()

    def onOKButtonClick(self, sender, e):
        print 'Applying attrs to selected polygon'
        self.Update = True
        self.Close()
    
    def GetUpdateStatus(self):
        return self.Update

def getAttrs(_in, _key):
    results = []
    for each in _in:
        if _key == 'Object Name':
            results.append(rs.ObjectName(each))
        
        else:

            if rs.IsUserText(each):
                for eachKey in rs.GetUserText(each):
                    if _key in eachKey:
                        results.append(rs.GetUserText(each, _key))
                        break
    
    if len(set(results))>1:
        return '<varies>'
    

def setAttrs(_obj, _key, _val):
    if _val != '<varies>':
        rs.SetUserText(_obj, _key, _val)

def RunCommand( is_interactive ):
    # Get existing props
    name_Exg = getAttrs( rs.SelectedObjects(), 'Object Name')

    dialog = Dialog_WindowProperties( name_Exg)
    rc = dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
    name_New = dialog.GetUserInput()

    try:
        update = dialog.GetUpdateStatus()
    except:
        update = False

    if update==True:
        for eachObj in rs.SelectedObjects():

            rs.SetUserText(eachObj, 'Object Name', '%<ObjectName("{}")>%'.format( str(eachObj) ) )
            if 'varies' not in str(name_New): rs.ObjectName(eachObj, name_New)

    return 0

RunCommand(True)

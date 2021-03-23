"""
Sets and allows editing of bldg/space type libraries

Jedi Master EM's PHPP_EditComponoentLibrary == Majorly the basis of this module
https://github.com/PH-Tools/LBT-2-PH

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






class Model:

    def __init__(self, selObjs):
        self.selectedObjs = selObjs
        self.GroupContent = self.setGroupContent()
        self.setInitialGroupData()

    def setInitialGroupData(self):
        for grp in self.GroupContent:
            grp.getDocumentLibraryExgValues()

    def updateGroupData(self, _data):
        for grp in self.GroupContent:
            grp.updateGroupData( [v['Data'] for v in _data.values() if grp.LibType == v['LibType']] )
    
    def addBlankRowToGroupData(self, _grID):
        for gr in self.GroupContent:
            if gr.Name == _grID:
                gr.addBlankRowToData()
    
    def _clearDocumentLibValues(self, _keys):
        if not rs.IsDocumentUserText():
            return
        
        for eachKey in rs.GetDocumentUserText():
            for k in _keys:
                if k in eachKey:
                    rs.SetDocumentUserText(eachKey)

    def setDocumentLibValues(self, _data):
#out with the old
        keys = set()
        for v in _data.values():
            keys.add(v['LibType'])
        self._clearDocumentLibValues( list(keys))
#in with the new: Adding in values from the GridView Window
        for k, v in _data.items():
            idNum = self._idAsInt(v['Data']['ID'])
            key = "{}_{:02d}".format( v['Libtype'], idNum )
            rs.SetDocumentUserText(key, json.dumps(v['Data']))

    def _idAsInt(self, _in):
        try:
            return int(_in)
        except:
            print 'ID was not Int?? Enter Valid ID number'
            return 1
    
    def setGroupContent(self):

        gr1 = Group()
        gr1.Name ='Space Properties'
        # Grid order \n'd allows it to be collapseable
        gr1.ViewOrder = [
            'ID',
            'Space Name',
            'Activity', 
            'OCC-Schg', 
            'Lighting Schg', 
            'Equip Schg', 
            'EDP W/SF', 
            'LPD W/SF', 
            'Occ/SF', 
            'Min-Flow-x:y', 
            'Min-Flow/SF', 
            'Design Heat tmp', 
            'Heat Temp Schg', 
            'Dsg Cool tmp', 
            'Cool tmp schg'
                         ]
        gr1.LibType = 'eQuest_Space_Attrs'
        gr1.Editable = [
            False,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
                    ]
        gr1.ColType = [
            'int',
            'str',
            'str',
            'str',
            'str',
            'str',
            'float',
            'float',
            'float',
            'str',
            'float',
            'float',
            'str',
            'float',
            'float'
                    ]
        gr1.getBlankRow()
        gr1.getDocumentLibraryExgValues()

        return [gr1]

    def removeRow(self, _grID, _rowID):
        for gr in self.GroupContent:
            if gr.Name == _grID:
                gr.removeRow(_rowID)

    def getSpaceAttrLibAdress(self):
        if rs.IsDocumentUserText():
            return rs.GetDocumentUserText('eQ_Spc_Attr_Lib')
        else:
            return '...'
    
    def setLibraryFileAdress(self):
        """Opens a dialogue window so the user can select the workbook
        """
        fd = Rhino.UI.OpenFileDialog()
        fd.Filter = "Excel FIles (*.xlsx;*.xls)|*.xlsx'*.xls"
        #-------------------------------------
        # Going to be fancy like Jedi Master EM and add a warning before proceeding
        # https://developer.rhino3d.com/api/rhinoscript/user_interface_methods/messagebox.htm
        msg = "Loading space attributes from a fill will overwrite all "\
            "The Current Library Values in the Current Rhino File"\
            "HIGHLY RECCOMEND SAVE AS: BEFORE PROCEEDING IF THE CURRENT LIB"\
            "IF YOU ARE NOT COMPLETELY CERTAIN THAT THIS IS THE WAY"
        proceed = rs.MessageBox(msg, 1 | 48, 'Warning')
        if proceed ==2:
            return fd.FileName

    @contextmanager
    def readingFromExcel(self, _lib_path):
        """Context manager for handling open / close / cleanup for Excel App"""
        # OG Ref: https://github.com/PH-Tools/LBT-2-PH
        #Ref: https://stackoverflow.com/questions/158706/how-do-i-properly-clean-up-excel-interop-objects
        #Ref: https://devblogs.microsoft.com/visualstudio/marshal-releasecomobject-considered-dangerous/
        try:
            # make temp copy
            #----------------------------------------------------------------
            self.saveDir = os.path.split(_lib_path)[0]
            self.tempFile = '{}_temp.xlsx'.format(random.randint(0,1000))
            self.tempFilePath = os.path.join(self.saveDir, self.tempFile)
            copyfile(_lib_path, self.tempFilePath)
            # Read from
            self.ex = Excel.ApplicationClass()
            self.ex.Visible = False
            self.ex.DisplayAlerts = False
            self.workbook = self.ex.Workbooks.Open(self.tempFilePath)
            self.worksheets = self.workbook.Worksheets
            yield
        except:
            self.workbook.Close()
            self.ex.Quit()
            self.ex = None
            gc.collect()
            os.remove(self.tempFilePath)
        finally:
            self.workbook.close()
            self.ex.Quit()
            self.ex = None
            gc.collect()
            os.remove(self.tempFilePath)
    
    def readRoomAttrsFromExcel(self):
        if rs.IsDocumentUserText():
            libpath = rs.GetDocumentUserText('eQ_Spc_Attr_Lib')
        try:
            if libpath==None:
                return []
            
            if not os.path.exists(libPath):
                return []
            
            #-------------------------------
            print 'Reading the main Room model attr workbook....beepBoopBeep'
            with self.readingFromExcel(libPath):
                try:
                    wsSpaces = self.worksheets['Space']

        
    













RunCommand(True)

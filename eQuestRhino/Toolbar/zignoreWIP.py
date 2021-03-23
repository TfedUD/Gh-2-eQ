import Rhino
import scriptcontext as sc
import System
import rhinoscriptsyntax as rs 
import Eto
import re



class Dialog_WindowExample(Eto.Forms.Dialog):
    """Inhereting Eto.Forms.Dialog as above: really makes Eto write like PysimpleGui and tkinter and stuff I feel like.
    Work in progress: does not run right   time != plentiful 
    """
      
    def __init__(self, _exgUserText):
        self.Title = 'New toolbar WIP'
        self.Resizeable = False

        #----------------------------------------------------------------
        # Text Box and shit
        self.textBoxLabel = Eto.Forms.Label(Text='Text Box!')
        self.textBoxTextBox = Eto.Forms.TextBox( Text=str(_exgUserText))

        #----------------------------------------------------------------
        # Buttons and shit
        self.Button_OK = Eto.Forms.Button(Text='OK')
        self.Button_OK.Click += self.onOKButtonClick
        self.Button_Cancel = Eto.Forms.Button(Text='Cancel')
        self.Button_Cancel.Click += self.onCancelButtonClick

        #----------------------------------------------------------------
        # Layout and shit
        # some refs: https://github.com/picoe/Eto/wiki/DynamicLayout
        self.layout = Eto.Forms.DynamicLayout()#Parent window if I am not mistaken
        self.layout.Spacing = Eto.Drawing.Size(10,10)
        self.layout.Padding = Eto.Drawing.Padding(15)
        #----------------------------------------------------------------
        # Add in groups and organize as ye please
        self.groupbox_Main = Eto.Forms.GroupBox(Text='This is where this label goes')

        self.layout_group_main = Eto.Forms.DynamicLayout()
        self.layout_group_main.Padding = Eto.Drawing.Padding(20)
        self.layout_group_main.Spacing = Eto.Drawing.Size(10,10)
        #-----------------------------------
        # Bring in our buttons and textboxes and stuff to the group_main
        self.layout_group_main.AddRow(self.textBoxLabel, self.textBoxTextBox)
        self.layout_group_main.AddRow(self.Button_OK, self.Button_Cancel)
        #-----------------------------------
        # kinda like .pack() in tkinter but a little more organized: and not to bad yea?
        self.groupbox_main.Content = self.layout_group_main
        self.layout.Add(self.groupbox_main)
        #--------------------------------------------------------------
        # and our closing statement
        self.Content = self.layout

        #------------------------------
        # thing dooers
        def GetUserInput(self):
            usrTxt = self.textBoxTextBox.Text
            return usrTxt
        
        def onOKButtonClick(self, sender, e):
            print 'You pressed OK'
            self.Update = False
            self.Close()

        def onCancelButtonClick(self, sender, e):
            print 'Canceled' # text will appear in the Rhino cmd line
            self.Update = False
            self.Close()

        

def RunCommand( is_interactive ):
    exgUserText = None
    dialog = Dialog_WindowExample(exgUserText)
    rc = dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)

            

RunCommand(True)
            














from fileBldr import eQfloor as eqf
import os
import itertools




class InpFile(eqf):
    topLevel = 'INPUT ..\n\n\n\n'
    spacer = '\n\n'
    dby = '$ ---------------------------------------------------------\n'
    abortDiag = dby+'$              Abort, Diagnostics\n'+dby+spacer
    globalParam = dby+'$              Global Parameters\n'+dby+spacer
    comply = dby+'$              Compliance Data\n'+dby+spacer
    siteBldg = dby+'$              Site and Building Data\n'+dby+spacer
    matslayers = dby+'$              Materials / Layers / Constructions\n'+dby+spacer
    glzCode = dby+'$              Glass Type Codes\n'+dby+spacer
    glzTyp = dby+'$              Glass Types\n'+dby+spacer
    WindowLayers = dby+'$              Window Layers\n'+dby+spacer
    iLikeLamp = dby+'$              Lamps / Luminaries / Lighting Systems\n'+dby+spacer
    daySch = dby+'$              Day Schedules\n'+dby+spacer
    weekSch = dby+'$              Week Schedules\n'+dby+spacer
    annualSch = dby+'$              Annual Schedules\n'+dby+spacer
    polygons = dby+'$              Polygons\n'+dby+spacer
    wallParams = dby+'$              Wall Parameters\n'+dby+spacer
    fixBldgShade = dby+'$              Fixed and Building Shades\n'+dby+spacer
    miscCost = dby+'$              Misc Cost Related Objects\n'+dby+spacer

    starmoney = '$ *********************************************************\n'
    starBlnk = '$ **                                                     **\n'

    perfCurve = starmoney+starBlnk+'$ **                Performance Curves                   **\n'\
        +starBlnk+starmoney+spacer
    floorNspace = starmoney+starBlnk+'$ **      Floors / Spaces / Walls / Windows / Doors      **\n'\
        +starBlnk+starmoney+spacer
    elecFuelMeter = starmoney+starBlnk+'$ **              Electric & Fuel Meters                 **\n'\
        +starBlnk+starmoney+spacer

    elecMeter = dby+'$              Electric Meters\n'+dby+spacer
    fuelMeter = dby+'$              Fuel Meters\n'+dby+spacer
    masterMeter = dby+'$              Master Meters\n'+dby+spacer

    hvacCircLoop = starmoney+starBlnk+'$ **      HVAC Circulation Loops / Plant Equipment       **\n'\
        +starBlnk+starmoney+spacer
    
    pumps = dby+'$              Pumps\n'+dby+spacer
    heatExch = dby+'$              Heat Exchangers\n'+dby+spacer
    circLoop = dby+'$              Circulation Loops\n'+dby+spacer
    chillyboi = dby+'$              Chillers\n'+dby+spacer
    boilyboi = dby+'$              Boilers\n'+dby+spacer
    dwh = dby+'$              Domestic Water Heaters\n'+dby+spacer
    heatReject = dby+'$              Heat Rejection\n'+dby+spacer #allAmericanHeatRejects
    towerFree = dby+'$              Tower Free Cooling\n'+dby+spacer
    pvmod = dby+'$              Photovoltaic Modules\n'+dby+spacer
    elecgen = dby+'$              Electric Generators\n'+dby+spacer
    thermalStore = dby+'$              Thermal Storage\n'+dby+spacer
    groundLoopHx = dby+'$              Ground Loop Heat Exchangers\n'+dby+spacer
    compDhwRes = dby+'$              Compliance DHW (residential dwelling units)\n'+dby+spacer

    steamAndcldMtr = starmoney+starBlnk+'$ **            Steam & Chilled Water Meters             **\n'\
        +starBlnk+starmoney+spacer

    steamMtr = dby+'$              Steam Meters\n'+dby+spacer
    chillMeter = dby+'$              Chilled Water Meters\n'+dby+spacer

    hvacSysNzone = starmoney+starBlnk+'$ **               HVAC Systems / Zones                  **\n'\
        +starBlnk+starmoney+spacer
    
    miscNmeterHvac = starmoney+starBlnk+'$ **                Metering & Misc HVAC                 **\n'\
        +starBlnk+starmoney+spacer
    
    equipControls = dby+'$              Equipment Controls\n'+dby+spacer
    loadManage = dby+'$              Load Management\n'+dby+spacer

    UtilRate = starmoney+starBlnk+'$ **                    Utility Rates                    **\n'\
        +starBlnk+starmoney+spacer
    
    ratchets = dby+'$              Ratchets\n'+dby+spacer
    blockCharge = dby+'$              Block Charges\n'+dby+spacer
    utilRate = dby+'$              Utility Rates\n'+dby+spacer

    outputReporting = starmoney+starBlnk+'$ **                 Output Reporting                    **\n'\
        +starBlnk+starmoney+spacer

    loadsNonHr = dby+'$              Loads Non-Hourly Reporting\n'+dby+spacer
    sysNonHr = dby+'$              Systems Non-Hourly Reporting\n'+dby+spacer
    plntNonHr = dby+'$              Plant Non-Hourly Reporting\n'+dby+spacer
    econNonHr = dby+'$              Economics Non-Hourly Reporting\n'+dby+spacer
    hourlyRep = dby+'$              Hourly Reporting\n'+dby+spacer

    theEnd = dby+'$              THE END\n'+dby+'\nEND ..\nCOMPUTE ..\nSTOP ..\n'



    def __init__(self, _ttB, floors=[], **kwargs):#Floor Object in entierety


        self.ttb = _ttB

        self._floors = []
        for floor in floors:
            self.add_flr(floor)

        for k, v in kwargs.items():
            setattr(self,k,v)

        self._floors = []
        for floor in floors:
            self.add_flr(floor)
        
        self._flr_polystr = []
        for floor in floors:
            self.add_flrPly(floor)
        
        self._flr_space = []
        for floor in floors:
            self.add_flrSpace(floor)

        self._flr_zone = []
        for floor in floors:
            self.add_zone(floor)

        

# --------------------------------------------------------------
    def add_zone(self, obj):
        self._flr_zone.append(obj.floor_zone_strs)
#----------------------------------------------------------------   
    def add_flrPly(self, obj):
       self._flr_polystr.append(obj.floor_poly_strs)


#----------------------------------------------------------------
    def add_flrSpace(self, obj):
        self._flr_space.append(obj.floor_space_strs)

#----------------------------------------------------------------
# I think we can leave the next block out
    def add_flr(self, obj):
        self._floors.append(obj)
    @property
    def flors(self):
        return(self._floors)
# ----------------------------------------------------------------

################################################################
### Do for all _incoming floor properties to write to inp
############## EACH PROPERTY RETURNS THE HEADER AND COMBINED INP OBJECTS
############## BY FLOOR IN ORDER.... MAY NEED TO ADD STUFF TO MAKE SURE ITS IN ORDER
############## TO BE CONTINUED

    @property
    def floor_inp_poly(self):
        """ Returns the *.inp formatted polygon block from all floor objects """
        return(self._inp_polyfill(self._flr_polystr, self.polygons))

    @staticmethod
    def _inp_polyfill(obj,ply):
        """Combines the floor{spaces} inp objects and stacks them toogether"""
        goods = [x for n in obj for x in n]
        strang = ''.join(i for i in goods)
        block = ply+strang
        return  block

    @property
    def floor_inp_space(self):
        """ Returns the *.inp formatted spaces block from all floor objects """
        return(self._inp_spacefill(self._flr_space, self.floorNspace))
    
    @staticmethod
    def _inp_spacefill(obj,spc):
        """Combines the floor{spaces} inp objects and stacks them toogether"""
        goods = [x for n in obj for x in n]
        strang = ''.join(i for i in goods)
        block = spc+strang
        return block

    @property
    def floor_inp_zone(self):
        return(self._inp_zonefill(self._flr_zone, self.hvacSysNzone))

    @staticmethod
    def _inp_zonefill(obj,zn):
        goods = [x for n in obj for x in n]
        strang = ''.join(i for i in goods)
        block = zn+strang
        return block
################################# The INP file  kinda chaos but it'l work for now ##########################

    def __str__(self):
        allTheThings =[self.topLevel, self.abortDiag, self.globalParam,self.ttb, self.comply,
                        self.siteBldg, self.matslayers, self.glzCode, self.glzTyp,
                        self.WindowLayers, self.iLikeLamp, self.daySch, self.weekSch,
                        self.annualSch, self.floor_inp_poly, self.wallParams, self.fixBldgShade,
                        self.miscCost, self.perfCurve, self.floor_inp_space, self.elecFuelMeter,
                        self.elecMeter, self.fuelMeter, self.masterMeter, self.hvacCircLoop, 
                        self.pumps, self.heatExch, self.circLoop, self.chillyboi, self.boilyboi,
                        self.dwh, self.heatReject, self.towerFree, self.pvmod, self.elecgen,
                        self.thermalStore, self.groundLoopHx, self.compDhwRes, self.steamAndcldMtr,
                        self.steamMtr, self.chillMeter, self.floor_inp_zone, self.miscNmeterHvac,
                        self.equipControls, self.loadManage, self.UtilRate, self.ratchets, 
                        self.blockCharge, self.utilRate, self.outputReporting, self.loadsNonHr,
                        self.sysNonHr, self.plntNonHr, self.econNonHr, self.hourlyRep,
                        self.theEnd
                        ]
        runningLowOnVarNames = '\n'.join(i for i in allTheThings)  #will this fix it

        return(runningLowOnVarNames)






    
################################################################



   
    # Do @property w/ static method for each set of inp_string:
    # Create additional @prop with staticmethod to be used as the .inpfileContents to write out 


    # NO DO KWARGS! can we do kwargs with all those vars? prolly have to put em all in there
    # somewhere
    

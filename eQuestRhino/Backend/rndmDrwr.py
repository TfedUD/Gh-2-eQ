"""
This was going to be the random drawer but it turned into making each block in *.inp into a class
Kinda crunchy. but will be improved upon. 
Ed if you are seeing this: plz refer to: https://images-cdn.9gag.com/photo/a8GpvLd_700b.jpg
"""

class Hdr:
    """Create block title.
    Use example: Hdr('Abort, Diagnostics')
    """
    def __init__(self, cmnts):
        self.cmnts = cmnts
        dby = '$ '+'-'*57

    @property
    def hdBlk(self):
        """x = Hdr('Abort, Diagnostics').hdBlk
        """
        return dby+'\n'+'$'+' '*13+'{}\n'.format(self.cmnts)+dby+'\n'

    ###
class GlblParams:
    """y = GlblParams('OA_adj', '1.25')
    """
    def __init__(self, prm, prmval):
        self.prm = prm
        self.prmval = prmval
        
    @property
    def ttHdr(self):
        return Hdr('Global Parameters').hdBlk+'\n'
    @property
    def parameter(self):
        return 'PARAMETER\n'+'   '+'"{}"'.format(self.prm)+' '*(16-len(self.prm))+'={}'.format(self.prmval)+'  ..'
        
    ###

class TitleRP:
    """Use: Title, Run Periods, DD, HD blocks of inp
    Examp: qwe = TitleRP('BIDMC','Proposed Design', 'Construction Documents', 'Entire Year', 1, 1, 2018, 12, 31, 2018, 'HDD BOSTON 99.6%', 8.1, 'CDD BOSTON 1%', 87.6, 14.9, 71.7)
    """
    def __init__(self, prjNm, blpp, prjphs, rP, bM, bD, bY, eM, eD, eY, hdD, hddTmp, cdD, cddH, cddR, cdwbH):
        self.prjNm = prjNm
        self.blpp = blpp
        self.prjphs = prjphs
        self.rP = rP
        self.bM = bM
        self.bD = bD
        self.bY = bY
        self.eM = eM
        self.eD = eD
        self.eY = eY
        self.hdD = hdD
        self.hddTmp = hddTmp
        self.cdD = cdD
        self.cddH = cddH
        self.cddR = cddR
        self.cdwbH = cdwbH

    @property
    def ttHdr(self):
        return Hdr('Title, Run Periods, Design Days, Holidays').hdBlk
    @property
    def ttB(self):
        return '\nTITLE\n   LINE-1'+' '*10+'= *{}*'.format(self.prjNm)+'\n   LINE-2'+' '*10+'= *{}*'.format(self.blpp)+'\n   LINE-3'+' '*10+'= *{}*'.format(self.prjphs)+'\n   ..\n\n'
    @property
    def runP(self):
        return '"{}" = RUN-PERIOD-PD'.format(self.rP)+'\n   BEGIN-MONTH'+' '*(10-len('month'))+'= {}'.format(self.bM)+'\n   BEGIN-DAY'+' '*(10-len('day'))+'= {}'.format(self.bD)+'\n   BEGIN-YEAR'+' '*(10-len('year'))+'= {}'.format(self.bY)+'\n   END-MONTH'+' '*(12-len('month'))+'= {}'.format(self.eM)+'\n   END-DAY'+' '*(12-len('day'))+'= {}'.format(self.eD)+'\n   END-YEAR'+' '*(12-len('year'))+'= {}'.format(self.eY)+'\n   ..\n\n'
    @property
    def hcDD(self):
        return '"{}"'.format(self.hdD)+'= DESIGN-DAY\n   TYPE'+' '*13+'= HEATING\n   DRYBULB-HIGH'+' '*5+'= {}\n   ..'.format(self.hddTmp)+'\n"{}"'.format(self.cdD)+'= DESIGN-DAY\n   TYPE'+' '*13+'= COOLING\n   DRYBULB-HIGH'+' '*5+'= {}'.format(self.cddH)+'\n   DRYBULB-RANGE    ={}'.format(self.cddR)+'\n   WETBULB-AT-HIGH  {}'.format(self.cdwbH)+'\n   ..\n'
    @property
    def hldyBlk(self):
        return '\n"Standard US Holidays" = HOLIDAYS\n   LIBRARY-ENTRY "US"\n   ..\n\n'

    ###

class compDat:
    """placeholder / maker of compliance data required block
    exmp: x = compDat()
    print(x.cmphB)
    """
    def __init__(self):
        self == self
        
    @property
    def cmphB(self):
        return Hdr('Compliance Data').hdBlk

    ###

class SiteBuldingData:
    """site and building data block
    kjh = SiteBuldingData(-45)
    print(kjh.sbdHdr+kjh.stprms)
    """
    
    def __init__(self, azmt):
        self.azmt = azmt
        
    @property
    def sbdHdr(self):
        return Hdr('Compliance Data').hdBlk + '\n\n'
    @property
    def stprms(self):
        return '"Site Data" = SITE-PARAMETERS\n   ..\n\n"Building Data" = BUILD-PARAMETERS\n  AZIMUTH'+' '*10+'= {}\n'.format(self.azmt)+'  HOLIDAYS'+' '*8+'= "Standard US Holidays"\n   ..\n\n\nPROJECT-DATA\n   ..'




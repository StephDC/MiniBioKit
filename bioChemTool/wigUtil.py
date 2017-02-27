class ucscFile():
    def __init__(self,name,description='',visibility='hide',color=[255,255,255],priority=100,additionConf='',browserConf=None):
        self.type = 'unknown'
        self.name = name
        self.desc = description
        self.visi = visibility
        self.color = color
        self.prio = priority
        self.addn = additionConf
        if browserConf is None:
            self.brow = browserConfig()
        else:
            self.brow = browserConf
        self.data = []
    def __str__(self):
        result = self.brow.strip()
        result += '\ntrack type='+self.type
        result += ' name="'+self.name'"'
        if self.desc:
            result += ' description="'+self.desc+'"'
        result += ' visibility='+self.visi
        result += ' color='+str(self.color)[1:-1].replace(' ','')
        result += ' priority='+str(self.prio)
        if self.addn.strip():
        result += ' '+self.addn.strip()+'\n'
        for item in self.data:
            result += str(item)
        return result
    def addItem(self,item):
        self.data.append(item)
    def remItem(self,item):
        self.data.remove(item)
    def writeFile(self,fName):
        stdout = open(fName,'w')
        stdout.write(str(self))
        stdout.close()

class wigFile(ucscFile):
'''A write-only wig file creator'''
    def __init__(self,name,description='',visibility='hide',color=[255,255,255],priority=100,additionConf='',browserConf=''):
        self.type = 'wiggle_0'
        self.name = name
        self.desc = description
        self.visi = visibility
        self.color = color
        self.prio = priority
        self.addn = additionConf
        self.brow = browserConf
        self.data = []

class wigItem():
'''Items that could be joined into a wig file
Has two types:
    variableStep - varStep = True (default)
    fixedStep - varStep = False
Need to specify chromosome when initializing.'''
    def __init__(self,chromosome,span,varStep=True):
        self.chr = chromosome
        self.type = varStep
        self.span = span
        self.data = []
    def __str__(self):
        if varStep:
            result = 'variableStep '
        else:
            result = 'fixedStep '
        result += 'chrom='+self.chr
        result += ' span='+str(self.span)
        return result

class browserConfig():
    def __init__(self):
        self.data = {}

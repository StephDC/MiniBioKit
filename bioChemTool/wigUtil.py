class equalDict(dict):
    def __str__(self):
        result = ''
        for item in self.keys():
            if self[item] is not None:
                result += item+'='+self[item]+' '
        return result[:-1]

class spaceList(list):
    def __str__(self):
        result = ''
        for item in self:
            result+=str(item)+' '
        return result[:-1]

class ucscFile():
    '''Universal file structure for UCSC Genome Sequence files including wig
        and '''
    def __init__(self,name,description='',visibility='hide',color='255,255,255',priority='100',additionConf='',browserConf=None):
        self.config = equalDict()
        self.config['type'] = 'unknown'
        self.config['name'] = name
        self.config['description'] = description
        self.config['visibility'] = visibility
        self.config['color'] = color
        self.config['priority'] = priority
        self.addn = additionConf
        if browserConf is None:
            self.brow = equalDict()
        else:
            self.brow = browserConf
        self.data = []
    def __str__(self):
        result = str(self.brow) if self.brow else ''
        result += '\ntrack '
        result += str(self.config)
        if self.addn.strip():
            result += ' '+self.addn.strip()
        result += '\n'
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
    def __init__(self,name,description='',visibility='hide',color='255,255,255',priority='100',additionConf='',browserConf=''):
        self.config = equalDict()
        self.config['type'] = 'wiggle_0'
        self.config['name'] = name
        self.config['description'] = description
        self.config['visibility'] = visibility
        self.config['color'] = color
        self.config['priority'] = priority
        self.addn = additionConf
        self.brow = browserConf
        self.data = []

class wigItem():
    '''Items that could be joined into a wig file
Has two types:
    variableStep - varStep = True (default)
    fixedStep - varStep = False
Need to specify chromosome when initializing.'''
    def __init__(self,chromosome,span,varStep=True,start=None):
        self.chr = chromosome
        self.type = varStep
        self.start = start
        if not varStep and not start:
            raise SyntaxError('fixedStep requires start position.')
        self.span = span
        self.data = []
    def __str__(self):
        if self.type:
            result = 'variableStep '
        else:
            result = 'fixedStep '
        result += 'chrom='+self.chr
        if self.type:
            if self.span:
                result += ' span='+str(self.span)
            result += '\n'
        else:
            result += ' start='+str(self.start)
            result += ' step='+str(self.span)
        for item in self.data:
            result += str(item)+'\n'
        return result
    def __getitem__(self,key):
        return self.data[key]
    def __setitem__(self,key,item):
        self.data[key] = item
    def __iter__(self):
        return self.data.__iter__()
    def append(self,item):
        self.data.append(item)
    def pop(self):
        return self.data.pop()



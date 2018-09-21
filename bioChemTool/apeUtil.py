from . import commonUtil
import math

class apeFile():
    '''The class of apeFile to interact with the filesystem'''
    def __init__(self,fName,load=True):
        self.fName = fName
        self.data = None
        if load:
            stdin = open(fName,'r')
            self.data = parseApeFile(stdin)
            stdin.close()
    def write(self,outFile=None):
        fName = outFile if outFile else self.fName
        stdout = open(fName,'w')
        stdout.write('\n'.join([str(i) for i in self.data]))
        stdout.close()
    def __getitem__(self,key):
        result = self.get(key)
        if result is None:
            raise KeyError(key)
        return result
    def keys(self):
        result = set()
        for item in self.data:
            result.add(item.nombre)
        return result
    def get(self,key):
        result = self.getall(key)
        return result[0] if result else None
    def getall(self,key):
        result = []
        for item in self.data:
            if item.nombre == key.upper():
                result.append(item)
        return result

class apeData():
    '''The class of apeData to store the ApE Data in a file'''
    def __init__(self,nombre,data):
        self.nombre = nombre
        self.data = data
    def __str__(self):
        return self.nombre+str(self.data)

class inlineList(list):
    def __str__(self):
        if len(self) == 0:
            return ''
        return '    '+'    '.join([str(i) for i in self])
#    def __repr__(self):
#        return str(self)
    def addData(self,data):
        self.append(data)
    
class lineList(list):
    def __str__(self):
        return '\n'.join([str(i) for i in self])
#    def __repr__(self):
#        return str(self)
    def addData(self,data):
        self.append(data)

class seqData():
    def __init__(self):
        self.data = ''
    def addData(self,data):
        tmp = data.split(' ')
        seqStart = False
        for item in tmp:
            if item.isdigit():
                seqStart = True
            elif seqStart and item.strip().isalpha():
                self.data += item
    def __str__(self):
        result = ''
        tmp = self.data
        numCount = 0
        numLen = '{:>'+str(math.ceil(math.log10(len(self.data))/8)*8)+'}'
        while tmp:
            if numCount % 6 == 0:
                result+='\n'+numLen.format(numCount*10+1)
            result += ' '+tmp[:10]
            numCount += 1
            tmp = tmp[10:]
        return result

class featureList():
    def __init__(self):
        self.data = []
    def addData(self,data):
        if data.strip().split(' ')[0] == 'misc_feature':
            for item in data.strip().split(' ')[1:]:
                if item:
                    if item[0] == 'c':
                        direct = False
                        location = [int(i) for i in item[11:-1].split('..')]
                    else:
                        direct = True
                        location = [int(i) for i in item.split('..')]
            self.data.append(featureItem('misc_feature',location,direct))
        else:
            self.data[-1].data.append(data)

class featureItem():
    def __init__(self, nombre, location, direction):
        self.nombre = nombre
        self.location = location
        self.direction = direction
        self.data = []

def parseApeFile(stdin):
    result = []
    lastItem = None
    for line in stdin:
        if line and line != '\n':
            if line[0] != ' ':
                result.append(lastItem)
                tmp = line.split(' ')
                itemType = tmp[0].strip()
                if itemType == 'ORIGIN':
                    itemData = seqData()
# TODO: Implement FEATURES
#               elif itemType == 'FEATURES':
#                   itemData = featureList()
                else:
                    itemData = lineList([inlineList([])])
                    for inlineItem in tmp[1:]:
                        if inlineItem.strip():
                            itemData[0].append(inlineItem.strip())
                lastItem = apeData(itemType,itemData)
            else:
                lastItem.data.addData(line[:-1])
    result.append(lastItem)
    return result[1:]

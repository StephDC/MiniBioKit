class SAMParseWarning(SyntaxError):
    def __init__(self,name,part):
        SyntaxError.__init__(self,'The '+name+' did not look like a '+name+'. '+part)

# Utilities for parsers
import sys
if sys.version[0] == '2':
    FileNotFoundError = IOError
def isIn(keys):
    #Useful to check for keys
    return lambda x: x in keys
def addList(key,val,stdout):
    if key in stdout:
        stdout[key].append(val)
    else:
        stdout[key] = [val]
def noverify(key):
    if key[0] in 'XYZ' or key in ['GC','GQ','GS','MF','SQ','S2']:
        return True
    else:
        return False
def bytesToInt(data):
    result = 0
    for i in reversed(bytearray(data)):
        result = result << 8
        result += i
    return result
# This is a dirty readLine that would attempt to read more.
def readLine(data,readLen=50):
    origPos = data.tell()
    more = data.read(readLen)
    while more.find(b'\x00') != -1:
        more += data.read(readLen)
    result = more[:more.index(b'\x00')]
    data.seek(origPos+len(result)+1)
    return result
def parseKey(name,key,val,stdout,part,valid=None,prefix='',append=False):
    if val.strip()[:2] == key:
        try:
            tmp = val[val.index(':')+1:].strip()
        except Exception:
            raise SAMParseWarning(part,prefix+'-'+key)
        else:
            if valid is None or valid(tmp):
                if append:
                    addList(name,tmp,stdout)
                else:
                    stdout[name] = tmp
            else:
                raise SAMParseWarning(part,prefix+'-'+key)

# Parsers
def parseHD(stdin,stdout):
    # Parse the file header line for version
    tmp = stdin.split('\t')
    if tmp[0].strip() != '@HD':
        raise SAMParseWarning('header','-HD')
    else:
        try: # As a safety measurement - maybe some index error would happen
            for item in tmp[1:]:
                if len(item.strip()) > 3:
                    parseKey('Version','VN',item,stdout,'header',prefix='HD')
                    parseKey('Sort','SO',item,stdout,'header',valid=isIn(['unknown','unsorted','queryname','coordinate']),prefix='HD')
                    parseKey('Group','GO',item,stdout,'header',valid=isIn(['none','query','reference']),prefix='HD')
            if 'Version' not in stdout:
                raise SAMParseWarning('header','HD-VN')
        except Exception as e:
            if type(e) is not SAMParseWarning:
                raise SAMParseWarning('header','-HD')
            else:
                raise
def parseSQ(stdin,stdout):
    tmp = stdin.split('\t')
    try:
        for item in tmp[1:]:
            if len(item.strip()) >3:
                parseKey('SeqNum','SN',item,stdout,'header',prefix='SQ',append=True)
                parseKey('SeqLen','LN',item,stdout,'header',prefix='SQ',append=True)
                parseKey('AltLocus','AH',item,stdout,'header',prefix='SQ',append=True)
                parseKey('Assembly','AS',item,stdout,'header',prefix='SQ',append=True)
                parseKey('HashM','M5',item,stdout,'header',prefix='SQ',append=True)
                parseKey('Species','SP',item,stdout,'header',prefix='SQ',append=True)
                parseKey('URI','UR',item,stdout,'header',prefix='SQ',append=True)
        if 'SeqNum' not in stdout:
            raise SAMParseWarning('header','SQ-SN')
        if 'SeqLen' not in stdout:
            raise SAMParseWarning('header','SQ-LN')
        if len(stdout['SeqNum']) != len(stdout['SeqLen']):
            raise SAMParseWarning('header','SQ-SN-LN')
    except Exception as e:
        if type(e) is not SAMParseWarning:
            raise SAMParseWarning('header','-SQ')
        else:
            raise
def parseRG(stdin,stdout):
    pass
def parsePG(stdin,stdout):
    tmp = stdin.split('\t')
    try:
        for item in tmp[1:]:
            if len(item.strip()) > 3:
                parseKey('ProgID','ID',item,stdout,'header',prefix='PG',append=True)
                parseKey('ProgName','PN',item,stdout,'header',prefix='PG',append=True)
                parseKey('Command','CL',item,stdout,'header',prefix='PG',append=True)
                if 'ProgID' in stdout:
                    parseKey('PrevProg','PP',item,stdout,'header',valid=isIn(stdout['ProgID']),prefix='PG',append=True)
                else:
                    parseKey('PrevProg','PP',item,stdout,'header',prefix='PG',append=True)
                parseKey('Description','DS',item,stdout,'header',prefix='PG',append=True)
                parseKey('ProgVer','VN',item,stdout,'header',prefix='PG',append=True)
        if 'ProgID' not in stdout:
            raise SAMParseWarning('header','PG-ID')
    except Exception as e:
        if type(e) is not SAMParseWarning:
            raise SAMParseWarning('header','-PG')
        else:
            raise
def parseCO(stdin,stdout):
    tmp = stdin[stdin.index(CO)+2].strip()
    addList('Comment',tmp,stdout)

def parseHeader(stdin,stdout):
    if len(stdin) < 9:
        raise SAMParseWarning('header','')
    tmp = stdin.split('\t')
    if tmp[0].strip() == '@HD':
        parseHD(stdin,stdout)
    elif tmp[0].strip() == '@SQ':
        parseSQ(stdin,stdout)
    elif tmp[0].strip() == '@RG':
        parseRG(stdin,stdout)
    elif tmp[0].strip() == '@PG':
        parsePG(stdin,stdout)
    elif tmp[0].strip() == '@CO':
        parseCO(stdin,stdout)
    else:
        raise SAMParseWarning('header',tmp[0].strip()[1:])
def parseOption(stdin):
    tagList = {
'AM':'i',
'AS':'i',
'BC':'Z',
'BQ':'Z',
'CC':'Z',
'CM':'i',
'CO':'Z',
'CP':'i',
'CQ':'Z',
'CS':'Z',
'CT':'Z',
'E2':'Z',
'FI':'i',
'FS':'Z',
'H0':'i',
'H1':'i',
'H2':'i',
'HI':'i',
'IH':'i',
'LB':'Z',
'MC':'Z',
'MD':'Z',
'MQ':'i',
'NH':'i',
'NM':'i',
'OC':'Z',
'OP':'i',
'OQ':'Z',
'PG':'Z',
'PQ':'i',
'PT':'Z',
'PU':'Z',
'QT':'Z',
'Q2':'Z',
'R2':'Z',
'RG':'Z',
'RT':'Z',
'SA':'Z',
'SM':'i',
'TC':'i',
'U2':'Z',
'UQ':'i'
}
    result = {}
    for item in stdin:
        if (noverify(item[:2]) or (item[:2] in tagList and item[3:4] == tagList[item[:2]])) and item[4]==':':
            result[item[:2]] = item[5:]
        else:
            raise SAMParseWarning('Option',item[:2])
    return result
def parseFlag(stdin):
    tmp = int(stdin)
    result = []
    fList = ['multiSegments','allProperlyAligned','segUnmapped','nextSegUnmapped',
        'seqRevComp','nextSeqRevComp','firstSeg','lastSeg','secondAlign','notPassFilters','PCROptDup','supAlign']
    for i in range(12):
        if bool((1<<i) & tmp):
            result.append(fList[i])
    return result
def parseData(stdin,flag=True):
    tmp = stdin.strip().split('\t')
    if len(tmp) < 11:
        raise SAMParseWarning('alignment','Data:\n'+stdin)
    result = {}
    keys = ['qName','Flag','rName','Pos','MapQ','Cigar','rNext','pNext','tLen','Seq','Qual']
    for item in range(11):
        result[keys[item]] = tmp[item].strip()
    if flag:
        result['Flag'] = parseFlag(result['Flag'])
    if len(tmp) > 11:
        result['Option'] = parseOption(tmp[11:])
    return result

# Class
class samIndex():
    def __init__(self,fName):
        self.fName = fName
        try:
            stdin = open(fName,'rb')
        except FileNotFoundError:
            self.data = None
        else:
            self.length = len(stdin.read())-4
            self.data = {}
            stdin.close()
    def __len__(self):
        return self.length+4
    def parseData(self):
        stdin = open(fName,'rb')
        tmp = stdin.read(4)
        if tmp != b'\x53\x41\x49\x01':
            raise SAMParseWarning('index','Magic Number seemed bad.')
        tmp = stdin.read(2)
        if tmp != b'\x01\x00':
            raise SAMParseWarning('index','Index file version wrong.')
        numWidth = bytesToInt(tmp.read(1))
        while stdin.tell() != self.length:
            tmp = bytesToInt(stdin.read(numWidth)),readLine(stdin),readLine(stdin)
            if tmp[1] not in self.data:
                self.data[tmp[1]] = {'index':[],'name':[]}
            self.data[tmp[1]]['index'].append(tmp[0])
            self.data[tmp[1]]['index'].append(tmp[1])
        if stdin.read()[:4] != '\x01IAS':
            raise SAMParseWarning('index','Index file seemed incomplete.')
    def __getitem__(self,index):
        result = []
        if self.data is None:
            raise SAMParseWarning('index','The SAM file did not come with its index.')
        elif self.data == []:
            self.parseData()
        for item in self.data:
            if index in self.data[item]:
                result.append(self.data[item][index]['index'])
        return result
    def getItem(self,index,chrNum=None):
        if chrNum is not None:
            if self.data == []:
                self.parseData()
            if type(chrNum) is int:
                chromosome = 'chr'+str(chrNum)
            else:
                chromosome = chrNum
            return self.data[chromosome][item]['index']
        else:
            return self[index]
    def makeIndex(self,fHandle,searchKey = None,forceWrite = False):
        if not forceWrite:
            try:
                stdout = open(self.fName,'rb')
            except FileNotFoundError:
                pass
            else:
                stdout.close()
                raise FileExistsError('The index file already exists. Use forceWrite=True to force overwrite it.')
        if type(fHandle) is str:
            stdin = open(fHandle,'r')
        elif type(fHandle) is samFile:
            stdin = open(fHandle.fName,'r')
        else:
            raise SAMParseError('SAM','Parser received a file that did not look like a SAM file')
    # This would consume a file iterator
        fin = 0
        self.data = {}
        if searchKey is not None:
            result = []
        for item in stdin:
            if bool(item.strip().split('\t')) and item.strip()[0]!='@':
                tmp = parseData(item.strip())
                if tmp is not None:
                    if tmp['rName'] not in self.data:
                        self.data[tmp['rName']] = {'name':[],'index':[]}
                    self.data[tmp['rName']]['name'].append(tmp['qName'])
                    self.data[tmp['rName']]['index'].append(fin)
                    if searchKey is not None and tmp['rName'] == searchKey:
                        result.append(fin)
            fin += len(item)
        stdin.close()
        stdout = open(self.fName,'wb')
        stdout.write(b'SAI\x01')
        import math
        numLength = int(math.log(fin,2)/8)+1
        for data in self.data:
            for datum in range(len(self.data[data]['name'])):
                index = bytearray(numLength)
                tmp = self.data[data]['index'][datum]
                for fin in range(numLength):
                    index[fin] = tmp % 256
                    tmp = tmp >> 8
                    if tmp == 0:
                        break
                stdout.write(bytes(index))
                stdout.write(data.encode('ascii'))
                stdout.write('\x00')
                stdout.write(self.data[data]['name'][datum].encode('ascii'))
                stdout.write('\x00')
        stdout.write(b'\x01IAS')
        stdout.close()
        if searchKey is not None:
            return result
class samIter():
    def __init__(self,data):
        self.data = open(data.fName,'r')
        tmp = self.data.readline()
        while tmp.strip()[0] == '@':
            tmp = self.data.readline()
        if tmp == '':
            self.retval = None
        else:
            self.retval = parseData(tmp.strip())
    def __next__(self):
        tmp = self.data.readline()
        while tmp.strip()[0] == '@':
            tmp = self.data.readline()
        if tmp == '':
            tmp = self.retval
            self.retval = None
            if tmp is None:
                raise StopIteration
            else:
                return tmp
        else:
            retval = self.retval
            self.retval = parseData(tmp.strip())
            return retval
    next = __next__
class samFile():
    def __init__(self,fName):
        self.fName = fName
        self.header = None
        self.index = None
        stdin = open(fName,'r')
        ptr = stdin.readline()
        # Empirically determined header line existence
        if len(ptr) > 8:
            self.header = {}
            try:
                parseHD(ptr,self.header)
                ptr = stdin.readline()
                while ptr[0] == '@':
                    parseHeader(ptr,self.header)
                    ptr = stdin.readline()
            except SAMParseWarning as e:
                print('WARNING: '+str(e))
                self.header = None
    def __iter__(self):
        return samIter(self)
    def __getitem__(self,index):
        stdin = open(self.fName,'r')
        result = []
        # Do we have an index available?
        if self.index is None:
            self.index = samIndex(self.fName+'.sai')
            if self.index.data is None:
                stdin.close()
                return self.index.makeIndex(self.fName,index)
        tmp = self.index[index]
        for item in tmp:
            stdin.seek(item)
            result.append(parseData(stdin.readline().strip()))
        stdin.close()
        if result == []:
            raise IndexError
        return result

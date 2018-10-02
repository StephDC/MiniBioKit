# This file is the common utilities used by other utilities.
# It is not supposed to be called directly, thus it does not
# have the #! at the beginning.
# However the use of this utility in other parts of your code
# is strongly encouraged.

## Not Working ##
class delList(list):
    ''' Delimeter-separated list, with default delimeter of space ( ) '''
    def setDel(self,delim):
        self.delimeter = delim
    def __str__(self):
        return self.delimeter.join([str(i) for i in self])

class equalDict(dict):
    ''' Equal-sign (=) connected dict, with default separator of a space ( )'''
    def __init__(self,data={},delimeter=' '):
        dict.__init__(data)
        self.delimeter = delimeter
    def __str__(self):
        result = ''
        for item in self.keys():
            if self[item] is not None and len(str(self[item])) > 0:
                if type(self[item]) is str and self[item].find(self.delimeter) >= 0:
                    result += item + '="' + self[item] + '"'+self.delimeter
                else:
                    result += item+'='+str(self[item])+self.delimeter
        return result[:-1]

class spaceList(list):
    '''Obsolete definition'''
    def __str__(self):
        result = ''
        for item in self:
            result += str(item)+' '
        return result[:-1]
class spaceList(list):
    def __str__(self):
        return ' '.join([str(i) for i in self])

class tabList(delList):
    '''Obsolete definition'''
    def __str__(self):
        result = ''
        for item in self:
            result += str(item)+'\t'
        return result[:-1]

class tabList(list):
    def __str__(self):
        return '\t'.join([str(i) for i in self])
#spaceList = lambda x=[]:delList(x,' ')
#tabList = lambda x=[]:delList(x,'\t')

class listOrder(list):
    def __lt__(self,other):
        ptr = 0
        while ptr < len(self) and self[ptr] == other[ptr]:
            ptr+=1
        if ptr == len(self) or ptr == len(other):
            return len(self) < len(other)
        else:
            return self[ptr] < other[ptr]
    def __eq__(self,other):
        if len(self) == len(other):
            for item in range(len(self)):
                if self[item]!=other[item]:
                    return False
            return True
        return False

class stdout():
    name = "stdout"
    def __init__(self):
        self.disabled = False
    def write(self,data):
        if self.disabled:
            raise ValueError("I/O operation on closed file.")
        if type(data) == bytes:
            tmp = data.decode('UTF-8')
        else:
            tmp = data
        if len(tmp) and tmp[-1] == '\n':
            tmp = tmp[:-1]
        print(tmp)
    def writable(self):
        return not self.disabled
    def writelines(self,dataset):
        for item in dataset:
            self.write(item)
    def readable(self):
        return False
    def close(self):
        self.disabled = True

class RegionIter():
    def __init__(self,chrom,pos,end):
        self.chrom = chrom
        self.pos = pos
        self.end = end
    def __iter__(self):
        return self
    def __next__(self):
        self.pos += 1
        return Region(self.chrom,self.pos-1,self.pos)

class Region():
    def __init__(self,chrom,start,end,data=None):
        self.chrom=chrom
        self.start=start
        self.end=end
        self.data = data
    def __getitem__(self,key):
        if type(key)==str:
            if key == 'chr':
                return self.chrom
            elif key == 'start':
                return self.start
            elif key == 'end':
                return self.end
        elif type(key)==int and key <= self.end-self.start:
            return Region(self.chrom,self.start+key,self.start+key+1)
        elif type(key)==slice and key.step is None:
            result = Region(self.chrom,self.start,self.end,self.data)
            if key.start is not None:
                if key.start < 0:
                    result.start = result.end + key.start
                else:
                    result.start = result.start + key.start
            if key.stop is not None:
                if key.stop < 0:
                    result.end = result.end + key.stop
                else:
                    result.end = self.start + key.stop
            if result.end - result.start < 0 or result not in self:
                raise KeyError('Illegal index')
            return result
        else:
            raise KeyError('Illegal key')
    def __str__(self):
        return 'chr'+str(self.chrom)+':'+str(self.start)+'-'+str(self.end)
    def __repr__(self):
        return str(self)
    def __len__(self):
        return self.end - self.start
    def __lt__(self,other):
        if type(other) != Region:
            raise TypeError('Comparisons only make sense if they belong to the same type.')
        if self.chrom != other.chrom:
            return self.chrom < other.chrom
        elif self.start != other.start:
            return self.start < other.start
        else:
            return self.end < other.end
    def __eq__(self,other):
        if type(other) != Region:
            return False
        if self.start == self.end:
            return other.start == other.end
        else:
            return self.chrom == other.chrom and self.start == other.start and self.end == other.end
    def __contains__(self,other):
        if type(other) == int:
            return self.start <= other < self.end
        elif type(other) == Region:
            if self.chrom == other.chrom and self.start <= other.start and self.end >= other.end:
                return True
            else:
                return False
        else:
            return NotImplemented
    def __add__(self,other):
        if type(other) == int:
            self.end += other
        #elif other is None:
        #    raise TypeError("NoneType + Regions is undefined")
        elif type(other) == Region:
            if self.overlap(other) or self.start == other.end or self.end == other.start:
                return Region(self.chrom,min((self.start,other.start)),max((self.end,other.end)))
            else:
                return NotImplemented #('Two regions are not overlapping or connected to each other.')
        else:
            return NotImplemented
    def __radd__(self,other):
        if type(other) == int:
            if self.start > other:
                self.start -= other
            else:
                raise IndexError("Extending beyond the beginning of the genome")
        else:
            return self.__add__(other)
    def __mul__(self,other):
        if type(other) != int:
            return NotImplemented
        else:
            result = Region(self.chrom,self.start,self.end)
            result.resize(len(self)*other)
            return result
    def __iter__(self):
        return RegionIter(self.chrom,self.start,self.end)
    def resize(self,size):
        mid = self['start']+self['end']
        self['start'] = mid - size >> 1
        self['end'] = mid + size >> 1
        if self['start'] < 1:
            self['start'] = 1
    def overlap(self,other):
        if type(other) != Region:
            raise NotImplemented
        return self[0] in other or other[0] in self

def chrList(maxNum):
    result = ['chr']*maxNum
    for i in range(maxNum):
        result[i] += str(i+1)
    return result

def insertItem(dest,item,skey = lambda x: x):
    ''' Insert item into an ordered list to keep the list in order. '''
    uBond = len(dest)
    lBond = -1
    if len(dest) != 0:
        while uBond - lBond > 1:
            ptr = (uBond+lBond) >> 1
            if skey(dest[ptr]) > skey(item):
                uBond = ptr
            else:
                lBond = ptr
    dest.insert(uBond,item)

def fiveNum(dataSet):
    tmp = sorted(dataSet)
    result = {}
    result['min'] = tmp[0]
    result['max'] = tmp[-1]
    result['median'] = tmp[len(dataSet)>>1]
    result['Q1'] = tmp[len(dataSet)>>2]
    result['Q3'] = tmp[-len(dataSet)>>2]
    return result

def splitQuote(data,cleaver=' '):
    quoteType = '\'"'
    quoted = None
    result = []
    tmp = ''
    for char in data:
        if char in quoteType:
            if quoted is None:
                quoted = char
            elif char == quoted:
                quoted = None
        elif char == cleaver and quoted is None:
            if tmp:
                result.append(tmp)
            tmp = ''
        else:
            tmp += char
    if tmp:
        result.append(tmp)
    return result

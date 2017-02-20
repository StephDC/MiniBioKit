# No hashbang as it is not supposed to be called from CGI / CLI
# Feel free to import it to get some randomized 8mers to test your code

import random
# Pending Removal
class rand8mer():
    def __init__(self, randstr = 'ACGT'):
        self.randstr = randstr
        self.data = random.getrandbits(16)
        if enumDNA(revComp(str(self))) < self.data:
            self.data = enumDNA(revComp(str(self)))
    def __str__(self):
        result = ''
        for i in range(8):
            result += self.randstr[3 & (self.data >> (2*i))]
        return result
    def __repr__(self):
        return str(self)
    def __iter__(self):
        return self
    def __next__(self):
        return rand8mer(self.randstr)

class rand8merlist():
    def __init__(self, randstr = 'AGCT', length = 1):
        self.length = length+1
        self.initLength = length+1
        self.instance = rand8mer(randstr)
    def __repr__(self):
        return str(self.instance)
    def __str__(self):
        return str(self.instance)
    def __iter__(self):
        return self
    def __next__(self):
        self.length -= 1
        if self.length:
            self.instance = next(self.instance)
            return self.instance
        else:
            self.length = self.initLength
            raise StopIteration

ncode = {'DNA':'ACGT','RNA':'ACGU'}
revCompTable = {'DNA':'ATCGWWSSMKRYBVDHNN','RNA':'AUCGWWSSMKRYBVDHNN'}
fuzzyTable = {'A':'A','T':'T','U':'U','C':'C','G':'G','W':'ATU','S':'CG','M':'AC','K':'GTU','R':'AG','Y':'CTU','B':'CGTU','D':'AGTU','H':'ACTU','V':'ACG','N':'ACGTU'}

def revComp(data, ntype = 'DNA'):
    result = ''
    for i in data:
        result = revCompTable[ntype][revCompTable[ntype].index(i) ^ 1] + result
    return result

def enumDNA(data, dataTable = 'ACGT'):
    result = 0
    for item in reversed(data):
        result = (result << 2) + dataTable.index(item)
    return result

def fuzzyNuc(seq, ntype = 'DNA'):
    result = False
    for item in seq:
        if item not in ncode[ntype]:
            result = True
            break
    return result

class nucSeq():
    def __init__(self,data,ntype = 'DNA'):
        self.ntype = ntype
        self.reversed = False
        if (not fuzzyNuc(data,ntype)) and enumDNA(revComp(data),ncode[ntype]) < enumDNA(data,ncode[ntype]):
            self.reversed = True
            self.data = revComp(data)
        else:
            self.data = data
    def __str__(self):
        return revComp(self.data,self.ntype) if self.reversed else self.data
    def __repr__(self):
        return "5'-"+str(self)+"-3'"
    def __len__(self):
        return len(self.data)
    def __eq__(self,other):
        try:
            if type(other) == str:
                return self.data == other or self.data == revComp(other,self.ntype)
            else:
                return self.data == other.data
        except Exception:
            return False
    def __getitem__(self,item):
        if item >= len(self) or item < -len(self):
            raise IndexError
        if self.reversed:
            item = (item ^ -1) % len(self)
        if item < 0:
            item = (len(self) - 1) - (item ^ -1) % len(self)
        if self.reversed:
            return revComp(self.data[item],self.ntype)
        else:
            return self.data[item]
    def __reversed__(self):
        return nucSeq(revComp(self.data),self.ntype)
    def __add__(self,other):
        try:
            return nucSeq(str(self)+str(other),self.ntype)
        except Exception:
            raise NotImplemented
    def __radd__(self,other):
        try:
            return nucSeq(str(other)+str(self),self.ntype)
        except Exception:
            raise NotImplemented
    def __mul__(self,other):
        if type(other) != int:
            raise NotImplemented
        else:
            return nucSeq(str(self)*other,self.ntype)
    def fuzzyMatch(self,other):
        cmpstr = str(self),str(other)
        result = True
        for item in range(len(self)):
            match = False
            for nt in fuzzyTable[cmpstr[0][item]]:
                if nt in fuzzyTable[cmpstr[1][item]]:
                    match = True
                    break
            result = result and match
            if not result:
                break
        return result or self.fuzzyMatch(revComp(other,self.ntype))

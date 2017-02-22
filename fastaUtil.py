import bioChemData.nucleotide

def treatLineFeed(fh,rl):
    '''Require file handler fh and remaining length rl
Return missing string or raise StopIteration'''
    seekpoint = fh.tell()
    tmp = fh.readline()
    if tmp == '':
        # End of file
        raise StopIteration
    elif tmp[0] == '>':
        # Beginning of the next sequence
        raise StopIteration
    elif tmp[0] == ';':
        # Comment
        seekpoint += len(tmp)-1
        tmp = '\n'
    if len(tmp)-1 > rl:
        fh.seek(seekpoint+rl)
        return tmp[:rl]
    else:
        fh.seek(seekpoint+len(tmp))
        return tmp[:-1] + treatLineFeed(fh,rl - len(tmp)+1)

class fastaIter():
    def __init__(self,seqName,fileHandle,readLength = 8):
        self.name = seqName
        self.data = fileHandle
        self.rl = readLength
    def __repr__(self):
        return "Sequence "+self.name+" with reading length of "+str(self.rl)
    def __iter__(self):
        return self
    def __next__(self):
        tmp = self.data.tell()
        result = self.data.read(self.rl)
        if result[0] == '\n':
            tmp += 1
            self.data.seek(tmp)
            result = self.data.read(self.rl)
        while result[0] == ';':
            self.data.seek(tmp)
            result = self.data.readline()
            tmp = self.data.tell()
            if result[0] != ';':
                tmp -= len(result)
                result = result[:self.rl]
        if '\n' in result:
            self.data.seek(tmp+result.index('\n'))
            result = result[:result.index('\n')] + treatLineFeed(self.data,self.rl-result.index('\n'))
        self.data.seek(tmp+1)
        return bioChemData.nucleotide.nucSeq(result)

class fastaFile():
    def __init__(self,fName):
        self.fName = fName
        stdin = open(fName,'r')
        self.seqtitle = []
        for line in stdin:
            if line[0] == '>':
                self.seqtitle.append(line[1:-1])
        stdin.close()
    def __iter__(self):
        fh = open(self.fName,'r')
        tmp = fh.readline()
        return fastaIter(self.seqtitle[0],fh)
    def read(self,length,begin = None):
        tmp = open(self.fName,'r')
        if begin is not None:
            tmp.seek(begin)
        result = tmp.read(length)
        if tmp.find('\n') >= 0:
            result += tmp.read(1)
            result.remove('\n')
        tmp.close()
        return result
# Takes Sequence Name and Reading Length as parameters. Returns a fastaIter.
    def quickSeek(self,seq,readlen):
        if seq not in self.seqtitle:
            raise FileNotFoundError('Sequence '+seq+' not found in file '+self.fName+' .')
        stdin = open(self.fName,'r')
        line = stdin.readline()
        while line[0]!='>' and line[1:-1] != seq:
            line = stdin.readline()
        return fastaIter(seq,stdin,readlen)
    def readSeq(self,seq):
        if seq not in self.seqtitle:
             raise FileNotFoundError('Sequence '+seq+" not found in file "+self.fName+' .')
        stdin = open(self.fName)
        foundMatch = False
        result = ''
        for line in stdin:
            if line[0] == '>' and line[1:-1] == seq:
                foundMatch = True
            elif line[0] == '>' and foundMatch:
                break
            elif foundMatch and line[0] != ';':
                result += line.strip().upper()
        return result

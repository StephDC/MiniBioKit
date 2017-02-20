class fastaIter():
    def __init__(self,seqName,fileHandle,readLength = 8):
        self.data = fileHandle
        self.rl = readLength
    def __iter__(self):
        return self
    def __next__(self):
        tmp = self.data.tell()
        result = self.data.read(self.rl)
        while '\n' in result:
            result += self.data.read(1)
            result = result[:result.index('\n')]+result[result.index('\n')+1:]
        self.data.seek(tmp+1)
        return result

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

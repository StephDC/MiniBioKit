import commonUtil

class iterCache():
    '''iterCache: The cache used by the dsvParser
    This would serve as the cache to balance between disk read and memory space
    It should be initialized by the iterParse initializer, but feel free to
    use it in any other places where it might be useful.
    '''
    def __init__(self,mem):
        self.mem = mem
        self.index = []
        self.data = []
        self.extra = None
        if mem[:6] == 'random':
            import random
            self.extra = lambda : (int(mem[6:]) > random.randint(1,100))
            self.mem = 'random'
        elif mem[:5] == 'limit' or mem[:5] == 'linux':
            self.mem = mem[:5]
            self.extra = int(mem[5:])
    def __len__(self):
        return len(self.index)
    def getItem(self,query):
        if query in self.index:
            print("query "+query+" hit at "+str(self.index.index(query)))
            return self.data[self.index.index(query)]
        else:
            return None
    def setItem(self,data,hit=False):
        if data[0] in self.index:
            if self.mem == 'linux':
                self.data.__delitem__(self.index.index(data[0]))
                self.index.remove(data[0])
        else:
            if self.mem == 'memsaver':
                pass
            elif self.mem == 'jit':
                self.index.append(data[0])
                self.data.append(data)
            elif self.mem == 'random' and self.extra():
                self.index.append(data[0])
            elif self.mem == 'limit':
                if hit and len(self.index) >= self.extra:
                    self.index.__delitem__(0)
                    self.data.__delitem__(0)
                if len(self.index) < self.extra:
                    self.index.append(data[0])
                    self.data.append(data)
            elif self.mem == 'linux' and not hit:
                if len(self.index) < self.extra:
                    self.index.append(data[0])
                    self.data.append(data)

class iterParse_iterator():
    def __init__(self,stdin,header,lineParser):
        self.stdin = stdin
        self.index = header
        self.lineParse = lineParser
    def __iter__(self):
        return self
    def __next__(self):
        tmp = None
        while tmp is None:
            result = self.stdin.readline()
            if result == '':
                self.stdin.close()
                raise StopIteration
            else:
                tmp = self.lineParse(result[:-1])
        return tmp
    next = __next__

class dsvParse():
    '''dsvParse: The Iterated DSV Parser
    This would allow parsing a Tab-separated value data with limited memory space
    or with faster access speed.
    This would also be able to parse Comma-separated value and Pipe-separated value
    given the separator was specified.
    '''
    def __init__(self,stdin,mem = 'memsaver',sep = '\t',quote = None, head=True):
        '''Parameters:
        stdin: Input file name
        mem: Memory model - memsaver, jit, random, limit
        sep: Value separator, default: Tab
        quote: Quote used to separate strings, default: None, can specify one or a pair of quote
        '''
        self.fName = stdin
        self.cache = iterCache(mem)
        self.sep = sep
        self.quote = quote
        header = open(stdin)
        self.keys = header.readline()[:-1].split(sep)
        header.close()
        if self.quote is not None:
            for i in range(len(self.keys)):
                # Item pending removal
                if self.keys[i] is None:
                    pass
                # Optional quote
                elif self.keys[i][0] == quote[0] and self.keys[i][-1] == quote[-1]:
                    self.keys[i] = self.keys[i][1:-1]
                # Quote that merges items
                elif self.keys[i][0] == quote[0]:
                    self.keys[i] = self.keys[i][1:]
                    k = i+1
                    while self.keys[k][-1] != quote[-1]:
                        self.keys[i] += self.keys[k]
                        self.keys[k] = None
                        k+=1
                    self.keys[i] += self.keys[k][:-1]
            while None in self.keys:
                self.keys.remove(None)
    def __str__(self):
        return "<iterParsedDSV fileName="+self.fName+" delimeter="+repr(self.sep)+" memoryModel="+self.cache.mem+">"
    def __iter__(self):
        stdin = open(self.fName)
        stdin.readline()
        return iterParse_iterator(stdin,self.keys,self.parseLine)
    def __repr__(self):
        return str(self)
    def parseLine(self,line):
        result = line.split(self.sep)
        if self.quote is not None:
            for i in range(len(result)):
                if result[i] is None:
                    pass
                elif result[i][0] == quote[0]:
                    if result[i][-1] == quote[-1]:
                        result[i] = result[i][1:-1]
                    else:
                        result[i] = result[i][1:]
                        k = i
                        while result[k][-1] != quote[-1]:
                            result[i] += result[k]
                            result[k] = None
                            k += 1
                        result[i] += result[k][:-1]
            while None in result:
                result.remove(None)
        if len(result) != len(self.keys):
            raise SyntaxError('Unequal number of data found, data line:\n'+line)
        return commonUtil.tabList(result)
    def findLine(self,name):
        result = self.cache.getItem(name)
	    # Not yet cached?
        if result is None:
            stdin = open(self.fName)
            hit = False
            for line in stdin:
                tmp = self.parseLine(line[:-1])
                # Found item
                if tmp[0] == name:
                    result = tmp
                    hit = True
                    break
                self.cache.setItem(tmp,hit)
            stdin.close()
        return result
    __getitem__ = fineLine
    def findCol(self,key):
        if key not in self.keys:
            raise KeyError("Key "+key+" not found in this file")
        else:
            kid = self.keys.index(key)
            result = []
            stdin = open(self.fName)
            for item in stdin:
                result.append(self.parseLine(item)[kid])
            return result
    def getItem(self,name,key):
        if key not in self.keys:
            raise KeyError("Key "+key+" not found in this file")
        else:
            tmp = self.findLine(name)
            if tmp is None:
                raise KeyError("Data "+name+" not found in this file")
            else:
                return tmp[self.keys.index(key)]

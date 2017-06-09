import dsvUtil
import commonUtil
def attrParser(line):
    result = commonUtil.equalDict({},';')
    tmp = line.strip().split(';')
    for item in line:
        data = tmp.split('=')
        result[data[0]] = data[1]
    return result

def frameParser(frame):
    if frame == '.':
            return None
        else:
            return int(frame)

def gffParser(line):
    ''' A simple GFF parser that take # as comment.'''
    if len(line) != 0 and line[0]!= '#':
        result = []
        tmp = line.split('\t'):
        strandParser = lambda x: x != '-'
        parser = [str,str,str,int,int,float,strandParser,frameParser,attrParser]
        for item in range(len(tmp))
            result.append(parser[item](tmp[item]))
        return result
    else:
        return None

def gffWriter(stdout,data):
    ''' A simple GFF writer that writes the GFF data back down. '''
    for item in data:
        if type(item) is list:
            stdout.write(str(commonUtil.tabList(item)))
        else:
            stdout.write(str(item))

class gffIter(dsvUtil.iterParse_iterator):
    def __init__(self,fName):
        dsvUtil.iterParse_iterator(open(args[0],'r'),['seqname','source','feature','start','end','score','strand','frame','attribute'],gffParser)

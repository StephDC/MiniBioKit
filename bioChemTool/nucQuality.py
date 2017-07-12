#! /usr/bin/env python3
import sys
from . import dsvUtil
commonUtil = dsvUtil.commonUtil

## Starts file def ##
nucHeader = ['chr','start','end']
def nucParse(line):
    if not bool(line.strip()) or line.strip()[0] == '#':
        return None
    result = []
    typeList = [str,int,int]
    tmp = line.strip().split('\t')
    for item in range(3):
        result.append(typeList[item](tmp[item]))
    return result
readHeader = ['chr','mid','width','nothing','quality']
def readParse(line):
    if not bool(line.strip()) or line.strip()[0] == '#' or line.strip()[:5]=='chrom':
        return None
    result = []
    typeList = [str,int,int,str,int]
    tmp = line.strip().split('\t')
    for item in range(5):
        result.append(typeList[item](tmp[item]))
    return result
## Ends file def ##
__doc__ = sys.argv[0]+''': A program that quantifies the quality of a nucleosome call
Synopsis:\n\t'''+sys.argv[0]+''' scanWidth nucleosomeCall.tsv readMidPoint1.tsv readMidPoint2.tsv ...
Parameters:
    nucleosomeCall.tsv - a Tab-separated value file that stores the nucleosome position
                         with the format of "Chromosome Start End".
    readMidPoint.tsv   - a Tab-separated value file that stores the midpoints of reads
                         in IDX format.
    scanWidth          - an integer specifying the width of the histogram.'''

def main(args):
    if len(args) < 3:
        print(__doc__)
    scanWidth = int(args[0])
    result = [0] * (scanWidth +1)
    for item in args[2:]:
        nucIn = dsvUtil.iterParse_iterator(open(args[1]),nucHeader,nucParse)
        next(nucIn)
        readIn = dsvUtil.iterParse_iterator(open(item),readHeader,readParse)
        data = runStats(nucIn,readIn,scanWidth)
        for i in range(scanWidth+1):
            result[i] += data[i]
    for item in range(scanWidth+1):
        print(item - (scanWidth >> 1), result[item], sep='\t')

def runStats(nucIn,readIn,scanWidth):
    result = [0] * (scanWidth+1)
    nucQueue = []
    curChr = None
    for item in readIn:
        if curChr != item[0]:
            curChr = item[0]
            nucQueue = []
        while nucIn is not None and nucIn.getLast('chr') == curChr and nucIn.getLast('start')+nucIn.getLast('end') >> 1 <= item[1] + (scanWidth >> 1):
            nucQueue.append(nucIn.getLast('start')+nucIn.getLast('end') >> 1)
            try:
                next(nucIn)
            except StopIteration:
                nucIn = None
        while nucQueue and nucQueue[0] < item[1] - (scanWidth >> 1):
            nucQueue = nucQueue[1:]
        if not (nucQueue or nucIn):
            break
        for pos in nucQueue:
            result[pos - item[1] + (scanWidth >> 1)] += 1
    return result

if __name__ == '__main__':
    main(sys.argv[1:])

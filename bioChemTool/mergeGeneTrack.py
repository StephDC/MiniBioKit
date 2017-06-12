#! /usr/bin/env python3
import sys
import gffUtil

def compareSegment(smaller,bigger,chrList):
    ''' Return True if smaller is smaller than bigger '''
    if chrList.index(smaller[0]) > chrList.index(bigger[0]):
        return False
    if chrList.index(smaller[0]) == chrList.index(bigger[0]):
        return smaller[3] < bigger[3]
    return True

def main(args):
    ## PARAMETERS ##
    overlapCutoff = 0.5 # Amount of max non-overlapping region between all segments.
    qualifyCutoff = 0.5 # Amount of qualified segments needed to make the whole group qualified.
    chrList = []
    ## END PARAMS ##
    stdout = {'mean':open(args[0]+'_mean.gff','w'),'median':open(args[0]+'_median.gff','w')}
    stdin = []
    for item in args[1:]:
        stdin.append(gffUtil.gffIter(item))
    snapshot = [None]*len(stdin)
    while stdin.count(None) < len(stdin)*(1-qualifyCutoff):
        firstSeg = None
        #lastSeg = None
        for item in range(len(stdin)):
            try:
                if snapshot[item] is None and stdin[item] is not None:
                    snapshot[item] = next(stdin[item])
                    if snapshot[item][0] not in chrList:
                        chrList.append(snapshot[item][0])
            except StopIteration:
                snapshot[item] = None
                stdin[item] = None
            if snapshot[item] is not None:
                if firstSeg is None or compareSegment(snapshot[item],firstSeg,chrList):
                    firstSeg = snapshot[item]
        # Now the first seg is found and snapshot is filled.
        if firstSeg is None:
            break # Done. No segment left.
        # See if this list contains enough qualified entries
        segLength = firstSeg[4]-firstSeg[3]
        commonReg = [firstSeg[3],firstSeg[4]]
        counter = []
        for item in range(len(snapshot)):
            if snapshot[item] is not None and snapshot[item][3] < firstSeg[3]+overlapCutoff*segLength:
                if snapshot[item][3] > commonReg[0]:
                    commonReg[0] = snapshot[item][3]
                if snapshot[item][4] < commonReg[1]:
                    commonReg[1] = snapshot[item][4]
                counter.append(item)
        if len(counter) > len(stdin)*(qualifyCutoff):
            # Qualified entry found.
            mean = [0,0]
            sortList = []
            originText = ''
            for item in counter:
                mean[0] += snapshot[item][3]
                mean[1] += snapshot[item][4]
                gffUtil.commonUtil.insertItem(sortList,[snapshot[item][3],snapshot[item][4]],lambda x:x[0])
                snapshot[item] = None
                originText += '123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'[item]
            firstSeg[8]['trackNum'] = len(counter)-stdin.count(None)
            firstSeg[8]['commonReg'] = str(commonReg[0])+':'+str(commonReg[1])
            firstSeg[8]['origin'] = originText
            firstSeg[6] = '-+'[int(firstSeg[6])]
            firstSeg[3] = int(mean[0] / len(sortList))
            firstSeg[4] = int(mean[1] / len(sortList))
            sqrdev = 0
            for item in sortList:
                sqrdev += (int(mean[0] / len(sortList)) - item[0])**2
            firstSeg[8]['stddev'] = (sqrdev/len(sortList))**0.5
            stdout['mean'].write(str(firstSeg)+'\n')
            if len(sortList) & 1:
                firstSeg[3] = (sortList[len(sortList)>>1][0]+sortList[(len(sortList)>>1)-1][0]) >> 1
                firstSeg[4] = (sortList[len(sortList)>>1][1]+sortList[(len(sortList)>>1)-1][1]) >> 1
            else:
                firstSeg[3] = sortList[len(sortList)>>1][0]
                firstSeg[4] = sortList[len(sortList)>>1][1]
            sqrdev = 0
            for item in sortList:
                sqrdev += (firstSeg[3] - item[0])**2
            firstSeg[8]['stddev'] = (sqrdev/len(sortList))**0.5
            stdout['median'].write(str(firstSeg)+'\n')
        else:
            snapshot[snapshot.index(firstSeg)] = None
    stdout['mean'].close()
    stdout['median'].close()

if __name__ == '__main__':
    main(sys.argv[1:])

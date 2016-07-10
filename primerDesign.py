#! /usr/bin/env python3

import sys
from bioChemData import restrictionEnzyme
from bioChemData import protein

def compStrand(posStrand):
    result = ''
    mapping = {'A':'T','C':'G','T':'A','G':'C'}
    for i in posStrand:
        result = result + mapping[i]
    return result

def revCompStrand(posStrand):
    iterator = reversed(compStrand(posStrand))
    result = ''
    for i in iterator:
        result += i
    return result

def gcRatio(posStrand):
    return 100 * (posStrand.count('C')+posStrand.count('G')) / len(posStrand)

def formatSeq(posStrand):
    print('//\tLength: '+str(len(posStrand)))
    for i in range(len(posStrand)//60+1):
        print('\t'+posStrand[i*60:i*60+60].upper())

def formatTriplet(posStrand,unpairedAtFirst=False):
    offset = 0
    result = ''
    if unpairedAtFirst:
        offset = len(posStrand)%3
        if offset:
            result = posStrand[:offset].upper()+' '
    for i in range(len(posStrand)//3 + 1):
        result += posStrand[offset+i*3:offset+i*3+3].upper()+' '
    return result[:-1]

def makeStructureFile(fName,removeStop=False):
    fileName = open(fName,'r')
    print('Vector:\t'+fileName.readline().strip())
    print('Gene:\t'+fileName.readline()[:-1])
    gene = fileName.readline()[:-1].upper()
    print('Protein Sequence:')
    formatSeq(protein.nucleotideTranslation(gene))
    print('Gene Sequence:')
    formatSeq(gene)
    restEnz = fileName.readline()[:-1].split('\t')
    restSeq = [restrictionEnzyme.enzymeSequence(restEnz[0]),
               restrictionEnzyme.enzymeSequence(restEnz[1])]
    print('Restriction Enzyme:\t'+restEnz[0]+'\t'+restEnz[1])
    print('Enzyme Sequence: \t'+restSeq[0].printSequence()+'\t'+restSeq[1].printSequence())
    fwd = fileName.readline()[:-1]+gene[:20]
    if removeStop:
        rev = revCompStrand(gene[-23:-3]+fileName.readline()[:-1])
    else:
        rev = revCompStrand(gene[-20:]+fileName.readline()[:-1])
    print('Forward Primer:')
    print('\t'+fwd)
    print('// \tGC Ratio:',gcRatio(fwd))
    print('Reverse Primer:')
    print('\t'+rev)
    print('// \tGC Ratio:',gcRatio(rev))
    print('//\n//\tPlus Strand DNA Sequence for reference:')
    print('// \t'+formatTriplet(revCompStrand(rev),True))

def main(args):
    posStr = args[0]
    print('F:\t5\'-'+posStr+"-3'")
    print('R:\t3\'-'+compStrand(posStr)+"-5'")
    print('R:\t5\'-'+revCompStrand(posStr)+"-3'")
    print('GC Ratio:',gcRatio(posStr))

if __name__ == '__main__':
    makeStructureFile(sys.argv[1],True)

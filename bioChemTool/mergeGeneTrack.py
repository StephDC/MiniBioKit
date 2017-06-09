#! /usr/bin/env python3
import sys
import gffUtil

def main(args):
    # Usage: MasterYeastCoor.txt File1.gff File2.gff
    stdin = dsvUtil.dsvParse(args[0])
    data = {}
    for item in ['#Chrom','Name_sgd','gene_start','gene_end','TSS_strand']:
        data[item] = stdin.findCol(item)[1:]
    gene = []
    chrList = []
    result = {}
    for item in range(len(data['#Chrom'])):
        gene.append([data['Name_sgd'][item],{'chr':data['#Chrom'][item],'strand':data['TSS_strand'][item]=='+','start':int(data['gene_start'][item]),'end':int(data['gene_end'][item]),'flag':0}])
        if data['#Chrom'][item] not in chrList:
            chrList.append(data['#Chrom'][item])
    # Now we have the data for the genes. Time to get some Nucleosome info.
    for chrName in chrList:
        nuc = []
        for data in range(1,len(args)):
            stdin = dsvUtil.iterParse_iterator(open(args[data],'r'),['chr','app','null','start','end','val','strand','null','stddev'],lambda x: x.split('\t'))
            for datum in stdin:
                if datum[0] == chrName:
                    nuc.append([int(datum[3]),int(datum[4]),args[data]])
        # Now we have the nucleosome locations. Time to find them by coordinate.
        # It could even run in parallel in the future.
        result[chrName]=callNuc(chrName,gene,nuc)
    badEntry = []
    print('#Chrom\tgene_start\tgene_end\tName_sgd\twarnFlag\tnuc-1_start\tnuc-1_end\tnuc+1_start\tnuc+1_end\tnucTN_start\tnucTN_end')
    for chrName in chrList:
        for gene in result[chrName]:
            rcg = result[chrName][gene]
            if rcg['gene'] is not None and rcg['minusOne'] is not None and rcg['plusOne'] is not None and rcg['transEnd'] is not None:
                print(chrName+'\t'+listTSV(rcg['gene'])+'\t'+gene+'\t'+listTSV(rcg['minusOne'][:2])+'\t'+listTSV(rcg['plusOne'][:2])+'\t'+listTSV(rcg['transEnd'][:2]))
            else:
                badEntry.append(rcg)
    if len(badEntry):
        print('# ------ Warning ------\n# The follow entries are missing nucleosome mapping informations.')
        for item in badEntry:
            print('#'+str(item))

### Here comes the actual code ###
def main(args):
    stdout = open(args[0],'w')
    stdin = []
    for item in args[1:]:
        stdin.append(gffUtil.gffIter(item))

if __name__ == '__main__':
    main(sys.argv[1:])

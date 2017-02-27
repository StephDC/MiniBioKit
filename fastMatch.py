#! /usr/bin/env python3
import sys
import fastaUtil
import bioChemData
def main(args):
    stdin = fastaUtil.fastaFile(args[0])
    data = stdin.readSeq(args[1])
    target = args[2]
    pointer = 0
    result = set()
    while data.find(target,pointer) != -1:
        tmp = data.find(target,pointer)
        result.add(tmp)
        pointer = tmp+1
    pointer = 0
    target = bioChemData.nucleotide.revComp(target)
    while data.find(target,pointer) != -1:
        tmp = data.find(target,pointer)
        result.add(tmp)
        pointer = tmp+1
    print(result)

if __name__ == '__main__':
    main(sys.argv[1:])

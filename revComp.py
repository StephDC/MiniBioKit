#! /usr/bin/env python3

import primerDesign
import sys

def main(inf,outf):
    stdin=open(inf)
    stdout=open(outf,'a')
    stdout.write(DNASeq.revCompStrand(stdin.read()))
    stdin.close()
    stdout.close()

if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2])

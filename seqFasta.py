#! /usr/bin/env python3

import sys

__doc__='''This program would make a FASTA file from a SEQ file.
SYNOPSIS:
    '''+sys.argv[0]+''' [-r] source target [sequence_name]'''

def parseArgs(args):
    revComp = False
    if len(args) < 1 or len(args)> 4:
        raise(SyntaxError("Wrong number of parameters"))
    if args[0] == '-r':
        revComp = True
        seqName = args[2][:args[2].find('.')]
        if len(args) > 3:
            seqName = args[3]
        main(args[1],args[2],seqName,revComp)
    elif len(args) > 2:
        seqName = args[2]
        main(args[0],args[1],seqName,revComp)
    else:
        seqName = args[1][:args[1].find('.')]
        main(args[0],args[1],seqName,revComp)

def main(inf,outf,name,rev):
    stdin=open(inf)
    stdout=open(outf,'a')
    stdout.write('>'+name+'\n')
    if rev:
        import primerDesign
        stdout.write(primerDesign.revCompStrand(stdin.read()))
    else:
        stdout.write(stdin.read())
    stdin.close()
    stdout.close()

if __name__ == '__main__':
    try:
        parseArgs(sys.argv[1:])
    except IndexError:
        raise(SyntaxError("Wrong number of parameters"))

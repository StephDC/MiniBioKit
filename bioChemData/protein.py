from . import sqldb
import os

dbPath = os.path.dirname(os.path.realpath(__file__))+'/data.sql'

class aminoAcid():
    def __init__(self,abbr1,abbr3,name,mm):
        self.abbr3 = abbr3
        self.abbr1 = abbr1
        self.name = name
        self.mm = mm
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def getOne(self):
        return self.abbr1
    def getThree(self):
        return self.abbr3
    def getMM(self):
        return self.mm

class aminoAcidDB():
    def __init__(self):
        self.db = sqldb.sqliteDB(dbPath,'protein')
    def getAA(self,abbr1):
        abbr3,nothing,name,mm = self.db.data.execute('SELECT * FROM protein WHERE one=?',abbr1).fetchone()
        mm = float(mm)
        return aminoAcid(abbr1,abbr3,name,mm)
    def getAA3(self,abbr3):
        abbr1 = self.db.getItem(abbr3,'one')
        name = self.db.getItem(abbr3,'name')
        mm = float(self.db.getItem(abbr3,'mm'))
        return aminoAcid(abbr1,abbr3,name,mm)

class translateDB():
    def __init__(self):
        self.db = sqldb.sqliteDB(dbPath,'translate')
    def getAA3(self,codon):
        return self.db.getItem(codon,'protein')

class pepSeq(list):
    def __add__(self,op):
        self.db = aminoAcidDB()
        if type(op) == str:
            if len(op) == 3:
                return pepSeq(list(self)+[self.db.getAA3(op)])
        elif type(op) == aminoAcid:
            print('Adding '+str(op))
            return pepSeq(list(self)+[op])
        elif type(op) == pepSeq:
            return pepSeq(list(self)+list(op))
        else:
            return NotImplemented
    def __str__(self):
        result = ''
        for item in self:
            if type(item) == aminoAcid:
                if item.getOne() == 'X':
                    break
                result += item.getOne()
            else:
                raise TypeError('Some non-amino acids were inserted into this peptide.')
        return result
    def __repr__(self):
        return 'N-'+str(self)+'-C'
    def nonsense(self):
        return len(self)>len(str(self))+1
    def molarMass(self):
        result = 18 # Molar Mass of H2O
        for item in self:
            result += item.mm
            result -= 18
        return result

def codonTranslate(codon,codonDB,aaDB):
    return aaDB.getAA3(codonDB.getAA3(codon))

def nucleotideTranslation(posStrand):
    pointer = 0
    result = pepSeq()
    adb = aminoAcidDB()
    cdb = translateDB()
    lastAA = adb.getAA('M')
    while posStrand[pointer:pointer+3] != 'ATG' and pointer <= len(posStrand)-3:
        pointer += 1
    while pointer <= len(posStrand)-3 and lastAA.getOne() != 'X':
        lastAA = adb.getAA3(cdb.getAA3(posStrand[pointer:pointer+3]))
        result.append(lastAA)
        pointer += 3
    return result

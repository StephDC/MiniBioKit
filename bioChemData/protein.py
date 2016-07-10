from . import sqldb
class aminoAcid():
    def __init__(self,abbr1,abbr3,name):
        self.abbr3 = abbr3
        self.abbr1 = abbr1
        self.name = name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def getOne(self):
        return self.abbr1
    def getThree(self):
        return self.abbr3

class aminoAcidDB():
    def __init__(self):
        self.db = sqldb.sqliteDB('bioChemData/data.sql','protein')
    def getAA3(self,abbr3):
        abbr1 = self.db.getItem(abbr3,'one')
        name = self.db.getItem(abbr3,'name')
        return aminoAcid(abbr1,abbr3,name)

class translateDB():
    def __init__(self):
        self.db = sqldb.sqliteDB('bioChemData/data.sql','translate')
    def getAA3(self,codon):
        return self.db.getItem(codon,'protein')

def codonTranslate(codon,codonDB,aaDB):
    return aaDB.getAA3(codonDB.getAA3(codon))

def nucleotideTranslation(posStrand):
    pointer = 0
    result = ''
    lastAA = 'M'
    adb = aminoAcidDB()
    cdb = translateDB()
    while posStrand[pointer:pointer+3] != 'ATG' and pointer <= len(posStrand)-3:
        pointer += 1
    while pointer <= len(posStrand)-3 and lastAA != 'X':
        lastAA = adb.getAA3(cdb.getAA3(posStrand[pointer:pointer+3])).getOne()
        result += lastAA
        pointer += 3
    return result

#! /usr/bin/python3
from . import sqldb
import sys
class enzSeq():
    def __init__(self,seq,cutSite):
        self.data = seq
        self.site = cutSite
    def __str__(self):
        return self.data
    def __repr__(self):
        return self.data[:self.site]+'^'+self.data[self.site:]
    def getSequence(self):
        return str(self)
    def printSequence(self):
        return self.__repr__()

def enzymeSequence(enzymeName):
    db = sqldb.sqliteDB('bioChemData/data.sql','enzyme')
    return enzSeq(db.getItem(enzymeName,'sequence'),int(db.getItem(enzymeName,'cutsite')))

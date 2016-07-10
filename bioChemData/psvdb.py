#! /usr/bin/python3

class psvDB():
    def __init__(self,dbFile):
        self.data = {}
        self.localFile = dbFile
        stdin = open(dbFile,'r')
        for line in stdin:
                tmp = line.split('|')
                dataSet = []
                for item in tmp:
                    dataSet.append(item.strip())
                self.data[dataSet[0]]=dataSet[1:]
        stdin.close()

    def __str__(self):
        result = ""
        for item in self.data.keys():
            result += item
            for subitem in self.data[item]:
                result += '|'
                result += str(subitem)
            result += '\n'
        return result

    def hasItem(self,item):
        return item in self.data.keys()

    def getItem(self,item,key):
        return self.data[item][self.data["header"].index(key)]

    def addItem(self,item):
        self.data[item[0]] = item[1:]
        self.updateDB()

    def remItem(self,item):
        result = self.data.pop(item)
        self.updateDB()
        return result

    def updateDB(self):
        stdout = open(self.localFile,"w")
        stdout.write(self.__str__())
        stdout.close()

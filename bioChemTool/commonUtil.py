# This file is the common utilities used by other utilities.
# It is not supposed to be called directly, thus it does not
# have the #! at the beginning.
# However the use of this utility in other parts of your code
# is strongly encouraged.

class delList(list):
    ''' Delimeter-separated list, with default delimeter of space ( ) '''
    def __init__(self,data=[],delimeter=' '):
        list.__init__(data)
        self.delimeter = delimeter
    def __str__(self):
        result = ''
        for item in self:
            result += str(item)+self.delimeter
        return result[:-1]

class equalDict(dict):
    ''' Equal-sign (=) connected dict, with default separator of a space ( )'''
    def __init__(self,data={},delimeter=' '):
        dict.__init__(data)
        self.delimeter = delimeter
    def __str__(self):
        result = ''
        for item in self.keys():
            if self[item] is not None and len(str(self[item])) > 0:
                if type(self[item]) is str and self[item].find(self.delimeter) >= 0:
                    result += item + '="' + self[item] + '"'+self.delimeter
                else:
                    result += item+'='+str(self[item])+self.delimeter
        return result[:-1]

class spaceList(list):
    def __str__(self):
        result = ''
        for item in self:
            result += str(item)+' '
        return result[:-1]

class tabList(delList):
    def __init__(self,data=[]):
        delList.__init__(self,data=data,delimeter='\t')

def insertItem(dest,item,skey = lambda x: x):
    ''' Insert item into an ordered list to keep the list in order. '''
    uBond = len(dest)
    lBond = -1
    if len(dest) != 0:
        while uBond - lBond > 1:
            ptr = (uBond+lBond) >> 1
            if skey(dest[ptr]) > skey(item):
                uBond = ptr
            else:
                lBond = ptr
    dest.insert(uBond,item)

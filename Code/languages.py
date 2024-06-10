#languages.py

ENGLISH = 0
FRENCH = 1

class lang:
    def __init__(self, select, ml, nl):
        self.msgList = ml
        self.selected = select
        self.numLang = nl
        self.textDisplay={}

        self.initDictionary()

    def initDictionary(self):
        for i in range(0,len(self.msgList),self.numLang):
            self.textDisplay[self.msgList[i]] = self.msgList[i+self.selected]


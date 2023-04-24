from Operators import *
#Class for define the alphabet while reading the string
class AlphabetDefinition:
    def __init__(self):
        self.alphabet = []

    def getAlphabet(self):
        return self.alphabet

    def getAlphabetNames(self):
        names = []
        for i in self.alphabet:
            names.append(i.name)
        return names

    def addSymbol(self, symbol):
        if symbol.name not in self.getAlphabetNames():
            self.alphabet.append(symbol)

        #get symbol dictionary, ADD EPSILON OR NOT
    def getSymbolDictionary(self):
        operators = [KleeneStar(),Union(), Concatenation(),LeftParenthesis(), RightParenthesis(), QuestionMark(), PositiveClosure()]
        symbolDictionary = {}
        for i in range(len(operators)):
            symbolDictionary[operators[i].symbol] = operators[i]
        return symbolDictionary
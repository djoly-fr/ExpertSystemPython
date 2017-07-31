#!/usr/bin/env python
# coding: utf-8
import re
import sys
import collections
# from find_rule import *
import find_rule as fr
# class Rule:
def and_rule(a, b):
    print ("and", a, b, a and b)
    return (a and b)

def impl(a):
    if a:
        return (True)
    else:
        return (None)

def xor_rule(a, b):
    print("xor", a, b, (a and not b) or (not a and b))
    return ((a and not b) or (not a and b))

def or_rule(a, b):
    print("or", a, b, a or b)
    return (a or b)

def not_rule(a):
    return (not a)

def implicationDic(equ):
    # dictionnaire des implications True => ou false <=>
    dic = {}
    index = 0
    for i in equ:
        if i.startswith('=>'):
            dic[index] = {"equ": i, "val": True}
        else:
            dic[index] = {"equ": i, "val": False}
        index += 1
    return dic

def letterForEachLine(file):
    # tableau tous les lettre pour chaque ligne
    letterLine = []
    file_content = file.split('\n')
    for lines in file_content[0:]:
        reg = re.findall("[A-Z]", lines)
        letterLine.append(reg)
    return letterLine

def letterDicValue(equal, letterFile):
    # dictionnaire des lettres avec leurs valeurs
    dic = {}
    print("DicValue")
    for i in letterFile:
        print("i", i)
        if equal[0].find(i) != -1:
            dic[i] = {"letter": i, "val": True, "constant": True}
        else:
            dic[i] = {"letter": i, "val": False, "constant": False}
    dic["1"] = {"letter": "1", "val": True, "constant": True}
    dic["0"] = {"letter": "0", "val": False, "constant": True}
    return dic

#pour avoir la position des lettres de la query
def findQueryLetter(query, left, right):
    dict = {}
    lq = list(query[0])
    i = 0
    tab = []

    for l in lq:
        i = 0
        dict[l] = {"letter": l, "right": []}
        for r in right:
            if l in r:
                if "right" in dict:
                    tab = dict[l]["right"]
                if i in tab:
                    print("non")
                else:
                    tab.append(i)
                    dict[l] = {"letter": l, "right": tab}
            i += 1
    return dict

def findLetterRightSide(letter, right):
    tab = []
    i = 0
    for r in right:
        if letter in r:
            tab.append(i)
        i += 1
    return tab

def printAll(dicEqu, dic, left, right, equal, query, letterFile, equ, letterLine):
    print ("dicEqu", dicEqu)
    print ("left", left)
    print ("right", right)
    print ("ewu" ,equ)
    print ("letterLine" , letterLine)
    print ("equal[0]", equal)
    print ("query", query)
    print ("letterFile", letterFile)
    print ("dic", dic)

#print le resultat de la query
def queryResult(query, dic):
    q = list(query[0])
    tmp = None
    for q in q:
        tmp = dic[q]["val"]
        if (tmp == None):
            print (q, "is undetermined")
        elif (tmp == True):
            print (q, "is True")
        else:
            print (q, "is False")

#fonction qui repond a la query de type B + A => E | F
def solveQuery(dict, leftTab, rightTab, alphabet, line, lineTab):
    Ret = collections.namedtuple('Ret', ['alpha', 'left'])
    print('dans SolveQuery')
    print("left", leftTab , "value ", line)
    r = Ret(alphabet, left=leftTab[line])
    print("left", leftTab)
    if len(leftTab[line]) > 1:
        retExp = solveExp(r, dict, leftTab[line], leftTab, rightTab, lineTab)
    else:
        if alphabet[leftTab[0]]["val"] == True:
            retExp = "1"
        else:
            retExp = "0"
    print("resultat de exp  ",retExp)
    r = Ret(alphabet, left=retExp)
    return r

#fonction recursive qui resout les expression type Q + (A | (D + B) + H) + E
def solveExp(r, dict, currentLine, leftTab, rightTab, lineTab):
    print("__debut solve __")
    if currentLine == "0" or currentLine == "1":
        return currentLine
    print("r ",r)
    currentLine = fr.findParanthese(r, dict, currentLine, leftTab, rightTab, lineTab)
    currentLine = fr.findExclamation(r, dict, currentLine, leftTab, rightTab, lineTab)
    currentLine = fr.findAnd(r, dict, currentLine, leftTab, rightTab, lineTab)
    currentLine = fr.findOr(r, dict, currentLine, leftTab, rightTab, lineTab)
    currentLine = fr.findXor(r, dict, currentLine, leftTab, rightTab, lineTab)
    return currentLine   #return le string de l exp, a la fin on aura 0 ou 1

#bruteforce pour le coté droit, il teste True, apres False
def solveRightSide(dict, leftTab, rightTab, alphabet, line, letter, lineTab):
    Ret = collections.namedtuple('Ret', ['alpha', 'left'])
    print ("+++++++++++entré+++++++++++", line, alphabet[letter]["val"])
    print("leftTab", leftTab)
    r = Ret(alphabet, left=leftTab[line])
    print ("+++++++++++entré+++++++++++", line, alphabet[letter]["val"])
    if len(rightTab[line]) > 1:
        print("_____1______")
        alphabet[letter]["val"] = True
        r = Ret(alphabet, left=leftTab[line])
        str = solveExp(r, dict, rightTab[line], leftTab, rightTab, lineTab)
        if str != leftTab[line]:
            print("_____2______")
            alphabet[letter]["val"] = False
            r = Ret(alphabet, left=leftTab[line])
            str = solveExp(r, dict, rightTab[line], leftTab, rightTab, lineTab)
            if str != leftTab[line]:
                print("_____3______")
                alphabet[letter]["val"] = None
                r = Ret(alphabet, left=leftTab[line])
        else:
            print("_____4______")
            alphabet[letter]["val"] = False
            r = Ret(alphabet, left=leftTab[line])
            str = solveExp(r, dict, rightTab[line], leftTab, rightTab, lineTab)
            if str == leftTab[line]:
                print("_____5______")
                alphabet[letter]["val"] = None
                r = Ret(alphabet, left=leftTab[line])
            else:
                alphabet[letter]["val"] = True
                r = Ret(alphabet, left=leftTab[line])
    else:
        if leftTab[line] == "1":
            alphabet[letter]["val"] = True
        else:
            alphabet[letter]["val"] = False
    alphabet[letter]["constant"] = True
    print ("sorti", line,  alphabet[letter]["val"])
    return r

def parseRightLetter(letter, leftTab, rightTab, r, lineTab):
    print("___parseRightLetter___", letter)
    tab = findLetterRightSide(letter, rightTab)
    Ret = collections.namedtuple('Ret', ['alpha', 'left'])
    print(tab)
    for line in tab:
        if lineTab[line] == False:
            r = Ret(r.alpha, left=leftTab[line])
            r = solveQuery(dict, leftTab, rightTab, r.alpha, line, lineTab)
            leftTab[line] = r.left
            lineTab[line] = True
            r = solveRightSide({}, leftTab, rightTab, r.alpha, line, letter, lineTab)
    return r

#dict : dict des lettres avec les lignes
#leftTab
#rightTab
#alphabet : dict des letter avec leur valeur et constant ou non
def parseQuery(dict, leftTab, rightTab, alphabet, queryTab, lineTab):
    Ret = collections.namedtuple('Ret', ['alpha', 'left'])
    #dict indique la position des queries
    for letter in dict:
        #on accede au contenu de la key de dict et il faut deux for pour ça
        print("dict[letter]", dict[letter]["right"])
        for line in dict[letter]["right"]:
            if lineTab[line] == False:
                print('value', line)
                print("left[line]", leftTab[line])
                print("right[line]", rightTab[line])
                r = Ret(alphabet, left=leftTab[line])
                #alphabet = solveQuery(alphabet, left, right, value,  )
                r = solveQuery(dict, leftTab, rightTab, alphabet, line, lineTab)
                leftTab[line] = r.left
                lineTab[line] = True
                solveRightSide(dict, leftTab, rightTab, alphabet, line, letter, lineTab)
                #alphabet = handleLeftSide(dict, left[value], right[value], alphabet, query)
    queryResult(queryTab, alphabet)
    return alphabet

def main(argv):
    file = open(argv[0], 'r')
    regex = re.compile(r"#.*", re.IGNORECASE)
    file2 = regex.sub("", file.read())
    file2 = file2.replace(" ", "")
    print(file2)
    leftTab = re.findall(".*[A-Z()!]\s*(?=\=>)|.*[A-Z]\s*(?=<\=>)", file2)
    rightTab = re.findall("(?<=\=>).*[A-Z]\s*(?=\n)|(?<=<\=>).*[A-Z]\s*(?=\n)", file2)
    equTab = re.findall("=>|<=>", file2)
    equalTab = re.findall("(?<=\n=).*", file2)
    queryTab = re.findall("(?<=\n\?).*", file2)
    # tableau tous les lettre pour chaque ligne
    letterLine = letterForEachLine(file2)
    # print letterLine
    #tableau de booleen pour chaque ligne vu, True ou False
    lineTab = [False] * len(letterLine)
    #toutes lettre du fichier avec doublon
    letterFile = []
    letterFile = re.findall("[A-Z]", file2)
    # dict pour le savoir si c'est => ou <=>
    dicEqu = implicationDic(equTab)
    # dictionnaire des lettres avec leurs valeurs
    dic = letterDicValue(equalTab, letterFile)
    # putLettersToTrue(dic, equal)
    printAll(dicEqu, dic, leftTab, rightTab, equalTab, queryTab, letterFile, equTab, letterLine)
    # determineBool(left, right, dicEqu, dic)
    #dict indique la position des queries
    dict = findQueryLetter(queryTab, leftTab, rightTab)
    parseQuery(dict, leftTab, rightTab, dic, queryTab, lineTab)

if __name__ == "__main__":
    main(sys.argv[1:])

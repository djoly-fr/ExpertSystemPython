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

def letterForEachLine(file):
    # tableau tous les lettre pour chaque ligne
    letterLine = []
    file_content = file.split('\n')
    for lines in file_content[0:]:
        reg = re.findall("[A-Z]", lines)
        letterLine.append(reg)
    return letterLine

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

def letterDicValue(equal, letterFile):
    # dictionnaire des lettres avec leurs valeurs
    dic = {}
    print("DicValue")
    for i in letterFile:
        print("i", i)
        if equal[0].find(i) != -1:
            dic[i] = {"letter": i, "val": True, "constant": True}
        else:
            dic[i] = {"letter": i, "val": False, "constant": None}
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
        # print (q)
        tmp = dic[q]["val"]
        if (tmp == None):
            print (q, "is undetermined")
        elif (tmp == True):
            print (q, "is True")
        else:
            print (q, "is False")

def not_rule(a):
    return (not a)


#je regarde si c'est superieur à deux caractères
def handleCalc(side, dic, dict):
    size = len(side)
    if size > 2:
        print ("size >2 ")
        return handleOperation(side, dic, dict)
    elif size <= 2:
        print ("size < 2")
        if side[0] == "!":
            return not dic[side[1]]["val"]
        else:
            return dic[side[0]]["val"]

#fonction qui repond a la query de type B + A => E | F
def solveQuery(dict, left, right, alphabet, query):
    Ret = collections.namedtuple('Ret', ['alpha', 'left'])
    r = Ret(alphabet, left=left)
    print("query", query)
    print("left", left)
    retExp = solveExp(r, dict, left)
    print("resultat de exp  ",retExp)
    return r

#fonction recursive qui resout les expression type Q + (A | (D + B) + H) + E
def solveExp(r, dict, str):

    print("__debut solve __")
    if str == "0" or str == "1":
        return str
    print("r ",r)
    str = fr.findParanthese(r, dict, str)
    str = fr.findExclamation(r, dict, str)
    str = fr.findAnd(r, dict, str)
    str = fr.findOr(r, dict, str)
    str = fr.findXor(r, dict, str)
    print ("_ fin a__", str)
    return str #return le string de l exp, a la fin on aura 0 ou 1

def parseQuery(dict, left, right, alphabet, query):
    print("dict " , dict)

    #dict indique la position des queries
    for key in dict:
        #on accede au contenu de la key de dict et il faut deux for pour ça
        print("dict[key]", dict[key]["right"])
        for value in dict[key]["right"]:
            print("left[value]", left[value])
            print("right[value]", right[value])
            #alphabet = solveQuery(alphabet, left, right, value,  )

            alphabet = solveQuery(dict, left[value], right[value], alphabet, query)
            #alphabet = handleLeftSide(dict, left[value], right[value], alphabet, query)
    return alphabet

def main(argv):
    file = open(argv[0], 'r')
    regex = re.compile(r"#.*", re.IGNORECASE)
    file2 = regex.sub("", file.read())
    file2 = file2.replace(" ", "")
    print(file2)
    left = re.findall(".*[A-Z]\s*(?=\=>)|.*[A-Z]\s*(?=<\=>)", file2)
    right = re.findall("(?<=\=>).*[A-Z]\s*(?=\n)|(?<=<\=>).*[A-Z]\s*(?=\n)", file2)
    equ = re.findall("=>|<=>", file2)
    equal = re.findall("(?<=\n=).*", file2)
    query = re.findall("(?<=\n\?).*", file2)
    #pour split le string en lettre
    # equal = list(equal[0])
    # tableau tous les lettre pour chaque ligne
    letterLine = letterForEachLine(file2)
    #toutes lettre du fichier avec doublon
    letterFile = []
    letterFile = re.findall("[A-Z]", file2)
    # dict pour le savoir si c'est => ou <=>
    dicEqu = implicationDic(equ)
    # dictionnaire des lettres avec leurs valeurs
    dic = letterDicValue(equal, letterFile)
    # putLettersToTrue(dic, equal)
    printAll(dicEqu, dic, left, right, equal, query, letterFile, equ, letterLine)
    # determineBool(left, right, dicEqu, dic)
    #dict indique la position des queries
    dict = findQueryLetter(query, left, right)

    parseQuery(dict, left, right, dic, query)

if __name__ == "__main__":
    main(sys.argv[1:])

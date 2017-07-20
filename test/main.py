#!/usr/bin/env python
# coding: utf-8
import re
import sys

class Rule:
    def and_rule(a, b):
        print("and")
        return (a and b)

    def impl(a):
        if a:
            return (True)
        else:
            return (None)

    def xor_rule(a, b):
        return ((a and not b) or (not a and b))

    def or_rule(a, b):
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
    for i in letterFile:
        if equal[0].find(i) != -1:
            dic[i] = {"letter": i, "val": True, "constant": True}
        else:
            dic[i] = {"letter": i, "val": False, "constant": None}
    return dic

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

def handleOperation(side, dic, dict):
    size = len(side)
    for index in side:
        i = index.find("+")
        print ("i", i)
        if i >= 0:
            print(index)
            #prendre l'element inferieur et l'element superieur pour faire le calcul
        else:
            print("let")
    return True
    #mettre à solved toutes les lignes où on a trouvé une solution
    #tant que ce n'est pas solved on boucle

def handleCalc(side, dic, dict):
    size = len(side)
    if size > 2:
        print ("size >2 ")
        return handleOperation(side, dic, dict)
    elif size <= 2:
        print ("< 2")
        return dic[side[0]]["val"]

def handleLeftSide(dict, left, right, dic, query):
    # print ("d")
    i = 0
    index = 0
    result = None
    lcalc = None
    rcalc = None
    l = list(left)
    r = list(right)
    for i in l:
        if (i >= 'A' and i <= 'Z'):
            # print(dic[i]["val"])
            # result = dic[i]["val"]
            result = handleCalc(l, dic, dict)
            print (dic[r[0]]["val"])
            dic[r[0]]["val"] = result
            print (dic[r[0]]["val"])
        index += 1
    queryResult(query, dic)
    return dic

def solveQuery(dict, left, right, dic, query):
    # print ("b")
    for key in dict:
        print(dict[key]["right"])
        for value in dict[key]["right"]:
            print(left[value])
            dic = handleLeftSide(dict, left[value], right[value], dic, query)
    return dic

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
    equal = list(equal[0])
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
    dict = findQueryLetter(query, left, right)
    solveQuery(dict, left, right, dic, query)

if __name__ == "__main__":
    main(sys.argv[1:])

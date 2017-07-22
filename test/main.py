#!/usr/bin/env python
# coding: utf-8
import re
import sys

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
    for i in letterFile:
        if equal[0].find(i) != -1:
            dic[i] = {"letter": i, "val": True, "constant": True}
        else:
            dic[i] = {"letter": i, "val": False, "constant": None}
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

def handleOperation(side, dic, dict):
    result = None
    rnot = None
    ind = 0
    for current, last in zip(side[1:], side):
        # diff = current - last
        print ("last", last)
        print ("current", current)
        not_ = last.find("!")
        add_ = last.find("+")
        or_ = last.find("|")
        xor_ = last.find("^")
        if current.find("!") >= 0:
            if add_ >= 0:
                ind = 1
            elif or_ >= 0:
                ind = 2
            elif xor_ >= 0:
                ind = 3
        print("ind", ind)
        if add_ >= 0 and result != None and ind != 1:
            print("bonjour")
            and_rule(result, dic[current]["val"])
        elif not_ >= 0 and ind == 1:
            print("lol")
            and_rule(result, not dic[current]["val"])
            ind = 0
        elif or_ >= 0 and result != None and ind != 2:
            or_rule(result, dic[current]["val"])
        elif not_ >= 0 and ind == 2:
            or_rule(result, dic[current]["val"])
            ind = 0
        elif xor_ >= 0 and result != None and ind != 3:
            xor_rule(result, dic[current]["val"])
        elif not_ >= 0 and ind == 3:
            xor_rule(result, dic[current]["val"])
            ind = 0
        # elif not_ >= 0:
        #     rnot = not_rule(dic[current]["val"])
        else:
            print("else")
            if  ind == 0 and dic[last]["val"] != None:
                print("hello")
                result = dic[last]["val"]
                print(result)
        print("result", result)
    return result
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
    i = 0
    index = 0
    result = None
    lcalc = None
    rcalc = None
    l = list(left)
    r = list(right)
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
        print("hello", dict[key]["right"])
        for value in dict[key]["right"]:
            print("bonjour", left[value])
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

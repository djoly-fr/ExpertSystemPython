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
def solveQuery(dict, left, right, alphabet, value):
    Ret = collections.namedtuple('Ret', ['alpha', 'left'])
    r = Ret(alphabet, left=left[value])
    print("left", left)
    if len(left[value]) > 1:
        retExp = solveExp(r, dict, left[value], left, right)
    else:
        # print("left0", left[0])
        if alphabet[left[0]]["val"] == True:
            retExp = "1"
        else:
            retExp = "0"
    print("resultat de exp  ",retExp)
    r = Ret(alphabet, left=retExp)
    return r

#fonction recursive qui resout les expression type Q + (A | (D + B) + H) + E
def solveExp(r, dict, str, left, right):
    print("__debut solve __")
    if str == "0" or str == "1":
        return str
    print("r ",r)
    str = fr.findParanthese(r, dict, str, left, right)
    str = fr.findExclamation(r, dict, str, left, right)
    str = fr.findAnd(r, dict, str, left, right)
    str = fr.findOr(r, dict, str, left, right)
    str = fr.findXor(r, dict, str, left, right)
    return str #return le string de l exp, a la fin on aura 0 ou 1

#bruteforce pour le coté droit, il teste True, apres False
def solveRightSide(dict, left, right, alphabet, value):
    Ret = collections.namedtuple('Ret', ['alpha', 'left'])
    r = Ret(alphabet, left=left)
    print ("+++++++++++entré+++++++++++", value, alphabet[value]["val"])
    if len(right) > 1:
        print("_____1______")
        alphabet[value]["val"] = True
        r = Ret(alphabet, left=left)
        str = solveExp(r, dict, right, left, right)
        if str != left:
            print("_____2______")
            alphabet[value]["val"] = False
            r = Ret(alphabet, left=left)
            str = solveExp(r, dict, right, left, right)
            if str != left:
                print("_____3______")
                alphabet[value]["val"] = None
                r = Ret(alphabet, left=left)
        else:
            print("_____4______")
            alphabet[value]["val"] = False
            r = Ret(alphabet, left=left)
            str = solveExp(r, dict, right, left, right)
            if str == left:
                print("_____5______")
                alphabet[value]["val"] = None
                r = Ret(alphabet, left=left)
            else:
                alphabet[value]["val"] = True
                r = Ret(alphabet, left=left)
                # str = solveExp(r, dict, right)
    else:
        if left == "1":
            alphabet[value]["val"] = True
        else:
            alphabet[value]["val"] = False
    alphabet[value]["constant"] = True
    print ("sorti", value,  alphabet[value]["val"])
    return r

def parseRightLetter(letter, left, right, r):
    print("___parseRightLetter___", letter)
    tab = findLetterRightSide(letter, right)
    Ret = collections.namedtuple('Ret', ['alpha', 'left'])
    print(tab)
    for line in tab:
        r = Ret(r.alpha, left=left[line])
        r = solveQuery(dict, left[line], right[line], r.alpha, line)
        left[line] = r.left
        print ("rightletter", left, left[line])
        r = solveRightSide({}, left[line], right[line], r.alpha, letter)
    # print ("CCCCCJJJDJDSNVLSDNVLDLKVNDFLNVKFDNVKLF")
    return r

def parseQuery(dict, left, right, alphabet, query):
    Ret = collections.namedtuple('Ret', ['alpha', 'left'])
    #dict indique la position des queries
    for key in dict:
        #on accede au contenu de la key de dict et il faut deux for pour ça
        print("dict[key]", dict[key]["right"])
        for value in dict[key]["right"]:
            print("left[value]", left[value])
            print("right[value]", right[value])
            r = Ret(alphabet, left=left[value])
            #alphabet = solveQuery(alphabet, left, right, value,  )
            r = solveQuery(dict, left, right, alphabet, value)
            left[value] = r.left
            solveRightSide(dict, left[value], right[value], alphabet, key)
            #alphabet = handleLeftSide(dict, left[value], right[value], alphabet, query)
    return alphabet

def main(argv):
    file = open(argv[0], 'r')
    regex = re.compile(r"#.*", re.IGNORECASE)
    file2 = regex.sub("", file.read())
    file2 = file2.replace(" ", "")
    print(file2)
    left = re.findall(".*[A-Z()!]\s*(?=\=>)|.*[A-Z]\s*(?=<\=>)", file2)
    right = re.findall("(?<=\=>).*[A-Z]\s*(?=\n)|(?<=<\=>).*[A-Z]\s*(?=\n)", file2)
    equ = re.findall("=>|<=>", file2)
    equal = re.findall("(?<=\n=).*", file2)
    query = re.findall("(?<=\n\?).*", file2)
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

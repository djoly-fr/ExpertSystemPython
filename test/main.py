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

# def determineBool(left, right, dicEqu, dic):
#     # print "a"
#     i = 0
#     for key in dic:
#         if dic[key]["val"] == True:
#             right[0]
#         i += 1

def printAll(dicEqu, dic, left, right, equal, query, letterFile, equ, letterLine):
    print "dicEqu", dicEqu
    print "left", left
    print "right", right
    print "ewu" ,equ
    print "letterLine" , letterLine
    print "equal[0]", equal
    print "query", query
    print "letterFile", letterFile
    print "dic", dic

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

if __name__ == "__main__":
    main(sys.argv[1:])

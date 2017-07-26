#!/usr/bin/env python
# coding: utf-8
import re
import sys
import collections
from main import *
import find_rule as fr

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
    r = Ret(alphabet, left=left)
    print("left", left)
    if len(left) > 1:
        retExp = solveExp(r, dict, left)
    else:
        if alphabet[left[0]]["val"] == True:
            retExp = "1"
        else:
            retExp = "0"
    print("resultat de exp  ",retExp)
    r = Ret(alphabet, left=retExp)
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
    return str #return le string de l exp, a la fin on aura 0 ou 1

def parseQuery(dict, left, right, alphabet, query):
    print("dict " , dict)
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
            r = solveQuery(dict, left[value], right[value], alphabet, value)
            left[value] = r.left
            #alphabet = handleLeftSide(dict, left[value], right[value], alphabet, query)
    return alphabet

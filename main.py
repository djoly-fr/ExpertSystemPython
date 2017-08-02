#!/usr/bin/env python
# coding: utf-8
from log import *
import re
import sys
import collections
# from find_rule import *
import find_rule as fr
# class Rule:
# #
# import logging
#
#
# #formatter = logging.Formatter("%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")
# formatter = logging.Formatter('[%(asctime)s] {%(filename)s:%(lineno)d} %(funcName)s %(levelname)s - %(message)s','%m-%d %H:%M:%S')
#
# handler = logging.StreamHandler() #logging.FileHandler("info.log", mode="a", encoding="utf-8")
#
# handler.setFormatter(formatter)
#
# # handler.setLevel(logging.DEBUG)
# handler.setLevel(logging.INFO)
#
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
# if not logger.handlers:
#     logger.addHandler(handler)

def and_rule(a, b):
    ret = a and b
    logger.debug("and {} {} {} ".format(a, b, ret))
    return ret

def impl(a):
    if a:
        return (True)
    else:
        return (None)

def xor_rule(a, b):
    ret = (a and not b) or (not a and b)
    logger.debug("xor {} {} {} ".format( a, b, ret))
    return ((a and not b) or (not a and b))

def or_rule(a, b):
    ret = a or b
    logger.debug("or {} {} {} ".format(a, b, ret))
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
    for i in letterFile:
        # logger.debug("i {}".format(i))
        if equal[0].find(i) != -1:
            dic[i] = {"letter": i, "val": True, "constant": True}
        else:
            dic[i] = {"letter": i, "val": False, "constant": False}
    dic["1"] = {"letter": "1", "val": True, "constant": True}
    dic["0"] = {"letter": "0", "val": False, "constant": True}
    logger.debug("DicValue {}".format(dic))
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
                    logger.debug("non")
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
    logger.debug("dicEqu {}".format(dicEqu))
    logger.debug("left {}".format(left))
    logger.debug("right {}".format(right))
    logger.debug("ewu {}".format(equ))
    logger.debug("letterLine {}".format(letterLine))
    logger.debug("equal[0] {}".format(equal))
    logger.debug("query {}".format(query))
    logger.debug("letterFile {}".format(letterFile))
    logger.debug("dic {}".format( dic))


#fonction qui repond a la query de type B + A => E | F
def solveQuery(dict, leftTab, rightTab, alphabet, line, lineTab):
    Ret = collections.namedtuple('Ret', ['alpha', 'left'])
    logger.debug('dans SolveQuery')
    logger.debug("left {} value {}".format(leftTab, line))
    r = Ret(alphabet, left=leftTab[line])
    logger.debug("left {}".format(leftTab))
    if len(leftTab[line]) > 1:
        retExp = solveExp(r, dict, leftTab[line], leftTab, rightTab, lineTab)
    else:
        if alphabet[leftTab[line]]["constant"] == False:
            # print ("enfin")
            r = parseRightLetter(alphabet[leftTab[line]]["letter"], leftTab, rightTab, r, lineTab)
            retExp = "1" if r.alpha[leftTab[line]]["val"] == True else "0"
            logger.debug("retExp {}".format(retExp))
        elif alphabet[leftTab[line]]["val"] == True: # j'ai ecrit 0 au lieu de line
            logger.debug("bonjour {}".format(alphabet[leftTab[line]]))
            retExp = "1"
        else:
            retExp = "0"
    logger.debug("resultat de exp  {}".format(retExp))
    r = Ret(alphabet, left=retExp)
    return r

#fonction recursive qui resout les expression type Q + (A | (D + B) + H) + E
def solveExp(r, dict, currentLine, leftTab, rightTab, lineTab):
    logger.debug("__debut solve __")
    if currentLine == "0" or currentLine == "1":
        return currentLine
    logger.debug("r {}".format(r))
    currentLine = fr.findParanthese(r, dict, currentLine, leftTab, rightTab, lineTab)
    currentLine = fr.findExclamation(r, dict, currentLine, leftTab, rightTab, lineTab)
    currentLine = fr.findAnd(r, dict, currentLine, leftTab, rightTab, lineTab)
    currentLine = fr.findOr(r, dict, currentLine, leftTab, rightTab, lineTab)
    currentLine = fr.findXor(r, dict, currentLine, leftTab, rightTab, lineTab)
    return currentLine   #return le string de l exp, a la fin on aura 0 ou 1

#bruteforce pour le coté droit, il teste True, apres False
def solveRightSide(dict, leftTab, rightTab, alphabet, line, letter, lineTab):
    Ret = collections.namedtuple('Ret', ['alpha', 'left'])
    logger.debug("+++++++++++entré+++++++++++{}{}{}".format(line, alphabet[letter]["val"], letter))
    logger.debug("leftTab".format(leftTab))
    r = Ret(alphabet, left=leftTab[line])
    logger.debug("+++++++++++entré+++++++++++|{}|{}|".format(rightTab[line], len(rightTab[line].replace(r"\s    ", ""))))
    if len(rightTab[line]) > 1:
        logger.debug("_____1______")
        alphabet[letter]["val"] = True
        r = Ret(alphabet, left=leftTab[line])
        str = solveExp(r, dict, rightTab[line], leftTab, rightTab, lineTab)
        if str != leftTab[line]:
            logger.debug("_____2______")
            alphabet[letter]["val"] = False
            r = Ret(alphabet, left=leftTab[line])
            str = solveExp(r, dict, rightTab[line], leftTab, rightTab, lineTab)
            if str != leftTab[line]:
                logger.debug("_____3______")
                alphabet[letter]["val"] = None
                r = Ret(alphabet, left=leftTab[line])
        else:
            logger.debug("_____4______")
            alphabet[letter]["val"] = False
            r = Ret(alphabet, left=leftTab[line])
            str = solveExp(r, dict, rightTab[line], leftTab, rightTab, lineTab)
            if str == leftTab[line]:
                logger.debug("_____5______")
                alphabet[letter]["val"] = None
                r = Ret(alphabet, left=leftTab[line])
            else:
                alphabet[letter]["val"] = True
                r = Ret(alphabet, left=leftTab[line])
    else:
        #gestion des conflit entre ligne
        if alphabet[letter]["constant"] == True:
            if alphabet[letter]["val"] == True and leftTab[line] == "0" :
                alphabet[letter]["val"] = None
            elif alphabet[letter]["val"] == False and leftTab[line] == "1":
                alphabet[letter]["val"] = None
            return r
        if leftTab[line] == "1":
            alphabet[letter]["val"] = True
            logger.debug("here".format(letter))
        else:
            logger.debug(leftTab[line])
            alphabet[letter]["val"] = False
            logger.debug("la {}".format(letter))
    alphabet[letter]["constant"] = True
    logger.debug("sorti {} {}".format(line, alphabet[letter]["val"]))
    return r

def parseRightLetter(letter, leftTab, rightTab, r, lineTab):
    logger.debug("___parseRightLetter___ {}".format(letter))
    tab = findLetterRightSide(letter, rightTab)
    Ret = collections.namedtuple('Ret', ['alpha', 'left'])
    logger.debug(tab)
    for line in tab:
        if lineTab[line] == False:
            r = Ret(r.alpha, left=leftTab[line])
            r = solveQuery(dict, leftTab, rightTab, r.alpha, line, lineTab)
            leftTab[line] = r.left
            lineTab[line] = True
            logger.debug("lineTab[line] {} {} ".format(lineTab[line], line))
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
        # logger.debug("dict[letter] {}".format(dict[letter]["right"]))
        for line in dict[letter]["right"]:
            if lineTab[line] == False:
                # print ("line", leftTab[line])
                # logger.debug('value {}'.format(line))
                # logger.debug("left[line] {}".format(leftTab[line]))
                # logger.debug("right[line] {}".format(rightTab[line]))
                r = Ret(alphabet, left=leftTab[line])
                #alphabet = solveQuery(alphabet, left, right, value,  )
                r = solveQuery(dict, leftTab, rightTab, alphabet, line, lineTab)
                leftTab[line] = r.left
                lineTab[line] = True
                # logger.debug("lineTab []".format(lineTab))
                logger.debug("lineTab {}".format(lineTab))
                solveRightSide(dict, leftTab, rightTab, alphabet, line, letter, lineTab)
                #alphabet = handleLeftSide(dict, left[value], right[value], alphabet, query)
        logger.debug("lineTab final {}".format(lineTab))
    queryResult(queryTab, alphabet)
    return alphabet

def main(argv):
    file = open(argv[0], 'r')
    regex = re.compile(r"#.*", re.IGNORECASE)
    file2 = regex.sub("", file.read())
    file2 = file2.replace(" ", "")


    logger.debug('file {}'.format(file2))
    while file2.find('\n\n') != -1:
        file2 = file2.replace('\n\n', '\n')
    logger.debug('file {}'.format(file2))

    leftTab = re.findall(".*[A-Z()!]\s*(?=\=>)|.*[A-Z]\s*(?=<\=>)", file2)
    rightTab = re.findall("(?<=\=>).*[A-Z]\s*(?=\n)|(?<=<\=>).*[A-Z]\s*(?=\n)", file2)
    equTab = re.findall("=>|<=>", file2)
    equalTab = re.findall("(?<=\n=).*", file2)
    queryTab = re.findall("(?<=\n\?).*", file2)
    # tableau tous les lettre pour chaque ligne
    letterLine = letterForEachLine(file2)
    # logletterLine
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

#logle resultat de la query
def queryResult(query, dic):
    q = list(query[0])
    tmp = None
    for q in q:
        tmp = dic[q]["val"]
        if (tmp == None):
            logger.info("{} is undetermined".format(q))
        elif (tmp == True):
            logger.info("{} is True".format(q))
        else:
            logger.info("{} is False".format(q))


if __name__ == "__main__":
    main(sys.argv[1:])

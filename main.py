#!/usr/bin/env python
# coding: utf-8
from log import *
import re
import sys
import collections
import copy
# from find_rule import *
import find_rule as fr
import random

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
    #logger.debug("and {} {} {} ".format(a, b, ret))
    return ret

def impl(a):
    if a:
        return (True)
    else:
        return (None)

def xor_rule(a, b):
    ret = (a and not b) or (not a and b)
    #logger.debug("xor {} {} {} ".format( a, b, ret))
    return ret

def or_rule(a, b):
    ret = a or b
    #logger.debug("or {} {} {} ".format(a, b, ret))
    return ret

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
    # logger.debug("DicValue {}".format(dic))
    return dic

#pour avoir la position des lettres de la query
def findQueryLetter(query, left, right):
    dict = {}
    lq = list(query[0])
    i = 0
    tab = []

    for l in lq:
        i = 0
        tab = []
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

def letterInRight(right):
    listLetter = set(re.findall("[A-Z]", right))
    logger.debug('ret letter in right {}'.format(listLetter))
    return listLetter

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
def solveQuery(dict, leftTab, rightTab, alphabet, line, lineTab, equTab):
    Ret = collections.namedtuple('Ret', ['alpha', 'left'])
    r = Ret(alphabet, left=leftTab[line])
    # logger.debug("left {}".format(leftTab))
    if len(leftTab[line]) > 1:
        retExp = solveExp(r, dict, leftTab[line], leftTab, rightTab, lineTab, equTab)
    else:
        if alphabet[leftTab[line]]["constant"] == False:
            # print ("enfin")
            r = parseRightLetter(alphabet[leftTab[line]]["letter"], leftTab, rightTab, r, lineTab, equTab)
            retExp = "1" if r.alpha[leftTab[line]]["val"] == True else "0"
            # logger.debug("resultat retExp{}".format(retExp))
        elif alphabet[leftTab[line]]["val"] == True: # j'ai ecrit 0 au lieu de line
            # logger.debug("bonjour {}".format(alphabet[leftTab[line]]))
            retExp = "1"
        else:
            retExp = "0"
    logger.debug("resultat de exp {} {} {} : gauche = {}".format(leftTab[line], equTab[line], rightTab[line], retExp))
    r = Ret(alphabet, left=retExp)
    return r

#fonction recursive qui resout les expression type Q + (A | (D + B) + H) + E
def solveExp(r, dict, currentLine, leftTab, rightTab, lineTab, equTab):
    # logger.debug("__debut solve __")
    if currentLine == "0" or currentLine == "1":
        return currentLine
    # logger.debug("r {}".format(r))
    currentLine = fr.findParanthese(r, dict, currentLine, leftTab, rightTab, lineTab, equTab)
    currentLine = fr.findExclamation(r, dict, currentLine, leftTab, rightTab, lineTab, equTab)
    currentLine = fr.findAnd(r, dict, currentLine, leftTab, rightTab, lineTab, equTab)
    currentLine = fr.findOr(r, dict, currentLine, leftTab, rightTab, lineTab, equTab)
    currentLine = fr.findXor(r, dict, currentLine, leftTab, rightTab, lineTab, equTab)
    return currentLine   #return le string de l exp, a la fin on aura 0 ou 1

#random degueu
def recurs(tab, number):
    i = 0
    tab2 = []
    for i in range(0, number):
        rand = random.randint(0, 1)
        if rand == 1:
            tab2.append(True)
        else:
            # print rand
            tab2.append(False)
    if tab2 not in tab:
        # print ("ok", tab2)
        tab.append(tab2)
    return tab

def random_tab(nbLetter):
    tab = []
    i = 0
    # nbLetter = 10
    pb = pow(2, nbLetter)
    # print 'pb' , pb
    while (len(tab) < pb):
        tab = recurs(tab, nbLetter)
        i += 1
    # print tab
    # print len(tab)
    # print i
    return tab


def fetchVarLetter(dict, leftTab, rightTab, alphabet, line, lineTab, equTab):
    rightLetter = re.findall("[A-Z]", rightTab[line])
    Ret = collections.namedtuple('Ret', ['letterTab', 'randomTab'])
    tab = []
    for letter in rightLetter:
        if alphabet[letter]["constant"] == False:
            if letter not in tab:
                tab.append(letter)
    randomTab = random_tab(len(tab))
    r = Ret(tab, randomTab= randomTab)
    return r

#bruteforce pour le coté droit, il teste True, apres False
def solveRightSide(dict, leftTab, rightTab, alphabet, line, lineTab, equTab):



    if equTab[line] == '=>':
        # logger.debug('dans implication')
        return solveImplicationRight2(dict, leftTab, rightTab, alphabet, line, lineTab, equTab)
    elif equTab[line] == '<=>':
        # logger.debug('dans equivalence')
        return solveEquivalenceRight2(dict, leftTab, rightTab, alphabet, line, lineTab, equTab)
    else:
        logger.error('ni implication ni equivqlence')
    return

def solveEquivalenceRight(dict, leftTab, rightTab, alphabet, line, letter, lineTab, equTab):
    Ret = collections.namedtuple('Ret', ['alpha', 'left'])
    r = Ret(alphabet, left=leftTab[line])
    const = alphabet[letter]["val"]
    logger.debug("dans solveEquivalenceRight \n {}{}{} letter: {}{}".format(leftTab[line],equTab[line], rightTab[line], letter,  alphabet[letter]["val"]))
    if len(rightTab[line]) > 1:
        alphabet[letter]["val"] = True
        r = Ret(alphabet, left=leftTab[line])
        str = solveExp(r, dict, rightTab[line], leftTab, rightTab, lineTab, equTab)
        if str != leftTab[line]:
            alphabet[letter]["val"] = False
            r = Ret(alphabet, left=leftTab[line])
            str = solveExp(r, dict, rightTab[line], leftTab, rightTab, lineTab, equTab)
            if str != leftTab[line]:
                alphabet[letter]["val"] = None
                r = Ret(alphabet, left=leftTab[line])
        else:
            alphabet[letter]["val"] = False
            r = Ret(alphabet, left=leftTab[line])
            str = solveExp(r, dict, rightTab[line], leftTab, rightTab, lineTab, equTab)
            if str == leftTab[line]:
                alphabet[letter]["val"] = None
                r = Ret(alphabet, left=leftTab[line])
            else:
                alphabet[letter]["val"] = True
                r = Ret(alphabet, left=leftTab[line])
    else:
        letter = rightTab[line]
        #gestion des conflit entre ligne
        if alphabet[letter]["constant"] == True:
            if const != alphabet[letter]["val"]:
                logger.info("Two values for : {}".format(letter))
                sys.exit(0)
            if alphabet[letter]["val"] == True and leftTab[line] == "0" :
                alphabet[letter]["val"] = None
            elif alphabet[letter]["val"] == False and leftTab[line] == "1":
                alphabet[letter]["val"] = None
                logger.debug("sortie \n solveEquivalenceRight \n {}{}{} letter: {}{}".format(leftTab[line],equTab[line], rightTab[line], letter,  alphabet[letter]["val"]))
            return r
        if leftTab[line] == "1":
            alphabet[letter]["val"] = True
        else:
            alphabet[letter]["val"] = False
    alphabet[letter]["constant"] = True
    logger.debug("sortie \n solveEquivalenceRight \n {}{}{} letter: {}{}".format(leftTab[line],equTab[line], rightTab[line], letter,  alphabet[letter]["val"]))
    # print(dict, '|' , leftTab, '|' ,  rightTab,  '|' , alphabet, '|' ,  line, '|' ,  letter, '|' ,  lineTab)
    return r

def solveEquivalenceRight2(dict, leftTab, rightTab, alphabet, line, lineTab, equTab):
    Ret = collections.namedtuple('Ret', ['alpha', 'left'])
    r = Ret(alphabet, left=leftTab[line])

    if leftTab[line] == "0":
        tmp = False
    else:
        tmp = True

    if len(rightTab[line]) > 1:
        possiblility = fetchVarLetter(dict, leftTab, rightTab, alphabet, line, lineTab, equTab)
        logger.debug('possibility {}'.format(possiblility))
        logger.debug("-------------dans brute force ----------------- \n {}{}{} ".format(leftTab[line], equTab[line],
                                                                                         rightTab[line]))
        for lineRand in possiblility.randomTab:
            for i in range(0, len(possiblility.letterTab)):
                alphabet[possiblility.letterTab[i]]["val"] = lineRand[i]
            str = solveExp(r, dict, rightTab[line], leftTab, rightTab, lineTab, equTab)
            logger.debug('brute force :  str: {} '.format(str))
            if str == leftTab[line]:
                for i in range(0, len(possiblility.letterTab)):
                    alphabet[possiblility.letterTab[i]]["constant"] = True
                r = Ret(alphabet, left=leftTab[line])
                break
    else:
        letter = rightTab[line]
        #gestion des conflit entre ligne
        if alphabet[letter]["constant"] == True:
            if tmp != alphabet[letter]["val"]:
                logger.info("Two values for : {}".format(letter))
                sys.exit(0)
            if alphabet[letter]["val"] == True and leftTab[line] == "0" :
                alphabet[letter]["val"] = None
            elif alphabet[letter]["val"] == False and leftTab[line] == "1":
                alphabet[letter]["val"] = None
                logger.debug("sortie \n solveEquivalenceRight \n {}{}{} letter: {}{}".format(leftTab[line],equTab[line], rightTab[line], letter,  alphabet[letter]["val"]))
            return r
        if leftTab[line] == "1":
            alphabet[letter]["val"] = True
        else:
            alphabet[letter]["val"] = False
        alphabet[letter]["constant"] = True
    logger.debug("sortie \n solveEquivalenceRight \n {}{}{} ".format(leftTab[line],equTab[line], rightTab[line]))
    return r


def solveImplicationRight2(dict, leftTab, rightTab, alphabet, line, lineTab, equTab):

    Ret = collections.namedtuple('Ret', ['alpha', 'left'])
    #logger.debug("dans solveImplicationRight \n {}{}{} ".format(leftTab[line],equTab[line], rightTab[line]))
    r = Ret(alphabet, left=leftTab[line])

    # si gauche 0 les letter variable a droite sont none
    if leftTab[line] == "0":
        listLetterRight = letterInRight(rightTab[line])
        for letter in listLetterRight:
            if alphabet[letter]['constant'] == False:
                alphabet[letter]['val'] = None
        r = Ret(alphabet, left=leftTab[line])
        return r

    if len(rightTab[line]) > 1:
        possiblility = fetchVarLetter(dict, leftTab, rightTab, alphabet, line, lineTab, equTab)
        logger.debug('possibility {}'.format(possiblility))
        logger.debug("-------------dans brute force ----------------- \n {}{}{} ".format(leftTab[line],equTab[line], rightTab[line]))
        for lineRand in possiblility.randomTab:
            for i in range(0, len(possiblility.letterTab)):
                alphabet[possiblility.letterTab[i]]["val"] = lineRand[i]
            str = solveExp(r, dict, rightTab[line], leftTab, rightTab, lineTab, equTab)
            logger.debug('brute force :  str: {} '.format(str))
            if str == leftTab[line]:
                for i in range(0, len(possiblility.letterTab)):
                    alphabet[possiblility.letterTab[i]]["constant"] = True
                r = Ret(alphabet, left=leftTab[line])
                break
    else:
        letter = rightTab[line]

        if leftTab[line] == '0':
            alphabet[letter]["val"] = None
            return r

        #gestion des conflit entre ligne
        if alphabet[letter]["constant"] == True:
            # if alphabet[letter]["val"] == True and leftTab[line] == "0" :
            #     alphabet[letter]["val"] = None
            # elif alphabet[letter]["val"] == False and leftTab[line] == "1":
            # if const != alphabet[letter]["val"]
            if alphabet[letter]["val"] == False and leftTab[line] == "1":
                logger.debug('conflit entre ligne')
                alphabet[letter]["val"] = None
            logger.debug("sortie2 solveImplicationRight \n {}{}{} letter: {}{}".format(leftTab[line],equTab[line], rightTab[line], letter,  alphabet[letter]["val"]))
            return r
        if leftTab[line] == "1":
            alphabet[letter]["val"] = True
            alphabet[letter]["constant"] = True
        else:
            logger.debug(leftTab[line])
            alphabet[letter]["val"] = None
    #logger.debug("sortie solveImplicationRight \n {}{}{} ".format(leftTab[line],equTab[line], rightTab[line]))
    return r



def solveImplicationRight(dict, leftTab, rightTab, alphabet, line, letter, lineTab, equTab):

    Ret = collections.namedtuple('Ret', ['alpha', 'left'])
    logger.debug("dans solveImplicationRight \n {}{}{} letter tester : {}".format(leftTab[line],equTab[line], rightTab[line], letter,  alphabet[letter]["val"]))
    r = Ret(alphabet, left=leftTab[line])
    const = alphabet[letter]["val"]
    if leftTab[line] == '0':
        alphabet[letter]["val"] = None
        return r
    if len(rightTab[line]) > 1:
        alphabet[letter]["val"] = True
        r = Ret(alphabet, left=leftTab[line])
        logger.debug("{}{}{} start solveExp test lettre : {} val: {}".format(leftTab[line], equTab[line],
                                                                                      rightTab[line], letter,
                                                                                      alphabet[letter]["val"], alphabet[letter]["val"] ))
        str = solveExp(r, dict, rightTab[line], leftTab, rightTab, lineTab, equTab)
        if str != leftTab[line]:
            alphabet[letter]["val"] = False
            r = Ret(alphabet, left=leftTab[line])
            logger.debug("{}{}{} start2 solveExp test lettre : {} val: {}".format(leftTab[line], equTab[line],
                                                                                 rightTab[line], letter,
                                                                                 alphabet[letter]["val"],
                                                                                 alphabet[letter]["val"]))
            str = solveExp(r, dict, rightTab[line], leftTab, rightTab, lineTab, equTab)
            if str != leftTab[line]:
                logger.debug('dans if {}')
                alphabet[letter]["val"] = None
                r = Ret(alphabet, left=leftTab[line])
        else:
            alphabet[letter]["val"] = False
            r = Ret(alphabet, left=leftTab[line])
            logger.debug("{}{}{} start3 solveExp test lettre : {} val: {}".format(leftTab[line], equTab[line],
                                                                                 rightTab[line], letter,
                                                                                 alphabet[letter]["val"],
                                                                                 alphabet[letter]["val"]))
            str = solveExp(r, dict, rightTab[line], leftTab, rightTab, lineTab, equTab)
            if str == leftTab[line]:
                alphabet[letter]["val"] = None
                r = Ret(alphabet, left=leftTab[line])
            else:
                alphabet[letter]["val"] = True
                r = Ret(alphabet, left=leftTab[line])
    else:
        letter = rightTab[line]
        #gestion des conflit entre ligne
        if alphabet[letter]["constant"] == True:
            # if alphabet[letter]["val"] == True and leftTab[line] == "0" :
            #     alphabet[letter]["val"] = None
            # elif alphabet[letter]["val"] == False and leftTab[line] == "1":
            # if const != alphabet[letter]["val"]
            if alphabet[letter]["val"] == False and leftTab[line] == "1":
                logger.debug('conflit entre ligne')
                alphabet[letter]["val"] = None
            logger.debug("sortie2 solveImplicationRight \n {}{}{} letter: {}{}".format(leftTab[line],equTab[line], rightTab[line], letter,  alphabet[letter]["val"]))
            return r
        if leftTab[line] == "1":
            alphabet[letter]["val"] = True
            alphabet[letter]["constant"] = True
        else:
            logger.debug(leftTab[line])
            alphabet[letter]["val"] = None
    logger.debug("sortie solveImplicationRight \n {}{}{} letter: {} {}".format(leftTab[line],equTab[line], rightTab[line], letter,  alphabet[letter]["val"]))
    return r


def parseRightLetter(letter, leftTab, rightTab, r, lineTab, equTab):
    logger.debug("___parseRightLetter___ letter: {} {}".format(letter, r.alpha[letter]["val"]))
    tab = findLetterRightSide(letter, rightTab)
    Ret = collections.namedtuple('Ret', ['alpha', 'left'])
    logger.debug(tab)
    for line in tab:
        logger.debug('line {} {} {} '.format(leftTab[line],equTab[line], rightTab[line]))
        if lineTab[line] == False:
            r = Ret(r.alpha, left=leftTab[line])
            logger.debug("{} {} {} start solve query for letter {}".format(leftTab[line],equTab[line], rightTab[line], letter))
            r = solveQuery(dict, leftTab, rightTab, r.alpha, line, lineTab, equTab)
            leftTab[line] = r.left
            lineTab[line] = True
            logger.debug("{} {} {} start solverightside letter {}".format(leftTab[line], equTab[line], rightTab[line], letter))
            r = solveRightSide({}, leftTab, rightTab, r.alpha, line, letter, lineTab, equTab)
    return r

#dict : dict des lettres avec les lignes
#leftTab
#rightTab
#alphabet : dict des letter avec leur valeur et constant ou non
def parseQuery(dict, leftTab, rightTab, alphabet, queryTab, lineTab, equTab):
    Ret = collections.namedtuple('Ret', ['alpha', 'left'])
    #dict indique la position des queries
    # logger.debug("DICCT {}".format(dict))
    tmp = copy.deepcopy(alphabet)
    tmp2 = list(lineTab)
    for letter in dict:
        # tmp = alphabet.copy()
        # tmp2 = lineTab
        # logger.info("TMP2 {}".format(tmp2))
        logger.info("---------debut recherche letter {}---------- ".format(letter))
        logger.info("letter presente dans ligne {}---------- ".format(dict[letter]["right"]))
        #on accede au contenu de la key de dict et il faut deux for pour ça
        # logger.debug("dict[letter] {}".format(dict[letter]["right"]))
        for line in dict[letter]["right"]:
            if lineTab[line] == False:
                # print ("line", leftTab[line])
                # logger.debug('value {}'.format(line))
                # logger.debug("right[line] {}".format(rightTab[line]))
                # logger.debug("left {}".format(leftTab))
                # logger.debug("left[line] {}".format(leftTab[line]))

                r = Ret(alphabet, left=leftTab[line])
                #alphabet = solveQuery(alphabet, left, right, value,  )
                # logger.debug('r1 {}'.format(r))
                r = solveQuery(dict, leftTab, rightTab, alphabet, line, lineTab, equTab)
                leftTab[line] = r.left
                lineTab[line] = True
                # logger.debug("lineTab []".format(lineTab))
                # logger.debug("lineTab {}".format(lineTab))
                # logger.debug('r2 {}'.format(r))
                solveRightSide(dict, leftTab, rightTab, alphabet, line, letter, lineTab, equTab)
                # logger.debug('r3 {}'.format(r))
                # print alphabet
                # print alphabet
                #alphabet = handleLeftSide(dict, left[value], right[value], alphabet, query)
        logger.debug("lineTab final {}".format(lineTab))
        logger.info("{} is {}".format(letter, r.alpha[letter]["val"]))
        alphabet = copy.deepcopy(tmp)
        lineTab = list(tmp2)
    # queryResult(queryTab, alphabet)
    return alphabet

#
# Tri les lignes dans l ordre d execution
#dict : dict des lettres avec les lignes
#leftTab
#rightTab
#alphabet : dict des letter avec leur valeur et constant ou non
def parseQuery2(letter, dict, leftTab, rightTab, alphabet, queryTab, lineTab, equTab):
    #logger.info('parseQuery2 letter {}'.format(letter))
    ret = []

    # les ligne ou gauche na que des constant en premier
    for index in range(len(leftTab)):
        listLetterLeft = set(re.findall("[A-Z]", leftTab[index]))
        addLine = True
        for letter3 in listLetterLeft:
            if alphabet[letter3]['constant'] == False or lineTab[index] == True:
                addLine = False
                break
        if addLine:
            ret.append(index)
            lineTab[index] = True
            logger.debug('mode constant add line {} in ret'.format(index))

    tab = findLetterRightSide(letter, rightTab)

    for line in tab:
        if lineTab[line] == True:
            continue

        lineTab[line] = True
        listLetterLeft = set(re.findall("[A-Z]", leftTab[line]))
        logger.debug('listLetterLeft {}'.format(listLetterLeft))
        for letter2 in listLetterLeft:
            ret.extend(parseQuery2(letter2, dict, leftTab, rightTab, alphabet, queryTab, lineTab, equTab))
        for i in tab:
            if i not in ret:
                ret.append(i)
        #ret.extend(tab)
        logger.debug('mode findLetterRightSide add line {} in ret'.format(tab))

    return ret

def main(argv):

    if argv == []:
        logger.error("Pas de fichier en argument, exit")
        sys.exit(1)
    try:  # On essaye de convertir l'année en entier
        file = open(argv[0], 'r')
    except:
        print("Erreur lors de l ouverture du fichier,exit")
        sys.exit(1)

    print ('file', file)
    regex = re.compile(r"#.*", re.IGNORECASE)
    file2 = regex.sub("", file.read())
    file2 = file2.replace(" ", "")



    logger.debug('file\n {}'.format(file2))
    while file2.find('\n\n') != -1:
        file2 = file2.replace('\n\n', '\n')
    logger.debug('file\n {}'.format(file2))
    leftTab = re.findall(".*[A-Z()!]\s*(?=\=>)|.*[A-Z()!]\s*(?=<\=>)", file2)
    rightTab = re.findall("(?<=\=>).*[A-Z()!]\s*(?=\n)|(?<=<\=>).*[A-Z()!]\s*(?=\n)", file2)
    equTab = re.findall("=>|<=>", file2)
    equalTab = re.findall("(?<=\n=).*", file2)
    queryTab = re.findall("(?<=\n\?).*", file2)
    dict = findQueryLetter(queryTab, leftTab, rightTab)
    for letter in dict:
        logger.info('---- start Solve letter {}------'.format(letter))
        leftTab = re.findall(".*[A-Z()!]\s*(?=\=>)|.*[A-Z()!]\s*(?=<\=>)", file2)
        rightTab = re.findall("(?<=\=>).*[A-Z()!]\s*(?=\n)|(?<=<\=>).*[A-Z()!]\s*(?=\n)", file2)
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
        alphabet = letterDicValue(equalTab, letterFile)
        # putLettersToTrue(dic, equal)
        printAll(dicEqu, alphabet, leftTab, rightTab, equalTab, queryTab, letterFile, equTab, letterLine)
        # determineBool(left, right, dicEqu, dic)
        #dict indique la position des queries

        sortedLine = parseQuery2(letter, dict, leftTab, rightTab, alphabet, queryTab, lineTab, equTab)
        logger.debug('sorted Line {}'.format(sortedLine))
        for line in sortedLine:
            logger.info('-----solve line {} -----'.format(line))
            logger.debug("{} {} {}".format(leftTab[line], equTab[line], rightTab[line]))
          #  logger.debug('ret solveQuery {}'.format(r))
            r = solveQuery(dict, leftTab, rightTab, alphabet, line, lineTab, equTab)
            #logger.debug('ret r {}'.format(r))

            leftTab[line] = r.left
            lineTab[line] = True
            #logger.debug('ret r2 {}'.format(r))
            #logger.debug("leftTab {}".format(leftTab))
            solveRightSide(dict, leftTab, rightTab, alphabet, line, lineTab, equTab)
            #logger.debug('ret r3 {}'.format(r))

        logger.debug('ret solveQuery {}'.format(r))
        queryResult2(letter, alphabet)
            # RETURN BSQ
    file.close()

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

#logle resultat de la query pour une letter
def queryResult2(letter, dic):
    tmp = dic[letter]["val"]
    if (tmp == None):
        logger.info("\n|-------------------|\n"
                    "|                   |\n"
                    "|{} is undetermined  |\n"
                    "|                   |\n"
                    "|-------------------|".format(letter))
    elif (tmp == True):
        logger.info("\n|-------------------|\n"
                    "|                   |\n"
                    "|{} is True          |\n"
                    "|                   |\n"
                    "|-------------------|".format(letter))
    else:
        logger.info("\n|-------------------|\n"
                    "|                   |\n"
                    "|{} is False         |\n"
                    "|                   |\n"
                    "|-------------------|".format(letter))

if __name__ == "__main__":
    main(sys.argv[1:])

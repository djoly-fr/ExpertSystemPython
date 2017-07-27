import re
import sys
import collections
from main import *

def findAnd(r, dict, currentLine, leftTab, rightTab):
    print("__debut and__ ", currentLine)
    print("YYYYYYY", r)
    positionOP = currentLine.find('+')
    if positionOP == -1:
        return currentLine
    letter1 = currentLine[positionOP - 1]
    letter2 = currentLine[positionOP + 1]
    print("letter1", letter1, r.alpha[letter1]["constant"])
    if r.alpha[letter1]["constant"] == False:
        r = parseRightLetter(letter1, leftTab, rightTab, r)
    if r.alpha[letter2]["constant"] == False:
        r = parseRightLetter(letter2, leftTab, rightTab, r)
    print("bool" , r.alpha[letter1]['val'])
    result =  r.alpha[letter1]["val"] and r.alpha[letter2]["val"]
    print("result ", result)
    if result == True:
        result = "1"
    else:
        result = "0"
    sub = currentLine.replace(letter1+"+"+letter2, result, 1)
    #sub = str[:letter1]+result+str[letter2]
    print("sub" , sub)
    newstr = solveExp(r, dict, sub, leftTab, rightTab)
    print("newstr" , newstr)
    return newstr

def findExclamation(r, dict, currentLine, leftTab, rightTab):
    print("__debut exclamation__ ", currentLine)
    positionOP = currentLine.find('!')
    if positionOP == -1:
        return currentLine
    letter = currentLine[positionOP + 1]
    print("letter1", letter)
    print("bool" , r.alpha[letter]['val'])
    if r.alpha[letter]["constant"] == False:
        r = parseRightLetter(letter, leftTab, rightTab, r)
    result = not r.alpha[letter]["val"]
    print("result ", result)
    if result == True:
        result = "1"
    else:
        result = "0"
    sub = currentLine.replace("!"+letter, result, 1)
    #sub = str[:letter1]+result+str[letter2]
    print("sub" , sub)
    newstr = solveExp(r, dict, sub, leftTab, rightTab)
    print("newstr" , newstr)
    return newstr

def findOr(r, dict, currentLine, leftTab, rightTab):
    print("__debut Or__ ", currentLine)
    positionOP = currentLine.find('|')
    if positionOP == -1:
        return currentLine
    letter1 = currentLine[positionOP - 1]
    letter2 = currentLine[positionOP + 1]
    print("letter1", letter1 )
    if r.alpha[letter1]["constant"] == False:
        print ("letterLine1", letter1)
        r = parseRightLetter(letter1, leftTab, rightTab, r)
    if r.alpha[letter2]["constant"] == False:
        print ("letterLine2")
        r = parseRightLetter(letter2, leftTab, rightTab, r)
    print("bool" , r.alpha[letter1]['val'])
    print("bool" , r.alpha[letter1]['val'])
    result = or_rule(r.alpha[letter1]["val"], r.alpha[letter2]["val"])
    print("result ", result)
    if result == True:
        result = "1"
    else:
        result = "0"
    sub = currentLine.replace(letter1+"|"+letter2, result, 1)
    #sub = str[:letter1]+result+str[letter2]
    print("sub" , sub)
    newstr = solveExp(r, dict, sub, leftTab, rightTab)
    print("newstr" , newstr)
    return newstr

def findXor(r, dict, currentLine, leftTab, rightTab):
    print("__debut xor__ ", currentLine)
    positionOP = currentLine.find('^')
    if positionOP == -1:
        return currentLine
    letter1 = currentLine[positionOP - 1]
    letter2 = currentLine[positionOP + 1]
    print("letter1", letter1 )
    if r.alpha[letter1]["constant"] == False:
        print ("letterLine1", letter1)
        r = parseRightLetter(letter1, leftTab, rightTab, r)
    if r.alpha[letter2]["constant"] == False:
        print ("letterLine2")
        r = parseRightLetter(letter2, leftTab, rightTab, r)
    print("bool" , r.alpha[letter1]['val'])
    print("bool" , r.alpha[letter1]['val'])
    result = xor_rule(r.alpha[letter1]["val"], r.alpha[letter2]["val"])
    print("result ", result)
    if result == True:
        result = "1"
    else:
        result = "0"
    sub = currentLine.replace(letter1+"^"+letter2, result, 1)
    #sub = str[:letter1]+result+str[letter2]
    print("sub" , sub)
    newstr = solveExp(r, dict, sub, leftTab, rightTab)
    print("newstr" , newstr)
    return newstr

def findParanthese(r, dict, currentLine, leftTab, rightTab):
    print('str dans find paranthese ', currentLine)
    position1 = currentLine.find('(')
    if position1 == -1:
        return currentLine
    tmp = 1
    lenght = len(currentLine)
    print("len" , lenght)
    i = position1 + 1
    print("i" , i)
    print("str", currentLine)
    position2 = 0
    while(i < lenght):
        print("str[i]", currentLine[i])
        print("tmp", tmp)
        if currentLine[i] == '(':
            tmp += 1
        elif currentLine[i] == ')' and tmp == 1:
            position2 = i
            break
        elif currentLine[i] == ')' and tmp != 1:
            tmp -= 1
        i += 1
    print("position2", position2)
    sub = currentLine[position1+1:position2]
    print("sub ", sub)
    ret = solveExp(r, dict, sub, leftTab, rightTab)
    newstr = currentLine.replace("("+sub+")", ret, 1)
    print("printstr" , newstr)
    return newstr

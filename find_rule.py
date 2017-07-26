import re
import sys
import collections
from main import *

def findAnd(r, dict, str, left, right):
    print("__debut and__ ", str)
    print("YYYYYYY", r)
    positionOP = str.find('+')
    if positionOP == -1:
        return str
    letter1 = str[positionOP - 1]
    letter2 = str[positionOP + 1]
    print("letter1", letter1, r.alpha[letter1]["constant"])
    if r.alpha[letter1]["constant"] == False:
        print ("letterLine1", letter1)
        r = parseRightLetter(letter1, left, right, r)
    if r.alpha[letter2]["constant"] == False:
        print ("letterLine2")
        r = parseRightLetter(letter2, left, right, r)
    print("bool" , r.alpha[letter1]['val'])
    result =  r.alpha[letter1]["val"] and r.alpha[letter2]["val"]
    print("result ", result)
    if result == True:
        result = "1"
    else:
        result = "0"
    sub = str.replace(letter1+"+"+letter2, result, 1)
    #sub = str[:letter1]+result+str[letter2]
    print("sub" , sub)
    newstr = solveExp(r, dict, sub, left, right)
    print("newstr" , newstr)
    return newstr

def findExclamation(r, dict, str, left, right):
    print("__debut exclamation__ ", str)
    positionOP = str.find('!')
    if positionOP == -1:
        return str
    letter = str[positionOP + 1]
    print("letter1", letter)
    print("bool" , r.alpha[letter]['val'])
    if r.alpha[letter]["constant"] == False:
        r = parseRightLetter(letter, left, right, r)
    result = not r.alpha[letter]["val"]
    print("result ", result)
    if result == True:
        result = "1"
    else:
        result = "0"
    sub = str.replace("!"+letter, result, 1)
    #sub = str[:letter1]+result+str[letter2]
    print("sub" , sub)
    newstr = solveExp(r, dict, sub, left, right)
    print("newstr" , newstr)
    return newstr

def findOr(r, dict, str, left, right):
    print("__debut Or__ ", str)
    positionOP = str.find('|')
    if positionOP == -1:
        return str
    letter1 = str[positionOP - 1]
    letter2 = str[positionOP + 1]
    print("letter1", letter1 )
    if r.alpha[letter1]["constant"] == False:
        print ("letterLine1", letter1)
        r = parseRightLetter(letter1, left, right, r)
    if r.alpha[letter2]["constant"] == False:
        print ("letterLine2")
        r = parseRightLetter(letter2, left, right, r)
    print("bool" , r.alpha[letter1]['val'])
    print("bool" , r.alpha[letter1]['val'])
    result = or_rule(r.alpha[letter1]["val"], r.alpha[letter2]["val"])
    print("result ", result)
    if result == True:
        result = "1"
    else:
        result = "0"
    sub = str.replace(letter1+"|"+letter2, result, 1)
    #sub = str[:letter1]+result+str[letter2]
    print("sub" , sub)
    newstr = solveExp(r, dict, sub, left, right)
    print("newstr" , newstr)
    return newstr

def findXor(r, dict, str, left, right):
    print("__debut xor__ ", str)
    positionOP = str.find('^')
    if positionOP == -1:
        return str
    letter1 = str[positionOP - 1]
    letter2 = str[positionOP + 1]
    print("letter1", letter1 )
    if r.alpha[letter1]["constant"] == False:
        print ("letterLine1", letter1)
        r = parseRightLetter(letter1, left, right, r)
    if r.alpha[letter2]["constant"] == False:
        print ("letterLine2")
        r = parseRightLetter(letter2, left, right, r)
    print("bool" , r.alpha[letter1]['val'])
    print("bool" , r.alpha[letter1]['val'])
    result = xor_rule(r.alpha[letter1]["val"], r.alpha[letter2]["val"])
    print("result ", result)
    if result == True:
        result = "1"
    else:
        result = "0"
    sub = str.replace(letter1+"^"+letter2, result, 1)
    #sub = str[:letter1]+result+str[letter2]
    print("sub" , sub)
    newstr = solveExp(r, dict, sub, left, right)
    print("newstr" , newstr)
    return newstr

def findParanthese(r, dict, str, left, right):
    position1 = str.find('(')
    if position1 == -1:
        return str
    tmp = 1
    lenght = len(str)
    print("len" , lenght)
    i = position1 + 1
    print("i" , i)
    print("str", str)
    position2 = 0
    while(i < lenght):
        print("str[i]", str[i])
        print("tmp", tmp)
        if str[i] == '(':
            tmp += 1
        elif str[i] == ')' and tmp == 1:
            position2 = i
            break
        elif str[i] == ')' and tmp != 1:
            tmp -= 1
        i += 1
    print("position2", position2)
    sub = str[position1+1:position2]
    print("sub ", sub)
    ret = solveExp(r, dict, sub, left, right)
    newstr = str.replace("("+sub+")", ret, 1)
    print("printstr" , newstr)
    return newstr

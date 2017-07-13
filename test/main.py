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

class letter:
    boolean = None
    constant = None

def letter(l):
    # tab = [:]
    dic = {}
    dic['letter'] = l
    dic['val'] = False
    dic['constant'] = False
    return dic

    dic['A'] = {}

def main(argv):
    file = open(argv[0], 'r')
    regex = re.compile(r"#.*", re.IGNORECASE)
    file2 = regex.sub("", file.read())
    file2 = file2.replace(" ", "")
    # print(file2)
    left = re.findall(".*[A-Z]\s*(?=\=>)|.*[A-Z]\s*(?=<\=>)", file2)
    right = re.findall("(?<=\=>).*[A-Z]\s*(?=\n)|(?<=<\=>).*[A-Z]\s*(?=\n)", file2)
    equ = re.findall("=>|<=>", file2)
    equal = re.findall("(?<=\n=).*", file2)
    query = re.findall("(?<=\n\?).*", file2)





    # tableau tous les lettre pour chaque ligne
    letterLine = []
    file_content = file2.split('\n')
    for lines in file_content[0:]:
        reg = re.findall("[A-Z]", lines)
        letterLine.append(reg)

    #toutes lettre du fichier avec doublon
    letterFile = []
    letterFile = re.findall("[A-Z]", file2)

    # dictionnaire des lettres avec leurs valeurs
    dic = {}
    for i in letterFile:
        if equal[0].find(i) != -1:
            dic[i] = {"letter": i, "val": True, "constant":True}
        else:
            dic[i] = {"letter": i, "val": False, "constant":False}
    #for lines in left[0:]:
        # tab.append(re.findall("[A-Z]", lines))
    # equal = equal.split("[A-Z]", 1)

    # for c in equal:
    #     dic[c] = {"letter": c, "val": True, "constant":True}

    print "left", left
    print "right", right
    print equ
    print "letterLine" , letterLine
    print equal[0]

    print query
    print letterFile
    print dic
    # print(and_rule(True, True))
    # for i in query[0]:
    #     for e in letterLine:

    #    print i



if __name__ == "__main__":
    main(sys.argv[1:])

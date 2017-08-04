#!/usr/bin/env python
# coding: utf-8
import re
import sys
import collections
import copy
import random
import math
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

def random_tab(nbLetter)
    tab = []
    i = 0
    # nbLetter = 10
    pb = pow(2, nbLetter)
    print 'pb' , pb
    while (len(tab) < pb):
        tab = recurs(tab, nbLetter)
        i += 1
    print tab
    print len(tab)

    print i
    return tab

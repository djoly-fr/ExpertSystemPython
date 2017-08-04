import sys
from log import logger
import re


def checkFile(argv):

    if argv == []:
        logger.error("Pas de fichier en argument, exit")
        sys.exit(1)
    try:  # On essaye de convertir l'année en entier
        file = open(argv[0], 'r')
    except:
        print("Erreur lors de l ouverture du fichier,exit")
        sys.exit(1)

    regex = re.compile(r"#.*", re.IGNORECASE)
    file2 = regex.sub("", file.read())
    file2 = file2.replace(" ", "")

    logger.debug('file\n {}'.format(file2))
    while file2.find('\n\n') != -1:
        file2 = file2.replace('\n\n', '\n')
    logger.debug('file\n {}'.format(file2))

    split = file2.split('\n')
    logger.debug('split {}'.format(split))
    for line in split:
        logger.debug('test {}'.format(line))
        if line == '':
            logger.debug('string vide')
        elif '=>' in line or line[0] == '=' or line[0] == '?':
            logger.debug('{} ok'.format(line))
        else:
            logger.debug('error in line {}'.format(line))
            sys.exit(1)

    sys.exit(1)
    #check une seul ligne d initialisation
    equalTab = re.findall("(?<=\n=).*", file2)
    if len(equalTab) > 1:
        print("Erreur deux lignes d initialisation")
    sys.exit(1)

    # find = re.findall(".*[A-Z()!]\s*(?=\=>)|.*[A-Z()!]\s*(?=<\=>)", file2)
    # rightTab = re.findall("(?<=\=>).*[A-Z()!]\s*(?=\n)|(?<=<\=>).*[A-Z()!]\s*(?=\n)", file2)
    # equTab = re.findall("=>|<=>", file2)
    equalTab = re.findall("(?<=\n=).*", file2)
    # queryTab = re.findall("(?<=\n\?).*", file2)
    logger.debug('equTab {}'.format(equalTab))
    return file
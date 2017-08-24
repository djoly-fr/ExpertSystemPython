import logging

formatter = logging.Formatter('%(message)s','%m-%d %H:%M:%S')
handler = logging.StreamHandler()
handler.setFormatter(formatter)

#Choisir le niveau de log
handler.setLevel(logging.DEBUG)
# handler.setLevel(logging.INFO)
#
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
if not logger.handlers:
    logger.addHandler(handler)

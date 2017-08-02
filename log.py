


import logging


#formatter = logging.Formatter("%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")
formatter = logging.Formatter('[%(filename)s:%(lineno)d] %(funcName)s %(levelname)s - %(message)s','%m-%d %H:%M:%S')

handler = logging.StreamHandler() #logging.FileHandler("info.log", mode="a", encoding="utf-8")

handler.setFormatter(formatter)

# handler.setLevel(logging.DEBUG)
handler.setLevel(logging.INFO)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
if not logger.handlers:
    logger.addHandler(handler)


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
# handler.setLevel(logging.DEBUG)
#
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
# if not logger.handlers:
#     logger.addHandler(handler)
#
# class log:
#     def info(*args, logtype='info', sep=' '):
#         getattr(logger, logtype)(sep.join(str(a) for a in args))
#
#     def critical(*args, logtype='critical', sep=' '):
#         getattr(logger, logtype)(sep.join(str(a) for a in args))
#
#     def debug(*args, logtype='debug', sep=' '):
#         getattr(logger, logtype)(sep.join(str(a) for a in args))
import logging
import sys


def get_std_logger(name):
    logger = logging.getLogger(name)
    stdout = logging.StreamHandler(stream=sys.stdout)
    fmt = logging.Formatter(
    fmt=(
            '%(asctime)s '
            '[%(levelname)-8s] '
            '%(module)s:%(lineno)d - %(message)s'
        ),
        datefmt='%d-%m-%Y %I:%M:%S %p IST'
    )
    stdout.setFormatter(fmt)
    logger.addHandler(stdout)
    logger.setLevel(level=logging.DEBUG)
    return logger

def intro_ascii():
    return r'''

   _____         _    _  _____ _____               _____ ______ 
  / ____|   /\  | |  | |/ ____/ ____|       /\    / ____|  ____|
 | |  __   /  \ | |  | | (___| (___ ______ /  \  | (___ | |__   
 | | |_ | / /\ \| |  | |\___ \\___ \______/ /\ \  \___ \|  __|  
 | |__| |/ ____ \ |__| |____) |___) |    / ____ \ ____) | |____ 
  \_____/_/    \_\____/|_____/_____/    /_/    \_\_____/|______|
                                                                
                                                                

'''

# def get_json_logger(name, file):
#     logger = logging.getLogger(name)
#     stdout = logging.FileHandler(file)
#     fmt = logging.Formatter(
#     fmt=(   '{ '
#             '"time":"%(asctime)s",'
#             '"level":"%(levelname)-8s",'
#             '"message":"%(message)s",'
#             '"config": "%(config)s",'
#             '"status": "%(status)s"'
#             ' }'
#         ),
#         datefmt='%d-%m-%Y %I:%M:%S %p IST'
#     )
#     stdout.setFormatter(fmt)
#     logger.addHandler(stdout)
#     logger.setLevel(level=logging.DEBUG)
#     return logger



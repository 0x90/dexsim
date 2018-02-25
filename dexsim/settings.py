import os
import sys
import logging

# MAIN_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# with open(os.path.join(MAIN_PATH, 'datas', 'filters.txt')) as f:
#     FILTERS = f.read().splitlines()


MAIN_PATH = os.path.abspath(os.path.dirname(__file__))
BAKSMALI_PATH = os.path.join(MAIN_PATH, 'jar', 'baksmali.jar')
SMALI_PATH = os.path.join(MAIN_PATH, 'jar', 'smali.jar')

if not os.path.exists(SMALI_PATH):
    logging.error('Could not find %s' % SMALI_PATH)
    sys.exit(-1)

if not os.path.exists(BAKSMALI_PATH):
    logging.error('Could not find %s' % BAKSMALI_PATH)
    sys.exit(-1)

FILTERS_PATH = os.path.join(MAIN_PATH, 'data', 'filters.txt')

if not os.path.exists(FILTERS_PATH):
    logging.error('Could not find %s' % FILTERS_PATH)
    sys.exit(-1)

# TODO: locate java binary!
JAVA_PATH = 'java'

with open(FILTERS_PATH) as f:
    FILTERS_LIST = f.read().splitlines()


logging.info('Loaded %i filters' % len(FILTERS_LIST))

# log_path = os.path.join(MAIN_PATH, 'dexsim.log')
#
# logging.basicConfig(
#     level=logging.DEBUG,
#     filename=log_path,
#     format='%(asctime)s %(levelname)s %(name)s: %(message)s',
#     filemode='w')


DEBUG = False

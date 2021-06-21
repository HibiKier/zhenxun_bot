import os


try:
    DATABASE_URI = os.environ['DATABASE_URI']
except KeyError:
    DATABASE_URI = ''

try:
    TL_M_KEY = os.environ['TL_KEY']
except KeyError:
    TL_M_KEY = []


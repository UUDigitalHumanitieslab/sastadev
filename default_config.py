import logging
import os.path as op
from .sentence_parser import parse


# logging object
SDLOGGER = logging.getLogger()

# local directory
SD_DIR = op.dirname(op.abspath(__file__))

# Alpino
ALPINO_HOST = 'localhost'
ALPINO_PORT = 7001

# Function to parse a sentence with Alpino
# Should take a string as input and return an lxml.etree
PARSE_FUNC = parse

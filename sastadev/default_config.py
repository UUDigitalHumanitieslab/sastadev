import logging
import os.path as op

from sastadev import sentence_parser

# logging object
SDLOGGER = logging.getLogger()

# local directory
SD_DIR = op.dirname(op.abspath(__file__))

# Alpino
ALPINO_HOST = 'localhost'
ALPINO_PORT = 7001

# Function to parse a sentence with Alpino
# Should take a string as input and return an lxml.etree
PARSE_FUNC = sentence_parser.parse

import logging

from sastadev import SD_DIR, sentence_parser


class SastadevConfig:
    '''Class for keeping track of application configuration'''

    def __init__(self,
                 ALPINO_HOST: str = 'localhost',
                 ALPINO_PORT: int = 7001,
                 LOGGER=logging,
                 SD_DIR: str = SD_DIR,
                 DATAROOT: str = '.',
                 PARSE_FUNC=sentence_parser.parse
                 ):
        self.ALPINO_HOST = ALPINO_HOST
        self.ALPINO_PORT = ALPINO_PORT
        self.LOGGER = LOGGER
        self.SD_DIR = SD_DIR
        self.DATAROOT = DATAROOT
        self.PARSE_FUNC = PARSE_FUNC
        print('Configuration initiated.')


settings = SastadevConfig()

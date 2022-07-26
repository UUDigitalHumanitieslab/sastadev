'''
The *alpinoparsing* module provides functions for:

* parsing: .. autofunction::  alpinoparsing::parse
* previewing a parse tree: .. autofunction:: alpinoparsing::previewurl
'''

import re
import urllib.parse
import urllib.request

from lxml import etree  # type: ignore
from memoize import memoize

import logging
from typing import Optional
#from sastatypes import SynTree, URL

#from config import SDLOGGER
#from sastatypes import SynTree, URL

alpino_special_symbols_pattern = r'[\[\]]'
alpino_special_symbols_re = re.compile(alpino_special_symbols_pattern)

gretelurl = 'https://gretel.hum.uu.nl/api/src/router.php/parse_sentence/'
previewurltemplate = 'https://gretel.hum.uu.nl/ng/tree?sent={sent}&xml={xml}'

emptypattern = r'^\s*$'
emptyre = re.compile(emptypattern)


def isempty(sent: str) -> bool:
    '''
    The function *isempty* checke whether the input string *sent* is the null strin or consists of white space only.
    '''
    result = emptyre.match(sent) is not None
    return result


@memoize
#def parse(origsent: str, escape: bool = True) -> Optional[SynTree]:
def parse(origsent: str, escape: bool = True):

    '''
    The function *parse* invokes the alpino parser (over teh internet, so an intenrent connection is required) to parse
    the string *origsent*.
    The parameter *escape* can be used to escape symbols that have a special meaning for Alpino. Is default value is
    *True*.

    This function is memoised, which might give unexpected results since the output type is mutable. Be careful if
    the same input string is parsed twice and ther resulting objects should really be considered two different
    instances.!

    '''
    if isempty(origsent):
        return None
    if escape:
        sent = escape_alpino_input(origsent)
    else:
        sent = origsent
    encodedsent = urllib.parse.quote(sent)
    fullurl = gretelurl + encodedsent
    try:
        r1 = urllib.request.urlopen(fullurl)
    except urllib.request.HTTPError as e:
        logging.error('{}: parsing <{}> failed'.format(e, sent))
        return None
    except urllib.error.URLError as e:
        logging.error('{}: parsing <{}> failed'.format(e, sent))
        return None
    else:
        if 300 > r1.status >= 200:
            streebytes = r1.read()
            # print(streebytes.decode('utf8'))
            stree = etree.fromstring(streebytes)
            return stree
        else:
            logging.error('parsing failed:', r1.status, r1.reason, sent)
            return None

#def previewurl(stree: SynTree) -> URL:
def previewurl(stree):
    '''
    The function *previewurl* returns the URL to preview the input SynTree *stree* in the GreTEL application.
    '''
    sents = stree.xpath('.//sentence')
    if sents != []:
        sent = etree.tostring(sents[0])
    else:
        sent = ''
    xml = etree.tostring(stree)
    encodedsent = urllib.parse.quote(sent)
    encodedxml = urllib.parse.quote(xml)
    fullurl = previewurltemplate.format(sent=encodedsent, xml=encodedxml)
    return fullurl


def escape_alpino_input(instr: str) -> str:
    '''
    The function escape_alpino_input takes as input a string *str* and returns this string with symbols wit ha
    special meaning for Alpino escaped, in particular the square bracket symbols [ and ] used for bracketed input.
    :param instr:
    :return:
    '''
    result = ''
    for c in instr:
        if c == '[':
            newc = '\['
        elif c == ']':
            newc = '\]'
        else:
            newc = c
        result += newc
    return result


def test() -> None:
    while True:
        sent = input('sentence (ENTER to stop): ')
        if sent != '':
            stree = parse(sent)
            if stree is not None:
                print(stree)
        else:
            exit(0)


def test1() -> None:
    sent1 = 'Het slechte weer heeft al schade aangericht'
    stree = parse(sent1)
    thepreviewurl = previewurl(stree)
    with open('previewurl.txt', 'w', encoding='utf8') as outfile:
        print(thepreviewurl, file=outfile)


if __name__ == '__main__':
    test1()
    # test()

import re
import urllib.parse
import urllib.request

from lxml import etree  # type: ignore
from memoize import memoize

import logging
#from config import SDLOGGER
#from sastatypes import SynTree, URL

alpino_special_symbols_pattern = r'[\[\]]'
alpino_special_symbols_re = re.compile(alpino_special_symbols_pattern)

gretelurl = 'https://gretel.hum.uu.nl/api/src/router.php/parse_sentence/'
previewurltemplate = 'https://gretel.hum.uu.nl/ng/tree?sent={sent}&xml={xml}'

emptypattern = r'^\s*$'
emptyre = re.compile(emptypattern)


def isempty(sent):
    result = emptyre.match(sent)
    return result


@memoize
def parse(origsent: str, escape: bool = True):
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


def previewurl(stree) :
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

'''
The *alpinoparsing* module provides functions for:

* parsing:

.. autofunction::  sastadev.alpinoparsing::parse

* previewing a parse tree:

.. autofunction:: sastadev.alpinoparsing::previewurl

'''

import sastadev.conf
import re
import urllib.parse
import urllib.request

from lxml import etree  # type: ignore

from sastadev.memoize import memoize

#from sastadev.sastatypes import SynTree, URL

#from sastadev.config import settings.logger
#from sastadev.sastatypes import SynTree, URL

urllibrequestversion = urllib.request.__version__

alpino_special_symbols_pattern = r'[\[\]]'
alpino_special_symbols_re = re.compile(alpino_special_symbols_pattern)

gretelurl = 'https://gretel.hum.uu.nl/api/src/router.php/parse_sentence/'
#gretelurl = 'http://gretel.hum.uu.nl/api/src/router.php/parse_sentence/'
previewurltemplate = 'https://gretel.hum.uu.nl/ng/tree?sent={sent}&xml={xml}'
#previewurltemplate = 'http://gretel.hum.uu.nl/ng/tree?sent={sent}&xml={xml}'

emptypattern = r'^\s*$'
emptyre = re.compile(emptypattern)


def isempty(sent: str) -> bool:
    '''
    The function *isempty* checks whether the input string *sent* is the null string or
    consists of white space only.

    '''
    result = emptyre.match(sent) is not None
    return result


@memoize
#def parse(origsent: str, escape: bool = True) -> Optional[SynTree]:
def parse(origsent: str, escape: bool = True):
    '''
    The function *parse* invokes the alpino parser (over the internet, so an internet connection is required) to parse
    the string *origsent*.
    The parameter *escape* can be used to escape symbols that have a special meaning
    for Alpino. Its default value is *True*.

    This function is memoised. In order to avoid unexpected results since the output type is mutable, a deepcopy
    of the result is returned. This is essential, because if the same input string is parsed twice,
    the resulting parse tree objects should really be two different instances.!

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
        sastadev.conf.settings.LOGGER.error('{}: parsing <{}> failed'.format(e, sent))
        return None
    except urllib.error.URLError as e:
        sastadev.conf.settings.LOGGER.error('{}: parsing <{}> failed'.format(e, sent))
        return None
    else:
        if 300 > r1.status >= 200:
            streebytes = r1.read()
            # print(streebytes.decode('utf8'))
            try:
                stree = etree.fromstring(streebytes)
            except etree.XMLSyntaxError as e:
                sastadev.conf.settings.LOGGER.error(f'Error: {e} for {sent}')
                stree = None
            return stree
        else:
            sastadev.conf.settings.LOGGER.error('parsing failed:', r1.status, r1.reason, sent)
            return None

#def previewurl(stree: SynTree) -> URL:


def previewurl(stree):
    '''
    The function *previewurl* returns the URL to preview the input SynTree *stree* in the GreTEL application.
    Many browsers have a limit on the length of a URL (it is absurd that that is the
    case)
    and the  inferior MS Office software only accepts URLs with a maximum length of 255
    characters (prehistoric!), so the URLs generated by this function may be too long
    for such inferior software.

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
    The function escape_alpino_input takes as input a string *str* and returns this string with symbols with a
    special meaning for Alpino escaped, in particular the square bracket symbols [ and ] used for bracketed input.
    :param instr:
    :return:
    '''
    result = ''
    for c in instr:
        if c == '[':
            newc = '\\['
        elif c == ']':
            newc = '\\]'
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

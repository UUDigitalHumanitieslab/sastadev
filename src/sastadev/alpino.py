import lexicon
import treebankfunctions

from config import PARSE_FUNC
from sastatypes import WordInfo
from typing import List, Tuple

def getalpinowordinfo(word: str) -> List[WordInfo]:
    '''
    The function *getalpinowordinfo* parses the input word in isolation, extracts its properties and returns some of
    the properties as a list of WordInfo objects.

    '''
    tree = PARSE_FUNC(word)
    relevantnode = treebankfunctions.find1(tree, '//node[parent::node[@cat="top"]]')
    if relevantnode is None:
        return []
    else:
        pos = treebankfunctions.getattval(relevantnode, 'pt')
        if pos == 'n':
            genus = treebankfunctions.getattval(relevantnode, 'genus')
            dehet = lexicon.het if genus == 'onz' else lexicon.de
            getal = treebankfunctions.getattval(relevantnode, 'getal')
            graad = treebankfunctions.getattval(relevantnode, 'graad')
            infl = 'd' if graad == 'dim' else ''
            infl += 'e' if getal == 'ev' else 'm'
            lemma = treebankfunctions.getattval(relevantnode, 'lemma')
            return([(pos, dehet, infl, lemma)])
        else:
            return []


def getdehetwordinfo(wrd: str) -> Tuple[List[WordInfo], str]:
    '''
    The function *getdehetwordinfo*  determines the properties of the input string *word* by first looking in the
    lexicon. It only includes properties if the word is a noun.
    If not found in the lexicon, it tries to find the properties from Alpino by means of the function
    *getalpinowordinfo*.
    It returns a tuple consisting of a list of WordInfo objects and a string indicating the source where the properties
    have been found.
    '''

    wordinfos = lexicon.getwordinfo(wrd)

    # we only want to consider nouns or words of unknown word class (such as kopje in CELEX)
    wordinfos = [wordinfo for wordinfo in wordinfos if wordinfo[0] in ['n', 'None']]
    # if any of the alternatives is a de-word, we keep only these
    dewordinfos = [wordinfo for wordinfo in wordinfos if wordinfo[1] == lexicon.de]
    if dewordinfos != []:
        wordinfos = dewordinfos
    #if any([wordinfo[1] == lexicon.de for wordinfo in wordinfos]):
    #    wordinfos = []

    # if not found yet we check with Alpino
    if wordinfos != []:
        source = 'celex'
    else:
        wordinfos = getalpinowordinfo(wrd)
        source = 'alpino'
    return (wordinfos, source)
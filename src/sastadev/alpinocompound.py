from sastadev.treebankfunctions import find1, getattval
from sastadev.conf import settings
from sastadev.lexicon import known_word


# verhuizen naar lexicon module
comma = ','
compoundsep = '_'

alpinoparse = settings.PARSE_FUNC


def isalpinocompound(wrd: str) -> bool:
    fullstr = f'geen {wrd}'   # geen makes it a noun and can combine with uter and neuter, count and mass, sg and plural
    tree = alpinoparse(fullstr)
    # find the noun
    if tree is None:
        settings.LOGGER.error(f'Parsing {fullstr} failed')
        return False
    nounnode = find1(tree, './/node[@pt="n"]')
    if nounnode is None:
        settings.LOGGER.error(f'No noun found in {fullstr} parse')
        return False
    nounwrd = getattval(nounnode, 'word')
    if nounwrd != wrd:
        settings.LOGGER.error(f'Wrong noun ({nounwrd}) found in {fullstr} parse')
        return False
    nounlemma = getattval(nounnode, 'lemma')
    if compoundsep in nounlemma:
        parts = nounlemma.split(compoundsep)
        unknownparts = [part for part in parts if not known_word(part)]
        result = unknownparts = []
        if not result:
            settings.LOGGER.error(f'Unknown words ({comma.join(unknownparts)}) found in {fullstr} parse')
            return False
        return True
    else:
        return False


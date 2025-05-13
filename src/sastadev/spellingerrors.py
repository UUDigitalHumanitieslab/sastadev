"""
Module with functions to detect and correct spelling errors
"""

testlist = [('babietjes', True, 'baby', "baby'tjes"),
            ('babietje', True, 'baby', "baby'tje"),
            ('babies', True, 'baby', "baby's"),
            ('hobbietjes', True, 'hobby', "hobby'tjes"),
            ('hobbietje', True, 'hobby', "hobby'tje"),
            ('hobbies', True, 'hobby', "hobby's"),
            ('autoos', False, 'autoos', 'autoos'),
            # ('koppies', False, 'kop', "kopjes")
            ]


def getbabysuffix(wrd: str) -> str:
    if wrd.endswith('ies'):
        suffix = 'ies'
    elif wrd.endswith('ietje'):
        suffix = 'ietje'
    elif wrd.endswith('ietjes'):
        suffix = 'ietjes'
    else:
        suffix = ''    # should not happen
    return suffix


def isbabyword(wrd: str) -> bool:
    result = wrd.lower().endswith('ies') or wrd.lower().endswith('ietje') or wrd.lower().endswith('ietjes')
    return result

def getbabylemma(wrd: str) -> str:
    suffix = getbabysuffix(wrd)
    if suffix == '':
        result = wrd
    else:
        result = f'{wrd[:-len(suffix)]}y'
    return result

def correctbaby(wrd: str) -> str:
    suffix = getbabysuffix(wrd)
    if suffix == '':
        result = wrd
    else:
        result = f"{wrd[:-len(suffix)]}y'{suffix[2:]}"
    return result


def tryme():
    for el, ref, lemmaref, refcorr in testlist:
        if isbabyword(el) != ref:
            pol = 'REALLY' if ref else "NOT"
            print(f'{el} is {pol} a babyword')
        corr = correctbaby(el)
        if corr != refcorr:
            print(f'Correction of {el} is NOT {corr} but {refcorr}')
        lemma = getbabylemma(el)
        if lemma != lemmaref:
            print(f'Lemma of {el} is NOT {lemma} but {lemmaref}')


if __name__ == '__main__':
    tryme()
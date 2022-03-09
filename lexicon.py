import celexlexicon
import treebankfunctions
from namepartlexicon import namepart_isa_namepart, namepart_isa_namepart_uc

space = ' '

celex = 'celex'
alpino = 'alpino'

chatspecials = ['xxx', 'yyy']


lexicon = celex

#Alpino often analyses certain words as tsw though they should be analysed as nouns
tswnouns = ['baby', 'jongen', 'juf', 'jufforouw', 'mam', 'mama', 'mamma', 'meisje', 'mens', 'meneer', 'mevrouw',
            'pap', 'papa', 'pappa', 'stouterd', 'opa', 'oma']

de = '1'
het = '2'
dets = {}
dets[de] = ['de', 'die', 'deze', 'onze', 'welke', 'iedere', 'elke', 'zulke']
dets[het] = ['het', 'dat', 'dit', 'ons', 'welk', 'ieder', 'elk', 'zulk']


def isa_namepart(word):
    return namepart_isa_namepart(word)

def isa_namepart_uc(word):
    return namepart_isa_namepart_uc(word)




def lookup(dct, key):
    result = dct[key] if key in dct else ''
    return result


def pvinfl2dcoi(word, infl, lemma):
    if lexicon == celex:
        results = celexlexicon.celexpv2dcoi(word, infl, lemma)
        wvorm = lookup(results, 'wvorm')
        pvtijd = lookup(results, 'pvtijd')
        pvagr = lookup(results, 'pvagr')
        positie = lookup(results, 'positie')
        buiging = lookup(results, 'buiging')
        dcoi_infl = []
        atts = [wvorm, pvtijd, pvagr, positie, buiging]
        for att in atts:
            if att != '':
                dcoi_infl.append(att)
        result = tuple(dcoi_infl)
    else:
        result = None
    return result


def getwordposinfo(word, pos):
    results = []
    if lexicon == celex:
        results = celexlexicon.getwordposinfo(word, pos)
    return results


def getwordinfo(word):
    results = []
    if lexicon == celex:
        results = celexlexicon.getwordinfo(word)
    return results


def informlexicon(word):
    allwords = word.split(space)
    result = True
    for aword in allwords:
        if lexicon == 'celex':
            result = result and celexlexicon.incelexdmw(aword)
        elif lexicon == 'alpino':
            result = False
        else:
            result = False
    return result


def informlexiconpos(word, pos):
    allwords = word.split(space)
    result = True
    for aword in allwords:
        if lexicon == 'celex':
            result = result and celexlexicon.incelexdmwpos(aword, pos)
        elif lexicon == 'alpino':
            result = False
        else:
            result = False
    return result


def chatspecial(word):
    result = word in chatspecials
    return result


def known_word(word):
    result = informlexicon(word) or isa_namepart(word) or chatspecial(word)
    return result


def getinflforms(thesubj, thepv, inversion):
    if lexicon == 'celex':
        pt = treebankfunctions.getattval(thepv, 'pt')
        pos = celexlexicon.pos2posnum[pt]
        infl = celexlexicon.dcoiphi2celexpv(thesubj, thepv, inversion)
        lemma = treebankfunctions.getattval(thepv, 'lemma')
        results = celexlexicon.getinflforms(lemma, pos, infl)
    else:
        results = []
    return results

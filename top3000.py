from xlsx import getxlsxdata
from treebankfunctions import getattval
from namepartlexicon import namepart_isa_namepart

def ishuman(node):
    lemma = getattval(node, 'lemma')
    pt = getattval(node, 'pt')
    vwtype = getattval(node, 'vwtype')
    result = (lemma, pt ) in semlexicon and 'human' in semlexicon[(lemma, pt)]
    result = result or vwtype == 'pers'
    result = result or namepart_isa_namepart(lemma)
    return result

def isanimate(node):
    lemma = getattval(node, 'lemma')
    pt = getattval(node, 'pt')
    result = (lemma, pt ) in semlexicon and 'animate' in semlexicon[(lemma, pt)]
    return result


def transitivity(node, tr):
    lemma = getattval(node, 'lemma')
    pt = getattval(node, 'pt')
    result = (lemma, pt ) in semlexicon and tr in trlexicon[(lemma, pt)]
    return result

def transitive(node):
    return transitivity(node, 'tr')

def pseudotr(node):
    return transitivity(node, 'tr/intr')


def intransitive(node):
    return transitivity(node, 'intr')

semicolon = ';'

filename = r'D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\woordenlijsten\Woordenlijsten Current.xlsx'


lexiconheader, lexicondata = getxlsxdata(filename)

semlexicon = {}
for row in lexicondata:
    lemma = row[1]
    pt = row[5]
    rawsems = row[6].split(semicolon)
    sems = [el.strip() for el in rawsems]
    semlexicon[(lemma, pt)] = sems

trlexicon = {}
for row in lexicondata:
    lemma = row[1]
    pt = row[5]
    rawtrs = row[8].split(semicolon)
    trs = [el.strip() for el in rawtrs]
    trlexicon[(lemma, pt)] = trs

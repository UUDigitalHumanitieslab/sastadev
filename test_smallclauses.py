from treebankfunctions import getstree, getnodeyield, getattval
from dedup import filledpauseslexicon
from top3000 import ishuman, transitive, intransitive, pseudotr, isanimate
from lexicon import known_word

space = ' '
biglocvzs = ['achter', 'beneden', 'binnen', 'boven', 'bovenop', 'buiten', 'dichtbij']

testbank = r"D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\TARSP\smallclausetest.xml"
schlichtingtreebank = r'D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\schlichtingtreebank\TREEBANK_ID.xml'
mieke06 = r"D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\miekeplat_tests\TARSP_MIEKE06_ID.xml"
mieke08 = r"D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\miekeplat_tests\TARSP_MIEKE08_ID.xml"
aurisraw = r"D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\Auris\AURIS_ELISKA_ORIGINAL_ID.xml"
tarsp02 = r"D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\tarspdata\Tarsp_02.xml"
tarsp06 = r"D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\tarspdata\Tarsp_06.xml"


def realword(node):
    result = True
    result = result and getattval(node, 'pt') not in ['tsw', 'let']
    result = result and getattval(node, 'lemma') not in ['xx', 'xxx', 'yyy', 'www']
    result = result and getattval(node, 'lemma') not in filledpauseslexicon

    return result


def hasgenitive(node):
    result = False
    return result

def aanwvnw(node):
    result = getattval(node, 'pt') == 'vnw' and getattval(node, 'vwtype') == 'aanw'
    return result


def n(node):
    result = getattval(node, 'pt') == 'n'
    return result


def getal(node):
    result = getattval(node, 'getal')
    return result

def pt(node):
    result = getattval(node, 'pt')
    return result

def bg(node):
    result = int(getattval(node, 'begin'))
    return result

def tw(node):
    result = getattval(node, 'pt') == 'tw'
    return result

def word(node):
    result = getattval(node, 'word')
    return result


def adj(node):
    result = getattval(node, 'pt') == 'adj'
    return result


def inf(node):
    result = getattval(node, 'pt') == 'ww' and getattval(node, 'wvorm') == 'inf'
    return result


def rpronoun(node):
    result = getattval(node, 'pt') == 'vnw' and \
             getattval(node, 'lemma') in ['er', 'hier', 'daar', 'ergens', 'overal', 'nergens', 'waar']
    return result

def bw(node):
    result = getattval(node, 'pt') == 'bw'
    return result

def lemma(node):
    result = getattval(node, 'lemma')
    return result

def predadv(node):
    result = locadv(node)
    result = result or (bw(node) and lemma(node) in ['niet', 'mee', 'weg'])
    return result

def locadv(node):
    result = getattval(node, 'pt') in ['bw', 'vz']
    frame = getattval(node, 'frame')
    result = result and ('loc' in frame or 'er_adverb' in frame)
    result = result or rpronoun(node)
    return result

def biglocvz(node):
    result = getattval(node, 'lemma') in biglocvzs
    return result

def getleavestr(leaves):
    leaveseq = ['{}:{}:{}:{}'.format(getattval(leave, 'end'), getattval(leave, 'word'), getattval(leave, 'lemma'),
                                     getattval(leave, 'pt')) for leave
                in leaves]
    leavestr = space.join(leaveseq)
    return leavestr

def knownnoun(node):
    word = getattval(node, 'word')
    lemma = getattval(node, 'lemma')
    postag = pt(node)
    result = postag == 'n' and (known_word(word) or known_word(lemma))
    return result

def smallclauses(leaves, reducedleaves):
    resultlist = []
    # aanwvnw or n + locbw
    if len(reducedleaves) <= 3:
        first = leaves[0]
        second = leaves[1]
    if len(reducedleaves) == 3:
        third = leaves[0]

    if len(reducedleaves) == 2:
        #fword = word(first)
        #sword = word(second)
        if (aanwvnw(first) or knownnoun(first)) and predadv(second):
            fpos = int(getattval(first, 'begin'))
            insertword = 'moet' if getal(first) != 'mv' else 'moeten'
            resultlist = [word(lv) for lv in leaves if bg(lv) <= fpos] + [insertword] + [word(lv) for lv in leaves if bg(lv) > fpos]
        elif (aanwvnw(second) or knownnoun(second) or tw(second)) and predadv(first):
            fpos = int(getattval(first, 'begin'))
            insertword = 'moet' if getal(second) != 'mv' else 'moeten'
            resultlist = [word(lv) for lv in leaves if bg(lv) <= fpos] + [insertword] + [word(lv) for lv in leaves if
                                                                                         bg(lv) > fpos]
        elif (aanwvnw(first) or knownnoun(first)) and adj(second):
            fpos = int(getattval(first, 'begin'))
            insertword = 'is' if getal(first) != 'mv' else 'zijn'
            resultlist = [word(lv) for lv in leaves if bg(lv) <= fpos] + [insertword] + [word(lv) for lv in leaves if
                                                                                         bg(lv) > fpos]
        elif (aanwvnw(second) or knownnoun(second) or tw(second)) and biglocvz(first):
            fpos = int(getattval(first, 'begin'))
            insertword = 'is' if getal(first) != 'mv' else 'zijn'
            resultlist = [word(lv) for lv in leaves if bg(lv) <= fpos] + [insertword] + [word(lv) for lv in leaves if
                                                                                         bg(lv) > fpos]
        elif knownnoun(first) and knownnoun(second) and not(lemma(first) == lemma(second)):
            if hasgenitive(first):
                pass
            else:
                fpos = int(getattval(first, 'begin'))
                insertword = 'is' if getal(first) != 'mv' else 'zijn'
                resultlist = [word(lv) for lv in leaves if bg(lv) <= fpos] + [insertword] + \
                             [word(lv) for lv in leaves if     bg(lv) > fpos]

        elif (aanwvnw(first) or knownnoun(first)) and inf(second):
            if intransitive(second):
                firstsubject = True
            elif transitive(second) and ishuman(first):
                firstsubject = True
            elif pseudotr(second) and (ishuman(first) or isanimate(first)):
                firstsubject = True
            else:
                firstsubject = False
            if firstsubject:
                insertwords = ['wil' if getal(first) != 'mv' else 'willen']
                fpos = int(getattval(first, 'begin'))
            else:
                insertwords = ['ik', 'wil']
                fpos = -1
            resultlist = [word(lv) for lv in leaves if bg(lv) <= fpos] + insertwords + [word(lv) for lv in leaves if
                                                                                        bg(lv) > fpos]

    return resultlist


def main():
    smalltest = False
    if smalltest:
        fullnames = [testbank]
    else:
        fullnames = [schlichtingtreebank, mieke06, mieke08, aurisraw, tarsp02, tarsp06]
    for infullname in fullnames:
        print(infullname)
        fulltreebank = getstree(infullname)
        if fulltreebank is not None:
            treebank = fulltreebank.getroot()
            for tree in treebank:
                leaves = getnodeyield(tree)
                reducedleaves = [leave for leave in leaves if realword(leave)]

                if len(reducedleaves) > 1 and len(reducedleaves) <= 3:
                    resultlist = smallclauses(leaves, reducedleaves)
                    if resultlist != []:
                        print('input:  ', getleavestr(leaves), '/', getleavestr(reducedleaves))
                        print('result: ', space.join(resultlist))


if __name__ == '__main__':
    main()

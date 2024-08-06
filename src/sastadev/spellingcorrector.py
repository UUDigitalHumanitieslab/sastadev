from spellchecker import SpellChecker
import os
from sastadev.history import childescorrections, HistoryCorrection
from sastadev.lexicon import known_word
from sastadev.xlsx import mkworkbook, add_worksheet
from typing import List


comma=','

def comparecorrections(corrections: List[str], goldrefs: List[HistoryCorrection]):
    sortedgoldrefs = sorted(goldrefs, key= lambda hc: hc.frequency, reverse=True)
    highestfreqcorrections = [hc.correction for hc in sortedgoldrefs]
    pairs = []
    if corrections is None:
        return []
    for correction in corrections:
        try:
            pos = highestfreqcorrections.index(correction)
            pairs.append((correction, pos+1))
        except:
            pass
    sortedpairs = sorted(pairs, key= lambda cp: cp[1])
    return sortedpairs


def childestest():

    header = ['word', 'found', 'count', 'results', 'reference']
    resultdata = []
    spell = SpellChecker(language='nl')
    okcount = 0
    wordcount = 0
    for word in childescorrections:
        if not known_word(word):
            wordcount += 1
            # if wordcount == 100:
            #    break
            corrections = spell.candidates(word)
            results = comparecorrections(corrections, childescorrections[word])
            resultsfound = 'yes' if results != [] else 'no'
            resultscount = len(results)
            if resultscount > 0:
                okcount += 1
            resultstr = comma.join([f'{c}-{p}' for c,p in results])
            sortedchildescorrections = sorted(childescorrections[word], key=lambda hc: hc.frequency)
            childescorrstrlist =  [f'{hc.correction}-{hc.frequency}' for hc in sortedchildescorrections ]
            childescorrstr = comma.join(childescorrstrlist)
            resultrow = [word, resultsfound, resultscount, resultstr, childescorrstr]
            resultdata.append(resultrow)

    scoreheader = ['count', 'ok', 'accuracy']
    scoredata = [[wordcount, okcount, okcount/wordcount*100]]

    outfilename = 'spellcorrresults.xlsx'
    outpath = 'D:\Dropbox\jodijk\myprograms\python\sastacode\spelltest'
    outfullname = os.path.join(outpath, outfilename)
    wb = mkworkbook(outfullname, [header], resultdata, freeze_panes=(1,0))
    add_worksheet(wb,[scoreheader], scoredata, freeze_panes=(1,0), sheetname='Score')
    wb.close()

if __name__ == '__main__':
    childestest()
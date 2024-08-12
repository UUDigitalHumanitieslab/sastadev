from spellchecker import SpellChecker
import os
from sastadev.history import childescorrections, HistoryCorrection
from sastadev.lexicon import known_word
from sastadev.readcsv import readcsv, writecsv
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


def auriscorrections():
    spell = SpellChecker(language='nl')
    correctionsdict = {}
    inputfilename = 'notknownwordsfrq.txt'
    inputfolder = r'D:\Dropbox\jodijk\myprograms\python\childesfreq\aurisfrqoutput'
    inputfullname = os.path.join(inputfolder, inputfilename)
    idata = readcsv(inputfullname)
    for i, row in idata:
        word = row[1]
        if word in correctionsdict:
            result = correctionsdict[word]
        else:
            result = spell.candidates(word)
            correctionsdict[word] = result

    outdata = []
    for word, corrections in correctionsdict.items():
        if corrections is not None:
            correctionsstr = comma.join(corrections)
        else:
            correctionsstr = ''
        row = [word, correctionsstr]
        outdata.append(row)

    outheader = ['word', 'corrections']
    outfilename = 'auriscorrections.txt'
    outfolder = r'D:\Dropbox\jodijk\myprograms\python\childesfreq\aurisfrqoutput'
    outfullname = os.path.join(outfolder, outfilename)
    writecsv(outdata, outfullname, outheader)


def simplecheck():
    spell = SpellChecker(language='nl')
    words = ['opbijten', 'irving', 'isaacs']
    for word in words:
        corrections = spell.candidates(word)
        if corrections is not None:
            pairs = [(corr, spell.word_usage_frequency(corr)) for corr in corrections]
        sortedpairs = sorted(pairs, key=lambda x: x[1], reverse=True)
        print(word)
        print(corrections)
        print(sortedpairs)

if __name__ == '__main__':
    # childestest()
    # auriscorrections()
    simplecheck()
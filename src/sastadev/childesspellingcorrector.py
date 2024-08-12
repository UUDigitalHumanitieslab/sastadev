from collections import defaultdict
from sastadev.conf import settings
from sastadev.lexicon import spellingadditions
from sastadev.readcsv import readcsv
import os
from spellchecker import SpellChecker
from typing import Dict, List, Tuple

comma = ','
hyphen = '-'

trg = 'TRG'
oth = 'OTH'

FrqDict = Dict[str, int]

spell = SpellChecker(language='nl')
# the words in the dictionary that have not been found in the corpus have been assigned freqency 50
# and the following probability:
nonoccurrenceprobability = 1.3132493418801947e-07

# we use this as threshold;only words with a probability higher than this one are considered as candidates
okthreshold = nonoccurrenceprobability

# function to read the childes frequency dict in, for targets and others and combine them also
def getchildesfrq() -> Tuple[FrqDict, FrqDict, FrqDict]:
    trgfrqdict = defaultdict(int)
    othfrqdict = defaultdict(int)
    allfrqdict = defaultdict(int)
    childesfrqfilename = 'knownwordsfrq.txt'
    childeslexiconfolder = os.path.join(settings.SD_DIR, 'data/childeslexicon')
    childesfrqfullname = os.path.join(childeslexiconfolder, childesfrqfilename)
    idata = readcsv(childesfrqfullname)
    for _, row in idata:
        role = row[0]
        word = row[1]
        frq = int(row[2])
        if role == trg:
            trgfrqdict[word] += frq
        elif role == oth:
            othfrqdict[word] += frq
        else:
            pass
        allfrqdict[word] += frq
    return trgfrqdict, othfrqdict, allfrqdict

# function to read the stored corrections into a dictionary

def getstoredcorrections() -> Dict[str, List[Tuple[str, int]]]:
    correctionsdict = {}
    correctionsfilename = 'storedcorrections.txt'
    correctionspath = os.path.join(settings.SD_DIR, 'data/storedcorrections')
    correctionsfullname = os.path.join(correctionspath, correctionsfilename)

    idata = readcsv(correctionsfullname)
    for i, row in idata:
        word = row[0]
        correctionsstr = row[1]
        correctionstrings = correctionsstr.split(comma)
        rawcorrections = [tuple(pairstr.split(hyphen)) for pairstr in correctionstrings]
        corrections = [(w, int(pen)) for  (w, pen) in rawcorrections]
        correctionsdict[word] = corrections

    return correctionsdict


def getpenalty(score, total):
    result = 101 + 100 - int(score/total*100)
    return result

#  a function for spelling correction

def correctspelling(word: str, max = None, threshold=okthreshold) -> List[Tuple[str, int]]:
    if word in correctionsdict:
        return correctionsdict[word]
    else:
        corrections = spell.candidates(word)
    if corrections is not None:
        pairs = [(corr, spell.word_usage_frequency(corr)) for corr in corrections]
    else:
        corrections = []


    trgfrqs = [trgfrqdict[corr] if corr in trgfrqdict else 0 for corr in corrections]
    allfrqs = [allfrqdict[corr] if corr in allfrqdict else 0 for corr in corrections]
    probs = [spell.word_usage_frequency(corr) for corr in corrections]

    corrscores = zip(trgfrqs, allfrqs, probs)
    corrtuples = zip(corrections, corrscores)

    sortedcorrtuples = sorted(corrtuples, key=lambda x: x[1], reverse=True)


    # filter candidates that do not occur in trgfrq and allfrq and have too low a probability
    selectedsortedcorrtuples = [ct for ct in sortedcorrtuples if ct[1][0] != 0 or
                                ct[1][1] != 0 or ct[1][2] > threshold or ct[0] in spellingadditions]

    trgfrqsum = sum(corrtuple[1][0] for corrtuple in selectedsortedcorrtuples)
    allfrqsum = sum(corrtuple[1][1] for corrtuple in selectedsortedcorrtuples)
    probsum = sum(corrtuple[1][2] for corrtuple in selectedsortedcorrtuples)
    if trgfrqsum != 0:
        result = [(corr, getpenalty(score[0], trgfrqsum)) for (corr, score) in selectedsortedcorrtuples]
    elif allfrqsum != 0:
        result = [(corr, getpenalty(score[1], allfrqsum)) for (corr, score) in selectedsortedcorrtuples]
    elif probsum != 0:
        result = [(corr, getpenalty(score[2], probsum)) for (corr, score) in selectedsortedcorrtuples]
    else:
        result = []

    if max is not None:
        result = result[:max]


    # store the result in the dictionary; write dictionary to file

    return result

def tryme():
    words = ['opbijten', 'oprijten', 'opgereten', 'peelkaal' , ' beete' , 'kamm', 'daaistoel', 'oelen', 'tein']
    for word in words:
        result = correctspelling(word, max=5)
        print(f'{word}: {result}' )






# read the childes frequency dict in, for targets and others and combine them also
trgfrqdict, othfrqdict, allfrqdict = getchildesfrq()

# read the stored corrections into a dictionary
correctionsdict = getstoredcorrections()

if __name__ == '__main__':
    tryme()
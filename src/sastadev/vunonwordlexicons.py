from sastadev.readcsv import readcsv
from sastadev.lexicon import known_word
import re
import os
from sastadev.conf import settings


space = ' '
interpunction = """.,/:;?!"'"""

def initializelexicon(lexiconfilename):
    lexicon = set()
    fptuples = readcsv(lexiconfilename, header=False)
    for _, fp in fptuples:
        strippedword = fp[0].strip()
        lexicon.add(strippedword)
    return lexicon





# initialize lexicons
lexiconfoldername = 'filledpauseslexicon'

filledpauseslexiconfilename = 'filledpauseslexicon.txt'
filledpauseslexiconfullname = os.path.join(settings.SD_DIR, lexiconfoldername, filledpauseslexiconfilename)
filledpauseslexicon = initializelexicon(filledpauseslexiconfullname)




nomlulexiconfilename = 'notanalyzewords.txt'
nomlulexiconfullname = os.path.join(lexiconfoldername, nomlulexiconfilename)
nomlulexicon = initializelexicon(nomlulexiconfullname)

vuwordslexiconfilename = 'vuwordslexicon.txt'
vuwordslexiconfullname = os.path.join(lexiconfoldername, vuwordslexiconfilename)
vuwordslexicon = initializelexicon(vuwordslexiconfullname)


junk = 0


def alldutchwords(correct: str) -> bool:
    newcorrect = normalize(correct)
    words = newcorrect.split()
    result = all([isvalidtoken(word) for word in words])
    return result


def isvalidtoken(wrd:str) -> bool:
    result = known_word(wrd) or wrd in interpunction
    return result


def normalize(utt):
    #replace interpunction by space + interpunction but not when preceded by = or [ or (; this is a bit ad hoc maybe uese the sastadev chat tokenization
    newutt = utt
    newutt = re.sub(r"([^=0\[\(])([\?\.!,;>'])", r'\1 \2', newutt)
    newutt = re.sub(r"([<'])", r'\1 ', newutt)
    tokens = newutt.split()
    newutt = space.join(tokens)
    return newutt



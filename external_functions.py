import re
from compounds import getcompounds
from Sziplus import sziplus6, vr5plus
from xenx import xenx
from imperatives import wx, wxy, wxyz, wxyz5, wondx, wond4, wond5plus
from TARSPscreening import tarsp_screening
from TARSPpostfunctions import vutotaal, gofase, gtotaal, pf2, pf3, pf4, pf5, pf6, pf7, pf
from queryfunctions import xneg_x, xneg_neg, VzN
from dedup import mlux, samplesize, neologisme, onvolledig, correct
from STAPpostfunctions import BB_totaal, GLVU, GL5LVU
from ASTApostfunctions import wordcountperutt, countwordsandcutoff, KMcount, finietheidsindex, getnounlemmas,\
    getlexlemmas, getalllemmas
from astaforms import astaform
from tarspform import mktarspform
from stapforms import makestapform
from asta_queries import asta_noun, asta_bijzin, asta_lex, asta_delpv
from methods import allok

normalfunctionpattern = r'<function\s+(\w+)\b'
builtinfunctionpattern = r'<built-in function\s+(\w+)\b'


# normalfunctionprefix = "<function "
# lnormalfunctionprefix = len(normalfunctionprefix)
# builtinfunctionprefix = "<built-in function "
# lbuiltinfunctionprefix = len(builtinfunctionprefix)

def getfname(f):
    return f.__name__


def oldgetfname(f):
    fstr = str(f)
    m = re.match(normalfunctionpattern, fstr)
    if m is not None:
        result = m.group(1)
    else:
        m = re.match(builtinfunctionpattern, fstr)
        if m is not None:
            result = m.group(1)
        else:
            result = ''
    return result


# Initialisation
thetarspfunctions = [getcompounds, sziplus6, xenx, vr5plus, wx, wxy, wxyz, wxyz5, wondx, wond4, wond5plus,
                     tarsp_screening, vutotaal, gofase, gtotaal, pf2, pf3, pf4, pf5, pf6, pf7, pf, xneg_x, xneg_neg,
                     mktarspform, VzN]

thestapfunctions = [BB_totaal, GLVU, GL5LVU, makestapform]

theastafunctions = [samplesize, mlux, neologisme, onvolledig, correct, wordcountperutt, countwordsandcutoff,
                    astaform, KMcount, finietheidsindex, getnounlemmas, getlexlemmas, getalllemmas, asta_noun,
                    asta_bijzin, asta_lex, asta_delpv, allok]

thefunctions = thetarspfunctions + thestapfunctions + theastafunctions

str2functionmap = {}

for f in thefunctions:
    fname = getfname(f)
    str2functionmap[fname] = f

junk = 0

# Used by SASTA to find form functions
form_map = {
    'TARSP': mktarspform,
    'ASTA': astaform,
    'STAP': makestapform
}

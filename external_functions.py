import re

from asta_queries import asta_bijzin, asta_delpv, asta_lex, asta_noun
from astaforms import astaform
from ASTApostfunctions import (KMcount, countwordsandcutoff, finietheidsindex,
                               getalllemmas, getlemmas, wordcountperutt)
from compounds import getcompounds
from dedup import correct, mlux, neologisme, onvolledig, samplesize
from imperatives import wond4, wond5plus, wondx, wx, wxy, wxyz, wxyz5
from methods import allok
from queryfunctions import VzN, xneg_neg, xneg_x
from STAPpostfunctions import GL5LVU, GLVU, BB_totaal
from Sziplus import sziplus6, vr5plus
from tarspform import mktarspform
from TARSPpostfunctions import (gofase, gtotaal, pf, pf2, pf3, pf4, pf5, pf6,
                                pf7, vutotaal)
from TARSPscreening import tarsp_screening
from xenx import xenx

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
                     tarsp_screening, vutotaal, gofase, gtotaal, pf2, pf3, pf4, pf5, pf6, pf7, pf, xneg_x, xneg_neg, mktarspform, VzN]

thestapfunctions = [BB_totaal, GLVU, GL5LVU]


theastafunctions = [samplesize, mlux, neologisme, onvolledig, correct, wordcountperutt, countwordsandcutoff,
                    astaform, KMcount, finietheidsindex, getlemmas, getalllemmas, asta_noun, asta_bijzin, asta_lex, asta_delpv, allok]

thefunctions = thetarspfunctions + thestapfunctions + theastafunctions


str2functionmap = {}

for f in thefunctions:
    fname = getfname(f)
    str2functionmap[fname] = f

form_map = {
    'TARSP': mktarspform,
    'ASTA': astaform
}

junk = 0

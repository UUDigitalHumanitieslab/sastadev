import re

import CHAT_Annotation as sastachat

#from CHAT_Annotation import CHAT_patterns, interpunction, wordpat
from sastadev.sastatoken import stringlist2tokenlist


def alts(pats, grouping=False):
    result = r''
    for pat in pats:
        if result == r'':
            result = pat
        else:
            result += '|' + pat
    if grouping:
        result = '(' + result + ')'
    else:
        result = '(?:' + result + ')'
    return result


#interpunction = r'[!\?\.,;]'  # add colon separated by spaces
#word = r'[^!\?;\.\[\]<>\s]+'
word = sastachat.wordpat
scope = r'<.+?>'
scopeorword = alts([scope, word])
myrepetition = r'\[x\s*[0-9]+\s*\]'
replacement = scopeorword + r'\s*\[:.+?\]'
realwordreplacement = scopeorword + r'\s*\[::.+?\]'
alternativetranscription = r'\[=\?.+?\]'
# dependenttier # p. 71
commentonmainline = r'\[%.+?\]'  # p. 71
#bestguess = scopeorword+r'\s*\[\?\]' #p. 70-71
bestguess = r'\[\?\]'
#overlap follows p. 71
#overlap precedes p. 71
repetition = scopeorword + r'\s*\[/\]\s*' + word  # p73 should actually cover the number of words inside the scope
retracing = scopeorword + r'\s*\[//\]\s*' + word  # p73
whitespace = r'\s+'


#sastaspecials = [r'\[::', r'\[=', r'\[:', r'\[=\?', r'\[x', r'\<', r'\>', r'\[\?\]', r'\[/\]', r'\[//\]', r'\[///\]', r'\[%', r'\]']
sastaspecials = list(sastachat.CHAT_patterns)
sastapatterns = sorted(sastaspecials, key=lambda x: len(x), reverse=True) + [word, sastachat.interpunction]
fullsastapatterns = alts(sastapatterns)
fullsastare = re.compile(fullsastapatterns)

allpatterns = [realwordreplacement, replacement, myrepetition, alternativetranscription, commentonmainline, bestguess, retracing]
sortedallpatterns = sorted(allpatterns, key=lambda x: len(x), reverse=True) + [word, sastachat.interpunction]
fullpattern = alts(sortedallpatterns)
#print(fullpattern)
fullre = re.compile(fullpattern)


def tokenize(instring):
    tokenstring = fullre.findall(instring)
    result = stringlist2tokenlist(tokenstring)
    return result


def sasta_tokenize(instring):
    if instring is None:
        return []
    tokenstring = fullsastare.findall(instring)
    result = stringlist2tokenlist(tokenstring, start=10, inc=10)
    return result

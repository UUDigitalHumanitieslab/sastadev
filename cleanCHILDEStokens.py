
import re
from copy import deepcopy

import CHAT_Annotation
import sastatok
from config import SDLOGGER
from metadata import Meta, bpl_none
from sastatoken import show

hexformat = '\\u{0:04X}'


space = ' '

scope_open = '<'
scope_close = '>'

bstate, mstate, estate = 0, 1, 2

bstate, ostate, oostate, costate, ccstate = 0, 1, 2, 3, 4


def findscopeclose(tokens, offset=0):
    tokenctr = 0
    bracketcounter = -1
    begin = None
    end = None
    for token in tokens:
        if token.word == scope_open:
            if bracketcounter == -1:
                begin = tokenctr
            bracketcounter += 1
        elif token.word == scope_close:
            if bracketcounter == 0:
                end = tokenctr
                break
            else:
                bracketcounter -= 1
        else:
            pass
        tokenctr += 1
    result = (begin + offset, end + offset) if begin is not None and end is not None else None
    return result


def clearnesting(intokens, repkeep):
    tokens = deepcopy(intokens)
    bracketcounter = -1
    newtokens = []
    metadata = []
    bopenfound = False
    tokenctr = 0
    ltokens = len(tokens)
    while tokenctr < ltokens:
        token = tokens[tokenctr]
        if token.word == scope_open:
            begin = tokenctr
            span = findscopeclose(tokens[tokenctr:], offset=tokenctr)
            if span is None:
                SDLOGGER.error('Syntax error:Scope Open Symbol {} with position = {} ignored (no corresponding closing bracket) in:\n {}'.format(token.word, token.pos, show(tokens)))
            else:
                (begin, end) = span
                (midtokens, midmetadata) = cleantokens(tokens[begin + 1:end], repkeep)
                newtokens += [tokens[tokenctr]] + midtokens + [tokens[end]]
                metadata += midmetadata
                tokenctr = end
        elif token.word == scope_close:
            SDLOGGER.error('Syntax error: unexpected {} excountered with position {} in:\n {}'.format(token.word, token.pos, show(tokens)))
            newtokens.append(token)
        else:
            newtokens.append(token)
        tokenctr += 1
    return(newtokens, metadata)


def checkline(line, newline, outfilename, lineno, logfile):
    if checkpattern.search(newline) or pluspattern.search(newline):
        print(outfilename, lineno, 'suspect character', file=logfile)
        print('input=<{}>'.format(line[:-1]), file=logfile)
        print('output=<{}>'.format(newline), file=logfile)
        thecodes = str2codes(newline)
        print('charcodes=<{}>'.format(thecodes), file=logfile)


def cleantext(utt, repkeep):
    newutt = robustness(utt)
    tokens = sastatok.sasta_tokenize(newutt)
    inwordlist = [t.word for t in tokens]
    intokenstrings = [str(token) for token in tokens]
    # print(space.join(intokenstrings))
    (newtokens, metadata) = cleantokens(tokens, repkeep)
    resultwordlist = [t.word for t in newtokens]
    resultstring = smartjoin(resultwordlist)
    resultposlist = [t.pos for t in newtokens]
    newmeta1 = Meta('tokenisation', inwordlist, atype='list', source='CHAT/Tokenisation', backplacement=bpl_none)
    newmeta2 = Meta('cleanedtokenisation', resultwordlist, atype='list', source='CHAT/Tokenisation', backplacement=bpl_none)
    newmeta3 = Meta('cleanedtokenpositions', resultposlist, atype='list', source='CHAT/Tokenisation', backplacement=bpl_none)
    metadata += [newmeta1, newmeta2, newmeta3]
    resultmetadata = metadata
    return (resultstring, resultmetadata)


def cleantokens(tokens, repkeep):
    newtokens = deepcopy(tokens)
    metadata = []

    (newtokens, nestingmetadata) = clearnesting(newtokens, repkeep)
    metadata += nestingmetadata

    for annotation in CHAT_Annotation.annotations:
        (newtokens, annotationmetadata) = annotation.apply(newtokens, repkeep)
        metadata += annotationmetadata
        tokenstrings = [str(token) for token in newtokens]
        # print(space.join(tokenstrings))

    return (newtokens, metadata)


def str2codes(str):
    result = []
    for i in range(len(str)):
        curchar = str[i]
        curcode = hexformat.format(ord(str[i]))
        result.append((curchar, curcode))
    return(result)


def removesuspects(str):
    result1 = re.sub(checkpattern, space, str)
    result2 = re.sub(pluspattern1, r'\1', result1)
    result = re.sub(pluspattern2, r'\1', result2)
    return result


robustnessrules = [(re.compile(r'\[\+bch\]'), '[+bch]', '[+ bch]', 'Missing space'),
                   (re.compile(r'\[\+trn\]'), '[+trn]', '[+ trn]', 'Missing space'),
                   (re.compile(r'\[:(?![:\s])'), '[:', '[: ', 'Missing space'),
                   (re.compile(r'(?<=\w)\+\.\.\.'), '+...', ' +...', 'Missing space'),
                   (re.compile(r'\u2018'), '\u2018', "'", "Left Single Quotation Mark (\u2018. Unicode U+2018) replaced by Apostrophe ' (Unicode U+0027)"),
                   (re.compile(r'\u2019'), '\u2019', "'", "Right Single Quotation Mark (\u2019, Unicode U+2019) replaced by Apostrophe ' (Unicode U+0027)"),
                   (re.compile(r'\u201C'), '\u201C', '"', 'Left Double Quotation Mark (\u201C, Unicode U+201C) replaced by Quotation Mark (", Unicode U+0022)'),
                   (re.compile(r'\u201D'), '\u201D', '"', 'Right Double Quotation Mark (\u201D, Unicode U+201D) replaced by Quotation Mark (", Unicode U+0022)')
                   ]


def robustness(utt):
    newutt = utt
    for (regex, instr, outstr, msg) in robustnessrules:
        newnewutt = regex.sub(outstr, newutt)
        if newnewutt != newutt:
            SDLOGGER.warning('{}. Interpreted <{}> as <{}> in <{}>'.format(msg, instr, outstr, utt))
        newutt = newnewutt
    return newutt


# checkpattern = re.compile(r'[][\(\)&%@/=><_0^~↓↑↑↓⇗↗→↘⇘∞≈≋≡∙⌈⌉⌊⌋∆∇⁎⁇°◉▁▔☺∬Ϋ123456789·\u22A5\u00B7\u0001\u2260\u21AB]')
checkpattern = re.compile(r'[][\(\)&%@/=><_^~↓↑↑↓⇗↗→↘⇘∞≈≋≡∙⌈⌉⌊⌋∆∇⁎⁇°◉▁▔☺∬Ϋ·\u22A5\u00B7\u0001\u2260\u21AB\u2039\u203A]')
# + should not occur except as compound marker black+board
# next one split up in order to do substitutions
pluspattern = re.compile(r'(\W)\+|\+(\W)')
pluspattern1 = re.compile(r'(\W)\+')
pluspattern2 = re.compile(r'\+(\W)')


def ispunctuation(wrd):
    result = wrd in '.?!;,!<>'
    return result


def smartjoin(strings):
    result = ''
    lstrings = len(strings)
    if lstrings > 0:
        for i in range(lstrings - 1):
            if ispunctuation(strings[i + 1]):
                result += strings[i]
            else:
                result += strings[i] + space
        result += strings[lstrings - 1]
    return result
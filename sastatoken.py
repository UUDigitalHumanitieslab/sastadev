space = ' '


class Token:
    def __init__(self, word, pos, skip=False, subpos=0):
        self.word = word
        self.pos = pos
        self.subpos = subpos
        self.skip = skip

    def __repr__(self):
        fmtstr = 'Token(word={},pos={}, skip={}, subpos={})'
        result = fmtstr.format(repr(self.word), repr(self.pos), repr(self.skip), repr(self.subpos))
        return result

    def __str__(self):
        skipstr = ' (skip=True)' if self.skip else ''
        subposstr = '/{}'.format(self.subpos) if self.subpos != 0 else ''
        result = '{}{}:{}{}'.format(self.pos, subposstr, self.word, skipstr)
        return result


def stringlist2tokenlist(list):
    result = []
    llist = len(list)
    for el in range(llist):
        thetoken = Token(list[el], el)
        result.append(thetoken)
    return result


def tokenlist2stringlist(tlist, skip=False):
    if skip:
        result = [t.word for t in tlist if not t.skip]
    else:
        result = [t.word for t in tlist]
    return result


def tokenlist2string(tlist):
    wordlist = [t.word for t in tlist]
    result = space.join(wordlist)
    return result


def show(tokenlist):
    resultlist = []
    for token in tokenlist:
        resultlist.append(str(token))
    result = ', '.join(resultlist)
    return result

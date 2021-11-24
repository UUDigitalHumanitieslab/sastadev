
class AllResults:
    def __init__(self, uttcount, coreresults, postresults, allmatches, filename, analysedtrees):
        self.uttcount = uttcount
        self.coreresults = coreresults
        self.postresults = postresults
        self.allmatches = allmatches
        self.filename = filename
        self.analysedtrees = analysedtrees


def scores2counts(scores):
    '''
    input is a dictionary of Counter()s
    output is a dictionary of ints
    '''
    counts = {}
    for el in scores:
        countval = len(scores[el])
        counts[el] = countval
    return counts

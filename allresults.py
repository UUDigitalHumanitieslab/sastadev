
class AllResults:
    def __init__(self, uttcount, coreresults, exactresults, postresults, allmatches, filename, analysedtrees, allutts, annotationinput=False):
        self.uttcount = uttcount
        self.coreresults = coreresults
        self.exactresults = exactresults
        self.postresults = postresults
        self.allmatches = allmatches
        self.filename = filename
        self.analysedtrees = analysedtrees
        self.allutts = allutts
        self.annotationinput = annotationinput

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

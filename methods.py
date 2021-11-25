from query import pre_process

asta = 'asta'
stap = 'stap'
tarsp = 'tarsp'


def allok(query, xs, x):
    return True


class Method:
    def __init__(self, name, queries, item2idmap, altcodes, postquerylist, methodfilename, defaultfilter=allok):
        self.name = name
        self.queries = queries
        self.defaultfilter = defaultfilter
        self.item2idmap = item2idmap
        self.altcodes = altcodes
        self.postquerylist = postquerylist
        self.methodfilename = methodfilename


def implies(a, b):
    return (not a or b)


#filter specifies what passes the filter
def astadefaultfilter(query, xrs, xr): return query.process == pre_process or \
    (implies('A029' in xrs, xr not in xrs['A029'])
     and implies('A045' in xrs, xr not in xrs['A045']))


defaultfilters = {}
defaultfilters[asta] = astadefaultfilter
defaultfilters[tarsp] = allok
defaultfilters[stap] = allok

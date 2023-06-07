from typing import Callable, Dict, List

from sastadev.query import pre_process
from sastadev.sastatypes import (AltCodeDict, ExactResult, ExactResultsDict,
                                 ExactResultsFilter, FileName,
                                 Item_Level2QIdDict, MethodName, QId, Query,
                                 QueryDict)

asta = 'asta'
stap = 'stap'
tarsp = 'tarsp'

validmethods = [asta, stap, tarsp]

def validmethod(rawmethod: str) -> bool:
    method = rawmethod.lower()
    result = method in validmethods
    return result

def allok(query: Query, xs: ExactResultsDict, x: ExactResult) -> bool:
    return True


class Method:
    '''

    The *Method* class has the following properties and methods:

* name : MethodName: name of the method
* queries : QueryDict = queries: a dictionary containing the queries (key is query id)
* item2idmap : Item_Level2QIdDict. Dictionary that maps an (item, level) tuple to the QueryId
* altcodes: AltCodeDict: dictionary with alternative codes and their mapping to the standard code
* postquerylist : List[QId]: list of query id’s for queries that are post or form queries
* methodfilename: FileName: filename of the file that contains the language measures
* defaultfilter: ExactResultsFilter: name of the function that acts as the default filter to regulate interaction between prequeries and core queries. By default it has the value allok


    '''
    def __init__(self, name: MethodName, queries: QueryDict, item2idmap: Item_Level2QIdDict,
                 altcodes: AltCodeDict, postquerylist: List[QId], methodfilename: FileName,
                 defaultfilter: ExactResultsFilter = allok):
        self.name: MethodName = name
        self.queries: QueryDict = queries
        self.defaultfilter : ExactResultsFilter = defaultfilter
        self.item2idmap: Item_Level2QIdDict = item2idmap
        self.altcodes: AltCodeDict = altcodes
        self.postquerylist: List[QId] = postquerylist
        self.methodfilename: FileName = methodfilename


def implies(a: bool, b: bool) -> bool:
    return (not a or b)


#filter specifies what passes the filter
def astadefaultfilter(query: Query, xrs: ExactResultsDict, xr: ExactResult) -> bool:
    return query.process == pre_process or \
    (implies('A029' in xrs, xr not in xrs['A029'])
     and implies('A045' in xrs, xr not in xrs['A045']))


defaultfilters: Dict[MethodName, ExactResultsFilter] = {}
defaultfilters[asta] = astadefaultfilter
defaultfilters[tarsp] = allok
defaultfilters[stap] = allok

import os
from typing import Callable, Dict, List, Optional, Tuple

from sastadev.conf import settings
from sastadev.query import pre_process
from sastadev.sastatypes import (AltCodeDict, ExactResult, ExactResultsDict,
                                 ExactResultsFilter, FileName,
                                 Item_Level2QIdDict, MethodName, QId, Query,
                                 QueryDict)

asta = 'asta'
stap = 'stap'
tarsp = 'tarsp'

tarspmethods = [tarsp]
astamethods = [asta]
stapmethods = [stap]

validmethods = astamethods + stapmethods +  tarspmethods

astalexicalmeasures = ['A018', 'A021']  # LEX and N

class SampleSize:
    def __init__(self, maxuttcount=None, maxwordcount=None):
        self.maxuttcount : Optional[int] = maxuttcount
        self.maxwordcount: Optional[int] = maxwordcount


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
        self.defaultfilter: ExactResultsFilter = defaultfilter
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


def getmethodfromfile(filename: str) -> str:
    result = ''
    path, base = os.path.split(filename.lower())
    for m in supported_methods:
        if m in base:
            result = m
    if result == '':
        settings.LOGGER.error('No supported method found in filename')
        exit(-1)
    else:
        return result


def treatmethod(methodname: MethodName, methodfilename: FileName) -> Tuple[MethodName, FileName]:
    if methodname is None and methodfilename is None:
        settings.LOGGER.error('Specify a method using -m ')
        exit(-1)
    elif methodname is None and methodfilename is not None:
        resultmethodfilename = methodfilename
        resultmethodname = getmethodfromfile(methodfilename)
        settings.LOGGER.warning('Method derived from the method file name: {}'.format(resultmethodname))
    elif methodname is not None and methodfilename is None:
        if methodname.lower() in supported_methods:
            resultmethodname = methodname.lower()
            resultmethodfilename = supported_methods[methodname]
        else:
            resultmethodfilename = methodname
            resultmethodname = getmethodfromfile(methodname)
            settings.LOGGER.warning('Method derived from the method file name: {}'.format(resultmethodname))
    elif methodname is not None and methodfilename is not None:
        if methodname.lower() in supported_methods:
            resultmethodname = methodname.lower()
            resultmethodfilename = methodfilename
        else:
            settings.LOGGER.error('Unsupported method specified {}'.format(methodname))
            exit(-1)
    return resultmethodname, resultmethodfilename



codepath = settings.SD_DIR
methodspath = os.path.join(codepath, 'methods')


supported_methods = {}
supported_methods[tarsp] = os.path.join(methodspath, 'TARSP Index Current.xlsx')
supported_methods[asta] = os.path.join(methodspath, 'ASTA Index Current.xlsx')
supported_methods[stap] = os.path.join(methodspath, 'STAP_Index_Current.xlsx')


defaultfilters: Dict[MethodName, ExactResultsFilter] = {}
defaultfilters[asta] = astadefaultfilter
defaultfilters[tarsp] = allok
defaultfilters[stap] = allok

maxsamplesize: Dict[MethodName, SampleSize] = {}
maxsamplesize[asta] = SampleSize(maxwordcount=300)
maxsamplesize[tarsp] = SampleSize(maxuttcount=40)
maxsamplesize[stap] = SampleSize(maxuttcount=50)

lastuttqidcondition: Dict[MethodName, Callable] = {}
lastuttqidcondition[asta] = lambda q:  q in astalexicalmeasures
lastuttqidcondition[tarsp] = lambda q: True
lastuttqidcondition[stap] = lambda q: True

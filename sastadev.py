'''
This program takes as input:
-a treebank file,
-an assesment method file  (in Sasta Assessment Method (SAM) format),
-optionally either
--a annotated reference file (in Sasta Annotation File (SAF) format, or
-- a gold reference file (in Sasta Reference File (SRF) format, or
-- a gold reference count file (in SASTA Referecenc Count File Format), and
-optionally a platinum reference file (in Sasta  Reference File (SRF) format)

and yields as output
-an analysis file showing the results and comparing them to the gold and platinum reference if supplied
    (in SASTA Development Analysis (SDA) format)
-a new platinumfile (useful for creating or updating the platinum reference file), in SPR format
-a platinum check file: list the examples of mismatches between the results and the golf reference
-a gold counts comparison file (for  each measure the # of the results, the # of the golf reference count, and their difference) (tsv format)

and logs its actions through
-a logfile, and
-the terminal screen (sys.stderr)

All input is supposed to be encoded in UTF8, all output is also generated in UTF8
'''

# to do
# -Excel output, cleanup output code

from typing import Dict, List, Any

import xlrd
from lxml import etree
import os
import sys
import re
import csv
import datetime
import compounds
from collections import Counter, defaultdict
# from altcodes import altcodes
from optparse import OptionParser
import logging
from config import SDLOGGER
from SAFreader import get_annotations, get_golddata, richscores2scores, exact2global, richexact2global
from SAFreader import all_levels
from external_functions import str2functionmap
from treebankfunctions import getuttid, getyield, getmeta, getattval, getxmetatreepositions, getuttno, getuttidorno
from SRFreader import read_referencefile
from goldcountreader import get_goldcounts
from TARSPscreening import screening4stage
from allresults import AllResults, scores2counts
from readmethod import read_method, itemseppattern
from methods import allok
from query import pre_process, core_process, post_process, form_process, is_preorcore, query_inform, query_exists, \
    is_pre, is_core
from macros import expandmacros
from mismatches import mismatches, exactmismatches
from xlsx import mkworkbook
import xlsxwriter
from counterfunctions import counter2liststr
from mksilver import getsilverannotations, permprefix
from rpf1 import getscores, getevalscores, sumfreq
from targets import get_mustbedone, get_targets
from correcttreebank import correcttreebank, corr0, corr1, corrn, validcorroptions, errorwbheader
from methods import Method, defaultfilters

listDir = False
if listDir:
    print(dir())
    exit(0)

tarsp = 'tarsp'
stap = 'stap'
asta = 'asta'
gramat = 'gramat'

supported_methods = {}
supported_methods[tarsp] = './methods/TARSP Index Current.xlsx'
supported_methods[asta] = './methods/ASTA Index Current.xlsx'
supported_methods[stap] = './methods/TARSP Index Current.xlsx'

platinumchecksuffix = '_platinum.check.tsv'
platinumcheckeditedsuffix = '_platinum.check-edited.tsv'
platinumsuffix = '.platinum.tsv'
platinumeditedsuffix = '.platinum-edited.tsv'

# target_intarget, target_xsid, target_all = 0, 1, 2
# intargetxpath = '//meta[@name="intarget"]'
# xsidxpath = '//meta[@name="xsid"]'
# intargetvalxpath = './/meta[@name="intarget"]/@value'
# xsidvalxpath = './/meta[@name="xsid"]/@value'

proc = tarsp

logfile = sys.stderr

space = " "
comma = ","
semicolon = ';'
commaspace = ', '
tab = '\t'
pagesep = semicolon
txtext = ".txt"
tsvext = '.tsv'
logext = ".log"
xlsxext = '.xlsx'
samzn = 'samzn'
goldheaderrows = 1
# platinumheaderrows = 1
na = 'na'

getwordsxpath = ".//node[@pt or @pos]"

queryinfoheaderrow = ['id', 'cat', 'subcat', 'item']
queryresultsheaderrow = ['count', 'results', 'GoldCount', 'Goldresults', 'queryExists']
queryRGscoreheaderrow = ['recall', 'precision', 'f1score', 'intersection', 'gold-results', 'results-gold']
queryRPscoreheaderrow = ['platinum', 'plat_recall', 'plat_precision',
                         'plat_f1score', 'plat-results', 'results-plat']
queryGPscoreheaderrow = ['GP recall', 'GP precision', 'GP F1-score', 'GP intersection', 'P minus G', 'G minus P']

resultsheaderrow = queryinfoheaderrow + queryresultsheaderrow + queryRGscoreheaderrow + queryRPscoreheaderrow + queryGPscoreheaderrow
resultsheaderstring = tab.join(resultsheaderrow)
platinumheaderrow = ['id', 'cat', 'subcat', 'item', 'uttids', 'results-gold', 'status', 'remarks']
platinumheaderstring = tab.join(platinumheaderrow)

allmatches = {}
altcodes = {}


def checkplatinum(goldscores, platinumscores, queries):
    for qid in goldscores:
        if qid in platinumscores:
            # all values of gold must be in platinum
            if query_exists(queries[qid]):
                diff1 = goldscores[qid][2] - platinumscores[qid]
                if diff1 != Counter():
                    SDLOGGER.warning('{} has goldscores not in platinum: {}'.format(qid, diff1))


def mkerrorreport(errordict, errorreportfilename):
    header = ['name', 'count', 'uttid', 'value', 'source', 'cat', 'subcat', 'origutt', 'parsed_as']
    allrows = []
    for item in errordict:
        count = len(errordict[item])
        summaryrow = [item, count]
        allrows.append(summaryrow)
        for instance in errordict[item]:
            instancerow = instance[0:1] + instance[2:]
            fullrow = [item, ''] + instancerow
            allrows.append(fullrow)

    wb = mkworkbook(errorreportfilename, [header], allrows, freeze_panes=(1, 1))
    wb.close()


def erow(cnt):
    result = []
    for i in range(cnt):
        result.append('')
    return result


def getpostval(qid, thepostresults):
    if qid in thepostresults:
        result = thepostresults[queryid]
    else:
        result = ''
    return result


# def scores2counts(scores):
#    counts = {}
#    for el in scores:
#        countval = len(scores[el])
#        counts[el] = countval
#    return counts

def sf(number):
    if type(number) == float or type(number) == int:
        result = '{0:.1f}'.format(number)
    else:
        result = number
    return result


def getmarkedutt(m, syntree):
    thewordlist = getyield(syntree)
    thepositions = getwordpositions(m, syntree)
    themarkedyield = getmarkedyield(thewordlist, thepositions)
    yieldstr = space.join(themarkedyield)
    return yieldstr


def mark(str):
    result = '*' + str + '*'
    return result


def getwordpositionsold(matchtree, syntree):
    positions1 = []
    for node in matchtree.iter():
        if 'pt' in node.attrib:
            if 'end' in node.attrib:
                positions1.append(node.attrib['end'])

    indexednodes = {}
    for node in syntree.iter():
        if 'index' in node.attrib and ('pt' in node.attrib or 'cat' in node.attrib or 'pos' in node.attrib):
            theindex = node.attrib['index']
            indexednodes[theindex] = node

    thequery2 = ".//node[@index and not(@pt) and not(@cat)]"
    try:
        matches2 = matchtree.xpath(thequery2)
    except etree.XPathEvalError as e:
        matches2 = []
    positions2 = []
    for m in matches2:
        positions2 += getwordpositions(m, syntree)
    positions = positions1 + positions2
    result = [int(p) for p in positions]
    return result


def getwordpositions(matchtree, syntree):
    # nothing special needs to be done for index nodes since they also have begin and end
    positions = []
    for node in matchtree.iter():
        if 'end' in node.attrib:
            positions.append(node.attrib['end'])
    result = [int(p) for p in positions]
    return result


def getmarkedyield(wordlist, positions):
    pos = 1
    resultlist = []
    for w in wordlist:
        if pos in positions:
            resultlist.append(mark(w))
        else:
            resultlist.append(w)
        pos += 1
    return resultlist


def update(thedict, qid, goldtuple):
    (level, item, thecounter) = goldtuple
    if qid in thedict:
        (oldlevel, olditem, oldcounter) = thedict[qid]
        thedict[qid] = (oldlevel, olditem, oldcounter + thecounter)
    else:
        thedict[qid] = goldtuple


def logprint(str):
    print(str, file=logfile)
    if logfile != sys.stderr:
        print(str, file=sys.stderr)


def getitem2levelmap(mapping):
    resultmap: Dict[Any, List[Any]] = {}
    for (item, level) in mapping:
        if item in resultmap:
            resultmap[item].append(level)
        else:
            resultmap[item] = [level]
    return resultmap


def getcompounds(syntree):
    results = []
    tlist = syntree.xpath(getwordsxpath)
    for t in tlist:
        w = t.attrib['word']
        if compounds.iscompound(w):
            results.append(t)
    return results


def isxpathquery(query):
    cleanquery = query.lstrip()
    return cleanquery.startswith('//')


def doqueries(syntree, queries, exactresults, allmatches, criterion):
    uttid = getuttid(syntree)
    #uttid = getuttidorno(syntree)
    omittedwordpositions = getxmetatreepositions(syntree, 'Omitted Word', poslistname='annotatedposlist')
    # print(uttid)
    # core queries
    junk = 0
    for queryid in queries:
        if queryid not in exactresults:
            exactresults[queryid] = []
        thequeryobj = queries[queryid]
        if criterion(thequeryobj):
            if query_exists(thequeryobj):
                thelistedquery = thequeryobj.query
                if isxpathquery(thelistedquery):
                    expandedquery = expandmacros(thelistedquery)
                    thequery = "." + expandedquery
                    try:
                        matches = syntree.xpath(thequery)
                    except etree.XPathEvalError as e:
                        invalidqueries[queryid] = e
                        matches = []
                else:
                    thef = str2functionmap[thelistedquery]
                    matches = thef(syntree)
            else:
                matches = []
                exactresults[queryid] = []
            # matchingids = [uttid for x in matches]
            for m in matches:
                if (queryid, uttid) in allmatches:
                    allmatches[(queryid, uttid)].append((m, syntree))
                else:
                    allmatches[(queryid, uttid)] = [(m, syntree)]
                exactresult = (uttid, int(getattval(m, 'begin')) + 1)
                exactresults[queryid].append(exactresult)
            # if queryid in results:
            #    results[queryid].update(matchingids)
            # else:
            #    results[queryid] = Counter(matchingids)


def docorequeries(syntree, queries, results, allmatches):
    doqueries(syntree, queries, results, allmatches, is_core)


def doprequeries(syntree, queries, results, allmatches):
    doqueries(syntree, queries, results, allmatches, is_pre)


def dopostqueries(allresults, postquerylist, queries):
    # post queries
    for queryid in postquerylist:
        thequeryobj = queries[queryid]
        if query_exists(thequeryobj):
            thelistedquery = thequeryobj.query

            # it is assumed that these are all python functions
            thef = str2functionmap[thelistedquery]
            result = thef(allresults, queries)
            allresults.postresults[queryid] = result


def codeadapt(c):
    result = c
    result = re.sub(r'\.', r'\\.', result)
    result = re.sub(r'\(', r'\\(', result)
    result = re.sub(r'\)', r'\\)', result)
    result = re.sub(r'\?', r'\\?', result)
    result = re.sub(r'\*', r'\\*', result)
    result = re.sub(r'\+', r'\\+', result)
    result = re.sub(r' ', r'\\s+', result)
    return result


def mkpatterns(allcodes):
    basepattern = r''
    sortedallcodes = sorted(allcodes, key=len, reverse=True)
    adaptedcodes = [codeadapt(c) for c in sortedallcodes]
    basepattern = r'' + '|'.join(adaptedcodes) + '|' + itemseppattern
    fullpattern = r'^(' + basepattern + r')*$'
    return (re.compile(basepattern), re.compile(fullpattern))


def get_definedfornonemptygold(goldscores, queries):
    undefinedqueries = []
    definedfornonemptygoldscore = 0
    for queryid in goldscores:
        if goldscores[queryid] != emptycounter:
            if queryid in queries:
                if queries[queryid].query != '':
                    definedfornonemptygoldscore += 1
                else:
                    undefinedqueries.append(queryid)
    return (definedfornonemptygoldscore, undefinedqueries)


def get_comparison(resultscounts, goldcounts, queries):
    comparison = []
    for qid in queries:
        if qid in goldcounts:
            gold = goldcounts[qid]
            if qid in resultscounts:
                res = resultscounts[qid]
            else:
                res = 0
        else:
            gold = 0
            if qid in resultscounts:
                res = resultscounts[qid]
            else:
                res = 0
        comparison.append((qid, res, gold))
    return comparison


def getmethodfromfile(filename):
    result = ''
    path, base = os.path.split(filename.lower())
    for m in supported_methods:
        if m in base:
            result = m
    if result == '':
        SDLOGGER.error('No supported method found in filename')
        exit(-1)
    else:
        return result


def treatmethod(methodname, methodfilename):
    if methodname is None and methodfilename is None:
        SDLOGGER.error('Specify a method using -m ')
        exit(-1)
    elif methodname is None and methodfilename is not None:
        resultmethodfilename = methodfilename
        resultmethodname = getmethodfromfile(methodfilename)
        SDLOGGER.warning('Method derived from the method file name: {}'.format(resultmethodname))
    elif methodname is not None and methodfilename is None:
        if methodname.lower() in supported_methods:
            resultmethodname = methodname.lower()
            resultmethodfilename = supported_methods[methodname]
        else:
            resultmethodfilename = methodname
            resultmethodname = getmethodfromfile(methodname)
            SDLOGGER.warning('Method derived from the method file name: {}'.format(resultmethodname))
    elif methodname is not None and methodfilename is not None:
        if methodname.lower() in supported_methods:
            resultmethodname = methodname.lower()
            resultmethodfilename = methodfilename
        else:
            SDLOGGER.error('Unsupported method specified {}'.format(methodname))
            exit(-1)
    return resultmethodname, resultmethodfilename


topnodequery = './/node[@cat="top"]'


def getexactresults(allmatches):
    result = defaultdict(list)
    for (queryid, uttid) in allmatches:
        matchresults = []
        wholeuttmatch = False
        for (m, _) in allmatches[(queryid, uttid)]:
            # @@hier de topnode opzoeken@@
            if m is None:
                position = 0
                SDLOGGER.error('None match found')
            else:
                topnodes = m.xpath(topnodequery)
                if topnodes != []:
                    positionstr = getattval(topnodes[0], 'begin')
                    wholeuttmatch = True
                else:
                    positionstr = getattval(m, 'begin')
                    wholeuttmatch = getattval(m, 'cat') == 'top'
                try:
                    position = int(positionstr)
                except ValueError:
                    position = 0
                    SDLOGGER.error('getexactresults ValueError')
                else:
                    if not wholeuttmatch:
                        position += 1
            matchresults.append((uttid, position))
        result[queryid] += matchresults
    return result


def exact2results(exactresults):
    '''
    :param exactresults: dictionary key= query id, value is a list of (uttid, position) pairs
    :return: dictionary(key -queryid, value is a counter uttid: count
    '''
    results = {}
    for qid in exactresults:
        uttidlist = [uttid for (uttid, _) in exactresults[qid]]
        resultvalue = Counter(uttidlist)
        results[qid] = resultvalue
    return results


def passfilter(rawexactresults, method):
    '''
    let's only those through that satisfy the
    :param rawexactresults: dictionary with queryid as key and a Counter as value, exact results
    :param method: Method object
    :return: a filtered version of raw exact results: results that pass the filter
    '''
    exactresults = defaultdict(list)
    queries = method.queries
    for queryid in rawexactresults:
        query = queries[queryid]
        queryfilter = query.special2
        thefilter = method.defaultfilter if queryfilter is None or queryfilter == '' else str2functionmap[queryfilter]
        exactresults[queryid] = [r for r in rawexactresults[queryid] if thefilter(query, rawexactresults, r)]
    return exactresults


defaulttarsp = r"TARSP Index Current.xlsx"

parser = OptionParser()
parser.add_option("-f", "--file", dest="infilename",
                  help="Treebank File to be analysed")
parser.add_option("-m", "--method", dest="methodname",
                  help="Name of the method or (for backwards compatibility) "
                       "file containing definition of assessment method (SAM)")
parser.add_option("-a", "--anno", dest="annotationfilename",
                  help="SASTA Annotation Format File containing annotations to derive a  reference")
parser.add_option("-g", "--gold", dest="goldfilename",
                  help="File containing a gold reference in SASTA Reference Format")
parser.add_option("-c", "--goldcounts", dest="goldcountsfilename",
                  help="File containing  gold reference counts in  SASTA Counts Reference Format")
parser.add_option("-p", "--plat", dest="platinuminfilename",
                  help="File containing a platinum reference in SASTA Reference Format")
parser.add_option("-i", "--impl", dest="includeimplies", action="store_true",
                  help="Use the implies column of the method", default=False)
parser.add_option("-l", "--log", dest="logfilename",
                  help="File for logging")
parser.add_option("--corr", dest="corr", default='n',
                  help="0=No correction; 1=correction with 1 alternative; "
                       "n=correction with multiple alternatives (default) ")
parser.add_option("--mf", "--mfile", dest="methodfilename",
                  help="File containing definition of assessment method (SAM)")

(options, args) = parser.parse_args()

if options.corr is None:
    options.corr = corrn
if options.corr not in validcorroptions:
    validcorrstr = comma.join(validcorroptions)
    SDLOGGER.error('Illegal value for -c/--corr option: only the following are allowed: {}'.format(validcorrstr))
    exit(-1)

# @ hier ook toestaan dat er een annotatiefile als input komt (.xlsx)-done
if options.infilename is None:  # an XML file or an.xlsx file
    SDLOGGER.error('Specify an input treebank file name to analyse (.xml) or the name of an annotationfile (.xlsx)')
    exit(1)
(inbase, inext) = os.path.splitext(options.infilename)
if inext not in ['.xml', '.xlsx']:
    SDLOGGER.error('Illegal input file type: must be a treebank (.xml) or an annotationfile (.xlsx)')
    exit(1)
elif inext in ['.xlsx']:
    annotationinput = True
else:
    annotationinput = False

if options.logfilename is None:
    options.logfilename = inbase + logext

options.methodname, options.methodfilename = treatmethod(options.methodname, options.methodfilename)

# testlogfilename = inbase + "-test" + logext
# logfile = open(options.logfilename, 'w', encoding='utf8')
SDLOGGER.basicConfig(level=logging.INFO)
handler = SDLOGGER.FileHandler(options.logfilename, 'w', encoding='utf8')
logformat = '%(levelname)s:%(message)s'
formatter = SDLOGGER.Formatter(logformat)
handler.setFormatter(formatter)
root_logger = SDLOGGER.getLogger()
root_logger.addHandler(handler)
root_logger.setLevel(SDLOGGER.INFO)

SDLOGGER.info('Start of logging')

if options.annotationfilename is not None and options.goldcountsfilename is not None:
    SDLOGGER.info('Annotation file and Gold counts file found; gold counts file ignored')
elif options.goldfilename is not None and options.goldcountsfilename is not None:
    SDLOGGER.info('Gold Reference file and Gold counts file found; gold counts file ignored')

if options.methodfilename is None:  # an xslx file
    options.methodfilename = defaulttarsp
if options.annotationfilename is None:  # an xlsx file
    options.annotationfilename = inbase + ".anno" + '.xslx'
if options.platinuminfilename is None:
    options.platinuminfilename = inbase + platinumeditedsuffix + txtext

if options.goldfilename is not None and options.annotationfilename is not None:
    SDLOGGER.info('annotationfile and goldfile specified. Annotationfile will be used.')
if options.goldfilename is None:
    options.goldfilename = inbase + ".gold" + ".tsv" + ".txt"
if options.goldcountsfilename is None:
    options.goldcountsfilename = inbase + ".goldcounts" + ".xlsx"

invalidqueries = {}

(queries, item2idmap, altcodes, postorformquerylist) = read_method(options.methodfilename)
defaultfilter = defaultfilters[options.methodname]
themethod = Method(options.methodname, queries, item2idmap, altcodes, postorformquerylist,
                   options.methodfilename, defaultfilter)

# annotationfilename = r"D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\Auris\AurisdataAligned Current_out.tsv"
# annotationfilename = r"D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\Auris\AurisdataAligned TagsCleaned Current_out.tsv"

# print('annotationfilename=', options.annotationfilename, file=sys.stderr )

# read the annotation reference file if available, otherwise the gold file, otherwise quit
goldscores = {}
if options.annotationfilename != '' and os.path.exists(options.annotationfilename):
    allannutts, richexactgoldscores = get_golddata(options.annotationfilename, item2idmap, altcodes, queries,
                                                   options.includeimplies)
    annuttcount = len(allannutts)
    exactgoldscores = richscores2scores(richexactgoldscores)
    richgoldscores = richexact2global(richexactgoldscores)
    goldscores = richgoldscores
    goldcounts = scores2counts(goldscores)
    goldcountfilename = options.annotationfilename + ".goldcount.tsv.txt"
    goldcountfile = open(goldcountfilename, 'w', encoding='utf8')
    for el in goldcounts:
        print(el, goldcounts[el], sep=tab, file=goldcountfile)
    goldcountfile.close()
    reffilename = options.annotationfilename
elif options.goldfilename != '' and os.path.exists(options.goldfilename):
    goldscores = read_referencefile(options.goldfilename, logfile)
    goldcounts = scores2counts(goldscores)
    reffilename = options.goldfilename
elif options.goldcountsfilename != '' and os.path.exists(options.goldcountsfilename):
    goldcounts = get_goldcounts(options.goldcountsfilename)
    if goldcounts == {}:
        SDLOGGER.error('No gold counts found. Aborting')
        exit(-1)
    else:
        reffilename = options.goldcountsfilename
else:
    SDLOGGER.error('Neither an annotationfile nor a goldfile, nor a gold count file specified. Aborting')
    exit(1)

# rawcoreresults = {}
# exact = True
rawexactresults = defaultdict(list)

# @dit aanpassen , voor al de message-done
if not os.path.exists(options.infilename):
    SDLOGGER.error('Input treebank or annotationfile {} not found. Aborting'.format(options.infilename))
    exit(1)

# gather remarks on results of earlier runs, write them to a perm_file  and adapt the silverscore file

path2permfolder = 'silverperm'
(pathname, barefilename) = os.path.split(options.infilename)
(base, ext) = os.path.splitext(barefilename)
(fullbase, _) = os.path.splitext(options.infilename)
permpath = os.path.join(pathname, path2permfolder)

try:
    os.makedirs(permpath)
except FileExistsError:
    pass

perm_silverfilename = permprefix + base + '.xlsx'
perm_silverfullname = os.path.join(permpath, perm_silverfilename)
#
platinumcheckeditedfullname = fullbase + platinumcheckeditedsuffix + '.xlsx'

platinumoutfilename = fullbase + platinumsuffix + txtext
platinumcheckfilename = fullbase + platinumchecksuffix + txtext
silvercheckfilename = fullbase + platinumchecksuffix + '.xlsx'

(platbase, platext) = os.path.splitext(platinumcheckfilename)
platinumcheckxlfullname = platbase + '.xlsx'

silverannotationsdict = getsilverannotations(perm_silverfullname, platinumcheckeditedfullname,
                                             platinumcheckxlfullname, silvercheckfilename,
                                             platinumoutfilename, options.platinuminfilename, goldscores)

analysedtrees = []

# @vanaf nu gaat het om een treebank, dus hier een if statement toevoegen-done
if annotationinput:
    allutts, richexactscores = get_golddata(options.infilename, item2idmap, altcodes, queries, options.includeimplies)
    uttcount = len(allutts)
    exactresults = richscores2scores(richexactscores)
else:
    tree = etree.parse(options.infilename)
    origtreebank = tree.getroot()
    if origtreebank.tag != 'treebank':
        SDLOGGER.ERROR("Input treebank file does not contain a treebank element")
        exit(-1)
    allutts = {}
    uttcount = 0
    # determine targets
    targets = get_targets(origtreebank)
    treebank, errordict, allorandalts = correcttreebank(origtreebank, targets, options.methodname, options.corr)

    # create the new treebank
    fulltreebank = etree.ElementTree(treebank)
    newtreebankfilename = fullbase + '_corrected' + '.xml'
    fulltreebank.write(newtreebankfilename, encoding="UTF8", xml_declaration=False,
                       pretty_print=True)

    # create error file
    errorreportfilename = fullbase + '_errorreport' + '.xlsx'
    mkerrorreport(errordict, errorreportfilename)

    # create error logging
    errorloggingfilename = fullbase + '_errorlogging' + '.xlsx'

    allerrorrows = []
    for orandalts in allorandalts:
        allerrorrows += orandalts.OrigandAlts2rows(base)
    errorwb = mkworkbook(errorloggingfilename, [errorwbheader], allerrorrows, freeze_panes=(1, 1))
    errorwb.close()

    analysedtrees = []
    for syntree in treebank:
        uttcount += 1
        # SDLOGGER.error('uttcount={}'.format(uttcount))
        mustbedone = get_mustbedone(syntree, targets)
        if mustbedone:
            analysedtrees.append(syntree)
            doprequeries(syntree, queries, rawexactresults, allmatches)
            docorequeries(syntree, queries, rawexactresults, allmatches)
        uttid = getuttid(syntree)
        #uttno = getuttno(syntree)
        #allutts[uttno] = getyield(syntree)
        allutts[uttid] = getyield(syntree)

    # determine exactresults and apply the filter to catch interdependencies between prequeries and corequeries
    # rawexactresults = getexactresults(allmatches)
    exactresults = passfilter(rawexactresults, themethod)

# @ en vanaf hier kan het weer gemeenschappelijk worden; er met dus ook voor de annotatiefile een exactresults opgeleverd worden
# @d epostfunctions for lemma's etc moeten mogelijk wel aangepast worden


coreresults = exact2results(exactresults)

postresults = {}
allresults = AllResults(uttcount, coreresults, exactresults, postresults, allmatches, options.infilename, analysedtrees,
                        allutts, annotationinput)

postquerylist = [q for q in postorformquerylist if queries[q].process == post_process]
formquerylist = [q for q in postorformquerylist if queries[q].process == form_process]

dopostqueries(allresults, postquerylist, queries)
dopostqueries(allresults, formquerylist, queries)

(base, ext) = os.path.splitext(options.infilename)
outputfilename = base + "_analysis" + tsvext + txtext
outfile = open(outputfilename, 'w', encoding='utf8')

outxlsx = base + "_analysis" + xlsxext
outworkbook = xlsxwriter.Workbook(outxlsx, {"strings_to_numbers": True})
outworksheet = outworkbook.add_worksheet()
outstartrow = 0
outstartcol = 0
outrowctr = outstartrow
outworksheet.freeze_panes('E2')

platinuminfilefound = False
if os.path.exists(options.platinuminfilename):
    platinuminfilefound = True
    platinumresults = read_referencefile(options.platinuminfilename, logfile)
    checkplatinum(goldscores, platinumresults, queries)
else:
    SDLOGGER.info('Platinum file {} not found.'.format(options.platinuminfilename))
    platinumresults = {}

# platinumoutfilename = base + platinumsuffix + txtext
platinumoutfile = open(platinumoutfilename, 'w', encoding='utf8')
# platinumcheckfilename = base + platinumchecksuffix + txtext
platinumcheckfile = open(platinumcheckfilename, 'w', encoding='utf8')

countcomparisonfilename = base + '_countcomparison' + '.tsv' + '.txt'

# print the invalid queries
for q in invalidqueries:
    SDLOGGER.error("{}: {}: <{}>".format(q, invalidqueries[q], queries[q].query))

# print the header
print(resultsheaderstring, file=outfile)
outworksheet.write_row(outrowctr, outstartcol, resultsheaderrow)
outrowctr += 1

# print the platinumheader
print(platinumheaderstring, file=platinumoutfile)

# print the results
qcount = 0
invalidqcount = 0
undefinedqcount = 0
results = allresults.coreresults
# exactresults = getexactresults(allmatches)
exact = True

pcheaders = [['User1', 'User2', 'User3', 'MoreorLess', 'qid', 'cat', 'subcat', 'item', 'uttid', 'pos', 'utt']]
allrows = []

for queryid in results:
    sortedgolduttlist = []
    platinumoutresults = Counter()
    platinumoutresultsstring = ''
    qcount += 1
    theresults = results[queryid]
    resultstr = counter2liststr(theresults)
    if queryid in goldscores:
        # (goldlevel, golditem, goldcounter) = goldscores[queryid]
        goldcounter = goldscores[queryid][2]
        goldcount = sumfreq(goldcounter)
        sortedgolduttstr = counter2liststr(goldcounter)
    else:
        goldcount = 0
        sortedgolduttstr = ''
    thequery = queries[queryid]
    if query_exists(thequery):
        if queryid not in invalidqueries:
            qex = 'yes'
        else:
            qex = 'invalid'
            invalidqcount += 1
    else:
        qex = 'no'
        undefinedqcount += 1
    if query_exists(thequery) and queryid not in invalidqueries:
        # print(queryid, file=logfile)
        if queryid in goldscores:
            goldcounter = goldscores[queryid][2]
        else:
            goldcounter = Counter()
        (recall, precision, f1score) = getscores(theresults, goldcounter)
        liststargoldstr = counter2liststr(theresults & goldcounter)
        goldminustheresults = goldcounter - theresults
        goldminusliststr = counter2liststr(goldminustheresults)
        theresultsminusgold = theresults - goldcounter
        listminusgoldstr = counter2liststr(theresultsminusgold)
        if platinuminfilefound and queryid in platinumresults:
            theplatinumresults = platinumresults[queryid]
            sortedplatinumliststr = counter2liststr(theplatinumresults)
            liststarplatinumstr = counter2liststr(theresults & theplatinumresults)
            platinumminusliststr = counter2liststr(theplatinumresults - theresults)
            listminusplatinumliststr = counter2liststr(theresults - theplatinumresults)
            (platinumrecall, platinumprecision, platinumf1score) = getscores(theresults, theplatinumresults)

            goldstarplatinumstr = counter2liststr(goldcounter & theplatinumresults)
            platinumminusgoldstr = counter2liststr(theplatinumresults - goldcounter)
            goldminusplatinumstr = counter2liststr(goldcounter - theplatinumresults)
            (gprecall, gpprecision, gpf1score) = getscores(goldcounter, theplatinumresults)
        else:
            sortedplatinumliststr, liststarplatinumliststr, platinumminusliststr, listminusplatinumliststr = '', '', '', ''
            (platinumrecall, platinumprecision, platinumf1score) = (na, na, na)

            goldstarplatinumstr, platinumminusgoldstr, goldminusplatinumstr = '', '', ''
            (gprecall, gpprecision, gpf1score) = (na, na, na)

    else:
        goldcounter = Counter()
        (recall, precision, f1score) = (na, na, na)
        liststargoldstr, goldminusliststr, listminusgoldstr = '', '', ''
        sortedplatinumliststr, liststarplatinumliststr, platinumminusliststr, listminusplatinumliststr = '', '', '', ''
        (platinumrecall, platinumprecision, platinumf1score) = (na, na, na)
        theresultsminusgold = {}
        goldminustheresults = {}
        goldstarplatinumstr, platinumminusgoldstr, goldminusplatinumstr = '', '', ''
        (gprecall, gpprecision, gpf1score) = (na, na, na)

    platinumoutresults = theresults | goldcounter
    platinumoutresultsstring = counter2liststr(platinumoutresults)

    queryinforow = [queryid, queries[queryid].cat, queries[queryid].subcat, queries[queryid].item]
    queryresultsrow = [str(sumfreq(theresults)), resultstr, str(goldcount), sortedgolduttstr, qex]
    queryRGscorerow = [sf(recall), sf(precision), sf(f1score), liststargoldstr, goldminusliststr, listminusgoldstr]
    queryRPscorerow = [sortedplatinumliststr, sf(platinumrecall), sf(platinumprecision), sf(platinumf1score),
                       platinumminusliststr, listminusplatinumliststr]
    queryGPscorerow = [sf(gprecall), sf(gpprecision), sf(gpf1score), goldstarplatinumstr, platinumminusgoldstr,
                       goldminusplatinumstr]

    fullresultrow = queryinforow + queryresultsrow + queryRGscorerow + queryRPscorerow + queryGPscorerow
    print(tab.join(fullresultrow), file=outfile)
    outworksheet.write_row(outrowctr, outstartcol, fullresultrow)
    outrowctr += 1

    platinumrow = [queryid, queries[queryid].cat, queries[queryid].subcat, queries[queryid].item,
                   platinumoutresultsstring, listminusgoldstr, '', '']

    print(tab.join(platinumrow), file=platinumoutfile)

    # @with an annotationfile allmatches is empty so we need to redefine newrows (exactmismatches) markedutt (getmarkedutt)-done
    if exact:
        newrows = exactmismatches(queryid, queries, exactresults, exactgoldscores, allmatches, allutts,
                                  platinumcheckfile, silverannotationsdict, annotationinput)
        allrows += newrows
    else:
        if theresultsminusgold != {}:
            print('More examples', file=platinumcheckfile)
        for uttid in theresultsminusgold:
            if (queryid, uttid) in allmatches:
                for (m, syntree) in allmatches[(queryid, uttid)]:
                    markedutt = getmarkedutt(m, syntree)
                    platinumcheckrow1 = [queryid, queries[queryid].cat, queries[queryid].subcat, queries[queryid].item,
                                         uttid, markedutt]
                    print(tab.join(platinumcheckrow1), file=platinumcheckfile)

        if goldminustheresults != {}:
            print('Missed examples', file=platinumcheckfile)
        for uttid in goldminustheresults:
            if uttid in allutts:
                uttstr = space.join(allutts[uttid])
            else:
                SDLOGGER.warning('uttid {} not in allutts'.format(uttid))
            platinumcheckrow2 = [queryid, queries[queryid].cat, queries[queryid].subcat, queries[queryid].item, uttid,
                                 uttstr]
            print(tab.join(platinumcheckrow2), file=platinumcheckfile)

platinumcheckfullname = platinumcheckfile.name
(base, ext) = os.path.splitext(platinumcheckfullname)
# platinumcheckxlfullname = base + '.xlsx'
wb = mkworkbook(platinumcheckxlfullname, pcheaders, allrows, freeze_panes=(1, 9))
wb.close()

# compute the gold postresults
goldpostresults = {}
goldcounters = {}
allgoldmatches = {}
for qid in goldscores:
    goldcounters[qid] = goldscores[qid][2]
allgoldresults = AllResults(uttcount, goldcounters, exactgoldscores, goldpostresults, allgoldmatches, reffilename, [],
                            allannutts, annotationinput)
dopostqueries(allgoldresults, postquerylist, queries)

# compute the platinum postresults

platinumpostresults = {}

# print the postresults
thepostresults = allresults.postresults
for queryid in postquerylist:
    resultposval = str(getpostval(queryid, thepostresults))
    goldpostval = str(getpostval(queryid, goldpostresults))
    platinumpostval = str(getpostval(queryid, platinumpostresults))
    if queries[queryid].query != '':
        qex = 'yes'
    else:
        qex = 'no'

    queryinforow = [queryid, queries[queryid].cat, queries[queryid].subcat, queries[queryid].item]
    queryresultsrow = ['', resultposval, '', goldpostval, qex] + erow(6) + [platinumpostval] + erow(11)

    postrow = queryinforow + queryresultsrow
    postrowstring = tab.join(queryinforow + queryresultsrow)
    print(postrowstring, sep=tab, file=outfile)
    outworksheet.write_row(outrowctr, outstartcol, postrow)
    outrowctr += 1

# gather overall results, 2 cases: (1)for defined original measure queries only; (2) for all original measure queries

overallmethods = [(1, 'Overall (defined pre and core queries in the profile)',
                   lambda x: is_preorcore(x) and query_exists(x) and query_inform(x)),
                  (2, 'Overall (all pre and core queries in the profile)',
                   lambda x: is_preorcore(x) and query_inform(x)),
                  (3, 'Overall (original pre and core measures with defined queries only)',
                   lambda x: is_preorcore(x) and query_exists(x)),
                  (4, 'Overall (all original pre and core measures)', lambda x: is_preorcore(x))]

logheader = ['datetime', 'treebank', 'scorenr,' 'R', 'P', 'F1', 'P-R', 'P-P', 'P-F1', 'GP-R', 'GP-P', 'GP-F1', 'ref',
             'method']
logname = 'sastalog.txt'
biglogfile = open(logname, 'a', encoding='utf8')

exactlynow = datetime.datetime.now()
now = exactlynow.replace(microsecond=0).isoformat()

for (ctr, message, queryfunction) in overallmethods:
    # gather resultscount
    resultscount = 0
    for queryid in results:
        thequery = queries[queryid]
        if thequery.original and queryfunction(thequery):
            resultscount += sum(results[queryid].values())

    # gather goldcount
    goldcount = 0
    for queryid in goldscores:
        thequery = queries[queryid]
        goldcounter = goldscores[queryid][2]
        if thequery.original and queryfunction(thequery):
            goldcount += sum(goldcounter.values())

    # gather platinumcount
    platinumcount = 0
    for queryid in platinumresults:
        if queryid in queries:
            thequery = queries[queryid]
            if thequery.original and queryfunction(thequery):
                platinumcount += sum(platinumresults[queryid].values())
        else:
            SDLOGGER.warning('Query {} found in platinumresults but not in queries'.format(queryid))

    # resultsgoldintersectiocount
    resultsgoldintersectioncount = 0
    for queryid in results:
        thequery = queries[queryid]
        if thequery.original and queryfunction(thequery):
            if queryid in goldscores:
                goldcounter = goldscores[queryid][2]
                intersection = results[queryid] & goldcounter
                resultsgoldintersectioncount += sum(intersection.values())
            else:
                pass
                # SDLOGGER.warning('Query {} found in results but not in goldscores'.format(queryid))

    # resultsplatinumintersectioncount
    resultsplatinumintersectioncount = 0
    for queryid in results:
        thequery = queries[queryid]
        if thequery.original and queryfunction(thequery):
            if queryid in platinumresults:
                intersection = results[queryid] & platinumresults[queryid]
                resultsplatinumintersectioncount += sum(intersection.values())
            else:
                pass
                # SDLOGGER.warning('queryid {} not in platinumresults'.format(queryid))

    # goldplatinumintersectioncount
    goldplatinumintersectioncount = 0
    for queryid in platinumresults:
        if queryid in queries:
            thequery = queries[queryid]
            if thequery.original and queryfunction(thequery):
                if queryid in goldscores:
                    goldcounter = goldscores[queryid][2]
                    intersection = goldcounter & platinumresults[queryid]
                    goldplatinumintersectioncount += sum(intersection.values())
                else:
                    pass
                    # SDLOGGER.warning('Query {} in platinumresults but not in goldscores'.format(queryid))
        else:
            SDLOGGER.warning('Query {} in platinumresults but not in queries'.format(queryid))

    (recall, precision, f1score) = getevalscores(resultscount, goldcount, resultsgoldintersectioncount)
    (platinumrecall, platinumprecision, platinumf1score) = getevalscores(resultscount, platinumcount,
                                                                         resultsplatinumintersectioncount)
    (gprecall, gpprecision, gpf1score) = getevalscores(goldcount, platinumcount, goldplatinumintersectioncount)

    overallrow = ['', '', '', message, '', '', '', '', '', sf(recall), sf(precision), sf(f1score),
                  '', '', '', '', sf(platinumrecall), sf(platinumprecision), sf(platinumf1score), '', '',
                  sf(gprecall), sf(gpprecision), sf(gpf1score), '', '', '']

    print(tab.join(overallrow), file=outfile)
    outworksheet.write_row(outrowctr, outstartcol, overallrow)
    outrowctr += 1

    logrow = [now, options.infilename, str(ctr), sf(recall), sf(precision), sf(f1score),
              sf(platinumrecall), sf(platinumprecision), sf(platinumf1score),
              sf(gprecall), sf(gpprecision), sf(gpf1score),
              reffilename, options.methodfilename]

    print(tab.join(logrow), file=biglogfile)

biglogfile.close()
outfile.close()
outworkbook.close()
platinumoutfile.close()
platinumcheckfile.close()

resultscounts = scores2counts(results)

countcomparison = get_comparison(resultscounts, goldcounts, queries)
if countcomparison != []:
    countcomparisonfile = open(countcomparisonfilename, 'w', encoding='utf8')
    ccheader = ['Measure', 'result', 'gold', 'diff']
    ccheaderstr = tab.join(ccheader)
    print(ccheaderstr, file=countcomparisonfile)
    for (q, r, g) in countcomparison:
        if not (r == 0 and g == 0):
            print(q, r, g, r - g, sep=tab, file=countcomparisonfile)

definedqcount = qcount - undefinedqcount

emptycounter = Counter()

(definedfornonemptygoldscore, undefinedqueries) = get_definedfornonemptygold(goldscores, queries)
(definedfornonemptygoldcounts, undefinedqueries) = get_definedfornonemptygold(goldcounts, queries)

lgoldscores = len(goldscores)

if lgoldscores != 0:
    percentagecompletion1 = definedfornonemptygoldscore / lgoldscores * 100
    percentagecompletion1str = '{0:.1f}%'.format(percentagecompletion1)
else:
    percentagecompletion1str = 'N/A'

lgoldcounts = len(goldcounts)
if lgoldcounts != 0:
    percentagecompletion2 = definedfornonemptygoldcounts / lgoldcounts * 100
    percentagecompletion2str = '{0:.1f}%'.format(percentagecompletion2)
else:
    percentagecompletion2str = 'N/A'

finalmessagetemplate1 = '{} measures, {} undefined, {} defined,  of which {} invalid.'
finalmessagetemplate2 = '{} measures defined for a non empty gold score out of {} ({}).'
finalmessagetemplate3 = '{} measures defined for a non empty gold count out of {} ({}).'
print(finalmessagetemplate1.format(qcount, undefinedqcount, definedqcount, invalidqcount))
print(finalmessagetemplate2.format(definedfornonemptygoldscore, lgoldscores, percentagecompletion1str))
print(finalmessagetemplate3.format(definedfornonemptygoldcounts, lgoldcounts, percentagecompletion2str))
print('Undefined queries:', undefinedqueries)
SDLOGGER.info("Done!")
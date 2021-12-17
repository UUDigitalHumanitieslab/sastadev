'''
offers the function get_annotations() to obtain a dictionary with the annotations from a file
for the moment at the utteranceid level, to be extend edto the wordposition per uttid level

and the function read_annotations() to obtain a score dictionary with queryid as keys and Counter() as values
'''

#todo
#-additional columns unaligned treatment and generalisation
#-code alternatives and replacemtne extensions
#=codes written without spaces?

import os
import re
from collections import Counter, defaultdict

import xlrd

from config import SDLOGGER
from readmethod import itemseppattern, read_method

varitem = ''

txtext = ".txt"
comma = ","
tsvext = '.tsv'
commaspace = ', '
tab = '\t'
all_levels = set()
literallevels = ['lemma']

semicolon = ';'
labelsep = semicolon

wordcolheaderpattern = r'^\s*word\d+\s*$'
wordcolheaderre = re.compile(wordcolheaderpattern)
firstwordcolheaderpattern = r'^\s*word0*1\s*$'
firstwordcolheaderre = re.compile(firstwordcolheaderpattern)

speakerheaders = ['speaker', 'spreker', 'spk']
uttidheaders = ['id', 'utt', 'uttid']
levelheaders = ['level']
stagesheaders = ['fases', 'stages']
commentsheaders = ['comments', 'commentaar']


def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n - 1, type))


def clean(label):
    result = label
    result = result.lstrip()
    result = result.rstrip()
    result = result.lower()
    return result


def getlabels(labelstr, patterns):
    results = []
    (pattern, fullpattern) = patterns
    if fullpattern.match(labelstr):
        ms = pattern.finditer(labelstr)
        results = [m.group(0) for m in ms if m.group(0) not in ' ;,-/']
    else:
        results = []
        ms = pattern.finditer(labelstr)
        logstr = str([m.group(0) for m in ms if m.group(0) not in ' ;,-'])
        #print('Cannot interpret {};  found items: {}'.format(labelstr,logstr), file=sys.stderr)
        SDLOGGER.warning('Cannot interpret %s; found items: %s', labelstr, logstr)
        #exit(-1)
    return results


def iswordcolumn(str):
    result = wordcolheaderre.match(str.lower())
    return result


def isfirstwordcolumn(str):
    result = firstwordcolheaderre.match(str.lower())
    return result


def enrich(labelstr, lcprefix):
    labels = labelstr.split(labelsep)
    newlabels = []
    for label in labels:
        cleanlabel = clean(label)
        if label != "" and lcprefix != "":
            newlabels.append(lcprefix + ":" + cleanlabel)
        else:
            newlabels.append(cleanlabel)
    result = labelsep.join(newlabels)
    return result


def getcleanlevelsandlabels(thelabelstr, thelevel, prefix, patterns):
    results = []
    lcthelabelstr = thelabelstr.lower()
    lcprefix = prefix.lower().strip()
    lcthelabelstr = enrich(lcthelabelstr, lcprefix)
    thelabels = getlabels(lcthelabelstr, patterns)
    for thelabel in thelabels:
        if thelabel != "":
            cleanlabel = thelabel
            cleanlevel = clean(thelevel)
            result = (cleanlevel, cleanlabel)
            results.append(result)

    return results


def oldget_annotations(infilename, patterns):
    '''
    Reads the file with name filename in SASTA Annotation Format
    :param infilename:
    :param patterns
    :return: a dictionary  with as  key a tuple (level, item) and as value a Counter  with key uttid and value its count
    '''

    thedata = defaultdict(list)
    exactdata = defaultdict(list)
    cdata = {}

    # To open Workbook
    wb = xlrd.open_workbook(infilename)
    sheet = wb.sheet_by_index(0)

    startrow = 0
    startcol = 0
    headerrow = 0
    headers = {}
    lastrow = sheet.nrows
    lastcol = sheet.ncols
#    firstwordcol = 2
#    lastwordcol = lastcol - 4
    levelcol = 1
    uttidcol = 0
    stagescol = -1
    commentscol = -1

    uttlevel = 'utt'

    for rowctr in range(startrow, lastrow):
        if rowctr == headerrow:
            for colctr in range(startcol, lastcol):
                headers[colctr] = sheet.cell_value(rowctr, colctr)
                if iswordcolumn(headers[colctr]):
                    lastwordcol = colctr
                    if isfirstwordcolumn(headers[colctr]):
                        firstwordcol = colctr
                elif clean(headers[colctr]) in speakerheaders:
                    spkcol = colctr
                elif clean(headers[colctr]) in uttidheaders:
                    uttidcol = colctr
                elif clean(headers[colctr]) in levelheaders:
                    levelcol = colctr
                elif clean(headers[colctr]) in stagesheaders:
                    stagescol = colctr
                elif clean(headers[colctr]) in commentsheaders:
                    commentscol = colctr
        else:
            if sheet.cell_value(rowctr, uttidcol) != "":
                uttid = str(int(sheet.cell_value(rowctr, uttidcol)))
            thelevel = sheet.cell_value(rowctr, levelcol)
            thelevel = clean(thelevel)
            all_levels.add(thelevel)
            for colctr in range(firstwordcol, sheet.ncols):
                if thelevel in literallevels and colctr != stagescol and colctr != commentscol:
                    thelabel = sheet.cell_value(rowctr, colctr)
                    if colctr > lastwordcol:
                        tokenposition = 0
                    else:
                        tokenposition = colctr - firstwordcol + 1
                    thedata[(thelevel, thelabel)].append(uttid)
                    exactdata[(cleanlevel, cleanlabel)].append((uttid, tokenposition))
                elif thelevel != uttlevel and colctr != stagescol and colctr != commentscol:
                    thelabelstr = sheet.cell_value(rowctr, colctr)
                    thelevel = sheet.cell_value(rowctr, levelcol)
                    if lastwordcol + 1 <= colctr < sheet.ncols:
                        #prefix = headers[colctr] aangepast om het simpeler te houden
                        prefix = ""
                    else:
                        prefix = ""
                    cleanlevelsandlabels = getcleanlevelsandlabels(thelabelstr, thelevel, prefix, patterns)
                    if colctr > lastwordcol:
                        tokenposition = 0
                    else:
                        tokenposition = colctr - firstwordcol + 1
                    for (cleanlevel, cleanlabel) in cleanlevelsandlabels:
                        thedata[(cleanlevel, cleanlabel)].append(uttid)
                        exactdata[(cleanlevel, cleanlabel)].append((uttid, tokenposition))
    #wb.close() there is no way to close the workbook
    for atuple in thedata:
        cdata[atuple] = Counter(thedata[atuple])
    return cdata


def get_annotations(infilename, patterns):
    '''
    Reads the file with name filename in SASTA Annotation Format
    :param infilename:
    :param patterns
    :return: a dictionary  with as  key a tuple (level, item) and as value a list of (uttid, tokenposition) pairs
    '''

    thedata = defaultdict(list)
    cdata = {}

    # To open Workbook
    wb = xlrd.open_workbook(infilename)
    sheet = wb.sheet_by_index(0)

    startrow = 0
    startcol = 0
    headerrow = 0
    headers = {}
    lastrow = sheet.nrows
    lastcol = sheet.ncols
#    firstwordcol = 2
#    lastwordcol = lastcol - 4
    levelcol = 1
    uttidcol = 0
    stagescol = -1
    commentscol = -1

    uttlevel = 'utt'

    for rowctr in range(startrow, lastrow):
        if rowctr == headerrow:
            for colctr in range(startcol, lastcol):
                headers[colctr] = sheet.cell_value(rowctr, colctr)
                if iswordcolumn(headers[colctr]):
                    lastwordcol = colctr
                    if isfirstwordcolumn(headers[colctr]):
                        firstwordcol = colctr
                elif clean(headers[colctr]) in speakerheaders:
                    spkcol = colctr
                elif clean(headers[colctr]) in uttidheaders:
                    uttidcol = colctr
                elif clean(headers[colctr]) in levelheaders:
                    levelcol = colctr
                elif clean(headers[colctr]) in stagesheaders:
                    stagescol = colctr
                elif clean(headers[colctr]) in commentsheaders:
                    commentscol = colctr
        else:
            if sheet.cell_value(rowctr, uttidcol) != "":
                uttid = str(int(sheet.cell_value(rowctr, uttidcol)))
            thelevel = sheet.cell_value(rowctr, levelcol)
            thelevel = clean(thelevel)
            all_levels.add(thelevel)
            for colctr in range(firstwordcol, sheet.ncols):
                if thelevel in literallevels and colctr != stagescol and colctr != commentscol:
                    thelabel = sheet.cell_value(rowctr, colctr)
                    if colctr > lastwordcol:
                        tokenposition = 0
                    else:
                        tokenposition = colctr - firstwordcol + 1
                    #thedata[(thelevel, thelabel)].append(uttid)
                    cleanlevel = thelevel
                    cleanlabel = thelabel
                    if cleanlabel != '':
                        thedata[(cleanlevel, cleanlabel)].append((uttid, tokenposition))
                elif thelevel != uttlevel and colctr != stagescol and colctr != commentscol:
                    thelabelstr = sheet.cell_value(rowctr, colctr)
                    thelevel = sheet.cell_value(rowctr, levelcol)
                    if lastwordcol + 1 <= colctr < sheet.ncols:
                        #prefix = headers[colctr] aangepast om het simpeler te houden
                        prefix = ""
                    else:
                        prefix = ""
                    cleanlevelsandlabels = getcleanlevelsandlabels(thelabelstr, thelevel, prefix, patterns)
                    if colctr > lastwordcol:
                        tokenposition = 0
                    else:
                        tokenposition = colctr - firstwordcol + 1
                    for (cleanlevel, cleanlabel) in cleanlevelsandlabels:
                        thedata[(cleanlevel, cleanlabel)].append((uttid, tokenposition))
    #wb.close() there is no way to close the workbook
    return thedata


def update(thedict, qid, goldtuple):
    (level, item, thecounter) = goldtuple
    if qid in thedict:
        (oldlevel, olditem, oldcounter) = thedict[qid]
        thedict[qid] = (oldlevel, olditem, oldcounter + thecounter)
    else:
        thedict[qid] = goldtuple


def getitem2levelmap(mapping):
    resultmap: Dict[Any, List[Any]] = {}
    for (item, level) in mapping:
        if item in resultmap:
            resultmap[item].append(level)
        else:
            resultmap[item] = [level]
    return resultmap


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
    return(re.compile(basepattern), re.compile(fullpattern))


def get_golddata(filename, mapping, altcodes, queries, includeimplies=False):
    item2levelmap = {}
    mappingitem2levelmap = getitem2levelmap(mapping)
    altcodesitem2levelmap = getitem2levelmap(altcodes)
    allmappingitems = [item for (item, _) in mapping]
    allaltcodesitems = [item for (item, _) in altcodes]
    allitems = allmappingitems + allaltcodesitems
    patterns = mkpatterns(allitems)
    basicdata = get_annotations(filename, patterns)
    results = {}
    for thelevel, theitem in basicdata:
        thecounter = basicdata[(thelevel, theitem)]
        if (theitem, thelevel) in mapping:
            mappingitem = theitem
        elif (varitem, thelevel) in mapping:
            mappingitem = varitem
        else:
            mappingitem = theitem
        if (mappingitem, thelevel) in mapping:
            qid = mapping[(mappingitem, thelevel)]
            update(results, qid, (thelevel, theitem, thecounter))
            if includeimplies:
                for implieditem in queries[qid].implies:
                    if (implieditem, thecorrectlevel) in mapping:
                        impliedqid = mapping[(implieditem, thelevel)]
                        update(results, impliedqid, (altlevel, altitem, thecounter))
                    else:
                        SDLOGGER.error('Implied Item ({},{}) not found in mapping'.format(implieditem, thecorrectlevel))
        elif (theitem, thelevel) in altcodes:
            (altitem, altlevel) = altcodes[(theitem, thelevel)]
            qid = mapping[(altitem, altlevel)]
            update(results, qid, (altlevel, altitem, thecounter))
            SDLOGGER.info('{} of level {} invalid code replaced by {} of level {}'.format(theitem, thelevel, altitem, altlevel))
            if includeimplies:
                for implieditem in queries[qid].implies:
                    if (implieditem, thecorrectlevel) in mapping:
                        impliedqid = mapping[(implieditem, thelevel)]
                        update(results, impliedqid, (altlevel, altitem, thecounter))
                    else:
                        SDLOGGER.error('Implied Item ({},{}) not found in mapping'.format(implieditem, thecorrectlevel))
        elif theitem in mappingitem2levelmap:
            thecorrectlevels = mappingitem2levelmap[theitem]
            if len(thecorrectlevels) == 1:
                thecorrectlevel = thecorrectlevels[0]
                qid = mapping[(theitem, thecorrectlevel)]
                update(results, qid, (thecorrectlevel, theitem, thecounter))
                SDLOGGER.info('level {} of item {} replaced by correct level {}'.format(thelevel, theitem, thecorrectlevel))
            elif len(thecorrectlevels) > 1:
                SDLOGGER.error('Item {} of level {} not a valid coding (wrong level, multiple candidate levels: {}'.format(theitem, thelevel, str(thecorrectlevels)))
            else:
                SDLOGGER.error('{} of level {} not a valid coding (wrong level'.format(theitem, thelevel))
            if includeimplies:
                for implieditem in queries[qid].implies:
                    if (implieditem, thecorrectlevel) in mapping:
                        impliedqid = mapping[(implieditem, thecorrectlevel)]
                        update(results, impliedqid, (thecorrectlevel, theitem, thecounter))
                    else:
                        SDLOGGER.error('Implied Item ({},{}) not found in mapping'.format(implieditem, thecorrectlevel))
        elif theitem in altcodesitem2levelmap:
            thecorrectlevels = altcodesitem2levelmap[theitem]
            if len(thecorrectlevels) == 1:
                (thecorrectitem, thecorrectlevel) = altcodes[(theitem, thecorrectlevels[0])]
                qid = mapping[(thecorrectitem, thecorrectlevel)]
                update(results, qid, (thecorrectlevel, thecorrectitem, thecounter))
                SDLOGGER.info('level {} of item {} replaced by correct level {} and item {}'.format(thelevel, theitem, thecorrectlevel, thecorrectitem))
            elif len(thecorrectlevels) > 1:
                SDLOGGER.error('Item {} of level {} not a valid coding (item replaced by {}, wrong level, multiple candidate levels: {}'.format(theitem. thelevel, thecorrectitem, thecorrectlevels))
            else:
                SDLOGGER.error('{} of level {} not a valid coding (alternative item, wrong level)'.format(theitem, thelevel))
            if includeimplies:
                for implieditem in queries[qid].implies:
                    if (implieditem, thecorrectlevel) in mapping:
                        impliedqid = mapping[(implieditem, thecorrectlevel)]
                        update(results, impliedqid, (thecorrectlevel, theitem, thecounter))
                    else:
                        SDLOGGER.error('Implied Item ({},{}) not found in mapping'.format(implieditem, thecorrectlevel))

        else:
            SDLOGGER.error('{} of level {} not a valid coding'.format(theitem, thelevel))
    return results


def exact2global(thedata):
    '''
    turns a dictionary with  as values a list of (uttid, pos) tuples into a dictionary with the same keys and as values a counter of uttid
    :param thedata:
    :return:
    '''

    cdata = {}
    for atuple in thedata:
        newvalue = [uttid for (uttid, _) in thedata[atuple]]
        cdata[atuple] = Counter(newvalue)
    return cdata


def richexact2global(thedata):
    '''
    turns a dictionary with  as values a tuple (level, item,list of (uttid, pos) tuples) into a dictionary with the
    same keys and as values a tuple (level, item, counter of uttid)
    :param thedata:
    :return:
    '''

    cdata = {}
    for thekey in thedata:
        (thelevel, theitem, exactlist) = thedata[thekey]
        newvalue = [uttid for (uttid, _) in exactlist]
        cdata[thekey] = (thelevel, theitem, Counter(newvalue))
    return cdata


def richscores2scores(richscores):
    scores = {}
    for queryid in richscores:
        scores[queryid] = richscores[queryid][2]
    return scores


def read_annotations(methodfilename, annotationfilename, includeimplies=False):
    '''

    :param methodfilename: the name of the file containing the method (.xlsx)
    :param annotationfilename: the  filename of the file containing the annotations (.xlsx)
    :param includeimplies: a parameter to specify whether information in the implies column of the method must be taken into account (default False, keep it that way)
    :return: a dictionary with as key-value pairs with as key a queryid  and as value a Counter() with uttid as key
    '''

    (queries, item2idmap, altcodes, postquerylist) = read_method(methodfilename)
    richexactscores = get_golddata(annotationfilename, item2idmap, altcodes, queries, includeimplies)
    exactscores = richscores2scores(richexactscores)
    results = exact2global(exactscores)
    return results


if __name__ == "__main__":
    # Give the location of the input file
    #infilename = r"D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\Auris\AurisdataAligned Current.xlsx"
    #infilename = r"D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\Auris\AurisdataAligned TagsCleaned Current.xlsx"
    #infilename = r"D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\SchlichtingVoorbeeldGoldCurrent.xlsx"
    infilename = r"D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\aangeleverde data\ASTA\SASTA sample 01.xlsx"

    #Give the location of the method file
    methodfilename = r'D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\ASTA\ASTA Index Current.xlsx'

    thedata = {}
    thedata = read_annotations(methodfilename, infilename)

    (base, ext) = os.path.splitext(infilename)
    outputfilename = base + "_testgold" + tsvext + txtext
    outfile = open(outputfilename, 'w', encoding='utf8')

    for qid in thedata:
        print(qid, thedata[qid], sep=tab, file=outfile)

'''
    #header
    mysep = tab
    print('Level', 'Item', 'Count', 'Utts', sep=mysep, file=outfile)
    for atuple in thedata:
        (thelevel, theitem) = atuple
        thelist = list(thedata[atuple])
        sortedlist = sorted(thelist)
        sortedstrlist= map(str, sortedlist)
        print(thelevel, theitem, len(sortedlist), commaspace.join(sortedstrlist), sep=mysep, file=outfile)

'''

'''
This module offers the function get_annotations() to obtain a dictionary with the annotations from a file
for the moment at the utteranceid level, to be extended to the wordposition per uttid level

and the function read_annotations() to obtain a score dictionary with queryid as keys and Counter() as values
'''

# todo
# -additional columns unaligned treatment and generalisation
# -code alternatives and replacemtne extensions
# =codes written without spaces?

import re
from collections import Counter, defaultdict
from typing import Any, Dict, List, Match, Optional, Pattern, Tuple

from sastadev import xlsx
from sastadev.conf import settings
from sastadev.readmethod import itemseppattern
from sastadev.sastatypes import (FileName, Item, Level, Position, QId,
                                 QueryDict, UttId, UttWordDict)

varitem = ''

txtext = ".txt"
comma = ","
space = ' '
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
unalignedheaders = ['unaligned', 'hele zin', 'hele uiting']


def nested_dict(n: int, type: type):  # I do not know how to characterize the result type Dict n times deep endin gwith values of type type
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n - 1, type))


def clean(label: str) -> str:
    result = label
    result = result.lstrip()
    result = result.rstrip()
    result = result.lower()
    return result


def getlabels(labelstr: str, patterns: Tuple[Pattern, Pattern]) -> List[str]:
    results = []
    (pattern, fullpattern) = patterns
    if fullpattern.match(labelstr):
        ms = pattern.finditer(labelstr)
        results = [m.group(0) for m in ms if m.group(0) not in ' ;,-/']
    else:
        results = []
        ms = pattern.finditer(labelstr)
        logstr = str([m.group(0) for m in ms if m.group(0) not in ' ;,-'])
        # print('Cannot interpret {};  found items: {}'.format(labelstr,logstr), file=sys.stderr)
        settings.LOGGER.warning('Cannot interpret %s; found items: %s', labelstr, logstr)
        # exit(-1)
    return results


def iswordcolumn(str: str) -> Optional[Match[str]]:
    result = wordcolheaderre.match(str.lower())
    return result


def isfirstwordcolumn(str: str) -> Optional[Match[str]]:
    result = firstwordcolheaderre.match(str.lower())
    return result


def enrich(labelstr: str, lcprefix: str) -> str:
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


def getcleanlevelsandlabels(thelabelstr: str, thelevel: str, prefix: str, patterns: Tuple[Pattern, Pattern]) \
        -> List[Tuple[str, str]]:
    results: List[Tuple[str, str]] = []
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


# def oldget_annotations(infilename, patterns):
#     '''
#     Reads the file with name filename in SASTA Annotation Format
#     :param infilename:
#     :param patterns
#     :return: a dictionary  with as  key a tuple (level, item) and as value a Counter  with key uttid and value its count
#     '''
#
#     thedata = defaultdict(list)
#     exactdata = defaultdict(list)
#     cdata = {}
#
#     # To open Workbook
#     wb = xlrd.open_workbook(infilename)
#     sheet = wb.sheet_by_index(0)
#
#     startrow = 0
#     startcol = 0
#     headerrow = 0
#     headers = {}
#     lastrow = sheet.nrows
#     lastcol = sheet.ncols
#     #    firstwordcol = 2
#     #    lastwordcol = lastcol - 4
#     levelcol = 1
#     uttidcol = 0
#     stagescol = -1
#     commentscol = -1
#
#     uttlevel = 'utt'
#
#     for rowctr in range(startrow, lastrow):
#         if rowctr == headerrow:
#             for colctr in range(startcol, lastcol):
#                 headers[colctr] = sheet.cell_value(rowctr, colctr)
#                 if iswordcolumn(headers[colctr]):
#                     lastwordcol = colctr
#                     if isfirstwordcolumn(headers[colctr]):
#                         firstwordcol = colctr
#                 elif clean(headers[colctr]) in speakerheaders:
#                     spkcol = colctr
#                 elif clean(headers[colctr]) in uttidheaders:
#                     uttidcol = colctr
#                 elif clean(headers[colctr]) in levelheaders:
#                     levelcol = colctr
#                 elif clean(headers[colctr]) in stagesheaders:
#                     stagescol = colctr
#                 elif clean(headers[colctr]) in commentsheaders:
#                     commentscol = colctr
#         else:
#             if sheet.cell_value(rowctr, uttidcol) != "":
#                 uttid = str(int(sheet.cell_value(rowctr, uttidcol)))
#             thelevel = sheet.cell_value(rowctr, levelcol)
#             thelevel = clean(thelevel)
#             all_levels.add(thelevel)
#             for colctr in range(firstwordcol, sheet.ncols):
#                 if thelevel in literallevels and colctr != stagescol and colctr != commentscol:
#                     thelabel = sheet.cell_value(rowctr, colctr)
#                     if colctr > lastwordcol:
#                         tokenposition = 0
#                     else:
#                         tokenposition = colctr - firstwordcol + 1
#                     thedata[(thelevel, thelabel)].append(uttid)
#                     exactdata[(cleanlevel, cleanlabel)].append((uttid, tokenposition))
#                 elif thelevel != uttlevel and colctr != stagescol and colctr != commentscol:
#                     thelabelstr = sheet.cell_value(rowctr, colctr)
#                     thelevel = sheet.cell_value(rowctr, levelcol)
#                     if lastwordcol + 1 <= colctr < sheet.ncols:
#                         # prefix = headers[colctr] aangepast om het simpeler te houden
#                         prefix = ""
#                     else:
#                         prefix = ""
#                     cleanlevelsandlabels = getcleanlevelsandlabels(thelabelstr, thelevel, prefix, patterns)
#                     if colctr > lastwordcol:
#                         tokenposition = 0
#                     else:
#                         tokenposition = colctr - firstwordcol + 1
#                     for (cleanlevel, cleanlabel) in cleanlevelsandlabels:
#                         thedata[(cleanlevel, cleanlabel)].append(uttid)
#                         exactdata[(cleanlevel, cleanlabel)].append((uttid, tokenposition))
#     # wb.close() there is no way to close the workbook
#     for atuple in thedata:
#         cdata[atuple] = Counter(thedata[atuple])
#     return cdata
#
#
# def old2get_annotations(infilename: FileName, patterns: Tuple[Pattern, Pattern]) \
#         -> Tuple[UttWordDict, Dict[Tuple[Level, Item], List[Tuple[UttId, Position]]]]:
#     '''
#     Reads the file with name filename in SASTA Annotation Format
#     :param infilename:
#     :param patterns
#     :return: a dictionary  with as  key a tuple (level, item) and as value a list of (uttid, tokenposition) pairs
#     '''
#
#     thedata = defaultdict(list)
#     #cdata = {}
#
#     allutts = {}
#
#     # To open Workbook
#     wb = xlrd.open_workbook(infilename)
#     sheet = wb.sheet_by_index(0)
#
#     startrow = 0
#     startcol = 0
#     headerrow = 0
#     headers = {}
#     lastrow = sheet.nrows
#     lastcol = sheet.ncols
#     #    firstwordcol = 2
#     #    lastwordcol = lastcol - 4
#     levelcol = 1
#     uttidcol = 0
#     stagescol = -1
#     commentscol = -1
#
#     uttlevel = 'utt'
#
#     uttcount = 0
#
#     for rowctr in range(startrow, lastrow):
#         if rowctr == headerrow:
#             for colctr in range(startcol, lastcol):
#                 headers[colctr] = sheet.cell_value(rowctr, colctr)
#                 if iswordcolumn(headers[colctr]):
#                     lastwordcol = colctr
#                     if isfirstwordcolumn(headers[colctr]):
#                         firstwordcol = colctr
#                 elif clean(headers[colctr]) in speakerheaders:
#                     spkcol = colctr
#                 elif clean(headers[colctr]) in uttidheaders:
#                     uttidcol = colctr
#                 elif clean(headers[colctr]) in levelheaders:
#                     levelcol = colctr
#                 elif clean(headers[colctr]) in stagesheaders:
#                     stagescol = colctr
#                 elif clean(headers[colctr]) in commentsheaders:
#                     commentscol = colctr
#         else:
#             if sheet.cell_value(rowctr, uttidcol) != "":
#                 uttid = str(int(sheet.cell_value(rowctr, uttidcol)))
#             thelevel = sheet.cell_value(rowctr, levelcol)
#             thelevel = clean(thelevel)
#             all_levels.add(thelevel)
#             # if thelevel == uttlevel:
#             #    uttcount += 1
#             curuttwlist = []
#             for colctr in range(firstwordcol, sheet.ncols):
#                 if thelevel == uttlevel:
#                     curcellval = sheet.cell_value(rowctr, colctr)
#                     if curcellval != '':
#                         curuttwlist.append(curcellval)
#                 elif thelevel in literallevels and colctr != stagescol and colctr != commentscol:
#                     thelabel = sheet.cell_value(rowctr, colctr)
#                     if colctr > lastwordcol:
#                         tokenposition = 0
#                     else:
#                         tokenposition = colctr - firstwordcol + 1
#                     # thedata[(thelevel, thelabel)].append(uttid)
#                     cleanlevel = thelevel
#                     cleanlabel = thelabel
#                     if cleanlabel != '':
#                         thedata[(cleanlevel, cleanlabel)].append((uttid, tokenposition))
#                 elif thelevel != uttlevel and colctr != stagescol and colctr != commentscol:
#                     thelabelstr = sheet.cell_value(rowctr, colctr)
#                     thelevel = sheet.cell_value(rowctr, levelcol)
#                     if lastwordcol + 1 <= colctr < sheet.ncols:
#                         # prefix = headers[colctr] aangepast om het simpeler te houden
#                         prefix = ""
#                     else:
#                         prefix = ""
#                     cleanlevelsandlabels = getcleanlevelsandlabels(thelabelstr, thelevel, prefix, patterns)
#                     if colctr > lastwordcol:
#                         tokenposition = 0
#                     else:
#                         tokenposition = colctr - firstwordcol + 1
#                     for (cleanlevel, cleanlabel) in cleanlevelsandlabels:
#                         thedata[(cleanlevel, cleanlabel)].append((uttid, tokenposition))
#             if curuttwlist != []:
#                 allutts[uttid] = curuttwlist
#     # wb.close() there is no way to close the workbook
#     return allutts, thedata


def get_annotations(infilename: FileName, patterns: Tuple[Pattern, Pattern]) \
        -> Tuple[UttWordDict, Dict[Tuple[Level, Item], List[Tuple[UttId, Position]]]]:
    '''
    Reads the file with name filename in SASTA Annotation Format
    :param infilename:
    :param patterns
    :return: a dictionary  with as  key a tuple (level, item) and as value a list of (uttid, tokenposition) pairs
    '''

    thedata = defaultdict(list)

    allutts = {}

    # To open Workbook
    header, data = xlsx.getxlsxdata(infilename)

    levelcol = 1
    uttidcol = 0
    stagescol = -1
    commentscol = -1
    unalignedcol = -1

    uttlevel = 'utt'

    uttcount = 0

    for col, val in enumerate(header):
        if iswordcolumn(val):
            lastwordcol = col
            if isfirstwordcolumn(val):
                firstwordcol = col
        elif clean(val) in speakerheaders:
            spkcol = col
        elif clean(val) in uttidheaders:
            uttidcol = col
        elif clean(val) in levelheaders:
            levelcol = col
        elif clean(val) in stagesheaders:
            stagescol = col
        elif clean(val) in commentsheaders:
            commentscol = col
        elif clean(val) in unalignedheaders:
            unalignedcol = col
        else:
            pass  # maybe warn here that an unknow column header has been encountered?

    for row in data:
        if row[uttidcol] != "":
            uttid = str(int(row[uttidcol]))
        thelevel = row[levelcol]
        thelevel = clean(thelevel)
        all_levels.add(thelevel)
        # if thelevel == uttlevel:
        #    uttcount += 1
        curuttwlist = []
        for colctr in range(firstwordcol, len(row)):
            if thelevel == uttlevel:
                curcellval = row[colctr]
                if curcellval != '':
                    curuttwlist.append(curcellval)
            elif thelevel in literallevels and colctr != stagescol and colctr != commentscol:
                thelabel = row[colctr]
                if colctr > lastwordcol:
                    tokenposition = 0
                else:
                    tokenposition = colctr - firstwordcol + 1
                cleanlevel = thelevel
                cleanlabel = thelabel
                if cleanlabel != '':
                    thedata[(cleanlevel, cleanlabel)].append((uttid, tokenposition))
            elif thelevel != uttlevel and colctr != stagescol and colctr != commentscol:
                thelabelstr = row[colctr]
                thelevel = row[levelcol]
                if colctr == unalignedcol:
                    prefix = ''
                if lastwordcol + 1 <= colctr < len(row):
                    # prefix = headers[colctr] aangepast om het simpeler te houden
                    prefix = ""
                else:
                    prefix = ""
                cleanlevelsandlabels = getcleanlevelsandlabels(thelabelstr, thelevel, prefix, patterns)
                if colctr > lastwordcol or colctr == unalignedcol:
                    tokenposition = 0
                else:
                    tokenposition = colctr - firstwordcol + 1
                for (cleanlevel, cleanlabel) in cleanlevelsandlabels:
                    thedata[(cleanlevel, cleanlabel)].append((uttid, tokenposition))
        if curuttwlist != []:
            allutts[uttid] = curuttwlist
    return allutts, thedata


def update(thedict: Dict[QId, Tuple[Level, Item, List[Tuple[UttId, Position]]]], qid: QId,
           goldtuple: Tuple[Level, Item, List[Tuple[UttId, Position]]]):
    (level, item, thecounter) = goldtuple
    if qid in thedict:
        (oldlevel, olditem, oldcounter) = thedict[qid]
        thedict[qid] = (oldlevel, olditem, oldcounter + thecounter)
    else:
        thedict[qid] = goldtuple


def oldgetitem2levelmap(mapping: Dict[Tuple[Item, Level], Any]) -> Dict[Item, List[Level]]:
    resultmap: Dict[Item, List[Level]] = {}
    for (item, level) in mapping:
        if item in resultmap:
            resultmap[item].append(level)
        else:
            resultmap[item] = [level]
    return resultmap


def getitem2levelmap(mapping: Dict[Tuple[Item, Level], Any]) -> Dict[Item, Level]:
    resultmap: Dict[Item, Level] = {}
    for (item, level) in mapping:
        if item in resultmap:
            settings.LOGGER.error('Duplicate level {} for item {} with level {} ignored'.format(level, item, resultmap[item]))
        else:
            resultmap[item] = level
    return resultmap


def codeadapt(c: str) -> str:
    result = c
    result = re.sub(r'\.', r'\\.', result)
    result = re.sub(r'\(', r'\\(', result)
    result = re.sub(r'\)', r'\\)', result)
    result = re.sub(r'\?', r'\\?', result)
    result = re.sub(r'\*', r'\\*', result)
    result = re.sub(r'\+', r'\\+', result)
    result = re.sub(r' ', r'\\s+', result)
    return result


def mkpatterns(allcodes: List[str]) -> Tuple[Pattern, Pattern]:
    basepattern = r''
    sortedallcodes = sorted(allcodes, key=len, reverse=True)
    adaptedcodes = [codeadapt(c) for c in sortedallcodes]
    basepattern = r'' + '|'.join(adaptedcodes) + '|' + itemseppattern
    fullpattern = r'^(' + basepattern + r')*$'
    return (re.compile(basepattern), re.compile(fullpattern))


def get_golddata(filename: FileName, mapping: Dict[Tuple[Item, Level], QId], altcodes: Dict[Tuple[Item, Level], Tuple[Item, Level]],
                 queries: QueryDict, includeimplies: bool = False) \
        -> Tuple[UttWordDict, Dict[QId, Tuple[Level, Item, List[Tuple[UttId, Position]]]]]:
    # item2levelmap = {}
    mappingitem2levelmap = getitem2levelmap(mapping)
    altcodesitem2levelmap = getitem2levelmap(altcodes)
    allmappingitems = [item for (item, _) in mapping]
    allaltcodesitems = [item for (item, _) in altcodes]
    allitems = allmappingitems + allaltcodesitems
    patterns = mkpatterns(allitems)
    allutts, basicdata = get_annotations(filename, patterns)
    results: Dict[QId, Tuple[Level, Item, List[Tuple[UttId, Position]]]] = {}
    for thelevel, theitem in basicdata:
        thecounter = basicdata[(thelevel, theitem)]
        # unclear why this below here is needed
#        if (theitem, thelevel) in mapping:
#            mappingitem = theitem
#        elif (varitem, thelevel) in mapping:
#            mappingitem = varitem
#        else:
#            mappingitem = theitem
        if thelevel in literallevels:
            # we still have to determine how to deal with this
            pass
        elif (theitem, thelevel) in mapping:
            qid = mapping[(theitem, thelevel)]
            update(results, qid, (thelevel, theitem, thecounter))
            if includeimplies:
                for implieditem in queries[qid].implies:
                    impliedlevel = mappingitem2levelmap[implieditem]
                    if (implieditem, impliedlevel) in mapping:
                        impliedqid = mapping[(implieditem, impliedlevel)]
                        update(results, impliedqid, (impliedlevel, implieditem, thecounter))
                    else:
                        settings.LOGGER.error('Implied Item ({},{}) not found in mapping'.format(implieditem, impliedlevel))
        elif (theitem, thelevel) in altcodes:
            (altitem, altlevel) = altcodes[(theitem, thelevel)]
            qid = mapping[(altitem, altlevel)]
            update(results, qid, (altlevel, altitem, thecounter))
            settings.LOGGER.info(
                '{} of level {} invalid code replaced by {} of level {}'.format(theitem, thelevel, altitem, altlevel))
            if includeimplies:
                for implieditem in queries[qid].implies:
                    impliedlevel = mappingitem2levelmap[implieditem]
                    if (implieditem, impliedlevel) in mapping:
                        impliedqid = mapping[(implieditem, impliedlevel)]
                        update(results, impliedqid, (impliedlevel, implieditem, thecounter))
                    else:
                        settings.LOGGER.error('Implied Item ({},{}) not found in mapping'.format(implieditem, impliedlevel))
        elif theitem in mappingitem2levelmap:   # valid item but wrong level
            thecorrectlevel = mappingitem2levelmap[theitem]
            qid = mapping[(theitem, thecorrectlevel)]
            update(results, qid, (thecorrectlevel, theitem, thecounter))
            settings.LOGGER.info(
                'level {} of item {} replaced by correct level {}'.format(thelevel, theitem, thecorrectlevel))
            if includeimplies:
                for implieditem in queries[qid].implies:
                    impliedlevel = mappingitem2levelmap[implieditem]
                    if (implieditem, impliedlevel) in mapping:
                        impliedqid = mapping[(implieditem, impliedlevel)]
                        update(results, impliedqid, (impliedlevel, implieditem, thecounter))
                    else:
                        settings.LOGGER.error('Implied Item ({},{}) not found in mapping'.format(implieditem, impliedlevel))
        elif theitem in altcodesitem2levelmap:  # valid alternative item but wrong level
            theitemlevel = altcodesitem2levelmap[theitem]
            (thecorrectitem, thecorrectlevel) = altcodes[(theitem, theitemlevel)]
            qid = mapping[(thecorrectitem, thecorrectlevel)]
            update(results, qid, (thecorrectlevel, thecorrectitem, thecounter))
            settings.LOGGER.info(
                'level {} of item {} replaced by correct level {} and item {}'.format(
                    thelevel, theitem, thecorrectlevel, thecorrectitem)
            )
            if includeimplies:
                for implieditem in queries[qid].implies:
                    impliedlevel = mappingitem2levelmap[implieditem]
                    if (implieditem, impliedlevel) in mapping:
                        impliedqid = mapping[(implieditem, impliedlevel)]
                        update(results, impliedqid, (impliedlevel, implieditem, thecounter))
                    else:
                        settings.LOGGER.error('Implied Item ({},{}) not found in mapping'.format(implieditem, thecorrectlevel))

        else:
            settings.LOGGER.error('{} of level {} not a valid coding'.format(theitem, thelevel))
    return allutts, results


def exact2global(thedata: Dict[Tuple[Level, Item], List[Tuple[UttId, Position]]]) -> Dict[Tuple[Level, Item], Counter]:
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


def richscores2scores(richscores: Dict[QId, Tuple[Level, Item, Any]]) -> Dict[QId, Any]:
    scores = {}
    for queryid in richscores:
        scores[queryid] = richscores[queryid][2]
    return scores

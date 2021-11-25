import xlrd

from config import SDLOGGER
from query import Query, form_process, post_process

comma = ','

altitemsep = comma
implies_sep = comma
itemseppattern = r'[,-; ]'


def getboolean(str):
    if str is None:
        result = False
    elif str == '':
        result = False
    else:
        cleanstr = str.strip().lower()
        if cleanstr in ['no', 'false'] or cleanstr[0] in ['n', 'f']:
            result = False
        else:
            result = True
    return result


def getint(fase):
    try:
        result = int(fase)
    except:
        result = 0
    return result


def get_pages(val):
    #pages = val.split(pagesep)
    #result = pages
    result = val
    return result


def getaltitems(str):
    result = getlistofitems(str, altitemsep)
    return result


def getimplies(str):
    result = getlistofitems(str, implies_sep)
    return result


def getlistofitems(str, sep):
    rawresult = str.split(sep)
    cleanresult = [w.strip().lower() for w in rawresult]
    if cleanresult == ['']:
        cleanresult = []
    return cleanresult


def read_method(methodfilename):
    # To open Workbook
    wb = xlrd.open_workbook(methodfilename)
    sheet = wb.sheet_by_index(0)

    idcol, catcol, subcatcol, levelcol, itemcol, altcol, impliescol, \
        originalcol, pagescol, fasecol, querycol, informcol, screeningcol, processcol, special1col, special2col, commentscol = \
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16

    headerrow = 0

    queries = {}
    item2idmap = {}
    altcodes = {}

    postquerylist = []
    for rowctr in range(sheet.nrows):
        if rowctr != headerrow:
            id = sheet.cell_value(rowctr, idcol).strip()
            cat = sheet.cell_value(rowctr, catcol).strip()
            subcat = sheet.cell_value(rowctr, subcatcol).strip()
            level = sheet.cell_value(rowctr, levelcol).strip()
            item = sheet.cell_value(rowctr, itemcol).strip()
            altitems = getaltitems(sheet.cell_value(rowctr, altcol))
            implies = getimplies(sheet.cell_value(rowctr, impliescol))
            original = getboolean(sheet.cell_value(rowctr, originalcol))
            pages = get_pages(sheet.cell_value(rowctr, pagescol))
            fase = getint(sheet.cell_value(rowctr, fasecol))
            query = sheet.cell_value(rowctr, querycol)
            inform = sheet.cell_value(rowctr, informcol)
            screening = sheet.cell_value(rowctr, screeningcol)
            process = sheet.cell_value(rowctr, processcol).strip()
            special1 = sheet.cell_value(rowctr, special1col).strip()
            special2 = sheet.cell_value(rowctr, special2col).strip()
            comments = sheet.cell_value(rowctr, commentscol)

            queries[id] = Query(id, cat, subcat, level, item, altitems, implies, original, pages, fase, query, inform, screening, process,
                                special1, special2, comments)
            if queries[id].process in [post_process, form_process]:
                postquerylist.append(id)
            lcitem = item.lower()
            lclevel = level.lower()
            if (lcitem, lclevel) in item2idmap:
                SDLOGGER.error('Duplicate (item, level) pair for {} and {}'.format(item2idmap[(lcitem, lclevel)], id))
            item2idmap[(lcitem, lclevel)] = id
            for altitem in altitems:
                lcaltitem = altitem.lower()
                if (lcaltitem, lclevel) in altcodes:
                    SDLOGGER.error('Duplicate (alternative item, level) pair for {} and {}'.format(altcodes[(lcaltitem, lclevel)], id))
                altcodes[(lcaltitem, lclevel)] = (lcitem, lclevel)

        rowctr += 1
    return(queries, item2idmap, altcodes, postquerylist)

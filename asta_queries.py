from config import SDLOGGER
from dedup import getposition, showtns
from macros import expandmacros
from metadata import (longrep, repeated, repeatedseqtoken, repetition,
                      substringrep)
from stringfunctions import string2list
from treebankfunctions import (asta_recognised_lexnode,
                               asta_recognised_nounnode, clausecats, find1,
                               getattval, getnodeyield, getyield)

noun_xpath = './/node[%asta_noun%]'
expanded_noun_xpath = expandmacros(noun_xpath)

lex_path = './/node[%ASTA_LEX%]'
expanded_lex_xpath = expandmacros(lex_path)

astabijzinquerybase = './/node[%ASTA_Bijzin%]'
astabijzinquery = expandmacros(astabijzinquerybase)

astacoredelpvquery = './/node[%coredelpv%]'
expandedastacoredelpvquery = expandmacros(astacoredelpvquery)

dpancestorsquery = 'ancestor::node[@rel="dp"] | self::node[@rel="dp" or @rel="--"]'


def get_dupindex(stree, cond):
    dupindex = {}
    dupxpath = './/xmeta[{cond}]'.format(cond=cond)
    dupmetadatalist = stree.xpath(dupxpath)
    for meta in dupmetadatalist:
        if 'annotatedposlist' in meta.attrib and 'annotationposlist' in meta.attrib:
            keyliststr = meta.attrib['annotatedposlist']
            keylist = string2list(keyliststr)
            valueliststr = meta.attrib['annotationposlist']
            valuelist = string2list(valueliststr)
            if len(keylist) != len(valuelist):
                SDLOGGER.error('Error in metadata: {} in sentence {}'.format(meta, getyield(stree)))
            else:
                for key, val in zip(keylist, valuelist):
                    dupindex[key] = val
    return dupindex


def asta_noun(stree):
    results = asta_x(stree, expanded_noun_xpath, asta_recognised_nounnode)
    return results


def asta_lex(stree):
    results = asta_x(stree, expanded_lex_xpath, asta_recognised_lexnode)
    return results


def old_asta_noun(stree):
    theyield = getyield(stree)   # for debugging purposes
    thenodeyield = getnodeyield(stree)
    cond1 = '@value="{}" or @value="{}" or @value="{}" or @value="{}"'.format(repeated, repeatedseqtoken, longrep, substringrep)
    dupindex = get_dupindex(stree, cond1)
    cond2 = '@subcat="{}"'.format(repetition)
    allrepdupindex = get_dupindex(stree, cond2)
    revallrepdupindex = {val: key for key, val in allrepdupindex.items()}
    noun_nodes = stree.xpath(expanded_noun_xpath)
    # print(showtns(noun_nodes))

    clean_noun_nodes = noun_nodes

    # remove the nodes that should get it from this function
    clean_noun_nodes = [node for node in clean_noun_nodes if getattval(node, 'begin') not in allrepdupindex]

    # remove words not recognised as nouns; is dit nodig? Ja dit is nodig!!!
    clean_noun_nodes = [node for node in clean_noun_nodes if asta_recognised_nounnode(node)]
    # print(showtns(clean_noun_nodes))

    additional_nodes = []
    for key in dupindex:
        keynode = find1(stree, './/node[(@pt or @pos) and @begin="{}"]'.format(key))
        if keynode is not None:
            val = dupindex[key]
            valnode = find1(stree, './/node[(@pt or @pos) and @begin="{}"]'.format(val))
            if valnode is not None:
                if valnode in clean_noun_nodes:
                    additional_nodes.append(keynode)

    result = clean_noun_nodes + additional_nodes
    # print(showtns(result))
    return result


def verbleftof(node, positions):
    nodebegin = getattval(node, 'begin')
    for position in positions:
        if int(position) < int(nodebegin):
            return True
    return False


def asta_delpv(stree):
    coredelpvnodes = stree.xpath(expandedastacoredelpvquery)
    streeleaves = getnodeyield(stree)
    wwbegins = [getattval(node, 'begin') for node in streeleaves if getattval(node, 'pt') == 'ww']
    delpvnodes = [node for node in coredelpvnodes if node.xpath(dpancestorsquery) == [] or not (verbleftof(node, wwbegins))]
    return delpvnodes


def asta_x(stree, xpathexpr, recognized_x_f):
    theyield = getyield(stree)   # for debugging purposes
    thenodeyield = getnodeyield(stree)
    cond1 = '@value="{}" or @value="{}" or @value="{}" or @value="{}"'.format(repeated, repeatedseqtoken, longrep, substringrep)
    dupindex = get_dupindex(stree, cond1)
    cond2 = '@subcat="{}"'.format(repetition)
    allrepdupindex = get_dupindex(stree, cond2)
    revallrepdupindex = {val: key for key, val in allrepdupindex.items()}
    x_nodes = stree.xpath(xpathexpr)
    # print(showtns(noun_nodes))

    clean_x_nodes = x_nodes

    # remove the nodes that should get it from this function
    clean_x_nodes = [node for node in clean_x_nodes if getattval(node, 'begin') not in allrepdupindex]

    # remove words not recognised as nouns; is dit nodig? Ja dit is nodig!!!
    clean_x_nodes = [node for node in clean_x_nodes if recognized_x_f(node)]
    # print(showtns(clean_noun_nodes))

    additional_nodes = []
    for key in dupindex:
        keynode = find1(stree, './/node[(@pt or @pos) and @begin="{}"]'.format(key))
        if keynode is not None:
            val = dupindex[key]
            valnode = find1(stree, './/node[(@pt or @pos) and @begin="{}"]'.format(val))
            if valnode is not None:
                if valnode in clean_x_nodes:
                    additional_nodes.append(keynode)

    result = clean_x_nodes + additional_nodes
    # print(showtns(result))
    return result


def getmluxnodes(mluxnodes, posnodes, dupinfo):
    resultnodes = []
    for node in mluxnodes:
        nodeposition = getposition(node)
        origpos = get_origpos(nodeposition, dupinfo)
        targetnode = find_node(origpos, posnodes)
        if targetnode is not None:
            resultnodes.append(node)
    return resultnodes


def get_origpos(nodeposition, dupinfo):
    newposition = nodeposition
    if newposition not in dupinfo.longdups:
        result = None
    else:
        while newposition in dupinfo.longdups:
            newposition = dupinfo.longdups[newposition]
        result = newposition
    return result


def find_node(position, nodes):
    results = [node for node in nodes if getposition(node) == position]
    lresults = len(results)
    if lresults == 0:
        result = None
    elif lresults == 1:
        result = results[0]
    else:
        SDLOGGER.warning('Multiple nodes found for position {}: {}, in {}'.format(position, showtns(results), showtns(nodes)))
        result = results[0]
    return result


bijzin_xpath = './/node[%ASTA_Bijzin%]'
expanded_bijzin_xpath = expandmacros(bijzin_xpath)


def old_asta_bijzin(stree):
    candnodes = stree.xpath(expanded_bijzin_xpath)
    tops = stree.xpath('.//node[@cat="top"]')
    top = tops[0]
    done, resultingnodes = removehoofdzin(top, candnodes)
    return resultingnodes


def removerepetitions(ptnodes, stree):
    newptnodes = []
    for ptnode in ptnodes:
        ptnodeend = ptnode.attrib['begin'] if 'begin' in ptnode.attrib else None
        xmetaxpath = './/xmeta[@subcat="Repetition" and @annotatedposlist="[{}]"]'.format(ptnodeend)
        repmetas = stree.xpath(xmetaxpath)
        if repmetas == []:
            newptnodes.append(ptnode)
    return newptnodes


def asta_bijzin(stree):
    theyield = getyield(stree)
    clausenodes = stree.xpath(astabijzinquery)
    ptnodes = [n for n in clausenodes if 'pt' in n.attrib]
    okptnodes = removerepetitions(ptnodes, stree)
    trueclausenodes = [n for n in clausenodes if getattval(n, 'cat') in clausecats]
    # alternative 1
    # sortedclausenodes = sorted(trueclausenodes, key=lambda x: (int(getattval(x,'begin')), -int(getattval(x, 'end'))))
    # result = sortedclausenodes[1:] + okptnodes

    # alternative2 -follows the conventions for ASTA
    sortedclausenodes = sorted(trueclausenodes, key=lambda x: (int(getattval(x, 'begin')), int(getattval(x, 'end'))))
    if len(sortedclausenodes) > 1:
        cn0 = sortedclausenodes[0]
        cn1 = sortedclausenodes[1]
        if getattval(cn1, 'begin') == getattval(cn0, 'begin'):
            cn0end = getattval(cn0, 'end')
            newbegin = cn0end
            newokptnode = find1(cn1, '//node[@pt and @begin={newbegin}]'.format(newbegin=newbegin))
            result = sortedclausenodes[2:] + okptnodes + [newokptnode]
        else:
            result = sortedclausenodes[1:] + okptnodes
    else:
        result = sortedclausenodes[1:] + okptnodes

    return result


def removehoofdzin(stree, clausenodes):
    resultingnodes = clausenodes
    done = False
    for child in stree:
        chatt = getattval(child, 'cat')
        if chatt in clausecats:
            if child in clausenodes:
                resultingnodes.remove(child)
                done = True
                return done, resultingnodes
            else:
                done = True
        if not done:
            done, resultingnodes = removehoofdzin(child, clausenodes)
    return done, resultingnodes

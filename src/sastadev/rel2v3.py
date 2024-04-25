import copy
from lxml import etree
from typing import Optional
from sastadev.treebankfunctions import find1, getattval as gav, getnodeyield, immediately_precedes
from sastadev.sastatypes import SynTree
from sastadev.conf import settings
import os
npwithrelquery = """.//node[@cat="np" and node[@cat="rel" and node[@rel="rhd" and (@lemma="die" or @lemma="dat" )]]] """
firstwordquerytemplate = """.//node[@pt and @begin={begin}] """
relpronodequery = """//node[@cat="np"]/node[@cat="rel"]/node[@rel="rhd" and (@lemma="die" or @lemma="dat" )]"""



def nprel2v3(stree: SynTree) -> Optional[SynTree]:
    newstree = copy.deepcopy(stree)
    npwithrels = newstree.xpath(npwithrelquery)
    trueinstances = []
    for npwithrel in npwithrels:
        npwithrelbegin = gav(npwithrel, 'begin')
        npwithrelfirstword = find1(npwithrel, firstwordquerytemplate.format(begin=npwithrelbegin))
        npwithrelfirstwordbegin = int(gav(npwithrelfirstword, 'begin'))
        theyield = getnodeyield(npwithrel)
        npwithrelisfirst = True
        for node in theyield:
            node_end = int(gav(node, 'end'))
            nodept = gav(node, 'pt')
            if node_end <= npwithrelfirstwordbegin and nodept not in ['tsw', 'let']:
                npwithrelisfirst = False
                break
        # check whether the relative clause is not extraposed
        relpronode = find1(node, relpronodequery)
        theyield = getnodeyield(node)
        relproindex = theyield.index(relpronode)
        precedingwordnode = theyield[relproindex -1] if relproindex > 0 else None
        if precedingwordnode is not None and immediately_precedes(precedingwordnode, relpronode, newstree):
            extraposed = False
        else:
            extraposed = True
        if npwithrelisfirst and not extraposed:
            trueinstances.append(npwithrel)
    if len(trueinstances) == 0:
        return None
    else:
        if len(trueinstances) >= 1:
            settings.LOGGER.warning("rel2v3:Multiple sentence initial NPs with relative clause found ")
        thenpwithrel = trueinstances[0]
        # transform the tree
        # np[ mu1 mod/rel ] -> dp/np[mu1] dp/rel
        npparent = thenpwithrel.getparent()
        npid = gav(thenpwithrel, 'id')
        duid = f'{npid}a'
        relnode = find1(thenpwithrel, './node[@cat="rel"]')
        if relnode is not None:
            dunode = etree.Element('node', {'cat': 'du', 'rel':'--', 'id':duid})
            relnode.set('rel', 'dp')
            thenpwithrel.set('rel', 'dp')
            dunode.extend([thenpwithrel, relnode])
            npparent.prepend(dunode)
    return newstree

ooknog = """(@lemma="ook" or @lemma="nog")"""
nognpquery = f""".//node[(@cat="np" or @cat="pp") and node[{ooknog}]] """
nogquery = f"""./node[{ooknog}]"""
def nogoutnp(stree: SynTree) -> Optional[SynTree]:
    """
    moves adverbs ook and nog out of the np or pp; if under top node it creates a du node
    :param stree:
    :return:
    """
    newstree = copy.deepcopy(stree)
    nognps = newstree.xpath(nognpquery)
    if nognps == []:
        return None
    for nognp in nognps:
        nognodes = nognp.xpath(nogquery)
        nognpparent = nognp.getparent()
        nognpparentcat = gav(nognpparent, 'cat')
        # etree.dump(nognpparent)
        for nognode in nognodes:
            nognp.remove(nognode)
            # etree.dump(nognp)
            if nognpparentcat == 'top':
                dunode = etree.Element('node', {'cat': 'du'})
                nognode.set('rel', 'dp')
                dunode.append(nognode)
                nognp.set('rel', 'dp')
                dunode.append(nognp)
                nognpparent.append(dunode)
            else:
                nognpparent.append(nognode)
            # etree.dump(nognpparent)
    return newstree


def tryme(fn):
    fulltreebank = etree.parse(fn)
    treebank = fulltreebank.getroot()
    for stree in treebank:
        # newstree = nprel2v3(stree)
        newstree = nogoutnp(stree)
        etree.dump(newstree)


if __name__ == '__main__':
    infilename = 'test_tarsp.xml'
    infullname = os.path.join(settings.SD_DIR, 'data', 'development', infilename)
    tryme(infullname)
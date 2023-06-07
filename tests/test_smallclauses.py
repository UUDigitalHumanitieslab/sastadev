import os

from dataconfig import dataroot, intreebanksfolder
from smallclauses import bg, getleavestr, smallclauses, word

from sastadev.config import SDLOGGER
from sastadev.dedup import filledpauseslexicon
from sastadev.lexicon import known_word
from sastadev.metadata import (SASTA, Meta, bpl_delete, bpl_none,
                               defaultpenalty, insertion,
                               insertiontokenmapping, smallclause,
                               tokenmapping)
from sastadev.namepartlexicon import namepart_isa_namepart
from sastadev.sastatoken import Token, show
from sastadev.tokenmd import TokenListMD
from sastadev.top3000 import (genlexicon, intransitive, isanimate, ishuman,
                              pseudotr, transitive)
from sastadev.treebankfunctions import getattval, getnodeyield, getstree


def getfn(dataset, filename):
    result = os.path.join(dataroot, dataset, intreebanksfolder, filename)
    return result

testbank = getfn( 'sctest',  "smallclausetest.xml")
#schlichtingtreebank = r'D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\schlichtingtreebank\TREEBANK_ID.xml'
schlichtingtreebank = getfn('schlichting', 'TARVB2_ID2.xml')
mieke06 = getfn('miekeplat', "TARSP_MIEKE06_ID.xml")
mieke08 = getfn('miekeplat', "TARSP_MIEKE08_ID.xml")
aurisraw = getfn('Eliska', 'AURIS_ELISKA_ORIGINAL_ID.xml')
tarsp02 = os.path.join(dataroot, 'VKLTarsp', intreebanksfolder, 'Tarsp_02.xml')
tarsp06 = os.path.join(dataroot, 'VKLTarsp', intreebanksfolder, 'Tarsp_06.xml')
schlichtingall = os.path.join(dataroot, 'Schlichtingall', intreebanksfolder, 'TREEBANK_SCHLICHTING_CHAT_ID.xml')





def main():
    smalltest = False
    if smalltest:
        fullnames = [testbank]
    else:
        fullnames = [ schlichtingtreebank,  mieke06, mieke08, aurisraw, tarsp02, tarsp06, schlichtingall]
    for infullname in fullnames:
        print(f'\n{infullname}\n')
        fulltreebank = getstree(infullname)
        if fulltreebank is not None:
            treebank = fulltreebank.getroot()
            for tree in treebank:
                leaves = getnodeyield(tree)
                tokens = [Token(word(leave), bg(leave)) for leave in leaves]
                tokensmd = TokenListMD(tokens, [])
                resultlist = smallclauses(tokensmd, tree)
                if resultlist != []:
                    print('input:  ', getleavestr(leaves) )
                    print('output: ', show(resultlist[0].tokens))
                    print('result: ', resultlist[0].metadata)


if __name__ == '__main__':
    main()

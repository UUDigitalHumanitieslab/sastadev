from config import SDLOGGER
import os
from treebankfunctions import getstree, getnodeyield, getattval
from dedup import filledpauseslexicon
from top3000 import ishuman, transitive, intransitive, pseudotr, isanimate, genlexicon
from lexicon import known_word
from namepartlexicon import namepart_isa_namepart
from sastatoken import Token, show
from tokenmd import TokenListMD
from metadata import Meta, bpl_delete, defaultpenalty, insertion, smallclause, SASTA, bpl_none, tokenmapping,\
    insertiontokenmapping
from smallclauses import smallclauses, word, getleavestr, bg
from  dataconfig import dataroot, intreebanksfolder


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

from config import SDLOGGER
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


testbank = r"D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\TARSP\smallclausetest.xml"
schlichtingtreebank = r'D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\schlichtingtreebank\TREEBANK_ID.xml'
mieke06 = r"D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\miekeplat_tests\TARSP_MIEKE06_ID.xml"
mieke08 = r"D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\miekeplat_tests\TARSP_MIEKE08_ID.xml"
aurisraw = r"D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\Auris\AURIS_ELISKA_ORIGINAL_ID.xml"
tarsp02 = r"D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\tarspdata\Tarsp_02.xml"
tarsp06 = r"D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\tarspdata\Tarsp_06.xml"
#schlichtingall = r"D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\treebank_schlichting_all_examples\TREEBANK_SCHLICHTING_CHAT_ID.xml"





def main():
    smalltest = True
    if smalltest:
        fullnames = [testbank]
    else:
        fullnames = [ schlichtingtreebank,  mieke06, mieke08, aurisraw, tarsp02, tarsp06]
    for infullname in fullnames:
        print(infullname)
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

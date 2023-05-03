import sasta_explanation
import treebankfunctions as tbf
from auchann.align_words import align_words

space = ' '

#print(dir(sasta_explanation))
def test():
    # treetotest = 9
    infullname = r"D:\Dropbox\jodijk\Utrecht\Projects\SASTADATA\Auris\outtreebanks\DLD07_corrected.xml"
    fulltreebank = tbf.getstree(infullname)
    treebank = fulltreebank.getroot()
    treecount = 0
    for tree in treebank:
        treecount += 1
        # if treecount != treetotest:
        #     continue
        origutt = tbf.find1(tree, './/meta[@name="origutt"]/@value')
        # print(origutt)
        cleanuttelem = tbf.find1(tree, './/sentence')
        cleanutt = cleanuttelem.text
        explanationlist, postexplanationlist = sasta_explanation.finalmultiwordexplanation(tree)
        explanationstr = space.join(explanationlist + postexplanationlist) if explanationlist is not None else None
        # print(f'explanationstr={explanationstr}')
        if explanationstr is not None:
            alignment = align_words(cleanutt, explanationstr)
        else:
            alignment = None
        if explanationstr is not None:
            print(f' Orig:{origutt}\nClean:{cleanutt}\n Expl:{explanationstr}\nAlign:{alignment}\n\n')


if __name__ == '__main__':
    test()
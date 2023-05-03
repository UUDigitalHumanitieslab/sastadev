
import copy
from sastatypes import List, SynTree
#import CHAT_Annotation as schat  # put off because it causes an error: AttributeError: module 'CHAT_Annotation' has no attribute 'wordpat'

import treebankfunctions as tbf
#import find1, iswordnode, getattval
import stringfunctions as strf
from typing import Optional
from sastatoken import Token
from sastatok import gettokensplusxmeta
from tokenmd import TokenListMD
from auchann.align_words import align_words
from lexicon import known_word
from metadata import bpl_node, bpl_word, mkSASTAMeta


space = ' '
CHAT_explanation = 'Explanation'
explannwordlistxpath = f'.//xmeta[@name="{CHAT_explanation}"]/@annotationwordlist'
explannposlistxpath = f'.//xmeta[@name="{CHAT_explanation}"]/@annotationposlist'

def tokenreplace(oldtokens: List[Token], newtoken: Token) -> List[Token]:
    newtokens = []
    for token in oldtokens:
        if token.pos == newtoken.pos:
            newtokens.append(newtoken)
        else:
            newtokens.append(token)
    return newtokens


def explanationasreplacement(tokensmd: TokenListMD, tree: SynTree) -> Optional[TokenListMD]:
    # interpret single word explanation as replacement # this will work only after retokenistion of the origutt
    result = None
    origmetadata = tokensmd.metadata
    xtokens, xmetalist = gettokensplusxmeta(tree)
    explanations = [xm for xm in xmetalist if xm.name == 'Explanation']
    newtokens = copy.deepcopy(xtokens)
    newmetadata = origmetadata + xmetalist
    for explanation in explanations:
        newwordlist = explanation.annotationwordlist
        oldwordlist = explanation.annotatedwordlist
        tokenposlist = explanation.annotatedposlist
        if len(newwordlist) == 1 and len(tokenposlist) == 1 and len(oldwordlist) == 1:
            newword = newwordlist[0]
            oldwordpos = tokenposlist[0]
            oldword = oldwordlist[0]
            newtoken = Token(newword, oldwordpos)
            oldtoken = Token(oldword, oldwordpos)
            if known_word(newword):
                newtokens = tokenreplace(newtokens, newtoken)
                bpl = bpl_node if known_word(oldword) else bpl_word
                meta = mkSASTAMeta(oldtoken, newtoken, name='ExplanationasReplacement',
                                   value='ExplanationasReplacement',
                                   cat='Lexical Error', backplacement=bpl)
                newmetadata.append(meta)
                result = TokenListMD(newtokens, newmetadata)
    return result


def islet(token, tree):
    xpt = f'//node[@pt and @begin="{str(token.pos)}"]'
    node = tbf.find1(tree, xpt)
    result = tbf.getattval(node, 'pt') == 'let'
    return result

def finaltokenmultiwordexplanation(tokensmd: TokenListMD, tree: SynTree) -> Optional[str]:
    #get the multiword explanation and the last tokenposition it occupies

    #it is assumed that the chat annotations have not been extracted and no metadata have been produced
    xtokens, xmetalist = gettokensplusxmeta(tree)

    result = None
    origmetadata = tokensmd.metadata
    #xtokens, xmetalist = gettokensplusxmeta(tree)
    explanations = [xm for xm in xmetalist if xm.name == 'Explanation']
    finalmwexplanations = []
    for xm in explanations:
        lxm = len(xm.annotationwordlist)
        lastxmpos = xm.annotationposlist[-1]
        postexplanationtokens = [token for token in tokensmd.tokens if token.pos > lastxmpos]
        cond = lxm > 1 and all([islet(token, tree) for token in postexplanationtokens])
        if cond:
            finalmwexplanations.append(xm)
    if len(finalmwexplanations) == 0:
        result = None
    elif len(finalmwexplanations) > 1:
        result = None
        # report an error
    elif len(finalmwexplanations) == 1:
        finalexpl = finalmwexplanations[0]
        words = [token.word for token in tokensmd.tokens]
        utt = space.join(words)
        postexplanationwords = [token.word for token in postexplanationtokens]
        expl = space.join(finalexpl.annotationwordlist + postexplanationwords)
        resultalignment = align_words(utt, expl)
        result = str(resultalignment)
    else:
        result = None
        # report an error

    return result



def finalmultiwordexplanation(stree: SynTree) -> Optional[str]:

    #get the multiword explanation and the last tokenposition it occupies


    explannwrdliststr = tbf.find1(stree, explannwordlistxpath)
    # print(explannwrdliststr)
    explannwrdlist = strf.string2list(explannwrdliststr, quoteignore=True)
    # print(explannwrdlist)

    explannposliststr = tbf.find1(stree, explannposlistxpath)
    # print(explannposliststr)
    explannposlist = strf.string2list(explannposliststr)
    # print(explannposlist)


    ismultiword = len(explannwrdlist) > 1
    # @@maybe add a condition that the length is not significantly shorter than the original utterance

    if ismultiword:
        # any token in the tree with begin > last tokenposition of explanation can only be an interpunction sign
        # check whether it is the last one ignoring interpunction
        # @@ maybe add interjections

        postexplanationtuplelist = []
        explannposlast = int(explannposlist[-1]) * 10
        # print(explannposlast)

        explisfinal = True
        for node in stree.iter():
            if explisfinal:
                if tbf.iswordnode(node):
                    beginstr = tbf.getattval(node, 'begin')
                    if beginstr != '':
                        begin = int(beginstr)
                        word = tbf.getattval(node, 'word')
                        # print(f'begin={begin}, word={word}')
                        if begin > explannposlast:
                            nodept = tbf.getattval(node, 'pt')
                            # print(f'nodept={nodept}')
                            if nodept not in {'let'}:
                                explisfinal = False
                            else:
                                postexplanationtuplelist.append((begin, word))

        if explisfinal:
            result = explannwrdlist
        else:
            result = None
        sortedpostexplanationtuplelist = sorted(postexplanationtuplelist, key=lambda x: x[0])
        sortedpostexplanationlist = [x[1] for x in sortedpostexplanationtuplelist]
    else:
        result, sortedpostexplanationlist = None, []
    #print(f'result={result}, sortedpostexplanationlist={sortedpostexplanationlist}')
    return result, sortedpostexplanationlist
def getalignment(tree: SynTree)-> Optional[str]:
    origutt = tbf.find1(tree, './/meta[@name="origutt"]/@value')
    # print(origutt)
    cleanuttelem = tbf.find1(tree, './/sentence')
    cleanutt = cleanuttelem.text
    explanationlist, postexplanationlist = finalmultiwordexplanation(tree)
    explanationstr = space.join(explanationlist + postexplanationlist) if explanationlist is not None else None
    # print(f'explanationstr={explanationstr}')
    if explanationstr is not None:
        alignment = align_words(cleanutt, explanationstr)
    else:
        alignment = None
    return alignment

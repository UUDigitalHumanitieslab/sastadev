"""
The module *tblex* contains functiond that require function from the lexicon module and from the treebankfunctions module
"""

from sastatypes import SynTree
import lexicon as lex
from treebankfunctions import getattval, iscompound, isdiminutive

def recognised_wordnodepos(node: SynTree, pos: str) -> bool:
    '''
    The function *recognised_wordnodepos* determines for *node* whether it is a known
    word of part of speech code *pos*.

    It distinguishes several subcases that yield the result True:

    * the value of the *word* attribute of *node* is a known word form (as determined by the function *lex.informlexiconpos*

    * the lower-cased value of the *word* attribute of *node* is a known word form (as determined by the function *lex.informlexiconpos*

    * the node is a node for a compound, as determined by the function *iscompound*:

        .. autofunction:: treebankfunctions::iscompound
           :noindex:

    * the node is a node for a diminutive, as determined by the function *isdiminutive*:

        .. autofunction:: treebankfunctions::isdiminutive
           :noindex:

    * the node is a node for a name part, as determined by the function *lex.isa_namepart*


    '''
    word = getattval(node, 'word')
    lcword = word.lower()
    result = lex.informlexiconpos(word, pos) or lex.informlexiconpos(lcword, pos) or \
             iscompound(node) or isdiminutive(node) or lex.isa_namepart_uc(word)
    return result

def recognised_wordnode(node: SynTree) -> bool:
    '''
    The function *recognised_wordnode* determines for *node* whether it is a known word.

    It distinguishes several subcases that yield the result True:

    * the value of the *word* attribute of *node* is a known word form (as determined
    by the function *lex.informlexicon*

    * the lower-cased value of the *word* attribute of *node* is a known word form (as
    determined by the function *lex.informlexicon

    * the node is a node for a compound, as determined by the function *iscompound*:

        .. autofunction:: treebankfunctions::iscompound

    * the node is node for a diminutive, as determined by the function *isdiminutive*:

        .. autofunction:: treebankfunctions::isdiminutive

    * the node is a node for a name part, as determined by the function *lex.isa_namepart*


    '''

    word = getattval(node, 'word')
    lcword = word.lower()
    result = lex.informlexicon(word) or lex.informlexicon(lcword) or iscompound(node) or isdiminutive(
        node) or lex.isa_namepart(word)
    return result


def recognised_lemmanode(node: SynTree) -> bool:
    '''
    The function *recognised_lemmanode* checks whether the *lemma* of *node* is in
    the lexicon  (as determined by the function *lex.informlexicon*).

    '''
    lemma = getattval(node, 'lemma')
    result = lex.informlexicon(lemma)
    return result


def recognised_lemmanodepos(node: SynTree, pos: str) -> bool:
    '''
    The function *recognised_lemmanodepos* checks whether the *lemma* of *node* is in
    the lexicon with part of speech *pos* (as determined by * lex.informlexiconpos*).

    '''
    lemma = getattval(node, 'lemma')
    result = lex.informlexiconpos(lemma, pos)
    return result


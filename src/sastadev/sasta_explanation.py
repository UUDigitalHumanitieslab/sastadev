
from typing import Optional

#import find1, iswordnode, getattval
import stringfunctions as strf
import treebankfunctions as tbf

from sastadev.sastatypes import SynTree

#import CHAT_Annotation as schat  # put off because it causes an error: AttributeError: module 'CHAT_Annotation' has no attribute 'wordpat'


space = ' '
CHAT_explanation = 'Explanation'
explannwordlistxpath = f'.//xmeta[@name="{CHAT_explanation}"]/@annotationwordlist'
explannposlistxpath = f'.//xmeta[@name="{CHAT_explanation}"]/@annotationposlist'


def finalmultiwordexplanation(stree: SynTree) -> Optional[str]:
    #get the multiword explanation and the last tokenposition is occupies

    explannwrdliststr = tbf.find1(stree, explannwordlistxpath)
    explannwrdlist = strf.string2list(explannwrdliststr, quoteignore=True)

    explannposliststr = tbf.find1(stree, explannposlistxpath)
    explannposlist = strf.string2list(explannposliststr)

    ismultiword = len(explannwrdlist) > 1

    if ismultiword:
        # any token in the tree with begin > last tokenposition of explanation can only be an interpunction sign
        # check whether it is the last one ignoring interpunction

        explannposlast = int(explannposlist[-1])

        explisfinal = True
        for node in stree.iter():
            if explisfinal:
                if tbf.iswordnode(node):
                    beginstr = tbf.getattval(node, 'begin')
                    if beginstr != '':
                        begin = int(beginstr)
                        if begin > explannposlast:
                            nodept = tbf.getattval(node, 'pt')
                            if nodept not in {'let'}:
                                explisfinal = False

        if explisfinal:
            result = space.join(explannwrdlist)
        else:
            result = None
        return result

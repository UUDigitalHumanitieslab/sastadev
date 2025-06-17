from typing import List

from sastadev.allresults import mkresultskey
from sastadev.CHAT_Annotation import CHAT_replacement, CHAT_wordnoncompletion
from sastadev.correctionlabels import (
    alpinoimprovement,
    codareduction,
    contextcorrection,
    dehyphenation,
    emphasis,
    error,
    explanationasreplacement,
    finalndrop,
    inflectionerror,
    informalpronunciation,
    lexicalerror,
    morphologicalerror,
    noncompletion,
    regionalform,
    regionalvariantorlexicalerror,
    repetition,
    replacement,
    pronunciationvariant,
    spellingcorrection,
    unknownword,
    unknownwordsubstitution,
    wrongpronunciation,
)
from sastadev.metadata import (
    ALLSAMPLECORRECTIONS,
    BASICREPLACEMENTS,
    SASTA,
    THISSAMPLECORRECTIONS,
)
from sastadev.methods import Method, asta
from sastadev.sastatypes import ExactResults, ExactResultsDict, SynTree
from sastadev.ASTApostfunctions import mluxqid, samplesizeqid
from sastadev.treebankfunctions import (
    getattval,
    getmeta,
    getnodeyield,
    getxsid,
    getyieldstr,
)


mlureskey = mkresultskey(mluxqid)
samplesizereskey = mkresultskey(samplesizeqid)

wordreplacementtypes = [
    alpinoimprovement,
    codareduction,
    contextcorrection,
    dehyphenation,
    emphasis,
    error,
    explanationasreplacement,
    finalndrop,
    inflectionerror,
    informalpronunciation,
    lexicalerror,
    morphologicalerror,
    noncompletion,
    regionalform,
    regionalvariantorlexicalerror,
    repetition,
    replacement,
    pronunciationvariant,
    spellingcorrection,
    unknownword,
    unknownwordsubstitution,
    wrongpronunciation,
    CHAT_replacement,
    CHAT_wordnoncompletion,
]

namecondition = " or ".join([f'@name="{wrt}"' for wrt in wordreplacementtypes])

sources = [BASICREPLACEMENTS, ALLSAMPLECORRECTIONS, THISSAMPLECORRECTIONS]

sourcecondition = "or ".join([f'@source="{SASTA}/{source}"' for source in sources])

fullcondition = f"({namecondition}) or ({sourcecondition})"


def getnormalisedwnposition(wn: SynTree, stree: SynTree) -> int:
    theyield = getnodeyield(stree)
    for i, node in enumerate(theyield):
        if node == wn:
            return i + 1
    return 0


def wnisanASTAX(wn: SynTree, tree: SynTree, exactresult: ExactResults) -> bool:
    wnposition = getnormalisedwnposition(wn, tree)
    if wnposition == 0:
        return False
    foundastax = [
        el
        for el in exactresult
        if el[1] == wnposition and el[0] in [mlureskey, samplesizereskey]
    ]
    result = foundastax != []
    return result


def filterbymetadata(
    rawunknownwordnodes: List[SynTree], exactresults: ExactResultsDict, method: Method
) -> List[SynTree]:
    """
    Removes nodes from a list of nodes if they have already been replaced by
    SASTA. These can be found in the metadata of the utterance.
    """
    unknownwordnodes = []
    for wn in rawunknownwordnodes:
        fulltrees = wn.xpath("ancestor::alpino_ds")
        fulltree = fulltrees[0] if fulltrees != [] else None
        uttid = getxsid(fulltree)
        session = getmeta(fulltree, "session")
        wnbegin = getattval(wn, "begin")
        mdxpath = f"""./ancestor::alpino_ds/descendant::xmeta[({fullcondition}) and @annotationposlist="[{wnbegin}]"]"""
        replacements = wn.xpath(mdxpath)
        exactresult = exactresults[uttid] if uttid in exactresults else []
        if exactresult == []:
            print(
                f'{session}: Empty exactresult: {getattval(wn, "word")} in {uttid}: {getyieldstr(fulltree)}'
            )
        isASTAX = (
            wnisanASTAX(wn, fulltree, exactresult) if method.name == asta else False
        )
        if replacements == [] and not isASTAX:
            unknownwordnodes.append(wn)
    return unknownwordnodes

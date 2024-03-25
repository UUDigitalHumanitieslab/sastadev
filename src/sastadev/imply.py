'''
The *imply* module implements the function *removeimplies* to remove matches that are implied by a given match
'''
from typing import Dict, Tuple
from typing_extensions import TypeAlias
from collections import defaultdict
from sastatypes import ExactResults,  QId, QueryDict, Matches, Match,  SynTree, UttId
from sastadev.query import Query
from sastadev.treebankfunctions import getnodeyield, getattval as gav
from methods import Method
from allresults import matches2exactresults, ResultsKey

MatchesDict: TypeAlias = Dict[Tuple[ResultsKey, UttId], Matches]


def removeimplies(matches: MatchesDict, exactresults:ExactResults, method: Method) -> Tuple[MatchesDict, ExactResults]:
    toremovekeys = []
    toremovematches = defaultdict(list)
    queries = method.queries
    for qid, uttid in matches:
        thematches = matches[(qid,uttid)]
        thequery = queries[qid[0]]
        for item in thequery.implies:
            simpleimpliedqid = method.simpleitem2idmap[item]
            impliedqid = (simpleimpliedqid, simpleimpliedqid)
            if (impliedqid, uttid) in matches:
                theimpliedmatches = matches[(impliedqid, uttid)]
                for theimpliedmatch in theimpliedmatches:
                    for thematch in thematches:
                        valid = contains(thematch, theimpliedmatch)
                        if valid:
                            toremovematches[(impliedqid, uttid)].append(theimpliedmatch)
                            toremovekeys.append((impliedqid, uttid))

    newmatches = removematches(matches, toremovematches)
    newexactresults = matches2exactresults(newmatches)
    return newmatches, newexactresults

def contains(match: Match, impliedmatch: Match) -> bool:
    matchnode, topnode = match
    matchnodeyield = getnodeyield(matchnode)
    impliedmatchnode, impliedtopnode = impliedmatch
    impliedmatchnodeyield = getnodeyield(impliedmatchnode)
    matchpositions = {gav(node, 'end') for node in matchnodeyield}
    impliedmatchpositions = {gav(node, 'end') for node in impliedmatchnodeyield}
    result = impliedmatchpositions.issubset(matchpositions)  # of moeten de laagste identiek zijn?
    return result

def removematches(matches: MatchesDict, toremovematches: MatchesDict) -> MatchesDict:
    newmatchesdict = defaultdict(list)
    for key in matches:
        if key not in toremovematches:
            newmatchesdict[key] = matches[key]
        else:
            for matchnode in matches[key]:
                if matchnode not in toremovematches[key]:
                    newmatchesdict[key].append(matchnode)
    return newmatchesdict


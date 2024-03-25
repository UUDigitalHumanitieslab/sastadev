'''
This module contains definitions of types used in multiple modules
'''

from collections import Counter
from typing import Callable, Dict, List, Optional, Tuple, Union

from lxml import etree  # type: ignore
from typing_extensions import TypeAlias

from sastadev.query import Query
from sastadev.sastatoken import Token

Level = str  # in the future perhaps NewType('Level', str)
Position = int  # in the future perhapos NewType('Position', int)
PhiTriple = Tuple[str, str, str]
QId = str  # in the futute perhaps NewType('QId', str)
SynTree = etree.Element  # type: ignore
TreeBank = etree.Element
UttId = str  # in the future perhaps NewType('UttId', str)


Item = str  # in the future perhaps NewType('Item', str)
Item2LevelsDict = Dict[Item, List[Level]]
Item_Level = Tuple[Item, Level]

AltCodeDict = Dict[Item_Level, Item_Level]
AltId: TypeAlias = int
AnalysedTrees = List[Tuple[UttId, SynTree]]
BackPlacement: TypeAlias = int
CapitalName: TypeAlias = str
CountryName: TypeAlias = str
ContinentName: TypeAlias = str
CELEXPosCode: TypeAlias = str
FirstName: TypeAlias = str
LocationName: TypeAlias = str
DCOIPt: TypeAlias = str
DeHet: TypeAlias = str
CELEX_INFL: TypeAlias = str
DCOITuple: TypeAlias = Tuple
Lemma: TypeAlias = str
CorrectionMode: TypeAlias = str  # Literal['0','1','n']
ErrorDict: TypeAlias = Dict[str, List[List[str]]]
Level: TypeAlias = str  # in the future perhaps NewType('Level', str)
Item: TypeAlias = str  # in the future perhaps NewType('Item', str)
Item_Level: TypeAlias = Tuple[Item, Level]
IntSpan: TypeAlias = Tuple[int, int]
AltCodeDict: TypeAlias = Dict[Item_Level, Item_Level]
QId: TypeAlias = str  # in the futute perhaps NewType('QId', str)
ResultsKey: TypeAlias = Tuple[QId, str]
UttId: TypeAlias = str  # in the future perhaps NewType('UttId', str)
Position: TypeAlias = int  # in the future perhapos NewType('Position', int)
PositionStr: TypeAlias = str
Stage: TypeAlias = int
SynTree: TypeAlias = etree._Element  # type: ignore
GoldTuple: TypeAlias = Tuple[str, str, Counter]
GoldResults = Dict[QId, GoldTuple]
Item2LevelsDict: TypeAlias = Dict[Item, List[Level]]
Match: TypeAlias = Tuple[SynTree, SynTree]
Matches: TypeAlias = List[Match]
MatchesDict: TypeAlias = Dict[Tuple[ResultsKey, UttId], Matches]
MetaElement: TypeAlias = etree.Element
ExactResult: TypeAlias = Tuple[UttId, Position]
ExactResults: TypeAlias = List[ExactResult]
ExactResultsDict: TypeAlias = Dict[ResultsKey, ExactResults]  # qid
ExactResultsFilter = Callable[[Query, ExactResultsDict, ExactResult], bool]
Gender: TypeAlias = str
Penalty: TypeAlias = int
PhiTriple: TypeAlias = Tuple[str, str, str]
OptPhiTriple: TypeAlias = Optional[PhiTriple]
PositionMap: TypeAlias = Dict[Position, Position]
QueryDict: TypeAlias = Dict[QId, Query]
QIdCount: TypeAlias = Dict[QId, int]
MethodName: TypeAlias = str  # perhaps in the future NewType('MethodName', str)
FileName: TypeAlias = str  # perhaps in the future NewType('FileName', str)
ReplacementMode: TypeAlias = int
ResultsCounter: TypeAlias = Counter  # Counter[UttId]  # Dict[UttId, int]
ResultsDict: TypeAlias = Dict[QId, ResultsCounter]
SampleSizeTuple = Tuple[List[UttId], int, Optional[PositionStr]]
Span: TypeAlias = Tuple[PositionStr, PositionStr]
Item_Level2QIdDict: TypeAlias = Dict[Item_Level, QId]
Nort: TypeAlias = Union[SynTree, Token]
ExactResultsFilter: TypeAlias = Callable[[Query, ExactResultsDict, ExactResult], bool]
Targets: TypeAlias = int
Treebank: TypeAlias = etree.Element
TreePredicate: TypeAlias = Callable[[SynTree], bool]
TokenTreePredicate: TypeAlias = Callable[[Token, SynTree], bool]
URL: TypeAlias = str
UttTokenDict: TypeAlias = Dict[UttId, List[Token]]
UttWordDict: TypeAlias = Dict[UttId, List[str]]
WordInfo: TypeAlias = Tuple[Optional[CELEXPosCode], Optional[DeHet], Optional[CELEX_INFL], Optional[Lemma]]
# moved the following to allresuls.py
#CoreQueryFunction: TypeAlias = Callable[[SynTree], List[SynTree]]
#PostQueryFunction: TypeAlias = Callable[[SynTree, allresults.AllResults], List[SynTree]]
#QueryFunction: TypeAlias = Union[CoreQueryFunction, PostQueryFunction]



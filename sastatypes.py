'''
This module contains definitions of types used in multiple modules
'''

from typing import Dict, List, Any, Tuple, Callable, Pattern, Optional, NewType, Union
from lxml import etree # type: ignore
from collections import Counter
from query import Query
from sastatoken import Token

AltId = int
BackPlacement = int
CapitalName = str
CountryName = str
ContinentName = str
CELEXPosCode = str
FirstName = str
LocationName = str
DeHet = str
CELEX_INFL =str
DCOITuple = Tuple
Lemma = str
CorrectionMode = str  # Literal['0','1','n']
ErrorDict = Dict[str, List[List[str]]]
Level = str  # in the future perhaps NewType('Level', str)
Item = str  # in the future perhaps NewType('Item', str)
Item_Level = Tuple[Item, Level]
IntSpan = Tuple[int, int]
AltCodeDict = Dict[Item_Level, Item_Level]
QId = str  # in the futute perhaps NewType('QId', str)
UttId = str  # in the future perhaps NewType('UttId', str)
Position = int  # in the future perhapos NewType('Position', int)
PositionStr = str
#SynTree = etree._Element  # type: ignore
SynTree = etree.Element  # type: ignore
GoldTuple = Tuple[str, str, Counter]
Item2LevelsDict = Dict[Item, List[Level]]
Match = Tuple[SynTree, SynTree]
Matches = List[Match]
MatchesDict = Dict[Tuple[QId, UttId], Matches]
MetaElement = etree.Element
ExactResult = Tuple[UttId, Position]
ExactResults = List[ExactResult]
ExactResultsDict = Dict[QId, ExactResults]  # qid
Gender = str
Penalty = int
PhiTriple = Tuple[str, str, str]
OptPhiTriple = Optional[PhiTriple]
PositionMap = Dict[Position, Position]
QueryDict = Dict[QId, Query]
QIdCount = Dict[QId, int]
MethodName = str  # perhaps in the future NewType('MethodName', str)
FileName = str  # perhaps in the future NewType('FileName', str)
ReplacementMode = int
ResultsCounter = Counter  # Counter[UttId]  # Dict[UttId, int]
ResultsDict = Dict[QId, ResultsCounter]
Span = Tuple[PositionStr, PositionStr]
Item_Level2QIdDict = Dict[Item_Level, QId]
Nort = Union[SynTree, Token]
ExactResultsFilter = Callable[[Query, ExactResultsDict, ExactResult], bool]
Targets = int
Treebank = etree.Element
URL = str
UttTokenDict = Dict[UttId, List[Token]]
UttWordDict = Dict[UttId, List[str]]
WordInfo = Tuple[Optional[CELEXPosCode], Optional[DeHet], Optional[CELEX_INFL], Optional[Lemma]]
# moved the following to allresuls.py
#CoreQueryFunction = Callable[[SynTree], List[SynTree]]
#PostQueryFunction = Callable[[SynTree, allresults.AllResults], List[SynTree]]
#QueryFunction = Union[CoreQueryFunction, PostQueryFunction]




'''
This module contains definitions of types used in multiple modules
'''

from collections import Counter
from typing import Callable, Dict, List, Optional, Tuple, Union

from lxml import etree

from sastadev.query import Query
from sastadev.sastatoken import Token

Level = str  # in the future perhaps NewType('Level', str)
Position = int  # in the future perhapos NewType('Position', int)
PhiTriple = Tuple[str, str, str]
QId = str  # in the futute perhaps NewType('QId', str)
SynTree = etree.Element  # type: ignore
UttId = str  # in the future perhaps NewType('UttId', str)


Item = str  # in the future perhaps NewType('Item', str)
Item2LevelsDict = Dict[Item, List[Level]]
Item_Level = Tuple[Item, Level]


AltCodeDict = Dict[Item_Level, Item_Level]
AltId = int
AnalysedTrees = List[Tuple[UttId, SynTree]]
BackPlacement = int
CELEXPosCode = str
CELEX_INFL =str
CapitalName = str
ContinentName = str
CorrectionMode = str  # Literal['0','1','n']
CountryName = str
DCOIPt = str
DCOITuple = Tuple
DeHet = str
ErrorDict = Dict[str, List[List[str]]]
ExactResult = Tuple[UttId, Position]
ExactResults = List[ExactResult]
FileName = str  # perhaps in the future NewType('FileName', str)
FirstName = str
Gender = str
GoldTuple = Tuple[str, str, Counter]
GoldResults = Dict[QId, GoldTuple]
IntSpan = Tuple[int, int]
Item_Level2QIdDict = Dict[Item_Level, QId]
Lemma = str
LocationName = str
Match = Tuple[SynTree, SynTree]
Matches = List[Match]
MetaElement = etree.Element
MethodName = str  # perhaps in the future NewType('MethodName', str)
Nort = Union[SynTree, Token]
OptPhiTriple = Optional[PhiTriple]
Penalty = int
PositionMap = Dict[Position, Position]
PositionStr = str
Postag = str
Pt = str
QIdCount = Dict[QId, int]
QueryDict = Dict[QId, Query]
ReplacementMode = int
ResultsCounter = Counter  # Counter[UttId]  # Dict[UttId, int]
ResultsDict = Dict[QId, ResultsCounter]
SampleSizeTuple = Tuple[List[UttId], int, Optional[PositionStr]]
Source = str
Span = Tuple[PositionStr, PositionStr]
Stage = int
Targets = int
TokenTreePredicate = Callable[[Token, SynTree], bool]
TreePredicate = Callable[[SynTree], bool]
Treebank = etree.Element
URL = str
UttTokenDict = Dict[UttId, List[Token]]
UttWordDict = Dict[UttId, List[str]]
Word = str
WordInfo = Tuple[Optional[CELEXPosCode], Optional[DeHet], Optional[CELEX_INFL], Optional[Lemma]]
WordLower = str

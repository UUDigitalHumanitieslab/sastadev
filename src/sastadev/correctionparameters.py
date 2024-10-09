from dataclasses import dataclass
from sastadev.sastatypes import MethodName, TreeBank

@dataclass
class CorrectionParameters:
    method: MethodName
    options: dict
    allsamplecorrections : dict
    thissamplecorrections: dict
    treebank: TreeBank
    contextdict : dict

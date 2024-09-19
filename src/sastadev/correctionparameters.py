from dataclasses import dataclass
from sastadev.sastatypes import MethodName

@dataclass
class CorrectionParameters:
    method: MethodName
    options: dict
    allsamplecorrections : dict
    thissamplecorrections: dict

from dataclasses import dataclass
import os
from sastadev.conf import settings
from sastadev.sastatypes import MethodName
from sastadev.xlsx import getxlsxdata
from typing import List

space = ' '
MethodVariant = str


datasetfilename = 'DatasetOverview.xlsx'
datasetfolder = settings.DATAROOT
datasetfullname = os.path.join(datasetfolder, datasetfilename)


def robustint(x) -> int:
    if x == '' or x == space:
        result = 0
    else:
        result = int(x)
    return result


@dataclass
class DataSet:
    name: str
    methodname: MethodName
    use: str
    infigures: bool
    variant:  MethodVariant
    samples: int
    bronzecount: int
    source_org: str
    sourcepersons: str
    description: str


def row2dataset(row: List[str]) -> DataSet:
    rawname = row[0]
    lcname = rawname.strip()
    rawmethodname = row[1]
    methodname = rawmethodname.strip().lower()
    infigures = "yes" in row[3].lower()
    rawvariant = row[4]
    variant = rawvariant.strip().lower()

    result = DataSet(name=lcname, methodname=methodname, use=row[2], infigures=infigures, variant=variant,
                     samples=robustint(row[5]), bronzecount=robustint(row[6]), source_org=row[7], sourcepersons=row[8],
                     description=row[9])
    return result


def getalldatasets():
    datasets = []
    header, data = getxlsxdata(datasetfullname)
    for row in data:
        newdataset = row2dataset(row)
        datasets.append(newdataset)
    return datasets

alldatasets = getalldatasets()
infiguresdatasets = [d for d in alldatasets if d.infigures]
dsname2method = {d.name: d.methodname for d in alldatasets}

import os
from sastadev.conf import settings
from sastadev.constants import (checksuffix, errorsummaryfolder, errorsummarysuffix, intreebanksfolder,
                                silverpermfolder as permfolder, resultsfolder)
from sastadev.mksilver import updatepermdict
from sastadev.xlsx import write2excel
from sastadev.filefunctions import savecopy

pcheaders = [
    ['Sample', 'User1', 'User2', 'User3', 'MoreorLess', 'qid', 'cat', 'subcat', 'item', 'uttid', 'pos', 'utt',
     'origutt',
     'inform']]


def getallcomments(dataset, sample):
    datasetpath = os.path.join(settings.SD_DIR, settings.DATAROOT, dataset)
    intreebankspath = os.path.join(datasetpath, intreebanksfolder)
    filename = os.path.join(intreebankspath, f'{sample}.xml')
    permdatadict = dict()

    # read the permsample file, add to permdatadict
    permfilename = f'perm_{sample}.xlsx'
    permpath = os.path.join(settings.SD_DIR, settings.DATAROOT, dataset, permfolder)
    if not os.path.exists(permpath):
        os.makedirs(permpath)
    permfullname = os.path.join(permpath, permfilename)
    permdatadict, perm_header = updatepermdict(permfullname, permdatadict)

    # read the check file, add to permdatadict
    checkfilename = f'{sample}{checksuffix}.xlsx'
    resultspath = os.path.join(settings.SD_DIR, settings.DATAROOT, dataset, resultsfolder)
    if not os.path.exists(resultspath):
        os.makedirs(resultspath)
    checkfullname = os.path.join(resultspath, checkfilename)
    permdatadict, checkheader = updatepermdict(checkfullname, permdatadict)

    # read the errorsummary files, add to permdatadict
    errorsummarypath = os.path.join(settings.SD_DIR, settings.DATAROOT, dataset, errorsummaryfolder)
    if not os.path.exists(errorsummarypath):
        os.makedirs(errorsummarypath)
    errorsummaryfilenames = [fn for fn in os.listdir(errorsummarypath) if fn.endswith(errorsummarysuffix+'.xlsx')]
    for errorsummaryfilename in errorsummaryfilenames:
        errorsummaryfullname = os.path.join(errorsummarypath, errorsummaryfilename)
        permdatadict, errorsummaryheader = updatepermdict(errorsummaryfullname, permdatadict, sample=sample)


    # make a copy of the original permfullname if it exists
    if os.path.exists(permfullname):
        savecopy(permfullname, prevsuffix='', prevprefix='previous_')
    # write the permdatadict to perfullname
    write2excel(permdatadict, pcheaders, permfullname)

    return permdatadict


from optparse import OptionParser
import os
from sastadev.xlsx import getxlsxdata, mkworkbook
from sastadev.conf import settings
from sastadev.constants import permprefix

def addsamplecol(dataset, folder):
    fullpath = os.path.join(settings.SD_DIR, settings.DATAROOT, dataset, folder)
    rawfilenames = os.listdir(fullpath)
    filenames = [fn for fn in rawfilenames if fn.endswith('.xlsx')]
    for filename in filenames:
        fullname = os.path.join(fullpath, filename)
        base, ext = os.path.splitext(filename)
        if base.startswith(permprefix):
            sample = base[len(permprefix):]
        else:
            sample = base
        header, data = getxlsxdata(fullname)
        newheader = ['Sample'] + header
        newdata = []
        for row in data:
            newrow = [sample] + row
            newdata.append(newrow)
        wb = mkworkbook(fullname, [newheader], newdata)
        wb.close()

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-d", "--dataset", dest="dataset",
                      help="dataset")
    parser.add_option("-f", "--folder", dest="folder",
                      help="Name of the folder in dataset containing the files")
    (options, args) = parser.parse_args()
    if options.dataset is not None and options.folder is not None:
        addsamplecol(options.dataset, options.folder)
    else:
        print('Specify dataset (-d) and folder (-f)' )

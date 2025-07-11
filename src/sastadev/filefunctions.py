import os
import sys
import shutil
from sastadev.sastatypes import FileName

reportwidth = 0

# the following 2 are useful if you just have to read the files,
# they are less useful if you have to create new copies with the same folder structure


def getallfilenames(inpath, allowedexts):
    filenames = []
    for root, dirs, thefiles in os.walk(inpath):
        for filename in thefiles:
            fullname = os.path.join(root, filename)
            (base, ext) = os.path.splitext(filename)
            if ext in allowedexts:
                filenames.append(fullname)
    return filenames


def iterallfilenames(inpath, allowedexts):
    filenames = []
    for root, dirs, thefiles in os.walk(inpath):
        for filename in thefiles:
            fullname = os.path.join(root, filename)
            (base, ext) = os.path.splitext(filename)
            if ext in allowedexts:
                yield fullname


# @@add functions that arev useful if you have make new versions with the same folder structure

def reportevery(ctr, repevery, sep=' ', maxwidth=100, file=sys.stderr):
    global reportwidth
    # curreportwidth = reportwidth
    if ctr % repevery == 0:
        ctrstr = str(ctr)
        lcurreport = len(ctrstr) + len(sep)
        if reportwidth + lcurreport > maxwidth:
            print(file=sys.stderr)
            reportwidth = lcurreport
        else:
            print(ctr, end=sep, file=file)
            sys.stderr.flush()
            reportwidth += len(str(ctr)) + len(sep)


def getbasename(fullname):
    path, filename = os.path.split(fullname)
    base, ext = os.path.splitext(filename)
    return base

def savecopy(infullname, prevsuffix='_previous', prevprefix='', outpath=None):
    thepath, infilename = os.path.split(infullname)
    base, ext = os.path.splitext(infilename)
    previousinfilename = prevprefix + base + prevsuffix + ext
    if outpath is None:
        outpath = thepath
    previousinfullname = os.path.join(outpath, previousinfilename)
    shutil.copyfile(infullname, previousinfullname)


def getsamplename(fn: FileName) -> str:
    basename = getbasename(fn)
    samplename = basename[:basename.rfind('_')]
    return samplename
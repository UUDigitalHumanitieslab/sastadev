import os
import re
from collections import Counter, defaultdict
from typing import Dict, List

import pytest

from sastadev.celexlexicon import dmwdict
from sastadev.stringfunctions import tremavowels
from sastadev.syllablecount import (getfirsttremavowelpos, getvoweltier,
                                    vowelsylldict)
from sastadev.xlsx import add_worksheet, mkworkbook

maxexamples = 10
vseqs = Counter()
examples = defaultdict(list)
status = {}

qupattern = fr'([Qq])([Uu])([^{tremavowels}])'
qure = re.compile(qupattern)

yogapattern = '^y'
yogare = re.compile(yogapattern)

ouillpattern = r'(ou)(i)(ll)'
ouillre = re.compile(ouillpattern)

ieuwpattern = r'([EeIi]e)(u)(w)'
ieuwre = re.compile(ieuwpattern)

@pytest.mark.skip(reason="test code does not work")
def test_syllcount():

    def reduceexamples(examples:Dict[str,List]) -> Dict[str,List]:
        reducedexamples = {}
        for vseq, examplelist in examples.items():
            lexamplelist = len(examplelist)
            if  lexamplelist <= maxexamples:
                reducedexamples[vseq] = examplelist
            else:
                jump = lexamplelist // maxexamples
                reducedexamplelist = []
                for i in range(10):
                    theindex = i * jump
                    selectedexample = examplelist[theindex]
                    reducedexamplelist.append(selectedexample)
                reducedexamples[vseq] = reducedexamplelist
        return reducedexamples

    for word in dmwdict:
        reducedword = word
        #remove u after q unless followed by tremavowel
        reducedword = qure.sub(r'\1\3', reducedword)
        #remove y at the beginning of a word (yoga v. halcyon) will not work in compounds hulpyogi
        reducedword = yogare.sub(r'', reducedword)
        # oui -> ou before ll
        reducedword = ouillre.sub(r'\1\3', reducedword)
        # ieuw, eeuw -> iew, eew
        reducedword = ieuwre.sub(r'\1\3', reducedword)
        vt = getvoweltier(reducedword)
        for vs in vt:
            if vs not in vseqs:
                check = len(vs) == 1 or getfirsttremavowelpos(vs) >= 0 or vs in vowelsylldict
                ok = 'ok' if check else 'no'
                status[vs] = ok
            examples[vs].append(word)
        vseqs.update(vt)

    header = ['vseq', 'frq']
    data = sorted(vseqs.items(), key= lambda item: item[1], reverse=True)
    exampleheader = ['vseq',  'status', 'examples']
    reducedexamples = reduceexamples(examples)
    exampledata = []
    for vseq in vseqs:
        vseq_status = status[vseq] if vseq in status else 'unknown'
        if vseq in reducedexamples:
            examplestr = ', '.join(reducedexamples[vseq])
        else:
            examplestr = "$$$"
            print(f'Vowel sequence {vseq} not in examples')
        row = [vseq, vseq_status, examplestr]
        exampledata.append(row)
    sortedexampledata = sorted(exampledata, key=lambda el: el[0] )

    outfilename = 'CELEXvowelsequences.xlsx'
    outpath = r'D:\Dropbox\jodijk\Utrecht\Projects\SASTA emer\syllablecount'
    outfullname = os.path.join(outpath, outfilename)

    wb = mkworkbook(outfullname, [header], data, sheetname='Freq')
    add_worksheet(wb, [exampleheader], sortedexampledata, sheetname='Examples')
    wb.close()




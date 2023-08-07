import os

import pytest

from sastadev.goldcountreader import gcadd, get_goldcounts, tab, txtext


@pytest.mark.skip(reason='test code does not work')
def test_goldcountreader():
    inpath = './goldcountstestin'
    testfilename = 'overzicht_Mieke.xlsx'
    testfullname = os.path.join(inpath, testfilename)
    testset = ['TARSP_MIEKE03_ID.xml', 'TARSP_MIEKE04_ID.xml', 'TARSP_MIEKE05_ID.xml',
               'TARSP_MIEKE06_ID.xml', 'TARSP_MIEKE07_ID.xml', 'TARSP_MIEKE08_ID.xml']
    outpath = './goldcountstestout'
    for tbn in testset:
        tbndata = get_goldcounts(testfullname, tbn)
        outfilename = tbn + gcadd + txtext
        outfullname = os.path.join(outpath, outfilename)
        outfile = open(outfullname, 'w', encoding='utf8')
        # print('Results for {}:'.format(tbn), file =outfile)
        for el in tbndata:
            print(el, tbndata[el], sep=tab, file=outfile)
        outfile.close()

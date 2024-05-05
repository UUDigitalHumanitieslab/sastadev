from lxml import etree
import os
from sastadev.conf import settings
from sastadev.constants import intreebanksfolder
from sastadev.history import gathercorrections
import sastadev.sastatok


def tryhistory():
    dataset = 'vklstap'
    filenames = ['stap_02.xml']
    fullpath = os.path.join(settings.DATAROOT, dataset, intreebanksfolder)
    fullnames = [os.path.join(fullpath, fn) for fn in filenames]
    for fullname in fullnames:
        fulltreebank = etree.parse(fullname)
        treebank = fulltreebank.getroot()
        thehistory = gathercorrections(treebank)
        for wrong in thehistory:
            print(wrong)
            for correction in thehistory[wrong]:
                print(f'--{correction}')


if __name__ == '__main__':
    tryhistory()

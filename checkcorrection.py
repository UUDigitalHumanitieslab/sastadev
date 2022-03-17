'''
Compares the errorlogging file with the error reference file
'''

import os
from xlsx import getxlsxdata

dataset = 'vkltarsp'
dataset = 'vklstap'
dataset = 'vklasta'

if dataset == 'vkltarsp':
    resultspath = r'D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\tarspdata\tarsp'
    dataprefix = 'tarsp'

elif dataset == 'vklstap':
    resultspath = r'D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\stapdata'
    dataprefix = 'stap'

elif dataset == 'vklasta':
    resultspath = r'D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\astadata\asta'
    dataprefix = 'asta'


errorloggingfilename = dataprefix + '_errorlogging.xlsx'
errorloggingfullname = os.path.join(resultspath, errorloggingfilename)

referencepath = r'D:\jodijk\Dropbox\Surfdrive\Shared\SASTAPLUS\November'
errorreffilename = dataprefix + '_error_ref.xlsx'
errorreffullname = os.path.join(referencepath, errorreffilename)

logheader, logdata = getxlsxdata(errorloggingfullname)
refheader, refdata = getxlsxdata(errorreffullname)

refdict = {(row[0], row[1]): row[3] for row in refdata}

correctcorrections = 0
missedcorrections = 0
wrongcorrections = 0
for row in logdata:
    key = (row[0], row[5])
    if 'BEST' in row[10]:
        logsent = row[9]
        if key not in refdict:
            print('Missing example in refdict: {}'.format(key))
            print(row[9])
            missedcorrections += 1
        else:
            refsent = refdict[key]
            if refsent != logsent:
                print('Mismatch: {}'.format(key))
                print('refsent=<{}>'.format(refsent))
                print('logsent=<{}>'.format(logsent))
                wrongcorrections += 1
            else:
                correctcorrections += 1

allcorrections = correctcorrections + wrongcorrections + missedcorrections

correctioncounts = [correctcorrections, wrongcorrections, missedcorrections]
labels = ['correct corrections', 'wrong corrections', 'missed corrections']
labeled_corrections = zip(labels, correctioncounts)

print('\nSummary:\n')
for label, corr in labeled_corrections:
    print('{} = {} ({:.2f}%)'.format(label, corr, corr / allcorrections * 100))
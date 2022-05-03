'''
Module to specify the default location of the data to train and test sastadev
'''

import os

user = os.getlogin()
if user == 'Odijk101':
    dataroot = r'D:\jodijk\Dropbox\jodijk\Utrecht\Projects\SASTADATA'
#add other users here
else:
    dataroot = '.'

bronzefolder = 'bronze'
formsfolder = 'forms'
indatafolder = 'indata'
intreebanksfolder = 'intreebanks'
loggingfolder = 'logging'
outtreebanksfolder = 'outtreebanks'
resultsfolder = 'results'
silverfolder = 'silver'
silverpermfolder = 'silverperm'
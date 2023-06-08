from collections import Counter

qidcolheader = 'id'
uttcolheader = 'uttids'
tab = '\t'
comma = ','
platinumheaderrows = 0


def read_referencefile(infilename, logfile):
    '''
    a reference file is tsv file which contains a header with at least two column headers (idcolheader, uttcolheader)
    :param infilename:
    :return: a dictionary with for each queryid a Counter for the utterance ids
    '''
    infile = open(infilename, 'r')
    rowctr = 0
    results = {}
    for line in infile:
        if rowctr == platinumheaderrows:
            rowstr = line.lower()
            rowlist = rowstr.split(tab)
            try:
                qidcol = rowlist.index(qidcolheader)
            except ValueError:
                print('Error reading reference file; no ID column header', infilename, file=logfile)
                exit(-1)
            try:
                uttcol = rowlist.index(uttcolheader)
            except ValueError:
                print('Error reading reference file: no uttids column header in', infilename, file=logfile)
                exit(-1)
        elif rowctr > platinumheaderrows:
            rowstr = line[:-1]
            rowlist = rowstr.split(tab)
            qid = rowlist[qidcol]
            utts = rowlist[uttcol]
            if utts == '':
                uttlist = []
            else:
                rawuttlist = utts.split(comma)
                uttlist = [uttid.strip() for uttid in rawuttlist]
            results[qid] = Counter(uttlist)
        rowctr += 1
    infile.close()
    return results

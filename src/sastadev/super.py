from lexicon import informlexiconpos, issuperadjective


for wrd, gold in [('superhard', True), ('superlang', True), ('superman', False), ('supermarkt', False)]:
    errorfound = False
    result = issuperadjective(wrd)
    if result != gold:
        print(wrd, f'{result}/={gold}')
        errorfound = True
    if errorfound:
        assert False

junk = 0
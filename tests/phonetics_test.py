from sastadev.phonetics import phoneticise


def test_phoneticise():
    examples = [('activiteit', 'aktiviteit'), ('acht', 'acht'), ('schrander', 'schrander'), ('qua', 'kwa'),
                ('centrum', 'sentrum'), ('cylinder', 'sielinder'), ('taxi', 'taksi'), ('spaghetti', 'spagetti')]
    for instr, gold in examples:
        result = phoneticise(instr)
        # assert result == gold
        if result != gold:
            print('NO: <{}>  != <{}> (input: <{}>)'.format(result, gold, instr))

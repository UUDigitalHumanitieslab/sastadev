from sastadev.mismatches import exactcompare


def test_compare():
    testresults = [(1, 2), (1, 2), (1, 2), (1, 5), (1, 6), (2, 0), (2, 4)]
    goldresults = [(1, 2), (2, 4), (2, 6), (1, 0), (3, 5)]
    reftestminusgold = [(1, 2), (1, 5), (1, 6)]
    refgoldminustest = [(3, 5)]
    refintersection = [(1, 2), (1, 2), (2, 4), (2, 6)]
    (testminusgold, goldminustest, intersection) = exactcompare(
        testresults, goldresults)
    for (l, r, g) in zip(['R-G', 'G-R', 'R*G'], [testminusgold, goldminustest, intersection], [reftestminusgold, refgoldminustest, refintersection]):
        if r == g:
            print('{}: OK {} == {}'.format(l, r, g))
        else:
            print('{}: NO: {} != {}'.format(l, r, g))

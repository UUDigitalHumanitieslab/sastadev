import pytest

from sastadev.corrector import getalternatives, getexpansions, mkchatutt, space
from sastadev.sastatok import sasta_tokenize
from sastadev.tokeniseCHILDES import tokenise
from sastadev.tokenmd import TokenListMD


@pytest.mark.skip(reason='test code does not work')
def test_token():
    testutts = ['in het uh hier in het Breda uh silahe',
                'Gaatie gaatie jaaaa, dat zijn mouwe met stukkies in de am-bu-lan-ce met de kopje thee']
    testutts += ['ieduleen [: iedereen] lettu [: redden].	iedereen redden .']
    testutts += ['ieduleen [: iedereen] lettu [: redden].	iedereen redden . Mama mouwe hoog']
    testutts += ['de bal']
    testutts += ['dat eh is mooi']
    testutts += ['de zwembad', 'de eh zwembad', 'de ja man']
    testutts += ['dit --- is -- een - hyphen test']
    testutts += ['hebbe een boek']
    testutts += ['hebbe schoene']
    testutts += ['die dich(t)']
    testutts += ['de kopje thee']
    testutts += ['en <ke [: de]> [//] hier nog ke [: de] babypaardje.']
    testutts += ['de kopje thee', 'ke [: de] babypaardje.', 'de ponyautootje']
    testutts += ['in de am-bu-lan-ce met', 'de kopje thee',
                 'Gaatie', 'gaatie', 'jaaaa', 'mouwe', 'stukkies']
    testutts += ['waar sit die zeep ?', 'iets erin setten',
                 'ie(t)s e(r)in setten.', 'ie(t)s e(r)in setten .']
    testutts += ['ie(t)s e(r)in setten.']
    testutts = ['kat-oorbellen.']

    for testutt in testutts:
        # correction, metadata = getcorrection(testutt)
        print(testutt)
        print(space.join(correction))
        for metadatum in metadata:
            print(str(metadatum))


@pytest.mark.skip(reason='test code does not work')
def test_corrector():
    testutts = ['in het uh hier in het Breda uh silahe',
                'Gaatie gaatie jaaaa, dat zijn mouwe met stukkies in de am-bu-lan-ce met de kopje thee']
    for testutt in testutts:
        method = 'tarsp'
        testtokens = tokenise(testutt)
        alternatives = getalternatives(testtokens, method, None, 0)
        # for el in alternatives:
        #    print(testtokens[el], space.join(alternatives[el]))
        # outputalternatives(testtokens, alternatives, sys.stdout)
        print(space.join(testtokens))
        for alternative in alternatives:
            print(space.join(alternative))
            chatutt = mkchatutt(testtokens, alternative.word)
            print(space.join(chatutt))


def test_expand():
    testutts = ['je mag weleens inne als jij niet bijt .']
    testutts = ["das mooi als jij inne gaat"]
    # check second alternative
    # @@add example with 2 replacements
    for testutt in testutts:
        testtokens = sasta_tokenize(testutt)
        md = []
        uttmd = TokenListMD(testtokens, md)
        newuttmds = getexpansions(uttmd)
        for newuttmd in newuttmds:
            print(newuttmd)

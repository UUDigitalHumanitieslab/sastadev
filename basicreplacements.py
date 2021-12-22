from collections import defaultdict
from metadata import bpl_word, bpl_node
from deregularise import correctinflection

pron = 'Pronunciation'
orth = 'Orthography'
infpron = 'Informal Pronunciation'
initdev = 'Initial Devoicing'
codared = 'Coda Reduction'
apomiss = 'Missing Apostrophe'
addschwa = 'Schwa addition'
onsetred = 'Onset Reduction'
d_er = 'd-onset on er'
spellerr = 'Spelling Error'
varpron = 'Alternative Pronunciation'
pronerr = 'Wrong Pronunciation'
contract = 'Contraction'
t_ie = 't-Insertion with ie'
fndrop = 'Final n drop'
zdev = 'Devoicing of /z/'
wrongpron = 'Wrong Prunciation'
phonrepl = '/{wrong}/ instead of /{correct}/'
wronginfl = 'Incorrect inflection'
morph = 'Morphology'
overgen = 'Overgeneralisation'

Rvzlist = ['aan', 'achter', 'achteraan', 'achterin', 'achterop', 'af', 'beneden', 'benevens', 'bij', 'binnen',
           'binnenuit', 'boven', 'bovenaan', 'bovenin', 'bovenop', 'buiten', 'dichtbij', 'door', 'doorheen', 'heen',
           'in', 'langs', 'langsheen', 'langszij', 'mede', 'mee', 'middendoor', 'na', 'naar', 'naartoe', 'naast',
           'nabij', 'neer', 'om', 'omheen', 'onder', 'onderaan', 'op', 'over', 'overheen', 'rond', 'rondom', 'tegen',
           'tegenaan', 'tegenin', 'tegenover', 'toe', 'tussen', 'tussenin', 'tusssen', 'uit', 'van', 'vanaf',
           'vandaan', 'vandoor', 'vanop', 'vanuit', 'vanwege', 'vlakbij', 'voor', 'vooraan', 'voorbij', 'zonder']

ervzvariants = [('der' + vz, 'er' + vz, pron, varpron, d_er) for vz in Rvzlist] + \
               [("d'r" + vz, 'er' + vz, pron, varpron, d_er) for vz in Rvzlist]

basicreplacementlist = [('as', 'als', pron, infpron, codared), ('isse', 'is', pron, infpron, addschwa),
                        ('ooke', 'ook', pron, infpron, addschwa),
                        ('t', "'t", orth, spellerr, apomiss), ('effjes', 'eventjes', pron, infpron, varpron),
                        ('effetjes', 'eventjes', pron, infpron, varpron),
                        ('effe', 'even', pron, infpron, varpron),
                        ('set', 'zet', pron, infpron, initdev), ('hie', 'hier', pron, pronerr, codared),
                        ('eers', 'eerst', pron, pronerr, codared),
                        ('nie', 'niet', pron, infpron, codared),
                        ('s', 'is', orth, spellerr, apomiss), ('ooke', 'ook', pron, infpron, addschwa),
                        ('it', 'dit', pron, pronerr, onsetred),
                        ('da', 'dat', pron, infpron, codared),
                        ('si', 'zit', pron, infpron, codared),  # and zdev
                        ('ieduleen', 'iedereen', pron, wrongpron, phonrepl.format(wrong='l', correct='r')),
                        ('allemaaw', 'allemaal', pron, wrongpron, phonrepl.format(wrong='w', correct='l')),
                        ('amaal', 'allemaal', pron, infpron, varpron),
                        ('wiw', 'wil', pron, wrongpron, phonrepl.format(wrong='w', correct='l')),
                        ('annug', 'ander', pron, wrongpron, phonrepl.format(wrong='nug', correct='der')),
                        ('nohug', 'nodig', pron, wrongpron, phonrepl.format(wrong='hu', correct='di')),
                        ('magge', 'mogen', morph, wronginfl, '{} & {}'.format(overgen, infpron)),
                        ('maggen', 'mogen', morph, wronginfl, overgen)
                        ] + ervzvariants
# ('inne', 'in', pron, infpron, addschwa) # put off because it b;ock inne -> in de


basicreplacements = defaultdict(list)
for w1, w2, c, n, v in basicreplacementlist:
    basicreplacements[w1].append((w2, c, n, v))

basicexpansionlist = [('innu', ['in', 'de'], pron, infpron, contract),
                      ('inne', ['in', 'de'], pron, infpron, contract),
                      ('dis', ['dit', 'is'], pron, infpron, contract),
                      ('das', ['dat', 'is'], pron, infpron, contract),
                      ('tis', ['dit', 'is'], pron, infpron, contract),
                      ('is-t-ie', ['is', 'ie'], pron, infpron, t_ie),
                      ('als-t-ie', ['als', 'ie'], pron, infpron, t_ie),
                      ('of-t-ie', ['of', 'ie'], pron, infpron, t_ie),
                      ('as-t-ie', ['als', 'ie'], pron, infpron, t_ie)]

basicexpansions = defaultdict(list)
for w1, w2, c, n, v in basicexpansionlist:
    basicexpansions[w1].append((w2, c, n, v))

knownreplacements = [
    ('ze', "z'n", pron, infpron, fndrop, bpl_word),
    ('desu', 'deze', pron, infpron, zdev, bpl_word),
    ('mij', 'mijn', pron, infpron, fndrop, bpl_word),

]

knownreplacementsdict = {(repl[0], repl[1]): repl for repl in knownreplacements}


def getmeta4CHATreplacements(wrongword, correctword):
    if (wrongword, correctword) in knownreplacementsdict:
        result = knownreplacementsdict[(wrongword, correctword)]
    else:
        nwms = correctinflection(wrongword)
        if nwms != []:
            for nw, metavalue in nwms:  # hier wordt overschreven als er meerdere resultaten zouden zijn
                if nw == correctword:
                    result = (wrongword, correctword, 'Morphology', 'InflectionError', metavalue, bpl_word)
        else:
            result = (wrongword, correctword, 'Lexicology', 'Lexical Error', 'Paralaly', bpl_word)
    return result


# keer removed
disambiguation_replacements = [(['huis', 'water', 'paard', 'werk', 'stuur', 'feest', 'snoep', 'geluid',
                                 'kwartet', 'kruis'], 'gas'),
                               (['toren', 'fiets', 'puzzel', 'boom', 'vis', 'melk', 'zon', 'pot', 'klok',
                                 'school', 'boer', 'lepel', 'jas', 'tuin', 'fles', 'lucht', 'emmer', 'maan', 'kachel',
                                 'kwak', 'verf', 'hop', 'kam', 'spiegel', 'klap', 'stal', 'lijm', 'lift', 'kat',
                                 'wagen', 'schep', 'kus', 'wind', 'borstel', 'duim', 'strik', 'klik', 'pleister',
                                 'stok', 'knoop', 'rits', 'knikker', 'put', 'boor', 'plons', 'beurt', 'toeter', 'poot',
                                 'punt', 'post', 'gom', 'tap', 'kraanwagen', 'drup', 'wieg', 'kriebel', 'pit', 'zaag',
                                 'slof', 'deuk', 'hark', 'jeuk', 'stift', 'aard', 'hamster', 'kiek', 'haak', 'schroef',
                                 'tape', 'vorm', 'klem', 'mot', 'druppel'], 'teil'),
                               (['bomen', 'kussen', 'kaarten', 'beesten', 'weken', 'huizen', 'apen', 'poten',
                                 'wieken', 'paarden', 'stoelen', 'ramen', 'strepen', 'planten', 'groeten',
                                 'flessen', 'boeren', 'punten', 'tranen'], 'teilen'),
                               (['snel', 'wit', 'kort', 'dicht'], 'mooi'),
                               (['witte'], 'mooie')
                               ]


def getdisambiguationdict():
    disambiguationdict = {}
    for ws, repl in disambiguation_replacements:
        for w in ws:
            disambiguationdict[w] = repl
    return disambiguationdict

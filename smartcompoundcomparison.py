'''

This module provides a function to determine whether an illegal word is to be considered as a compound,
based on its correction and the lemma of its correction
'''
import editdistance
from normalise_lemma import normaliselemma

def reldistance(word, corr):
    thedistance = editdistance.distance(word, corr)
    result = thedistance / max(len(word), len(corr))
    return result

def iscompound(word, corr, rawcorrlemma):
    debug = True
    corrlemma = normaliselemma(corr, rawcorrlemma)
    corrlemmaparts = corrlemma.split('_')
    if len(corrlemmaparts) == 1:
        return False
    corrlemmaprefixlist = corrlemmaparts[:-1]
    corrlemmaprefix = ''.join(corrlemmaprefixlist)
    lcorrlemmaprefix = len(corrlemmaprefix)
    corrdistance = editdistance.distance(word, corr)
    relcorrdistance = reldistance(word, corr)
    if corr[:lcorrlemmaprefix] == corrlemmaprefix:
        corrleft = corrlemmaprefix
        corright = corr[lcorrlemmaprefix:]


        corrleftdistance = editdistance.distance(word, corrleft)
        corrrightdistance = editdistance.distance(word, corright)

        relcorrleftdistance = reldistance(word, corrleft)
        relcorrrightdistance = reldistance(word, corright)

        result = relcorrleftdistance >= relcorrdistance and relcorrrightdistance >= relcorrdistance
    else:
        result = relcorrdistance <= 0.4
    if debug:
        print(word, corr, corrlemma, relcorrdistance, relcorrleftdistance, relcorrrightdistance)
        print(word, corr, corrlemma, corrdistance, corrleftdistance, corrrightdistance)
    return result

def main():
    testlist = [
                ('zingdoppe', 'zingdoppen', 'zingen_doppen', True),
                ('koekkok', 'koekoeksklok', 'koekoek_klok', True),
                ('chocomelluk', 'chocolademelk', 'chocolade_melk', True),
                ('zepezop', 'zeepsop', 'zeep_sop', True),
                ('verffinger', 'vingerverf', 'vinger_verf', True),
                ('welə', 'welles', 'wel_les', True),
                ('stape', 'stapelbed', 'stapel_bed', False),
                ('ingedoet', 'ingedaan', 'in_doen', True),
                ('sakhoue', 'vasthouden', 'vast_houden', True),
                ('opraaien', 'opdraaien', 'op_draaien', True),
                ('aardbeiijs', 'aardbeienijs', 'aardbei_ijs', True),
                ('ophouwe', 'ophouden', 'op_houden', True),
                ('voorlese', 'voorlezen', 'voor_lezen', True),
                ('slijbaan', 'glijbaan', 'glij_baan', True),
                ('zwatte+piet', 'Zwarte_Piet', 'Zwarte_Piet', True),
                ('innezette', 'inzetten', 'in_zetten', True),
                ('dichhouwe', 'dichthouden', 'dicht_houden', True),
                ('bijhouwen', 'bijhouden', 'bij_houden', True),
                ('ommedaaje', 'omdraaien', 'om_draaien', True),
                ('poplepel', 'pollepel', 'pol_lepel', True),
                ('ingedoet', 'ingedaan', 'in_doen', True),
                ('pokeepel', 'pollepel', 'pol_lepel', True),
                ('afdoje', 'afdrogen', 'af_drogen', True),
                ('affedoen', 'afdoen', 'af_doen', True),
                ('afdooje', 'afdrogen', 'af_drogen', True),
                ('vrastauto', 'vrachtauto', 'vracht_auto', True),
                ('slaapliets', 'slaapliedje', 'slaap_lied', True),
                ('vasthouwen', 'vasthouden', 'vast_houden', True),
                ('ophouwen', 'ophouden', 'op_houden', True),
                ('slinderjurk', 'vlinderjurk', 'vlinder_jurk', True),
                ('abbesap', 'appelsap', 'appel_sap', True),
                ('vloerplussel', 'vloerpuzzel', 'vloer_puzzel', True),
                ('bestesap', 'bessensap', 'bes_sap', True),
                ('Astepoester', 'Asseposter', 'Asse_poster', True),
                ('affesap', 'appelsap', 'appel_sap', True),
                ('risstengeltjes', 'rietstengeltjes', 'riet_steng', True),
                ('zeemepaardjes', 'zeemeerminpaardje', 'zeemeermin_paard', True),
                ('vasthouwe', 'vasthouden', 'vast_houden', True),
                ('sampejonnetje', 'lampionnetje', 'lampion_net', True),

                ]
    max = len(testlist)
    max = 5
    for word, corr, corrlemma, ref in testlist[:max]:
        result = iscompound(word, corr, corrlemma)
        if result != ref:
            print(f'{word}, {corr}, {corrlemma}: {result}/={ref}')


if __name__ == '__main__':
    main()
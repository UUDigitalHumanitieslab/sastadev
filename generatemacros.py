
tarsp_wvzexceptions = {('hebben', 'van'),  # hebben can occur with pc/van but only in fixed expressions: last hebben van, spijt hebben van
                       ('slaan', 'op'),  # of course correct but not used in this sense wiyth very young children
                       ('lukken', 'in'), \
                       ('passen', 'bij'), \
                       ('vallen', 'vanaf'),
                       # next list derived from CHILDES via Paqu
                       # query: https://paqu.let.rug.nl:8068/?db=childesdutch&word=&rel=pc&hword=&postag=vz&hpostag=ww&meta=&sn=10
                       # and manual filtering see file Tarsp_wrongpcs.txt in the lassy folder
                       ('af_brengen', 'vanaf'),
                       ('af_komen', 'op'),
                       ('af_komen', 'van'),
                       ('af_komen', 'vanaf'),
                       ('bouwen', 'op'),
                       ('dansen', 'op'),
                       ('doen', 'overheen'),
                       ('door_gaan', 'op'),
                       ('draaien', 'om'),
                       ('eten', 'van'),
                       ('gaan', 'aan'),
                       ('gaan', 'om'),
                       ('gaan', 'overheen'),
                       ('gaan', 'tussendoor'),
                       ('gaan', 'voor'),
                       ('hebben', 'af'),
                       ('hebben', 'uit'),
                       ('helpen', 'bij'),
                       ('houden', 'voor'),
                       ('komen', 'achteraan'),
                       ('komen', 'af'),
                       ('komen', 'bij'),
                       ('komen', 'doorheen'),
                       ('komen', 'om'),
                       ('komen', 'tot'),
                       ('krijgen', 'af'),
                       ('krijgen', 'op'),
                       ('kunnen', 'omheen'),
                       ('liggen', 'bij'),
                       ('mee_gaan', 'met'),
                       ('plakken', 'aan'),
                       ('rijden', 'op'),
                       ('sabbelen', 'op'),
                       ('spelen', 'in'),
                       ('staan', 'op'),
                       ('staan', 'voor'),
                       ('struikelen', 'over'),
                       ('tellen', 'tot'),
                       ('uit_komen', 'in'),
                       ('varen', 'op'),
                       ('vast_knopen', 'aan'),
                       ('zeggen', 'in '),
                       ('zien', 'op'),
                       ('zijn', 'tegen'),
                       ('zijn', 'voor'),
                       ('zitten', 'op'),
                       ('zitten', 'voor'),
                       ('zoeken', 'op')
                       }

# also do erin erbij etc

Rlemma = """( @lemma="er{vz}" or @lemma="daar{vz}" or @lemma="hier{vz}" ) """

Tarsp_WVz_exception_basemodel = """(@pt="ww"  and @rel ="hd" and @lemma="{ww}" and
     ../node[@rel="pc" and
            ( (node[@rel="hd" and @lemma="{vz}"]) or
                ( @lemma="er{rvz}" or @lemma="daar{rvz}" or @lemma="hier{rvz}" )
            )
            ]
 )"""

pc_vc_exception_basemodel = """( @rel="pc" and node[@rel = "hd" and @lemma="{vz}"] and ../node[@rel="hd" and @pt="ww" and @lemma="{ww}"] )"""

macrodef_model = '{name} = """{exp}"""\n'


def generatemacros():
    newmacros = {}
    newparts = []
    for (ww, vz) in tarsp_wvzexceptions:
        if vz == 'tot':
            rvz = 'toe'
            newpart = Tarsp_WVz_exception_basemodel.format(ww=ww, vz=rvz, rvz=rvz)  # voor : hij werkte er niet mee
            newparts.append(newpart)
        elif vz == 'met':
            rvz = 'mee'
            newpart = Tarsp_WVz_exception_basemodel.format(ww=ww, vz=rvz, rvz=rvz)  # voor : hij kwam er niet toe
            newparts.append(newpart)
        else:
            rvz = vz
        newpart = Tarsp_WVz_exception_basemodel.format(ww=ww, vz=vz, rvz=rvz)
        newparts.append(newpart)
    partsor = ' or '.join(newparts)
    newmacro = "( {} )".format(partsor)
    newmacros['Tarsp_WVz_exception'] = newmacro

    newparts = []
    for (ww, vz) in tarsp_wvzexceptions:
        newpart = pc_vc_exception_basemodel.format(ww=ww, vz=vz)
        newparts.append(newpart)
    partsor = ' or '.join(newparts)
    newmacro = "( {} )".format(partsor)
    newmacros['Tarsp_pc_vc_exception'] = newmacro
    return newmacros


def main():
    macros = generatemacros()
    for macroname in macros:
        macrodef = macrodef_model.format(name=macroname, exp=macros[macroname])
        print(macrodef)


if __name__ == '__main__':
    main()

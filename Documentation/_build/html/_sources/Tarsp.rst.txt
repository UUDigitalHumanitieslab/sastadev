TARSP Language Measures
-----------------------

We will describe here all Tarsp language measures, in the order of the identifiers assigned to them. However, a few language measures are special in that they are very often used in other language measures, as described in :ref:`TarspAnnotation`. This concerns in particular the following language measures:

* T007: B
* Ond
* VC
* W



T001: (Vr)WOnd+
^^^^^^^^^^^^^^^


* **Name**: (Vr)WOnd+.
* **Category**: Zinsconstructies
* **Subcat**: Vragen
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 60
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T003: 6+
^^^^^^^^


* **Name**: 6+.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Sz
* **Original**: yes
* **In form**: yes
* **Page**: 56
* **Implementation**: Python function
* **Query** defined as::

    sziplus6






T004: Aan/uit
^^^^^^^^^^^^^


* **Name**: Aan/uit.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 57;58
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T005: als
^^^^^^^^^


* **Name**: als.
* **Category**: Verbindingswoorden
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 77
* **Implementation**: Xpath 
* **Query** defined as::

    //node[@lemma="als" and @pt="vg"]


Straightforward Xpath expression for the conjunction *als*.

* **Schlichting** "'als' is het eerste verbindingswoord van de ondergeschikte zin. 'als' wordt hier ook gescoord wanneer de onderschikkende zonder hoofdzin gebruikt wordt.

Fully covered but it is unclear whether *als* as used in comparisons also should be included. All Schlichting's examples concern conditional *als*. So maybe this query should be restricted somewhat.



T006: Avn
^^^^^^^^^


* **Name**: Avn. (Aanwijzend Voornaamwoord als nomen)
* **Category**: Voornaamwoorden
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 79
* **Implementation**: Xpath
* **Query** defined as::

    //node[@pt="vnw"  and @vwtype="aanw" and @lemma!="hier" and @lemma!="daar" and @lemma!="er" and 
	@rel!="det" and (not(@positie) or @positie!="prenom") ]


* The query with pt equal to *vnw* and vwtype equal to *aanw* selects demonstrative pronouns, but
* these include R-pronouns, so they are explicitly excluded
* the relation must not be *det* (otherwise the pronouns are not used independently)
* and if a *position* attribute is present it should not have the value *prenom* (otherwise it is not used independently)

* **Schlichting**: "Aanwijzend Voornaamwoord: 'die', 'dit', 'deze', 'dat' zelfstandig gebruikt." fully covered.




T007: B
^^^^^^^


* **Name**: B. (Bijwoordelijke Bepaling)
* **Category**: Zinsdelen
* **Subcat**: 
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 42
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Tarsp_B%]
	
@@


* **Schlichting**: "De bijwoordelijke bepaling zegt iets over de hele inhoud van de zin of iets over het werkwoord, een bijwoord of een bijvoeglijk naamwoord. Een zin kan meer dan één bijwoordelijke bepaling hebben.



T010: BBBv
^^^^^^^^^^


* **Name**: BBBv. (Bijwoord + Bijwoord + Bijvoeglijk woord)
* **Category**: Woordgroepen
* **Subcat**: Ov
* **Level**: Wg
* **Original**: yes
* **In form**: no
* **Page**: 70
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@cat="ap" and
    node[@rel="mod" and (@cat="ap" or @cat="advp") and
        node[@rel="mod" or @rel="me" ] and
        node[@rel="hd" ] and count(.//node)=2] and
    node[@rel="hd" and @pt="adj"] and count(node) =2]






T011: Bbijzin
^^^^^^^^^^^^^


* **Name**: Bbijzin.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Sz
* **Original**: yes
* **In form**: yes
* **Page**: 57
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@rel="mod"and @cat="cp" and node[@rel="body" and node[@pt="ww" and @pvagr and @rel="hd"]]]






T012: BBv/B
^^^^^^^^^^^


* **Name**: BBv/B.
* **Category**: Woordgroepen
* **Subcat**: 
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 67
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[(node[@rel="mod" and %adjoradv%] and
       node[@rel="hd"  and %adjoradv%])     
   ]






T013: BBvZn
^^^^^^^^^^^


* **Name**: BBvZn.
* **Category**: Woordgroepen
* **Subcat**: Ov
* **Level**: Wg
* **Original**: yes
* **In form**: no
* **Page**: 70
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T014: BBX
^^^^^^^^^


* **Name**: BBX.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 50
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Tarsp_BBX%]






T015: BepBvZn
^^^^^^^^^^^^^


* **Name**: BepBvZn.
* **Category**: Woordgroepen
* **Subcat**: 
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 71
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@cat="np" and
    node[@rel="det" ] and
    node[@rel="mod" and @pt="adj"] and
    node[@rel="hd" and @pt="n"]]






T016: BepZnBv
^^^^^^^^^^^^^


* **Name**: BepZnBv.
* **Category**: Woordgroepen
* **Subcat**: Ov
* **Level**: Wg
* **Original**: yes
* **In form**: no
* **Page**: 70
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[(@cat="ap" or @cat="advp") and node[(@rel="mod" or @rel="me") and @cat="np"]]






T017: BezZn
^^^^^^^^^^^


* **Name**: BezZn.
* **Category**: Woordgroepen
* **Subcat**: 
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 68
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@cat="np" and
    node[@pdtype="det" and @rel="det" and @positie="prenom"  and @vwtype="bez" and @pt="vnw" ] and
    node[(@pt="n"  or (@pt="adj" and @positie="nom")) and @rel="hd"]]






T018: Bijvoeglijke Bijzin
^^^^^^^^^^^^^^^^^^^^^^^^^


* **Name**: Bijvoeglijke Bijzin.
* **Category**: 
* **Subcat**: 
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@rel="mod"and @cat="rel" and parent::node[node[@pt="n" and @rel="hd"]]]






T019: Bijwoordelijke bepalingwoordgroep
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


* **Name**: Bijwoordelijke bepalingwoordgroep.
* **Category**: Uitbreiding Zinsdelen
* **Subcat**: 
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 75
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T020: Bijzin z Verb
^^^^^^^^^^^^^^^^^^^


* **Name**: Bijzin z Verb.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 53;54
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T023: Bv/B
^^^^^^^^^^


* **Name**: Bv/B.
* **Category**: Eenwoordzin
* **Subcat**: 
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 40
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@cat="top" and node[@pt='adj' or @pt='bw' or @pt='vz'] and 
         count(.//node[%realnode%])=1]
  






T024: Bv z e
^^^^^^^^^^^^


* **Name**: Bv z e.
* **Category**: Woordstructuur
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 87;88
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T025: BvBepZn
^^^^^^^^^^^^^


* **Name**: BvBepZn.
* **Category**: Woordgroepen
* **Subcat**: 
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 69
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@cat="np" and node[@rel="det"] and node[@rel="mod" and @pt="bw" and (not(@special) or @special!="er")] and count(node)=3]






T027: BvZn
^^^^^^^^^^


* **Name**: BvZn.
* **Category**: Woordgroepen
* **Subcat**: 
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 66
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%BvZn%]






T029: BWondBB
^^^^^^^^^^^^^


* **Name**: BWondBB.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 53
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Tarsp_BWOndBB%]






T030: BX
^^^^^^^^


* **Name**: BX.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 46;47
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[(@cat="top" and not(.//node[%pv%]) and not(.//node[@lemma="niet"]) and not(.//node[@rel="dlink"]) and
       (
       (count(.//node[@cat="du" and count(node[%realnode%])=2  and node[%singlewordbw%] and node[(@pt or %corephrase%) ]])=1 ) or
	   (node[%bxnp1%]) or
	   (node[@cat="du" and count(node[%realnode%])=1 and node[%bxnp1%]]) or
	   (node[%bxnp2%]) or
	   (node[@cat="du" and count(node[%realnode%])=1 and node[%bxnp2%]])
       )) or %Tarsp_bnonfin%
	  ]






T031: C 
^^^^^^^^


* **Name**: C .
* **Category**: Zinsdelen
* **Subcat**: 
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 43;44
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T032: de
^^^^^^^^


* **Name**: de.
* **Category**: Woordgroepen
* **Subcat**: 
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 66
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@cat="np" and node[@rel="det" and @lemma="de"] and count(node)=2]






T033: die/dezeZn
^^^^^^^^^^^^^^^^


* **Name**: die/dezeZn.
* **Category**: Woordgroepen
* **Subcat**: 
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 68
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@cat="np" and node[@pt="n" and @rel="hd"] and node[@pt="vnw" and @vwtype="aanw" and @rel="det" and (@lemma="die" or @lemma="deze")] and count(node)=2]






T034: dit/datZn
^^^^^^^^^^^^^^^


* **Name**: dit/datZn.
* **Category**: Woordgroepen
* **Subcat**: 
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 71
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@cat="np" and node[@pt="n" and @rel="hd"] and node[@pt="vnw" and @vwtype="aanw" and @rel="det" and (@lemma="dit" or @lemma="dat")] and count(node)=2]






T035: een
^^^^^^^^^


* **Name**: een.
* **Category**: Woordgroepen
* **Subcat**: 
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 64
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[node[@lemma="een" and @pt="lid"] and node[@pt="n" and @rel="hd"] and count(node)=2 ]






T036: en
^^^^^^^^


* **Name**: en.
* **Category**: Verbindingswoorden
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 77
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@pt="vg" and @lemma="en" ]






T037: er
^^^^^^^^


* **Name**: er.
* **Category**: Voornaamwoorden
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 81
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@lemma="er"]






T038: geen X
^^^^^^^^^^^^


* **Name**: geen X.
* **Category**: Woordgroepen
* **Subcat**: 
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 72
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@cat="np" and
    node[@pt="vnw" and @rel="det" and @lemma="geen"] and
    node[@pt="n" and @rel="hd"]]






T039: hè
^^^^^^^^


* **Name**: hè.
* **Category**: Zinsconstructies
* **Subcat**: Vragen
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 59;60
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[ @lemma="hè"]






T040: hem
^^^^^^^^^


* **Name**: hem.
* **Category**: Voornaamwoorden
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 82
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@word="hem" and @pt="vnw"]






T041: het 
^^^^^^^^^^


* **Name**: het .
* **Category**: Voornaamwoorden
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 80
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@lemma="het" and @pt='vnw' ]






T042: hetZn
^^^^^^^^^^^


* **Name**: hetZn.
* **Category**: Woordgroepen
* **Subcat**: 
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 71
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@cat="np" and
    node[@pt="lid" and @rel="det" and @lemma="het"] and
    node[@rel="hd" and @pt="n"]]






T043: hij
^^^^^^^^^


* **Name**: hij.
* **Category**: Voornaamwoorden
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 80
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@lemma="hij" and @pt="vnw"]






T044: Hww i
^^^^^^^^^^^


* **Name**: Hww i.
* **Category**: Woordgroepen
* **Subcat**: 
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 65
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Tarsp_Hwwi%]






T045: Hww Vd
^^^^^^^^^^^^


* **Name**: Hww Vd.
* **Category**: Woordgroepen
* **Subcat**: 
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 69
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[(@pt="ww" and @rel="hd" and 
           (@lemma="hebben" or @lemma="worden" or @lemma="zijn") and
       parent::node[node[@rel="vc" and (@cat="ppart" or (@pt="ww" and @wvorm="vd"))]
       ]) or %robusthwwvd%]






T046: HwwZ
^^^^^^^^^^


* **Name**: HwwZ.
* **Category**: Woordstructuur
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 84;85
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Tarsp_HwwZ%]






T047: ik
^^^^^^^^


* **Name**: ik.
* **Category**: Voornaamwoorden
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 79
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@lemma="ik" ]






T048: Into
^^^^^^^^^^


* **Name**: Into.
* **Category**: Zinsconstructies
* **Subcat**: Vragen
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 59
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T049: Inv
^^^^^^^^^


* **Name**: Inv.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 50
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[(((@cat="sv1" and not(parent::node[@cat="whq"])) or
        (@cat="smain" )
       ) and 
      node[@pt="ww" and @rel="hd" and (not(@stype) or @stype!="imparative") ] and node[@rel="su" and number(@end)>../node[@rel="hd"]/@end]) or 
      %robustinversion%]






T050: jij
^^^^^^^^^


* **Name**: jij.
* **Category**: Voornaamwoorden
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 79
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@lemma="jij" or (@lemma="je"  and (@vwtype="pr" or @vwtype="pers") and (@rel="su" ))]






T051: jou
^^^^^^^^^


* **Name**: jou.
* **Category**: Voornaamwoorden
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 82
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[(@lemma="je" or @lemma="jou") and (@vwtype="pr" or @vwtype="pers") and (@rel="obj1" or @rel="obj2")]







T052: Kop
^^^^^^^^^


* **Name**: Kop.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 47;48
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Tarsp_Kop%]






T053: maar
^^^^^^^^^^


* **Name**: maar.
* **Category**: Verbindingswoorden
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 77
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@lemma="maar" and 
       ((@pt="vg") or
        (@pt="bw" and parent::node[@cat="smain"] and @begin=parent::node/@begin))
      ]






T054: Sv1
^^^^^^^^^


* **Name**: Sv1.
* **Category**: 
* **Subcat**: 
* **Level**: Zc
* **Original**: no
* **In form**: no
* **Page**: 
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@cat="sv1" and (@rel="--" or @rel="nucl")]






T055: Mededelende Zin
^^^^^^^^^^^^^^^^^^^^^


* **Name**: Mededelende Zin.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 44;45
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T056: mij
^^^^^^^^^


* **Name**: mij.
* **Category**: Voornaamwoorden
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 81
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[(@lemma="me" or @lemma="mij") and (@vwtype="pr" or @vwtype="pers")]







T057: MvTT
^^^^^^^^^^


* **Name**: MvTT.
* **Category**: Woordstructuur
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 87
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@pt="ww" and @pvagr="mv" and @pvtijd="tgw" ]






T058: MvZn
^^^^^^^^^^


* **Name**: MvZn.
* **Category**: Woordstructuur
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 83;84
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@pt = "n" and @getal="mv" ]






T059: Nabep
^^^^^^^^^^^


* **Name**: Nabep.
* **Category**: Woordgroepen
* **Subcat**: 
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 73
* **Implementation**: Xpath with macros
* **Query** defined as::

    // node[@rel="mod" and (not(@lemma) or (@lemma!="ook" and @lemma!="dan")) and parent::node[@cat="np" and node[@rel="hd" and @pt!="ww"]] and @begin >= ../node[@rel="hd"]/@end]






T060: Nevens
^^^^^^^^^^^^


* **Name**: Nevens.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Sz
* **Original**: yes
* **In form**: yes
* **Page**: 56
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[node[@rel="cnj" and (@cat="smain" or @cat="sv1")] and node[@rel="crd" ]]






T061: Nevenschikkende
^^^^^^^^^^^^^^^^^^^^^


* **Name**: Nevenschikkende.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 54
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T062: Ombep
^^^^^^^^^^^


* **Name**: Ombep.
* **Category**: Woordgroepen
* **Subcat**: 
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 74
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T063: Ond
^^^^^^^^^


* **Name**: Ond.
* **Category**: Zinsdelen
* **Subcat**: 
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 41
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@rel="su" and (@pt or @cat) or
       (@rel="mod" and @lemma="er" and ../node[@rel="su" and @begin>=../node[@rel="mod" and @lemma="er"]/@end]) or
       (@rel="mod" and @lemma="er" and ../node[@rel="su" and not(@pt) and not(@cat)])

]






T064: OndB
^^^^^^^^^^


* **Name**: OndB.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 45
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Tarsp_OndB%]






T065: OndBVC
^^^^^^^^^^^^


* **Name**: OndBVC.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 51
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Tarsp_OndBVC%]






T066: Onderbr
^^^^^^^^^^^^^


* **Name**: Onderbr.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 58
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T067: Onderschikkend: B
^^^^^^^^^^^^^^^^^^^^^^^


* **Name**: Onderschikkend: B.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 55;56
* **Implementation**: Xpath with macros
* **Query** defined as::

     @@to be added@@

    






T068: Onderschikkend: VC
^^^^^^^^^^^^^^^^^^^^^^^^


* **Name**: Onderschikkend: VC.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 55
* **Implementation**: Xpath with macros
* **Query** defined as::

    @@to be added@@
    






T069: Onderschikkende
^^^^^^^^^^^^^^^^^^^^^


* **Name**: Onderschikkende.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 54;55
* **Implementation**: Xpath with macros
* **Query** defined as::

   @@to be added@@

    






T070: Onderwerpswoordgroep
^^^^^^^^^^^^^^^^^^^^^^^^^^


* **Name**: Onderwerpswoordgroep.
* **Category**: Uitbreiding Zinsdelen
* **Subcat**: 
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 75
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@rel="su" and @cat]






T071: OndVC
^^^^^^^^^^^


* **Name**: OndVC.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 46
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Tarsp_OndVC%]






T072: OndW
^^^^^^^^^^


* **Name**: OndW.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 46
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Tarsp_OndW%]






T073: OndWB
^^^^^^^^^^^


* **Name**: OndWB.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 49
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Tarsp_OndWB%]






T074: OndWBB
^^^^^^^^^^^^


* **Name**: OndWBB.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 52
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Tarsp_OndWBB%]






T075: OndWBVC
^^^^^^^^^^^^^


* **Name**: OndWBVC.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 52
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Tarsp_OndWBVC%]






T076: OndWVC
^^^^^^^^^^^^


* **Name**: OndWVC.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 48
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Tarsp_OndWVC%]






T077: OndWVCVC(X)
^^^^^^^^^^^^^^^^^


* **Name**: OndWVCVC(X).
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 53
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Tarsp_OndWVCVCX%]






T078: Ov2
^^^^^^^^^


* **Name**: Ov2.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 48
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T079: Ov3
^^^^^^^^^


* **Name**: Ov3.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 51
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Tarsp_Ov3%]






T080: Ov7
^^^^^^^^^


* **Name**: Ov7.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 58
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T081: OvWg7
^^^^^^^^^^^


* **Name**: OvWg7.
* **Category**: Woordgroepen
* **Subcat**: 
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 74
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T082: OvVerb6
^^^^^^^^^^^^^


* **Name**: OvVerb6.
* **Category**: Verbindingswoorden
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 78
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T083: Ov4
^^^^^^^^^


* **Name**: Ov4.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 52
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Tarsp_Ov4%]






T084: Ov5
^^^^^^^^^


* **Name**: Ov5.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 53
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Tarsp_Ov5%]






T085: Overige
^^^^^^^^^^^^^


* **Name**: Overige.
* **Category**: Voornaamwoorden
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 82
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@lemma="alles"  or @lemma="niets" or @lemma="niks" or (@lemma="wat" and @vwtype= "onbep") or @lemma="u" or @lemma="ons"  or @lemma="zelf"]






T086: SamZn
^^^^^^^^^^^


* **Name**: SamZn.
* **Category**: Woordstructuur
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 86
* **Implementation**: Xpath with macros
* **Query** defined as::

    getcompounds

For words that do not occur in the Alpino lexicon, Alpino has a rule system to determine whether a string is a compound. So it correctly analyzes:

* *ponyautootje* (as a compound with the parts *pony* and *auto*, lemma = pony_auto)

The Alpino lexicon contains words that are compounds and many of these are explicitly marked as a compound. The lemma of such words contains an underscore between the parts of the compound. Examples:

* *teddybeer* ( lemma = *teddy_beer*)


Alpino leaves any affixes between the compounds out puts the lemmas of each part in the lemma:

* *aardbeienijs* (lemma = *aardbei_ijs*)
* *zonnepanelen* (lemma = *zon_paneel*)
* *grotemensenfeestje* (lemma = groot_mens_feest)

but there are various inconsistencies (as acknowledged by Gertjan van Noord), eg. the analysis of *kinderbadje*:

* *kinderbadje* (lemma = *kinder_bad*)

In this example not the lemma (*glijden*) but the actual form has been used:

* *glijbaan* (lemma = *glij_baan*)


If the first part is a diminutive, various strategies are followed by Alpino inconsistently:

* ijsjesverkoop (lemma = *ijsje_verkoop*)
* worstjeswinkel (lemma = *worst_DIM_winkel*)
* grapjespiet (lemma = *grap_DIM_piet*)

New versions of Alpino may treat these words differently.

However, not all words that are a compound are marked as such  in the Alpino lexicon (e.g. *tafelkleed*). Therefore we also use a list of compounds derived from CELEX.

The language measure T086 has been implemented by the Python function getcompounds from the compounds module, which has been described :ref:`here <getcompounds-label>`.
  





T087: Stam
^^^^^^^^^^


* **Name**: Stam.
* **Category**: Woordstructuur
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 86
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@pt="ww" and @pvtijd="tgw" and
        not(%Tarsp_kijkVU%) and
     not(%Tarsp_hww% or
     @lemma = "hebben" or
     @lemma = "worden" or
     @lemma = "zijn"   
     )
     and @pvagr="ev"  ]






T088: Stam+t
^^^^^^^^^^^^


* **Name**: Stam+t.
* **Category**: Woordstructuur
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 86
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@pt="ww" and @pvagr="met-t" and not(%Tarsp_hww% or
     @lemma = "hebben" or
     @lemma = "worden" or
     @lemma = "zijn"   
     ) ]






T089: Sz2+
^^^^^^^^^^


* **Name**: Sz2+.
* **Category**: 
* **Subcat**: 
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 
* **Implementation**: Xpath with macros
* **Query** defined as::

       //node[@cat="top" and count(.//node[@cat="smain" or @cat="cp" or @cat="whsub" or @cat="rel" or @cat="whrel"  or @cat="whq" or @cat="whsub" or 
                                       ( @cat="sv1" and not(parent::node[@cat="whq"]))
                             ]
                     )>=2]






T090: Sz3+
^^^^^^^^^^


* **Name**: Sz3+.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Sz
* **Original**: yes
* **In form**: yes
* **Page**: 57
* **Implementation**: Xpath with macros
* **Query** defined as::

       //node[@cat="top" and count(.//node[@cat="smain" or @cat="cp" or @cat="whsub" or @cat="rel" or @cat="whrel"  or @cat="whq" or @cat="whsub" or 
                                       ( @cat="sv1" and not(parent::node[@cat="whq"]))
                             ]
                     )>=3]






T091: V (lijdend)
^^^^^^^^^^^^^^^^^


* **Name**: V (lijdend).
* **Category**: Zinsdelen
* **Subcat**: 
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 42
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T092: V (meewerkend)
^^^^^^^^^^^^^^^^^^^^


* **Name**: V (meewerkend).
* **Category**: Zinsdelen
* **Subcat**: 
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 42;43
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T093: V (voorzetsel)
^^^^^^^^^^^^^^^^^^^^


* **Name**: V (voorzetsel).
* **Category**: Zinsdelen
* **Subcat**: 
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 43
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T094: V.U. Divers
^^^^^^^^^^^^^^^^^


* **Name**: V.U. Divers.
* **Category**: V.U.
* **Subcat**: 
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 37
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[ (@lemma!="ja" and @lemma!="nee" and @word!="xxx" and @lemma != "mama" and @word!="xx" and 
       ((@pt="tsw" and @lemma!="hè") or
        (@pt="tsw" and @lemma="hè" and @rel="tag" and number(@end)<=number(../node[@rel="nucl"]/@begin)) or
        ((@lemma="au" or @lemma="hoepla" or @lemma="dag" or @lemma="kijk" or @lemma="hap" or @lemma="aai" ) and
         (@rel="--" or @rel="sat" or @rel="tag"))  		 
		 ) )	or  %Tarsp_kijkVU%	 or %Tarsp_hehe%
          ]






T095: V.U. Soc. AangP
^^^^^^^^^^^^^^^^^^^^^


* **Name**: V.U. Soc. AangP.
* **Category**: V.U.
* **Subcat**: 
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 37;38
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@pt="n" and @word!="hè" and @word!="xxx"  and @word!="xx" and @rel="tag" ]






T096: V.U. Ster
^^^^^^^^^^^^^^^


* **Name**: V.U. Ster.
* **Category**: V.U.
* **Subcat**: 
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 38;39
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T150: V.U. Nee/ja
^^^^^^^^^^^^^^^^^


* **Name**: V.U. Nee/ja.
* **Category**: V.U.
* **Subcat**: 
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 38
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@lemma="ja" or @lemma="nee"]






T097: VC
^^^^^^^^


* **Name**: VC.
* **Category**: 
* **Subcat**: 
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%complement% and parent::node[(@cat="smain" or @cat="sv1" or @cat="ssub" or @cat="inf" or @cat="ppart") ]]






T098: Vcbijzin
^^^^^^^^^^^^^^


* **Name**: Vcbijzin.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Sz
* **Original**: yes
* **In form**: yes
* **Page**: 56;57
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[((@rel="vc" or @rel="su") and (@cat="cp" or @cat="whsub")) or %directerede_vcbijzin%]






T099: VCW
^^^^^^^^^


* **Name**: VCW.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 46
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T100: VCWOndBB
^^^^^^^^^^^^^^


* **Name**: VCWOndBB.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 52
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Tarsp_VCWOndBB%]






T101: VCWoordgroep
^^^^^^^^^^^^^^^^^^


* **Name**: VCWoordgroep.
* **Category**: Uitbreiding Zinsdelen
* **Subcat**: 
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 75
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@cat and ((@rel="obj1" or @rel="obj2" or @rel="pc" or @rel="predc" or @rel="ld" or (@rel="vc" and (@cat="cp" or @cat="whq" or @cat="whsub")) ) and parent::node[(@cat="smain" or @cat="sv1" or @cat="ssub" or @cat="inf" or @cat="ppart") ])]






T102: Verb Ov
^^^^^^^^^^^^^


* **Name**: Verb Ov.
* **Category**: 
* **Subcat**: 
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 78
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[((@pt="vg" and 
        (@lemma="dat" or @lemma="of" or @lemma="toen")
        ) or
       (@pt="vnw" and @vwtype="vb")) and
       parent::node[(@cat="whsub" or @cat="ssub" or @cat="rel" or @cat="cp" or @cat="whrel") and @rel!="nucl"]
      ]






T103: Vergr trap
^^^^^^^^^^^^^^^^


* **Name**: Vergr trap.
* **Category**: Woordstructuur
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 88
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T104: Verkl
^^^^^^^^^^^


* **Name**: Verkl.
* **Category**: Woordstructuur
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 83
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@pt="n" and @graad="dim"]






T105: Verl Tijd
^^^^^^^^^^^^^^^


* **Name**: Verl Tijd.
* **Category**: Woordstructuur
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 87
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[ @pvtijd="verl" and @pt="ww" and @wvorm="pv"]






T106: Vo/bij
^^^^^^^^^^^^


* **Name**: Vo/bij.
* **Category**: Woordgroepen
* **Subcat**: 
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 71
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[node[@pt="vz" and @rel="hd"] and 
            node[@rel="obj1" and 
                 ((@index and not(@pt or @cat)) or
                  (@end < ../node[@rel="hd"]/@begin)
                 )]]






T107: Vobij
^^^^^^^^^^^


* **Name**: Vobij.
* **Category**: Voornaamwoorden
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 80
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Vobij%]






T108: Volt dw
^^^^^^^^^^^^^


* **Name**: Volt dw.
* **Category**: Woordstructuur
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 85;86
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@pt="ww" and @wvorm="vd"]






T109: Voltd fg
^^^^^^^^^^^^^^


* **Name**: Voltd fg.
* **Category**: Woordstructuur
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 88
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T110: Vr
^^^^^^^^


* **Name**: Vr.
* **Category**: 
* **Subcat**: 
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[ @cat="whq"]






T111: Vr(XY)
^^^^^^^^^^^^


* **Name**: Vr(XY).
* **Category**: Zinsconstructies
* **Subcat**: Vragen
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 60
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Tarsp_VrXY%]






T112: Vr4
^^^^^^^^^


* **Name**: Vr4.
* **Category**: Zinsconstructies
* **Subcat**: Vragen
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 61
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Tarsp_Vr4%]






T113: Vr5+
^^^^^^^^^^


* **Name**: Vr5+.
* **Category**: Zinsconstructies
* **Subcat**: Vragen
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 61;62
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Tarsp_Vr5plus%]






T114: VzB
^^^^^^^^^


* **Name**: VzB.
* **Category**: Woordgroepen
* **Subcat**: 
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 72
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[node[@rel="hd" and @pt="vz"] and 
       node[@rel="obj1" and 
            ( (@pt="vz" or @pt="bw") or 
              (%Rpronoun% and @begin=../node[@rel="hd"]/@end)) ]]






T115: VzBepBvZn
^^^^^^^^^^^^^^^


* **Name**: VzBepBvZn.
* **Category**: Woordgroepen
* **Subcat**: 
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 74
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T116: VzBepZn
^^^^^^^^^^^^^


* **Name**: VzBepZn.
* **Category**: Woordgroepen
* **Subcat**: 
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 66;67
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@cat="pp" and node[ @rel="obj1" and node[@rel="det"] ]]






T117: VzN
^^^^^^^^^


* **Name**: VzN.
* **Category**: Woordgroepen
* **Subcat**: 
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 65
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Tarsp_VzN%]






T118: VzZnAz
^^^^^^^^^^^^


* **Name**: VzZnAz.
* **Category**: Woordgroepen
* **Subcat**: Ov
* **Level**: Wg
* **Original**: yes
* **In form**: no
* **Page**: 70
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T119: S1W
^^^^^^^^^


* **Name**: S1W.
* **Category**: Eenwoordzin
* **Subcat**: 
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 40;41
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@cat="top" and node[@pt='ww'] and count(node)=1]






T120: W
^^^^^^^


* **Name**: W.
* **Category**: Zinsdelen
* **Subcat**: 
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 41;42
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Tarsp_coreW%]






T121: W(X)
^^^^^^^^^^


* **Name**: W(X).
* **Category**: Zinsconstructies
* **Subcat**: Gebiedende Wijs
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 62
* **Implementation**: Xpath with macros
* **Query** defined as::

    wx






T122: PV-loos
^^^^^^^^^^^^^


* **Name**: PV-loos.
* **Category**: 
* **Subcat**: 
* **Level**: Zc
* **Original**: no
* **In form**: no
* **Page**: 
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@cat="top" and not(.//node[@pt="ww" and @pvagr])]






T123: waarschijnlijk fout geanalyseerde nevenschikking
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


* **Name**: waarschijnlijk fout geanalyseerde nevenschikking.
* **Category**: 
* **Subcat**: 
* **Level**: Zc
* **Original**: no
* **In form**: no
* **Page**: 
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T124: want
^^^^^^^^^^


* **Name**: want.
* **Category**: Verbindingswoorden
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 77;78
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@lemma="want" and @pt="vg"]






T125: WBVC
^^^^^^^^^^


* **Name**: WBVC.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 51
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Tarsp_WBVC%]






T126: Wdeel
^^^^^^^^^^^


* **Name**: Wdeel.
* **Category**: Woordgroepen
* **Subcat**: 
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 68
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@pt="ww" and contains(@lemma,"_") and @rel ="hd" and parent::node[node[@rel="svp"]]]






T127: Werkwoordswoordgroep
^^^^^^^^^^^^^^^^^^^^^^^^^^


* **Name**: Werkwoordswoordgroep.
* **Category**: Uitbreiding Zinsdelen
* **Subcat**: 
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 75
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@pt="ww" and @rel="hd"  and parent::node[node[ @rel="vc" and (@cat="inf" or @cat="ppart")]]]






T128: wij
^^^^^^^^^


* **Name**: wij.
* **Category**: Voornaamwoorden
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 81
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@lemma="wij" or @lemma="we" ]






T129: Wond(X)
^^^^^^^^^^^^^


* **Name**: Wond(X).
* **Category**: Zinsconstructies
* **Subcat**: Vragen
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 60
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Tarsp_WOndX%]






T130: WOnd4
^^^^^^^^^^^


* **Name**: WOnd4.
* **Category**: Zinsconstructies
* **Subcat**: Vragen
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 61
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Tarsp_WOnd4%]






T131: WOnd5+
^^^^^^^^^^^^


* **Name**: WOnd5+.
* **Category**: Zinsconstructies
* **Subcat**: Vragen
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 61
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Tarsp_WOnd5plus%]






T132: woordgroep(onderstrepen)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


* **Name**: woordgroep(onderstrepen).
* **Category**: Zinsdelen
* **Subcat**: 
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 44
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[(@cat="ap" or @cat="advp" or @cat="np" or @cat="pp" or 
       node[@rel="vc" and (@cat="inf" or @cat="ppart")]) and parent::node[count(node[@cat or @pt!="let"])>1]]






T133: WVz
^^^^^^^^^


* **Name**: WVz.
* **Category**: Woordgroepen
* **Subcat**: 
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 72;73
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[node[@pt="ww"  and @rel ="hd"] and node[@rel="pc" and not(%Tarsp_B%)]]






T134: WW
^^^^^^^^


* **Name**: WW.
* **Category**: Woordgroepen
* **Subcat**: 
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 73
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T135: WXY
^^^^^^^^^


* **Name**: WXY.
* **Category**: Zinsconstructies
* **Subcat**: Gebiedende Wijs
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 63
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%wxy%]






T136: WXYZ
^^^^^^^^^^


* **Name**: WXYZ.
* **Category**: Zinsconstructies
* **Subcat**: Gebiedende Wijs
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 63
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%wxyz%]






T137: WXYZ5*
^^^^^^^^^^^^


* **Name**: WXYZ5*.
* **Category**: Zinsconstructies
* **Subcat**: Gebiedende Wijs
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 63
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%wxyz5%]






T138: X en X (en X)
^^^^^^^^^^^^^^^^^^^


* **Name**: X en X (en X).
* **Category**: Woordgroepen
* **Subcat**: 
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 72
* **Implementation**: Xpath with macros
* **Query** defined as::

    xenx






T139: X(W)deel
^^^^^^^^^^^^^^


* **Name**: X(W)deel.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 48;49
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T140: Xneg
^^^^^^^^^^


* **Name**: Xneg.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 49;50
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[(@rel='--' or @rel="nucl") and count(node) = 2 and node[ @lemma!="niet"] and 
       (node[@lemma="niet" ] or 
	    node[@cat="advp" and node[@lemma="niet"] ]
	   )
	  ]






T141: XY(W)deel
^^^^^^^^^^^^^^^


* **Name**: XY(W)deel.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 51
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T142: ze
^^^^^^^^


* **Name**: ze.
* **Category**: Voornaamwoorden
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 80;81
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[ @getal="mv"  and (@persoon="3p" or @persoon="3")  and @vwtype="pers" and @pdtype="pron" and @pt="vnw"]






T143: zelf
^^^^^^^^^^


* **Name**: zelf.
* **Category**: Voornaamwoorden
* **Subcat**: Ov
* **Level**: VVW
* **Original**: yes
* **In form**: no
* **Page**: 
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T144: zij
^^^^^^^^^


* **Name**: zij.
* **Category**: Voornaamwoorden
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 82
* **Implementation**: Xpath with macros
* **Query** defined as::

    
        //node[@pt="vnw"  and @vwtype="pers" and @getal="ev" and @genus="fem"   and @pdtype="pron"]







T145: Zn
^^^^^^^^


* **Name**: Zn.
* **Category**: Eenwoordzin
* **Subcat**: 
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 40
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@cat="top" and 
      (node[@pt="n" or (@pt="tw" and @numtype="hoofd") or (@lemma="paar" and @pt="lid")] or 
       node[@cat="du" and node[@pt="n" or (@pt="tw" and @numtype="hoofd") or (@lemma="paar" and @pt="lid")]]) and 
      count(.//node[%realnode%])=1]






T147: ZnZn
^^^^^^^^^^


* **Name**: ZnZn.
* **Category**: Woordgroepen
* **Subcat**: 
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 69
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@cat="top" and .//node[node[@pt="n" and @rel="hd"] and node[@pt="n" and not(@rel="hd")] ] or
          node[@cat="du" and count(node[@rel="dp" and @pt="n"])>=2]
          ]






T148: Znx
^^^^^^^^^


* **Name**: Znx.
* **Category**: Woordgroepen
* **Subcat**: 
* **Level**: Wg
* **Original**: yes
* **In form**: no
* **Page**: 40
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T151: V.U. Totaal
^^^^^^^^^^^^^^^^^


* **Name**: V.U. Totaal.
* **Category**: Aggregate
* **Subcat**: 
* **Level**: 
* **Original**: yes
* **In form**: yes
* **Page**: 39
* **Implementation**: Xpath with macros
* **Query** defined as::

    vutotaal






T152: G Totaal
^^^^^^^^^^^^^^


* **Name**: G Totaal.
* **Category**: Aggregate
* **Subcat**: 
* **Level**: 
* **Original**: yes
* **In form**: yes
* **Page**: 20
* **Implementation**: Xpath with macros
* **Query** defined as::

    gtotaal






T153: G.O Fase
^^^^^^^^^^^^^^


* **Name**: G.O Fase.
* **Category**: Aggregate
* **Subcat**: 
* **Level**: 
* **Original**: yes
* **In form**: yes
* **Page**: 20
* **Implementation**: Xpath with macros
* **Query** defined as::

    gofase






T154: PFII
^^^^^^^^^^


* **Name**: PFII.
* **Category**: Aggregate
* **Subcat**: 
* **Level**: 
* **Original**: yes
* **In form**: yes
* **Page**: 23
* **Implementation**: Xpath with macros
* **Query** defined as::

    pf2






T155: PFIII
^^^^^^^^^^^


* **Name**: PFIII.
* **Category**: Aggregate
* **Subcat**: 
* **Level**: 
* **Original**: yes
* **In form**: yes
* **Page**: 23
* **Implementation**: Xpath with macros
* **Query** defined as::

    pf3






T156: OvZnBv4
^^^^^^^^^^^^^


* **Name**: OvZnBv4.
* **Category**: Woordgroepen
* **Subcat**: 
* **Level**: WG
* **Original**: yes
* **In form**: yes
* **Page**: 69
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

    






T157: Screening
^^^^^^^^^^^^^^^


* **Name**: Screening.
* **Category**: Aggregate
* **Subcat**: 
* **Level**: 
* **Original**: no
* **In form**: no
* **Page**: 94
* **Implementation**: Xpath with macros
* **Query** defined as::

    tarsp_screening






T158: PFIV
^^^^^^^^^^


* **Name**: PFIV.
* **Category**: Aggregate
* **Subcat**: 
* **Level**: 
* **Original**: yes
* **In form**: yes
* **Page**: 23
* **Implementation**: Xpath with macros
* **Query** defined as::

    pf4






T159: PFV
^^^^^^^^^


* **Name**: PFV.
* **Category**: Aggregate
* **Subcat**: 
* **Level**: 
* **Original**: yes
* **In form**: yes
* **Page**: 23
* **Implementation**: Xpath with macros
* **Query** defined as::

    pf5






T160: PFVI
^^^^^^^^^^


* **Name**: PFVI.
* **Category**: Aggregate
* **Subcat**: 
* **Level**: 
* **Original**: yes
* **In form**: yes
* **Page**: 23
* **Implementation**: Xpath with macros
* **Query** defined as::

    pf6






T161: PFVII
^^^^^^^^^^^


* **Name**: PFVII.
* **Category**: Aggregate
* **Subcat**: 
* **Level**: 
* **Original**: yes
* **In form**: yes
* **Page**: 23
* **Implementation**: Xpath with macros
* **Query** defined as::

    pf7






T162: PF
^^^^^^^^


* **Name**: PF.
* **Category**: Aggregate
* **Subcat**: 
* **Level**: 
* **Original**: yes
* **In form**: yes
* **Page**: 23
* **Implementation**: Xpath with macros
* **Query** defined as::

    pf






T165: Formulier
^^^^^^^^^^^^^^^


* **Name**: Formulier.
* **Category**: Forms
* **Subcat**: 
* **Level**: 
* **Original**: yes
* **In form**: yes
* **Page**: 
* **Implementation**: Xpath with macros
* **Query** defined as::

    mktarspform






















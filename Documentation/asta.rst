.. _ASTA:

ASTA Language Measures
======================

.. _A001_A:

A001: A
-------------

* **Name**: A
* **Level**: Taalmaat
* **Original**: yes
* **In Form**: yes
* **Page**: nw p. 36
* **Implementation**: Xpath with macros
* **Query** defined as::

   //node[%asta_adj%]


This is not a language measure according to the original definition of ASTA. It has been introduced by [Boxum et al. 2019]. It should be modified so that it does not count for ASTAbasic but does count for ASTAextended.

The macro **asta_adj** is defined as follows::

    asta_adj = """
    (%ASTA_geboren% or
     %attributive_adj% or
     %attributive_adjinadjp% or
     %rangtw% or
     %substantivisedadj% or
     %substantivisedrangtw% or
     %attributive_pastp% or
     %attributive_presp% or
     %simplepredicative_adj% or
     %simplepredicative_adjinadjp% or
     %indefdet%
    )
    """

It joins a lot of macros als alternatives (joined by *or*). We will discuss each of them:

* **ASTA_geboren**. According to ASTA, the word *geboren* must be considered an adjective ("Alle vormen van geboren en geleden worden gezien als bijvoeglijk naamwoord in combinatie met een koppelwerkwoorden", [ASTA Appendix, p. 3]). The consensus is that it is a verb despite the absence of other forms, and Alpino analyses it as a verb . So, special measures are needed to identify *geboren* as an adjective. The macro **ASTA_geboren** is defined very simple, as follows::

        ASTA_geboren = """ (@word="geboren") """

  * **Remark** We  do not cover *geleden* yet, which Alpino analyses as an adverb (*bw*).

* **attributive_adj**: for bare attributive adjectives. The macro is defined as follows::


        attributive_adj = """
            (@pt="adj" and
             (@rel="mod" and
              parent::node[@cat="np"] and
              ../node[@rel="hd" and (@pt="n" or @pt="vnw" or @cat="mwu")] and
              (not(@begin < ../node[@rel="det" and (@pt="lid" or @pt="vnw")]/@begin) or @lemma='heel' or @lemma='geheel')
             )
            )
        """

  It requires that a node is an *adjective*, with relation *mod*, inside an *NP* that has a *noun*, *vnw*, or *mwu* head. It must not precede a determiner unless it is *heel* or *geheel* .

  * **Remark** We must check why only *heel* and *geheel* can precede a determiner. Possibly to exclude *al* (*al het water*)? but indefinite pronouns should be included

* **attributive_adjinadjp**: for adjectives in attributively used *AP*'s. It is defined as::

        attributive_adjinadjp = """
           (@pt="adj" and
            (@rel="hd" and
             parent::node[@cat="ap" and parent::node[@cat="np"] and
             ../node[@rel="hd" and (@pt="n" or @pt="vnw" or @cat="mwu")]]
             )
            )
        """

  It is analogous to the **attributive_adj** macro, though now the adjective is the head in an *ap* that modifies a nominal element.

  * **Remark** The condition on the relation (*mod*) is lacking here.

* **rangtw**: Cardinal numerals count as an adjective. The macro is defined as follows::

        rangtw = """
           (@pt="tw" and @numtype="rang")
        """

* **substantivisedadj** A substantivised adjective counts as an adjective. The macro definition is self-explanatory::

        substantivisedadj = """
           (@pt="adj" and @rel="hd" and parent::node[@cat="np"])
        """

* **substantivisedrangtw**. A substantivised ordinal numeral also counts as an adjective. The macro definition is uses the attribute *positie* to determine the substantivised nature of the numeral::

        substantivisedrangtw = """
            (%rangtw% and @positie = "nom" )
        """


* **attributive_pastp** for attributively used past participles. The macro definition is self-explanatory::

        attributive_pastp = """
           (@pt="ww" and @wvorm="vd" and @rel="mod" and parent::node[@cat="np"])
        """

* **attributive_presp** for attributively used present participles. The macro definition is self-explanatory::

        attributive_presp = """
           (@pt="ww" and @wvorm="od" and @rel="mod" and parent::node[@cat="np"])
        """

* **simplepredicative_adj** for predicatively used adjectives. The macro definition is self-explanatory, but uses several other macros::

        simplepredicative_adj = """
             (@pt="adj" and %simplepredicative%)    """
        simplepredicative = """ (%predicative% and ../node[%ASTA_basickopww%])"""
        predicative = """ (@rel="predc" or @rel="predm" ) """

  The macro **basickopww** is defined as follows::

        ASTA_basickopww = """ (@pt="ww" and @rel="hd" and
                               @lemma!="uit_zien" and @lemma!="heten" and @lemma!="gaan" and @lemma!="zitten" and
                                 (contains(@frame, "copula") or not(@stype="topic_drop")) and
                               parent::node[node[@rel="predc"] and
                               not(node[@rel="obj1"]) ] )"""

  It requires:
    * the node to be verb
    * but not any of *uit_zien*, *heten*,  *gaan* or *zitten*
    * that contains a copula frame or it does not contain the value *topic_drop* for the attribute *stype*
    * that has a *predc* sibling
    * but not an *obj1* sibling

* **simplepredicative_adjinadjp**. for adjectives as a head of a predicative *AP*. The definition of the macro is self-explanatory::

        simplepredicative_adjinadjp = """
             (@pt="adj" and @rel="hd" and parent::node[@cat="ap" and %simplepredicative%])
        """

* **indefdet** for indefinite pronouns with grammatical relation *det*::

        indefdet = """ (@rel="det" and @pt="vnw" and @vwtype="onbep")"""



* **Nieuwe maten**: "De uitgevoerde groepsvergelijkingen met de nieuwe maten tonen aan dat mensen met afasie significant afwijkend scoren op de maten [...] en ‘aantal bijvoeglijke naamwoorden’ ten opzichte van de controlegroep."


.. _A002_Aantal_Uitingen:

A002: Aantal Uitingen
---------------------------

* **Name**: Aantal Uitingen
* **Level**: Taalmaat
* **Original**: yes
* **In Form**: yes
* **Page**: 10-11
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A003_BIJZIN:

A003: BIJZIN
------------------

* **Name**: BIJZIN
* **Level**: Taalmaat
* **Original**: yes
* **In Form**: yes
* **Page**: 12
* **Implementation**: Python function
* **Query** defined as::

   asta_bijzin


.. autofunction:: asta_queries::asta_bijzin

The macro *ASTA_bijzin* is defined as follows::

    ASTA_Bijzin = """
	 (
			 ((@cat="ssub" and @rel="cnj" and not(%firstssubconjunct%) and not(%ASTA_CBijzinzin%)) or
			  (@cat="whrel" or @cat="rel" or @cat="whsub") or
			  ((@cat="smain" or @cat="sv1")and @rel="--") or
			  (@cat="cp" and node[@cat="ssub" or @cat="conj"])	or
			  (@cat="sv1" and (@rel="mod" or @rel="cnj") ) or
			  (@cat="smain" and (@rel="cnj" or @rel="body" or @rel="nucl" or @rel="dp") and
			    not(%ASTA_CBijzinzin%)) or
			  (@cat="oti") or
			   %ASTA_CBijzin% or
			   %directerede_vcbijzin% or
			   (@pt="vg" and @conjtype="onder" and @rel="--"  ) or
			   ((@pt="bw" or @pt="vnw") and @rel="vc" and @wh="ywh")
			  )

	 )
	"""

Many subcases are distinguished:

* **ssub** if it has relation *cnj* but is not the first ssub conjunct (the *cp* dominating it will count in that case):

  * dus in allerlei afleiding of allerlei opleidingen die op verschillende manieren uh ertoe bijdragen dat je een verhoor goed kunt vastleggen  uh **en kunt**  uh **voeren**

  It should also not meet the requirements of the macro *ASTA_CBijzinzin*. This macro finds clauses introduced by the words *maar*, *want* and *dus*, and require special treatment (see below).


* **relative clauses** and **subordinate wh-questions** count as *bijzin*:

  * het gaat hier over de mensen **die opgeleid worden** om uhm les
  * **wat jij deed** uh deed jij iets met cijfers
  * Kunt u mij vertellen **wat er met jou is gebeurd** ?

* **Main clauses** with cat equal to *smain*  or *sv1*, and with relation *--*:

  * **Het is vlak bij winkelcentrum**
  * **weet ik niet**

  Most of these will be discarded if they are the leftmost *bijzin* in the function *asta_bijzin*


* **subordinate clauses introduced by a conjunction** (*cp*) if they contain an *ssub* or coordinated structure (*conj*) as a child, e.g.

  * en sindsdien weet ik niks van **tot ik** uh **bijkwam** hierzo
  * en uh **als er problemen zijn** kan een klant ook bij mij komen
  * dus in allerlei afleiding of allerlei opleidingen die op verschillende manieren uh ertoe bijdragen **dat je een verhoor goed kunt vastleggen**  uh en kunt  uh voeren

  **Remark** the *conj* case allows too much, e.g.:

  * niemand **behalve mijn zusje en mijn vader**


* **adverbial or conjunct** *sv1*:

  * oke je was aan het tennissen en **ben je toen gevallen** ?

* **smain with relation cnj, body, nucl, or dp**:

  * en **dat was de slokdarm** (*nucl*)
  * oke **je was aan het tennissen**  en ben je toen gevallen ? (*cnj*)
  * **ik heb veel**  euh **meer**  weet ik niet (*dp*)
  * nou en toen ben ik nou ja toen was het voor mij goed in de zin van **ik wist** nou ja er is heel hulp (*body*)

* **om-te infinitives**

  * omdat het dat gedeelte was niet stevig genoeg **om overheen te lopen**

* Clauses introduced by **maar**, **want** or **dus** such as:

  * mijn moeder is toen overleden *maar mijn vader was ook ziek*
  * uh bij uh ja dat is ook heel moeilijk **want dat is ook gewoon** euh ja
  * Ik voel me niet zo lekker dus blijf ik thuis

  are dealt with by the macro *ASTA_CBijzin*. The words *want* and *maar* require a special treatment because these words should be marked, not the clause that they introduce (as with other coordinations). And *dus* is, in the relevant cases, a modifying adverb in an *smain* clause ::

	ASTA_CBijzin = """
         (%ASTA_wantmaarbijzin% or
		  %ASTA_dusbijzin%)
	"""


  The definitions of *ASTA_wantmaarbijzin* and *ASTA_dusbijzin* are as follows::

	ASTA_wantmaarbijzin = """
	   ((@word="want" or @word="maar") and @rel="crd" and @pt="vg" and
		../node[((@cat="smain" or @cat="ssub" or (@cat="du" and node[@cat="smain" and @rel="nucl"]))) and
		@begin  >=../node[(@word="want" or @word="maar")]/@end]
	   )
	"""

	ASTA_dusbijzin = """
	(@lemma="dus" and parent::node[@cat="smain"] and  @begin=parent::node/@begin and @pt="bw" and @rel="mod")
	"""

  Note that these macros (when used inside //node[ .. ]) yield the nodes for the words *maar*, *want* and *dus*. In order to find the **clauses** introduced by them, one should use the macro *ASTA_CBijzinzin*, which uses the macros *ASTA_wantmaarbijzinzin* and *ASTA_dusbijzinzin*::

	ASTA_CBijzinzin = """
	( %ASTA_wantmaarbijzinzin% or
	  %ASTA_dusbijzinzin%
	)
	"""


	ASTA_wantmaarbijzinzin = """
		   ( (@cat="smain" or @cat= "ssub" or (@cat="du" and node[@cat="smain" and @rel="nucl"])) and
			 ../node[(@word="want" or @word="maar") and @rel="crd" and @pt="vg"] and
			 @begin  >=../node[(@word="want" or @word="maar")]/@end
		   )
	"""

	ASTA_dusbijzinzin = """
	(@cat="smain" and node[@lemma="dus"  and  @begin=parent::node/@begin and @pt="bw" and @rel="mod"])
	"""



* **Direct speech** (Directe rede) is dealt with by the macro *directerede_vcbijzin*, which identifies a main clause  immediately preceded or followed by a main clause (*smain*, or *sv1*, resp.) with a metaverb (verb of saying) as its head::

	directerede_vcbijzin = """( %clausecat% and not(@rel="cnj") and
	                           (preceding-sibling::node[%metasmain%] or
							    following-sibling::node[%metasv1%])
							  )"""


	clausecat = """(@cat="smain" or @cat="whq" or %baresv1% )"""
	metaverb = """(@lemma="zeggen" or @lemma="denken" or @lemma="vinden"
	              or @lemma="vragen" or @lemma="schreeuwen" or @lemma="fluisteren" )"""
	metasmain = """(@cat="smain" and not(@rel="cnj") and node[@rel="hd" and %metaverb%]) """
	metasv1 = """(@cat="sv1" and not(@rel="cnj") and node[@rel="hd" and %metaverb%]) """

	baresv1 = """( @cat="sv1" and not(parent::node[(@cat="whq" or @cat="whrel")]))"""


  **Remark** The use of *preceding-sibling* and *following-sibling* may work here but is strictly spoken not correct. The order should be taken care of by *begin* and *end* attributes.


* **Wrongly parsed subordinate conjunctions**, as in:

  * bij de opleiding was ik 5 of zo **toen**  ik de op op opleiding heb gedaan voor uh voor uh hui BEROEP2
  * dan kun je er ook tijdig bij zijn **zodat** ze hun uh


* **wh-words with relation** *vc* (possibly wrongly parsed):

  * ik weet niet **hoe** ik bij thuis ben gekomen (parsed as: *ik weet niet hoe*, plus *ik bij thuis ben gekomen*)



**Handleiding**

* Het voegwoord /dus/: hierbij geldt de volgende afspraak:

  * *Dus* markeert een nieuwe uiting als de woordvolgorde na /dus/ die van een hoofdzin is (**dealt with correctly, though SASTA marks no new utterances**):

    * Ik voel me niet zo lekker dus ik blijf thuis = 2 uitingen

  * *Dus* markeert het begin van een bijzin als de woordvolgorde na /dus/ die van een bijzin is (**Covered**):

    * Ik voel me niet zo lekker dus blijf ik thuis = 1 uiting met een bijzin

* Let op: een beknopte bijzin is geen bijzin. Daarom wordt deze niet meegeteld bij de bijzinnen (**covered**)
* Bijzin: Een zinsdeel of zinsdeelstuk dat zelf weer een zin is. Voorbeeld:

  * *dat het gaat vriezen*, is nu wel duidelijk.


.. _A004_g:

A004: g
-------------

* **Name**: g  (goed, correct)
* **Level**: Taalmaat
* **Original**: yes
* **In Form**: yes
* **Page**: 11
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A005_f:

A005: f
-------------

* **Name**: f  (fout, incorrect)
* **Level**: Taalmaat
* **Original**: yes
* **In Form**: yes
* **Page**: 11
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A006_ell:

A006: ell
---------------

* **Name**: ell  (ellips)
* **Level**: Grammaticale fout
* **Original**: yes
* **In Form**: yes
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A007_Finietheidsindex:

A007: Finietheidsindex
----------------------------

* **Name**: Finietheidsindex
* **Level**: Taalmaat
* **Original**: yes
* **In Form**: yes
* **Page**: 11
* **Implementation**:
* **Query** defined as:


This has been implemented in a function used in the creation of the ASTA form.





.. _A008_FONPAR:

A008: FONPAR
------------------

* **Name**: FONPAR
* **Level**: Taalmaat
* **Original**: yes
* **In Form**: yes
* **Page**:
* **Implementation**: Python function
* **Query** defined as::

   phonpar


.. autofunction:: ASTApostfunctions::phonpar


.. _A009_DEL_PV:

A009: DEL PV
------------------

* **Name**: DEL PV
* **Level**: Grammaticale fout
* **Original**: yes
* **In Form**: yes
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

   asta_delpv





.. _A010_geexcludeerde_woorden:

A010: geexcludeerde woorden
---------------------------------

* **Name**: geexcludeerde woorden
* **Level**: SampleGrootte
* **Original**: yes
* **In Form**: yes
* **Page**: new:36
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A011_Herhaling:

A011: Herhaling
---------------------

* **Name**: Herhaling
* **Level**: MLU
* **Original**: yes
* **In Form**: yes
* **Page**: 7
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A012_Interjecties:

A012: Interjecties
------------------------

* **Name**: Interjecties
* **Level**: SampleGrootte
* **Original**: yes
* **In Form**: yes
* **Page**: 8
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A013_K:

A013: K
-------------

* **Name**: K
* **Level**: Taalmaat
* **Original**: yes
* **In Form**: yes
* **Page**: new:36
* **Implementation**: Xpath with macros
* **Query** defined as::

   //node[%ASTA_kopww%]

The macro *ASTA_kopww* is defined as follows::

    ASTA_kopww = """ ( %ASTA_basickopww% or %ASTA_geboren_kopww% )"""

It uses two macros. The macro *ASTA_basickopww* is defined as follows::

    ASTA_basickopww = """ (@pt="ww" and @rel="hd" and
                           @lemma!="uit_zien" and @lemma!="heten" and @lemma!="gaan" and @lemma!="zitten" and
                           (contains(@frame, "copula") or not(@stype="topic_drop")) and
                           parent::node[node[@rel="predc"] and not(node[@rel="obj1"]) ] )"""

This defines copulas as verbs other than a few listed exceptions that have a *predc* sibling but not an *obj1* sibling and  either  have the string *copula* in their *frame* attribute, or the value of the attribute *stype* is not equal to *topic_drop*.  The condition on the *stype* attribute is needed to exclude analysing a verb as *vind* as a copula as in *vind ik goed*, with a topic-dropped direct object.

The macro *ASTA_geboren_kopww* is needed because *geboren* is considered an adjective in ASTA, so the verbs *zijn* or *worden* that *geboren* is a dependent of should also be analysed as a copula and not as an auxiliary verb::

    ASTA_geboren_kopww = """

    (@rel="hd" and @pt="ww" and (@lemma="zijn" or @lemma="worden") and
             (../node[@cat="ppart" and @rel="vc" and node[ @word="geboren" and @rel="hd"]] or
              ../node[@rel="vc" and @word="geboren"]
             )
    )
        """

**Remark**: the condition should be reformulated with *@lemma="geboren"* instead of *@word="geboren"* to deal properly with case variants.


**Handleiding**
  * /zijn/, /worden/, /blijven/, /blijken/, /lijken/ /schijnen/, /heten/, /dunken/ en /voorkomen/ als koppelwerkwoord tellen met in acht neming van de regels. (Zie E-ANS : www.ans.ruhosting.nl voor de uitleg wanneer deze woorden daadwerkelijk koppelwerkwoorden zijn).  (**covered** except for *heten*, which has been excluded because all sample annotate it as a lexical verb, and  Elsbeth and Nina conformed that they consider it a lexical verb).
  * Houd er rekening mee dat ook andere werkwoorden zich soms kunnen gedragen als een koppelwerkwoord ( ze zijn dan te vervangen door de koppelwerkwoorden zijn of worden) (all **covered**)

    * *De man raakte (werd) uitgeput*
      *Raken* = koppelwerkwoord
    * *Die opmerking viel (was)verkeerd*
      *Vallen* = koppelwerkwoord

**Appendix**

    * Hulpwerkwoorden van de lijdende vorm. Hulpwerkwoorden van lijdende vorm zijn *worden* en *zijn*.
        * *De baby wordt verzorgd door de moeder*
        * *Ik ben opgehaald door de ambulance*

      Deze hulpwerkwoorden worden binnen de ASTA niet geteld als hulpwerkwoord of lexicaal werkwoord, enkel als persoonsvorm c.q. koppelwerkwoord. (** The formulation here is ambiguous. In any case, passive auxiliaries should be considered auxiliaries and thus never be annotated. **COVERED**)

    * NB1: De koppelwerkwoorden *voorkomen*, *dunken*, *lijken*, *schijnen* en *blijken* kunnen soms als hulpwerkwoorden van modaliteit fungeren. Tel deze dan bij de modale (hulp)werkwoorden. (**covered**)
        * *Het bleek een infarct te zijn*

    * **Blijken**

       * In de uitingen: ‘Het was een infarct. Dat bleek pas veel later’ is /was/ een koppelwerkwoord en /bleek/ een lexicaal werkwoord (in de betekenis van duidelijk zijn). (In principle **covered**, but Alpino analyses *pas veel later* as  a *predc* instead of as a *mod*.)
       * In de uiting: ‘Het bleek dat het een infarct was’ is /bleek/ een lexicaal werkwoord (in de betekenis van duidelijk zijn) en /was/ een koppelwerkwoord. (**covered**)
       * In de uiting: ‘Het bleek een infarct’ is /bleek/ een koppelwerkwoord. (**covered**)
       * In de uiting: ‘Het bleek een infarct te zijn’ is /bleek/ hulpwerkwoord van modaliteit en /zijn/ een koppelwerkwoord. (**covered**)

    * **Blijven**

        * In de uiting: ‘Maar ik blijf er wel bij’ is /blijf erbij/ een lexicaal werkwoord. (**covered**)
        * In de uiting: ‘Ik blijf hier nog een tijdje oefenen’ is /blijf/ hulpwerkwoord van aspect en wordt dus bij de lexicale werkwoorden gerekend. (**covered**)
        * In de uiting: ‘Ik blijf thuis’ is /blijf/ geen koppelwoord maar een lexicaal werkwoord (in de betekenis van niet van plaats veranderen). (**covered**)
        * In de uiting: ‘Ik blijf bakker’ is /blijf/ een koppelwerkwoord. (**covered**)

    * **Geboren**

        * In de uitingen: ‘Ik ben geboren in Groningen’ en ‘Gisteren is mijn kleindochtertje geboren’ is /geboren/ een bijvoeglijk naamwoord en zijn /ben/ en /is/ koppelwerkwoorden. (**covered**)

    * **Geleden**

        * In de uiting: ‘Het is al even geleden’ is /is/ een koppelwerkwoord en /geleden/ een bijvoeglijk naamwoord (**Covered** for /is/ but **not** for /geleden/)

    * **Raken**

        * In de uiting: ‘Hij raakte uitgeput’ is /raakte/ een koppelwerkwoord (**Covered**)

    * **Worden**

        * In de uiting: ‘Ik ben beroerd geworden’ is /worden/ het koppelwerkwoord (en /ben/ het hulpwerkwoord van tijd). (**Covered**)

    * **Zijn**

       * In onderstaande uitingen is het werkwoord /zijn/ een koppelwerkwoord:8 (all **covered** except where indicated otherwise)

            * Daar ben je druk mee
            * Het is voorbij
            * Ik ben toe aan revalidatie (**not covered**)
            * Ik ben mijn evenwicht kwijt
            * Dat is wat ik zei
            * Ik denk dat het vijf uur was
            * En die vroeg aan mij hoe het was (in de betekenis van ‘hoe was de film?’)
            * Wat is het?
            * Het is me wat
            * Toen was het 11 uur
            * Toen was het leuk
            * Ik ben bezig
            * Ik ben ermee bezig
            * Ik ben vermoeid
            * Het is klaar
            * Mijn bril is kwijt
            * Ik ben dingen kwijt
            * Ik ben kwijt
            * Ik ben onderweg
            * We zijn met zijn achten thuis (**not covered**)
            * Ik ben de oudste van vier jongens

        * /Zijn/ is geen koppelwerkwoord in: (all **covered** except where indicated otherwise)

            * Dat is er met mij aan de hand
            * En die vroeg aan mij hoe het was (in de betekenis van ‘hoe gaat het?’) (**not covered**)
            * Ik ben hier
            * Met mij is het goed. (**not covered**)


.. _A014_PV_FOUT:

A014: PV FOUT
-------------------

* **Name**: PV FOUT
* **Level**: Taalmaat
* **Original**: yes
* **In Form**: yes
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A015_DEL_VNW:

A015: DEL VNW
-------------------

* **Name**: DEL VNW
* **Level**: Grammaticale fout
* **Original**: yes
* **In Form**: yes
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A016_EENWOORDSUITING:

A016: EENWOORDSUITING
---------------------------

* **Name**: EENWOORDSUITING
* **Level**: Grammaticale fout
* **Original**: yes
* **In Form**: yes
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A017_ONVOL:

A017: ONVOL
-----------------

* **Name**: ONVOL
* **Level**: Grammaticale fout
* **Original**: yes
* **In Form**: yes
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A018_LEX:

A018: LEX
---------------

* **Name**: LEX
* **Level**: Taalmaat
* **Original**: yes
* **In Form**: yes
* **Page**: 9
* **Implementation**: Xpath with macros
* **Query** defined as::

   asta_lex


.. autofunction:: asta_queries::asta_lex



.. _A020_M:

A020: M
-------------

* **Name**: M
* **Level**: Taalmaat
* **Original**: yes
* **In Form**: yes
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

   //node[@pt="ww" and %ASTA_modalww%]


The macro *ASTA_modalww* has a very simple definition::


    ASTA_modalww = """  (@lemma="zullen" or @lemma="willen" or
                         @lemma="moeten" or @lemma="mogen" or
                         @lemma="kunnen" or @lemma="hoeven") """



**Handleiding**

* /zullen/, /willen/, /moeten/, /mogen/, /kunnen/ altijd als modaal tellen. (**covered**)

**Appendix**

* Modale werkwoorden zijn *zullen*, *willen*, *moeten*, *mogen*, *kunnen* en *hoeven*. (**covered**)

    * Ik zal vertrekken
    * Hij wil naar huis (maar ook: hij wil naar huis fietsen)
    * Ik moet naar huis (maar ook: ik moet dat doen)
    * Het schaap mag de wei in
    * De leerlingen kunnen lezen
    * De man hoeft niets

  Het maakt niet uit of bovenstaande woorden daadwerkelijk als hulpwerkwoord gebruikt zijn of als een zelfstandig gebruikt werkwoord, ze worden altijd meegeteld bij de maat: modale (hulp)werkwoorden. (**covered**)

   NB1: De koppelwerkwoorden voorkomen, dunken, lijken, schijnen en blijken kunnen soms als hulpwerkwoorden van modaliteit fungeren. Tel deze dan bij de modale (hulp)werkwoorden. (**not covered**)

   * Het bleek een infarct te zijn

   NB2: het modale (hulp)werkwoorden hoeven is de handleiding van 2013 niet opgenomen als modaal. Het is echter wel degelijk een modaal (hulp)werkwoord. (**covered**)


.. _A021_N:

A021: N
-------------

* **Name**: N
* **Level**: Taalmaat
* **Original**: yes
* **In Form**: yes
* **Page**: 8
* **Implementation**: Xpath with macros
* **Query** defined as::

   asta_noun


.. autofunction:: asta_queries::asta_noun


.. _A022_NEO:

A022: NEO
---------------

* **Name**: NEO
* **Level**: Taalmaat
* **Original**: yes
* **In Form**: yes
* **Page**: 10
* **Implementation**: Python function
* **Query** defined as::

   neologisme


.. autofunction:: ASTApostfunctions::neologisme



.. _A024_PV:

A024: PV
--------------

* **Name**: PV
* **Level**: Taalmaat
* **Original**: yes
* **In Form**: yes
* **Page**: 12
* **Implementation**: Xpath with macros
* **Query** defined as::

   //node[@pt="ww" and @pvagr]





.. _A025_relevantie_van_het_antwoord:

A025: relevantie van het antwoord
---------------------------------------

* **Name**: relevantie van het antwoord
* **Level**:
* **Original**: yes
* **In Form**: ignore
* **Page**: new:36
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A026_SEMPAR:

A026: SEMPAR
------------------

* **Name**: SEMPAR
* **Level**: Taalmaat
* **Original**: yes
* **In Form**: yes
* **Page**:
* **Implementation**: Python function
* **Query** defined as::

   sempar


.. autofunction:: ASTApostfunctions::sempar



.. _A027_stereotypen:

A027: stereotypen
-----------------------

* **Name**: stereotypen
* **Level**:
* **Original**: yes
* **In Form**: ignore
* **Page**: new:36
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A028_Valse_Start:

A028: Valse Start
-----------------------

* **Name**: Valse Start
* **Level**: MLU
* **Original**: yes
* **In Form**: yes
* **Page**: 7
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A029_X:

A029: MLU/X
-------------

* **Name**: X
* **Level**: MLU
* **Original**: yes
* **In Form**: yes
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

   mlux


.. autofunction:: dedup::mlux

**Handleiding**

* Streep de volgende woorden weg binnen de zojuist bepaalde uitingsgrenzen.
  * minimale responsen ( /ja/ /nee/ /nou/ (tenzij gebruikt in de betekenis van /nu/)) (**covered**, though *nou* might be removed too often.)
  * iedere herhaling (**covered**, including many but not all partial repetitions)
  * iedere echolalie (**covered partially**)
  * iedere mislukte poging om te komen tot realisatie van het doelwoord (** covered partially**)
    * Ik ging zitten op de kast, nee stoel, nee bank Aantal woorden voor bepalen samplegrootte = 10, MLU=6
* Streep /hé/, /goh/, /och/ etc. weg. (**covered**)
* Uitingen die deels onverstaanbaar zijn worden in hun geheel weggelaten (eventuele lexicale maten zijn dan al wel geteld) (**covered**)

The next steps from the *Handleiding** are not covered here, because they must be done elsewhere (in the postqueries and/or form):

* Tel het aantal overgebleven uitingen.
* Indien de laatste uiting onvolledig is, door het afkappunt bij de 300-woordengrens, wordt deze uiting in zijn geheel weggelaten.
* Tel per overgebleven uiting het aantal woorden.
* Tel vervolgens het aantal woorden van de overgebleven uitingen bij elkaar op.
* Deel het totaal van de overgebleven woorden door het totaal aantal uitingen. Dit is de MLU.



.. _A030_SUBVZ:

A030: SUBVZ
-----------------

* **Name**: SUBVZ
* **Level**: Grammaticale fout
* **Original**: yes
* **In Form**: yes
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A031_DELVZ:

A031: DELVZ
-----------------

* **Name**: DELVZ
* **Level**: Grammaticale fout
* **Original**: yes
* **In Form**: yes
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A032_SUBPV:

A032: SUBPV
-----------------

* **Name**: SUBPV
* **Level**: Grammaticale fout
* **Original**: yes
* **In Form**: yes
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A033_DELPV:

A033: DELPV
-----------------

* **Name**: DELPV
* **Level**: Grammaticale fout
* **Original**: yes
* **In Form**: no
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A034_SUBLID:

A034: SUBLID
------------------

* **Name**: SUBLID
* **Level**: Grammaticale fout
* **Original**: yes
* **In Form**: yes
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A035_DELLID:

A035: DELLID
------------------

* **Name**: DELLID
* **Level**: Grammaticale fout
* **Original**: yes
* **In Form**: yes
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A036_DELS:

A036: DELS
----------------

* **Name**: DELS
* **Level**: Grammaticale fout
* **Original**: yes
* **In Form**: yes
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A037_MULFOUT:

A037: MULFOUT
-------------------

* **Name**: MULFOUT
* **Level**: Grammaticale fout
* **Original**: yes
* **In Form**: yes
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A038_ONVERST:

A038: ONVERST
-------------------

* **Name**: ONVERST
* **Level**: Grammaticale fout
* **Original**: yes
* **In Form**: yes
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A039_VOLGFOUT:

A039: VOLGFOUT
--------------------

* **Name**: VOLGFOUT
* **Level**: Grammaticale fout
* **Original**: yes
* **In Form**: yes
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A040_DELO:

A040: DELO
----------------

* **Name**: DELO
* **Level**: Grammaticale fout
* **Original**: yes
* **In Form**: yes
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A041_PVTIJDFOUT:

A041: PVTIJDFOUT
----------------------

* **Name**: PVTIJDFOUT
* **Level**: Grammaticale fout
* **Original**: no
* **In Form**: yes
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A042_SEMFOUT:

A042: SEMFOUT
-------------------

* **Name**: SEMFOUT
* **Level**: Grammaticale fout
* **Original**: no
* **In Form**: yes
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A043_SUBVW:

A043: SUBVW
-----------------

* **Name**: SUBVW
* **Level**: Grammaticale fout
* **Original**: no
* **In Form**: yes
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A044_paragrammatisch:

A044: paragrammatisch
---------------------------

* **Name**: paragrammatisch
* **Level**: Grammaticale fout
* **Original**: no
* **In Form**: yes
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A045_X:

A045: SampleGrootte/X
---------------------

* **Name**: X
* **Level**: SampleGrootte
* **Original**: yes
* **In Form**: yes
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

   samplesize

.. autofunction:: dedup::samplesize

**Handleiding**:

* Tel een herhaling mee om tot het totaal van 300 woorden te komen. Er is sprake van een herhaling als tenminste 50% van het aantal fonemen van het doelwoord is gerealiseerd. Indien minder dan 50% van het doelwoord is gerealiseerd, is er sprake van een valse start. (**covered**)
* Een herhaling hoeft niet direct aansluitend op de eerste realisatie te volgen. (**covered**)
* Uitzonderingen zijn /ja/ /nee/ /nou/. Ja ja ja ja ja = 1 woord (**covered**)
* Tel een minimale respons mee om tot het totaal aantal van 300 woorden te komen. (**covered**)
* Een minimale respons die een herhaling bevat wordt als één woord geteld. (**covered**)
* Tel een neologisme mee in het totaal aantal van 300 woorden. (**covered**)
* Tel een echolalie mee in het totaal aantal van 300 woorden. (**covered**)
* Tel een stereotype mee in het totaal aantal van 300 woorden. (**covered**)
* Het sample loopt tot en met woord nummer 300, ook al valt deze grens midden in een uiting. Tot deze grens worden alle lexicale maten bepaald. (**not covered**)
* Interjecties /hé/ /eh/ /ho/ /oh/ etc. niet meetellen voor het aantal van 300 woorden. (**covered**)
* De verstaanbare woorden binnen een deels onverstaanbare uiting worden meegeteld in het totaal aantal van 300 woorden. (**covered**)


.. _A046_nounlemma:

A046: nounlemma
---------------------

* **Name**: nounlemma
* **Level**: lemma
* **Original**: yes
* **In Form**: yes
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

   getnounlemmas


.. autofunction:: ASTApostfunctions::getnounlemmas


.. _A047_ASTA_form:

A047: ASTA form
----------------

* **Name**:
* **Level**: Formulier
* **Original**: yes
* **In Form**: yes
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

   astaform





.. _A048_BW:

A048: BW
--------------

* **Name**: BW
* **Level**: Taalmaat
* **Original**: no
* **In Form**: no
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**





.. _A049_verblemma:

A049: verblemma
---------------------

* **Name**: verblemma
* **Level**: lemma
* **Original**: yes
* **In Form**: yes
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

   getlexlemmas


.. autofunction:: ASTApostfunctions::getlexlemmas



.. _A050_pvgetalfout:

A050: pvgetalfout
-----------------------

* **Name**: pvgetalfout
* **Level**: Grammaticale fout
* **Original**: no
* **In Form**: yes
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

   **not implemented yet**






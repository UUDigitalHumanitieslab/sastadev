STAP Language Measures
======================

The STAP language measures have been written by Sjoerd Eilander, though Jan Odijk reviewed them and revised some of them, especially the ones for "bijwoordelijke bepalingen".

For each language measure, we explain the abbreviation and its name, specify how it has been implemented (as an Xpath query, as an Xpath query with macros, or as a Python function), and mention the section and the page where the measure is described in [van Ierland et al. 2008]. We also cite from the documentation to indicate which aspect of the documentation a particular part of the query implements.

S001: NS
--------

* **Name** NS: "nevenschikking" = coordination
* **Implementation**: Xpath query. 
* **Section:** 8.1
* **Page:** 50

It identifies 

* nodes for the words *en*, *maar*, *want*, *of* or *dus* ("Nevenschikking wordt gescoord wanneer het kind twee hoofd- of bijzinnen verbindt door een nevenschikkend voegwoord: *en*, *maar*, *want*, *of* of *dus*, in VU met en zonder samentrekking.")

* with grammatical relation *crd* (coordinator) and with a sibling node that bears the relation *cnj* (conjunct) and that has a clausal category ("Nevenschikking tussen woorden en woordgroepen wordt niet gescoord"):

  * smain - main clause
  * cp - subordinate clause introduced by a subordinating conjunction
  * rel - relative clause
  * ssub - subordinate clause
  * sv1 - verb initial clause
  * whq - main clause wh-question
  * whrel - wh-relative clause including free relative clauses
  * whsub - subordinate wh-question

  
* or with grammatical relation *dlink* - this for cases where a coordinator introduces a single clause, e.g. **en** *op de teefee mag het*, **maar** wat is Maria?*. ("Nevenschikking wordt ook gescoord wanneer een nevenschikkend voegwoord gebruikt is aan het begin van een hoofdzin die het begin van de beurt is, ook als een interjectie voorafgaat.")


S002: OS
--------

 
* **Name** OS: "onderschikking" = subordination
* **Implementation**: Xpath query. 
* **Section:** 8.2
* **Page:** 50


It identifies:

* nodes with a subordinate clausal category:  *cp*, *whrel*, *whsub*, *rel*. ("Onderschikking wordt gescoord wanneer een kind een bijzin gebruikt als onderdeel van een hoofdzin. Om als Onderschikking te tellen, moet tenminste
   * óf het onderschikkend voegwoord of een ander verbindingswoord aanwezig zijn;
   * óf de bijzins-woordvolgorde gerealiseerd zijn")

* a node with category ssub if at least it does not have any of the grammatical relations *body*, *cnj*, *tag* or *nucl*, in which cases it is an independent or conjunct *ssub* or covered by a clausal category immediately dominating *ssub* (*body*).

Other relevant cases:

* "Directe rede-zinnen worden niet gescoord bij Onderschikking": automatically taken care of since these are analysed by Alpino as main clauses.
* "Wanneer twee onderschikkende zinnen nevenschikkend verbonden zijn, wordt slechts éénmaal Onderschikking gescoord én eenmaal Nevenschikking. ". Achieved by excluding *cnj* as a relation.

**Remark** Cases with *tag*, *nucl*, *sat* and *mod* should be reconsidered: they usually occur in complex combinations of subordinate clauses where one should be counted and one should not (because of a superordinate cp). 

**Remark** *dp*, *mod* and *vc* also occur as relations (in Lassy-Small, not in STAP samples so far) and should be counted in (as they currently are)

**Remark** Maybe cat = sv1 with appropriate grammatical relations for subordinate clauses (e.g. rel = mod) and with a clausal node as parent should be added here, though it may be difficult to exclude parentheticals (e.g. "zie pag. 3")

S003: PV
--------

* **Name** PV: "persoonsvorm" = finite verb
* **Implementation**: Xpath query. 
* **Section:** 8.3
* **Page:** 51

It identifies nodes with the attribute *wvorm* set to "pv".

Concerning:

* "Bij deze variabele worden VU waarbij het kind minder of meer dan één persoonsvorm gebruikt, gescoord."
* "Bij de scoring wordt uitgegaan van 50 persoonsvormen. De VU met -1 moeten van 50 worden afgetrokken en de persoonsvormen die aangegeven zijn met +1, +2, etc. moeten weer bij dit getal worden opgeteld."

The results of the query for S003 are used in the computation of the relevant cells in the STAP form. See :ref:`STAP-form`



S004: SGG
---------

* **Name** SGG: "Samengesteld Gezegde" = composite predicate
* **Implementation**: Xpath query. 
* **Section:** 8.4
* **Page:** 52

"Een Samengesteld gezegde wordt gescoord, wanneer een kind naast de persoonsvorm nog een werkwoord gebruikt in dezelfde hoofd- of bijzin of in een toegevoegde beknopte bijzin."


The query identifies nodes

* for finite verbs (wvorm=pv) with grammatical relation *hd* (Head) 
* that have a sibling node with grammatical relation *vc* (verbal complement) and 

  * one of the grammatical categories *inf* (infinitival clause), *ti* (*te*-infinitival clause), or *ppart* (participial clause)
  * or a bare verb (pt = ww)
  
 A bare verb must be allowed for cases in which the superordinate verb has no argument (subject, direct object or indirect object) to serve as an antecedent for the subject of the nonfinite verb, e.g. *moet oefenen .*)
 
The STAP-Handleiding distinguishes several subcases:

* "Hulpwerkwoord + voltooid deelwoord.": covered by *ppart* and bare verb 
* "Hulpwerkwoord + infinitief (zonder te)": covered by *inf* and bare verb 
* "Hulpwerkwoord + (meestal) *te* of *aan het* --- + infinitief": *te* plus infinitive covered by *ti*, *aan het* plus infinitive is lacking and should be added (*ahi*)
* "Hoofdwerkwoord + (om) te + infinitief": *te* plus infinitive covered, *om te* plus infinitive is lacking, should be added (vc/oti). I am not sure that the example given (*ik doe dat om te winnen natuurlijk* is a correct example, I would analyse the *om te* infinitive here as an adverbial clause. A better example would be *ik heb geprobeerd om te winnen*".
* "Ook combinaties van deze soorten komen voor in één zin. Dit telt als één Samengesteld gezegde": covered if they involve coordination, as in the example given.
* "Voor scoring van Samengesteld gezegde is noodzakelijk dat twee werkwoorden volledig gerealiseerd zijn. Wanneer alleen een deel van een scheidbaar zelfstandig werkwoord gerealiseerd is, telt dit niet als Samengesteld gezegde. Voorbeeld: k.ik heb het op/": covered.

  
S005: VT
--------

* **Name** VT: "Verleden Tijd" = past tense
* **Implementation**: Xpath query. 
* **Section:** 8.5
* **Page:** 53

It identifies nodes for verbs in past tense (pvtijd=verl).

The *Handleiding* states:

* "Iedere Verleden tijd wordt gescoord, zowel correcte als incorrecte vormen, omdat beide soorten wijzen op morfologische activiteit van het kind: correct past tenses are covered, incorrect past tenses only if SASTA can correct it to a correct past tense. If the correct past tense is indicated by means of a CHAT annotation, e.g., *slaapten [: sliepen]*, then it can be counted as well, but this has not been implemented yet.
* "Een foute Verleden tijd, die reeds gescoord is bij Ongrammaticaliteit wordt hier dus weer gescoord.": see previous bullet

S006: VD
--------

* **Name** VD: "Voltooid Deelword" = perfect participle
* **Implementation**: Xpath query. 
* **Section:** 8.6
* **Page:** 54

It identifies nodes for perfect participles (wvorm=vd)

The *Handleiding* states:

* "Alle Voltooide deelwoorden worden gescoord, zowel correcte als incorrecte, omdat beide vormen wijzen op morfologische activiteit van het kind.". For incorrect past participles, see the remarks on incorrect past tenses.
* "Een Voltooid deelwoord dat functioneert als naamwoordelijk deel van het gezegde of als bijvoeglijke bepaling, wordt ook meegeteld.": covered 
* "In een VU kunnen meerdere Voltooid deelwoorden voorkomen": covered


S007: N
-------

* **Name** N: "Naamwoord" = noun
* **Implementation**: Xpath query. 
* **Section:** 8.7
* **Page:** 54

It identifies nodes

* that are either a noun (pt=n) ("Zelfstandige naamwoorden en eigennamen")
* or a substantivised adjective (pt=adj and @positie=nom) ("Zelfstandig gebruikte bijvoeglijke naamwoorden")
* or that are a numeral (pt=tw) but not a determiner (rel != det) ("Zelfstandig gebruikte telwoorden")
* or that are multiword units (cat = mwu) for a name (pos = name) ("Eigennamen die bestaan uit een voornaam en achternaam zijn als één Naamwoord gescoord.")

The "Handleiding" also states: "Maar eigennamen met een naamwoordelijke specificatie zijn geteld als twee Naamwoorden", and that is covered.


S008: BvBep
-----------


* **Name** BvBep: "Bijvoeglijke Bepaling" = attributive adjunct
* **Implementation**: Xpath query with macros
* **Section:** 8.8
* **Page:** 55

The query is defined as ``//node[%bijvbep%]``, where the definition of the macro *bijvbep* uses many other macros::

	bijvbep = """( (%corebijvbep% or %onbepvnwmod% or %twdet% or %apdet% or %app% or %detn% or %detnp% or %possdetp%) and not(%adjmodwwBB%))""" 

The explanation for the macros used is as follow:

* **corebijvbep** = 

  * nodes with rel = mod
  * but not adverbs or adverbial phrases
  * not relative clauses
  * with as parent a node with cat= np that 
  
    * does not contain a head with lcat = ap. It is unclear to me what is intended here. Perhaps an attempt to exclude substantivised adjectives?


* **onbepvnwmod**: nodes for indefinite pronouns with rel = det (e.g. **elke** *dag*)
* **twdet**: nodes for numerals with rel = det (e.g. **drie** *boeken*)
* **apdet**: nodes for aps with rel = det (e.g. **heel veel** *vaders*)
* **app**: nodes for np appositions, e.g *lapje* **zwarte stof**)@@no this is a mod@@
* **detn**: nodes for noun determiners, e.g. **Wims** *huis*
* **detnp**: nodes for np determiners, e.g., **een heleboel** *mensen*
* **possdetp**:  nodes for detps consisting of a modifiers noun and a possessive pronoun, e.g. **Anna d'r** *schoenen*
* **adjmodwwBB**: nodes for  uninflected adjectives or aps with an uninflected adjective as head that are modifiers to a verb (e.g. **hard** *praten*) should not be included

The *Handleiding* states:

* Als Bijvoeglijke bepaling worden opgevat attributief gebruikte bijvoeglijke naamwoorden of equivalenten daarvan. Een bijvoeglijk naamwoord dat naamwoordelijk deel van het gezegde is, is predikatief gebruikt en wordt niet gescoord, omdat de variabele Bijvoeglijke bepaling de complexiteit van de naamwoordgroep meet." This is covered by the requirement that the parent must be an *np*. It distinguishes:

    * "Bijvoeglijke naamwoorden, eventueel gecombineerd met een bijwoord van graad." covered by **corebijbep**. It states that "Meerdere bijvoeglijke naamwoorden na elkaar, gelden als één bijvoeglijke bepaling.", but the example given concerns an adverb + an adjective (*een verschrikkelijk ouwe boot*). Two attributive adjectives will currently count as 2 "bijvoeglijke naamwoorden". This may have to be changed.
    * "bijwoord van graad en bijv.nw.: één bijvoeglijke bepaling". covered
    * *Bijvoeglijk gebruikte telwoorden*. Covered. But the example   **twaalf** *uur 's nachts* is currently NOT covered (because "twaalf uur" is analyzed by Alpino as an *mwu* with two *mwp* parts. In the example *de* **laatste** *aflevering*, *laatste* is not considered a numeral but an adjective, and thus covered. In the final example **geen** *spijkertjes*, *geen* is not considered a numeral by Alpino but a determiner (vnw with relation *det*).
    * "Bijvoeglijk gebruikte vragende voornaamwoorden": covered by **onbepvnwmod**, e.g. *welke dag* (no example given in the *Handleiding*)
    * "Bijvoeglijk gebruikte onbepaalde voornaamwoorden": covered by **onbepvnwmod** (**iedere** *dag*) and by **apdet** (**heel veel** *vaders*), and by *detnp* (e.g. **een heleboel** *vaders*)
    * "Bijvoeglijk gebruikte voorzetselgroepen." Currently NOT covered (example: *een slaapkamertje* **van mijn broer**)
    * "Bijvoeglijk gebruikte zelfstandige naamwoorden": covered by **app** (*een soort* **motortje**, *een stuk* **eiland**). The *Handleiding* also gives *allemaal* as a "bijvoeglijke bepaling" to *water* in *nou eerst een stuk eiland en daar om allemaal water*, but that is a wrong analysis. "allemaal"is a separate word group here, acting as a secondary predicate. It does not form a single constituent with *water*.
    * "Bijstellingen". No examples given. If äppositions"is meant, the they are covered by **app**
 
Explicitly excluded are:

   * "Bijvoeglijke aanwijzende voornaamwoorden"
   * "bezittelijke voornaamwoorden"
   
 and neither of them is covered, but possessive  nouns and noun phrases are included in the query (by **detn** and **possdet**) though the *Handleiding* is silent about them. @@Should they be included@@? 
 

S009: zelfst.vnw.
-----------------

* **Name** zelfst.vnw.: "Zelfstandig voornaamwoord derde persoon" = independent  3rd person pronoun
* **Implementation**: Xpath query with macros
* **Section:** 8.9
* **Page:** 56

It identifies nodes for pronouns (pt = vnw) 

* that are not possessive pronouns (not(vwtype= bez))
* that are 3rd person (all the conditions on the attribute *persoon*
* with attribute pos not equal to *adv* (this excludes R-pronouns)
* and with *rel* not equal to *det* (because then they would be determiners, not independent pronouns)

The *Handleiding* states:

* "Deze variabele omvat alle zelfstandige voornaamwoorden 3e persoon" 
* "die geen deel uitmaken van een voorzetselgroep": this is currently NOT excluded. The *Handleiding* includes:

   * "Persoonlijke voornaamwoorden van de derde persoon" covered
   * "Zelfstandige aanwijzende voornaamwoorden": covered
   * "Zelfstandige onbepaalde voornaamwoorden": covered
   * "Zelfstandige vragende voornaamwoorden": covered
   * "Zelfstandig gebruikt geen (met er ervoor)": covered
   * "Betrekkelijk voornaamwoord met ingesloten antecedent":  covered.
   
   
* but it excludes some that are currently NOT excluded, i.e., "woorden die fungeren als voorlopig, herhaald of loos onderwerp of voorwerp":

      * **het** *had niet geregend* ("loos onderwerp"): NOT currently excluded. It can be covered by taking into account the *frame* attribute, e..g for *regenen*: *verb(hebben,sg3,* **het_subj** *)*, and by excluding the relation *sup* (e.g. **het** *is duidelijk dat hij ziek is*)
      * "loos voorwerp": not excluded, but it can be covered by excluding the relation *pobj1* (as in *ik waardeer* **het** *dat hij komt*)
      * "herhaald onderwerp": not excluded, some may be excluded because they are analyzed as relative pronouns, otherwise we have to look at satellite/nucleus configurations 




S010: BB p
-----------

* **Name** BB p: "Bijwoordelijke Bepaling van Plaats" = locative adverbial modifier
* **Implementation**: Xpath query with macros
* **Section:** 8.10
* **Page:** 59

The query is ``//node[%new_STAP_BB_p%]`` where the macro *new_STAP_BB_p* is defined as::

	new_STAP_BB_p = """
	(
	 (%ld_pp% or
	  %ld_vz% or 
	  %ld_erlocadv% or
	  %loc_ppBB% or
	  %locadvBB%  or
	  %locadvpBB% or
	  %predclocadj% or
	  %predclocap% or
	  %svp_bw% or
	  %loc_vzBB%
	 ) and
	 not(%new_STAP_BB_t%)
	)
	"""


We will discuss each of the parts of this macro:

* **ld_pp**: for pp's with the relation *ld*, e.g. *toen ik klaar was toen gingen we* **naar oma**, *die is nu* **op school**, *toen waren jullie* **in Turkije** *op vakantie*
* **ld_vz**: for adpositions with relation *ld*, e.g. *en dan als je* **beneden** *komt*
* **ld_erlocadv**: for locative adverbs including R-adverbs with relation *ld*. Locative adverbs  (macro *locadv*) are identified by the value of the attribute *frame* (must be *er_loc_adverb* or *loc_adverb*, or *er_adverb(P)*, where *P* is one of the (nonambiguous) locative adpositions (for locative adverbial pronouns), e.g. *hij heeft hem* **eruit** *gehaald*.
* **loc_ppBB**: for pp's that are adverbial modifiers and have  a locative adposition as their head. The notion "locative adposition" is defined  by the macro **loc_vz**, which simply gives a list of these adpositions. The notion "adverbial modifier" is defined by the macro **BB**:

  * **BB**: a phrase is an adverbial modifier if it bears one of the grammatical relations *mod*, *dp*, *--*, *nucl*, *whd* and, either the parent node is (not non)clausal  or it is a node for  an uninflected adjective or ap with an uninflected adjective as head that is a modifier to a verb (e.g. **hard** *praten*), see *adjmodwwBB* above.
  
* **locadvBB**: for adverbs with relation *ld*, and for locative adverbs that are adverbial modifiers. Locative adverbs are identified as above (macro **locadv**). Examples: *mag je* **daar** *filmpjes kijken.*, *dan gaat ie zelf* **achteruit**, *die is* **thuis** *?*
* **locadvpBB**: for adverbial phrases with a locative adverb as the head, e.g. *Maar bij het laatste nachtje sliep ik* **helemaal beneden** .
* **predclocadj**: for predicative locative adjectives, e.g *ik kan het gas niet* **hoger** zetten, *mag ik* **hoger** *zitten*
* **predclocap**: for predicative aps with a locative adjective as head, e.g., *mag ik* **veel hoger** *zitten?*
* **svp_bw**: for adverbs that function as an *svp*, e.g. *tasje doen we* **weg**, *kom je dan* **terug**. **Remark**: we should exclude *samen*, and *genoeg*.
* **loc_vzBB**: for locative adpositions functioning as an adverbial modifier. This is mainly for locative adpositions that could not be integrated into the structure, as e.g., in **op** *mijn eigen*
* **new_STAP_BB_t**: it should not be a temporal adverbial modifier. See section :ref:`BBT`


The *Handleiding* states:

* "Als bijwoordelijke bepaling worden alle bijwoordelijke bepalingen die zelfstandig zinsdeel zijn én bepalingen van gesteldheid gescoord. De bijwoordelijke bepalingen kunnen voorkomen in de vorm van voorzetselgroepen en in de vorm van losse bijwoorden of bijwoordcombinaties, met uitzondering van een klein aantal zeer frequente bijwoorden."
* "Niet gescoord als Bijwoordelijke bepalingen: *al meer toch dan niet toen dus nog weer eens nou nu wel gewoon ook zo maar te*. Deze bijwoorden worden als ze voorkomen als losse Bijwoordelijke bepaling niet gescoord, omdat ze heel stereotiep gebruikt kunnen worden en ze geen wezenlijke uitbreiding van de zin vormen. Ze worden wel gescoord als ze onderdeel van een woordgroep zijn." Though there is a macro **STAP_geen_BB** to take this into account, it is currently incorrectly not used in the query definitions. This should be added. 

* "Wel gescoord als Bijwoordelijke bepalingen":  *die vond* **zo lekker** **op de grond** zitten*:
    * "*zo*: onderdeel van een woordgroep *zo lekker*, die samen een bepaling van gesteldheid vormt, telt als één bijwoordelijke bepaling;"
    * *op de grond*: voorzetselgroep die een bijwoordelijke bepaling is." Covered by **locppBB** and by **ld_pp**.
* "Scheidbare delen van samengestelde werkwoorden die de vorm hebben van een voorzetsel (*hij ruimt het huis op*) worden niet als bijwoordelijke bepaling geteld; wel delen die de vorm hebben van een bijvoeglijk naamwoord (*hij maakt het huis schoon*) of van een bijwoord (*hij gooit de rommel weg*)." Adverbs are covered by **svp_bw** but adjectives are not covered yet.
* "In één VU kunnen meerdere bijwoordelijke bepalingen voorkomen die gescoord moeten worden. Opeenvolgende bijwoorden worden, voor zover (semantisch) mogelijk, samen genomen en beschouwd als één bijwoordelijke bepaling.". Covered where Alpino can integrate successive adverbs into one constituent. 

More specifically on "Bijwoordelijke bepalingen van plaats". It includes:

*  "Bijwoordelijke bepalingen van plaats, richting en oorsprong." covered
*  "Ook de vragende bijwoorden van plaats en richting (*waar*, *waarin*, *waarheen*, *waarnaar*, etc) worden hier gescoord." Covered by **ld_erlocadv**
*  Other examples:

  * *en dan gaat ie* **in zo'n soort fabriek**: covered by **ld_pp**
  * *we zijn* **op de camping**: covered by **ld_pp**
  * **daar** *is een zwembad*: covered by **ld_erlocadv**
  * *en dan gaan we* **daar naar heen**: 
  * *want nou ga ik morgen ook* **naar m'n vriendje van de camping**: covered by **ld_pp**
  * *want die woont* **daar** nu **in Grouw**: covered by **locadvBB** and by **ld_pp**.
  * *gaan we* **daarheen**: covered by **ld_erlocadv**
  * *en toen ging hij* **dwars door de ruit heen**: covered by **ld_pp**
  
* "de vet gedrukte opeenvolgende woorden passen semantisch bij elkaar: één Bijwoordelijke bepaling van plaats.": covered

.. _BBT
S011: BB t
----------

* **Name** BB t: "Bijwoordelijke Bepaling van Tijd" = temporal adverbial modifier
* **Implementation**: Xpath query with macros
* **Page:** 59

The query is defined as //node[%new_STAP_BB_t%], where the macro *new_STAP_BB_t* is defined as follows::

    new_STAP_BB_t = """ 
   %advBBt% or
   %advpBBt% or
   %npBBt% or
   %apBBt% or
   %adjBBt% or
   %ppnpBBt% or
   %geledenBBt%"""
   
We discuss each of the macros used inside this query

* **advBBt** searches for adverbs (*bw*) that are adverbial modifiers (**BB**, see above) and that meet the requirements of the **temp** macro. The macro **temp** identifies temporal adverbs by frame properties of the word  (**tempadv**) or the lemma (**templemma**) while avoiding excludedlemmas (**excludedlemma**):
   
   * **tempadv** simply checks for values of the *frame* attribute (*tmp_adverb*, *wh_tmp_adverb*) and the *special* attribute (*tmp*)
   * **templemma** simply lists some lemmas for which the frame or special attribute does not indicate the temporal character of the word, among them pronominal adverbs with the adposition *na* (macro **Rna**).
   * **excludedlemma** simply lists lemmas that should not be included as a temporal adverb. It probably should be replaced by the macro **STAP_geen_BB**
   
* **advpBBt** is defined as::

     advpBBt = """ (@cat="advp" and %BB% and node[@rel="hd" and %temp% ])"""
	 
  so it searches for adverb phrase (*advp*) that are adverbial modifiers (**BB**, see above) and that have a head that meets the conditions of the macro **temp**. 

* **npBBt** is defined as::

     npBBt = """ (@cat="np" and %BB% and node[@rel="hd" and %tempnoun%])"""

  so it searches for noun phrases that are adverbial modifiers and have a head that meets the condition of the macro **tempnoun**:
  
  * **tempnoun** checks the temporal character of a noun by checking its *frame* attribute or by inspecting the value of the *lemma* attribute. In the latter case a disjunction of lemmas for event nouns is given, currently very incomplete. This is probably better replaced by a function in the *generatemacros* module, where the event nouns are extracted from an external source.

  
* **adjBBt** searches for adjectives with grammatical relation *mod* outside of an NP (macro **notinNP**) that meet the conditions of macro **tempadj**. The latter macro checks for the values of the attributes *frame* and *special*, or for specific lemmas (currently only 1).
* **apBBt** searches for APs with grammatical relation *mod* and with a head that meets the requirements of the macro *tempadj*. There is no condition that the AP should not be inside an NP, but that probably has to be added.

* **ppnpBBt** searches for PPs that are adverbial modifiers (via the macro **BB**) or have the grammatical relation *ld* and:

  * either have a temporal adposition as its head, as determined by the macro **tempvz**, which simply is a disjunction of words or lemmas that are unambiguously temporal;
  * or have an NP complement with a head noun that is temporal, as determined by the macro **hastempnounhead**
  * or have a noun complement that is temporal as determined by the macro **tempnoun**
  * or have *mwu* as complement one part of which is a temporal noun (e.g. *'s avonds*)
  
* **geledenBBt** searches for past participial phrases (*ppart*) that are adverbial modifiers (via macro **BB**) and that have a head with lemma equal to *geleden*


The *Handleiding* states: "Deze variabele omvat Bijwoordelijke bepalingen van tijd, van duur, van frequentie en alles wat verwant is aan tijd. Ook de vragende bijwoorden van tijd (*wanneer*, *hoe lang*, etc) worden hier gescoord. It provides the example:

* *ja,* **volgende week** *ga ik verhuizen, als ik* **al lang** *vijf jaar ben*

of which it states: "In deze VU met een hoofdzin en een bijzin staan twee Bijwoordelijke bepalingen van tijd;". These are the boldfaced phrases "volgende week" (covered) and "al lang" (covered). "de bijwoordelijke bijzin van tijd wordt niet apart als Bijwoordelijke bepaling van tijd geteld." (covered).

There are also the examples:

* en toen ging m'n papa me optillen/
* en toen ging ik **'s avonds** op m'n papa z'n nek staan
* en toen ging ik eraf springen en m'n moeder **ook een keer**

Of these *'s avonds* is not covered, though it should be easy to add it::

    //node[@cat="mwu" and node[@rel="mwp" and %tempnoun%]
	
Also *ook een keer* is not covered because Alpino analyses the NP as a modifier of the noun *moeder*.

S012: BB o
----------

* **Name** BB t: "Overige Bijwoordelijke Bepaling" = other adverbial modifier
* **Implementation**: Xpath query with macros
* **Page:** 60

The query is defined as `//node[%new_STAP_BB_o%]` where the macro **new_STAP_BB_o** is defined as follows::

	new_STAP_BB_o = """ ((  %bbo_pt% or %bbo_cat% or %bbo_mwu%) and
						   not(%excludedadverb%) and 
						   (%BB% or %pred% or %svp_bbo%) and 
						   not(%new_STAP_BB_t%) and 
						   not(%new_STAP_BB_p%) 
						)
	""" 

We discuss each of the aspsects of this macro:

* **bbo_pt**: any node with a value for the *pt* attribute that can function as an adverbial modifier
* **bbo_cat**: any node with a value for the *cat* attribute that can function as an adverbial modifier
* **bbo_mwu**: any node with *cat* equal to "mwu* and containing a node that meets the requirements of the macro **bbo_pt**
* **excludedadverb**: this identifies the adverbs that should not be scored as an adverbial modifier 
* **(%BB% or %pred% or %svp_bbo%)**: functioning as an aderbial modifier (**BB**) or as a predicate (**pred**), whether as a complement (*predc*) or as a secondary predicte (*predm*), or as an *svp* (by the macro **svp_bbo**, which also requires *pt* to be equal to *adj* or *bw*, and allows a word with a specific *lemma*.
* **not(%new_STAP_BB_t%)**: it should not be a temporal adverbial modifier
* **not(%new_STAP_BB_p%)**: it should not be a locative adverbial modifier


The *Handleiding* states: "De Overige bijwoordelijke bepalingen omvatten:"

* Bijwoordelijke bepalingen met een andere functie dan plaats of tijd;": covered
* De overige vragende bijwoorden (*waarom*, *hoe*, etc) worden hier ook gescoord.: covered
* Examples:

   * *en nu is ie weg* **met de vuilnisauto**: covered
   * *en* **als het dan mooi weer is**, dan gaan we **met Dennis** *buiten voetballen* (not covered, Alpiono parses *met Dennis* as a *pc*, not as a *mod*). Maybe we should include pc/PPs with *met* as head as well.

* *Bepalingen van gesteldheid*:

  * *en dat vind ik* **zo leuk**: covered, but currently all *ap* ord *adj* nodes with relation equal to *predc* are covered, also the ones after copulas, which is wrong and should be corrected. This can be done easily by adapting the macro **pred** to require presence of a direct object if the relation is *predc*.







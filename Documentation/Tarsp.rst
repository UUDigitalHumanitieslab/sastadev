TARSP Language Measures
-----------------------

We will describe here all Tarsp language measures, in the order of the identifiers assigned to them. However, a few language measures are special in that they systematically composed out of recurring macros. See  :ref:`tarspannotations` for more on these language measures, which we will call *composed language measures*. We will discuss the most important macros that are used in the queries for such language measures first, in section :ref:`composedmeasures`.


.. _composedmeasures:

Macros for Composed Language Measures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Composed language measures often consist of:

* a macro for the mood of the clause (declarative, question, imperative)
* macros for 'zinsdelen'
* macros for counts of complements and modifiers

We will discuss each of these.

Macros for clause mood
""""""""""""""""""""""

The *mood* of a clause is determined on the basis of a lot of different clues. Interpunctuation symbols also play a role: we especially do not allow interpunctuation symbols that contradict a mood (e.g. an imperative followed by a question mark). We therefore use several macros for interpunctions symbols:

* **topcontainsquestionsmark**
* **topcontainsperiodmark**
* **topcontainsexclamationmark**

We give the definition of **topcontainsquestionmark**::

    topcontainsquestionmark = """(ancestor::node[@cat="top" and node[%questionmark%]])"""
    questionmark = """(@pt="let" and @word="?")"""

The other two are defined analogously.

The most problematic clausal category is *sv1*, since it can head declaratives, questions and imperatives (see :ref:`alpinoclauses`). Distinguishing these correctly is no trivial matter, and the queries we made are certainly not perfect.

.. _declaratives:

Declaratives
''''''''''''

Declarative clauses are identified by the macro **declarative**::

    declarative = """(@cat="smain" or
                     (@cat="ssub" and not(%partofwhquestion%)) or
                     (@cat="sv1" and not(%basicimperative%) and not(%ynquery%) and not(%partofwhquestion%)) )"""


Explanation:

* *smain* clauses are always declarative
* *ssub* clauses are declarative if they are not the body of a (subordinate) wh-question: not (%partofwhquestion%)
* *sv1* clauses are declarative if they are neither imperatives (not(%basicimperative%)), nor yes-no-questions (not(%ynquery%)), nor the body of (main) wh-question (not(%partofwhquestion%))

For the definition of the macro **basicimperative**, see :ref:`imperatives`, for the macro **ynquery** see :ref:`questions`.

The macro **partofwhquestion** is defined as follows::

   partofwhquestion = """((@cat="sv1" or @cat="ssub") and
                          @rel="body" and
                          parent::node[@cat="whq" or @cat="whsub" ]) """


.. _questions:

Questions
'''''''''

Yes-no questions are identified by the macro **ynquery**::

   ynquery = """@cat="sv1" and
             (@rel="--" or @rel="dp") and
             not(%topcontainsperiodmark%) and
              not(%topcontainsexclamationmark%) and
             node[@rel="hd" and @pt="ww" and @pvtijd !="conj" and
                  (@stype="ynquestion" or %topcontainsquestionmark% ) ] and
             (node[@rel="su"] or %topcontainsquestionmark%)    and
             (not(%impmodfound%) or %topcontainsquestionmark% )
            """

Explanation:

* Tarsp does not mark subordinate yes-no question (introduced by the subordinate conjunction *of*) in any special way, so we only deal with main clauses
* The category must be *sv1* and it must have one of the relations *--* or *dp*, so that it indeed is a main clause
* There must not be an period or an exclamation mark at the end of the utterance
* There must be a verb, but not in conjunctive form, and either Alpino has marked the utterance as a yes-no-question (via the attribute *stype* on the verb), or there is a question mark at the end of the sentence.
* There must be a subject or a question mark. Yes-no questions normally contain a subject. Imperatives most often do  not. So absence of a subject is seen as a  indication for an imperative unless there is a question mark
* Certain adverbs are often used with imperatives. Such adverbs should therefore not be present (not(%impmodfound%)), or there must be question mark.


*Wh*-questions are defined as follows::

    Tarsp_whq = """((@cat="whq" and @rel="--") or (@cat="whsub") or (@cat="whrel" and @rel="--"))"""

covering both main clauses (*whq*) and subordinate clauses (*whsub*), but also clauses that have been analysed by Alpino as independent (relation="--" ) relative clauses, which usually are actually wh-questions.


.. _imperatives:

Imperatives
'''''''''''

Imperatives are identified by the macro **basicimperative**::

    basicimperative = """(%normalimp% or %bareverbimp% )"""

Here the macro **normalimp** is defined as follows::

    normalimp = """(@cat="sv1" and
                    not(%topcontainsquestionmark%) and
                    (not(%topcontainsperiodmark%) or %impmodfound%) and
                    %imprelok% and
                    %impsubjectok% and
                    node[%wwimpok%]
                )"""

Explanation:

* The category must be *sv1*
* the utterance must not contain a question mark
* it does not contain a period unless an adverbial modifier typical for imperatives is present. The latter is checked by the macro **impmodfound**. Such an adverbial modifier can occur in the main clause but also in a subordinate nonfinite clause (macro **nonfinvc**). The adverbs typical for imperatives are *maar* and *eens* (macro **basicimpmod**)::

    impmodfound = """(%basicimpmod% or node[%nonfinvc% and %basicimpmod%])"""
    basicimpmod = """(node[@rel="mod" and (@lemma="maar" or @lemma="eens")])"""
    nonfinvc = """(@rel="vc" and %nonfincat%) """
    nonfincat = """(@cat="inf" or @cat="ppart")"""


* the relation of the  node must be typical for imperative clauses: **imprelok**::

    imprelok = """(@rel="--" or @rel="nucl")"""

* There are restrictions on subjects in imperative clauses, expressed by the macro **impsubjectok**::

    impsubjectok = """(not(%Ond%) or
                       (node[%subject% and
                        %impsubject%] and
                        (%impmodfound%  or %topcontainsexclamationmark%)
                       )
                      )"""
    impsubject = """(@rel="su" and (@word="jij" or @word="u"))"""

  Explanation:

    * there either is no subject, or
    * there is a subject but

      * it is *jij* or *u* (**impsubject**) and
      * either a imperative modifier is found (**impmodfound**) or the utterance contains an exclamation mark

* there are restrictions on the verb in an imperative clause, expressed by the macro **wwimpok**::

    wwimpok = """( %wwimpfeatok% and
                   not(%modalframe%) and
                   %zijnimpok%       and
                   %potentialimpverb%
              )"""

* These restrictions concern:

   * conditions on the verbal properties (**wwimpfeatok**). The verb must be a finite present tense singular form (**wwimpfin**), or an infinitive (**wwimpinf**)::

        wwimpfeatok = """(%wwimpfin% or %wwimpinf%)"""
        wwimpfin = """(@rel="hd" and @pt="ww" and @pvtijd="tgw" and @pvagr="ev" and @wvorm="pv") """
        wwimpinf = """(@rel="hd" and @pt="ww" and @wvorm="inf") """

   * the verb must not be a modal verb (**not(%modalframe%)**)::

        modalframe = """(contains(@frame,"modal"))"""

   * if the lemma of the verb is *zijn*, the form must be *wees* or *weest*::

        zijnimpok = """(not(@lemma="zijn") or @word="wees" or @word="weest")"""

   * the verb must be able to form an imperative. This is defined by the macro **potentialimpverb**, which basically excludes a list of verbs that have no imperative::

        potentialimpverb = """(not(contains(@lemma,"moeten") or contains(@lemma,"hoeven") or
                      contains(@lemma,"zullen") or contains(@lemma,"kunnen") or
                      contains(@lemma,"mogen") or @lemma="hebben" or contains(@lemma, "_hebben") or contains(@lemma, "weten")
                     )
                 )"""

The macro **bareverbimp** is defined as follows::

    bareverbimp = """(%wwimpok% and
                      %imprelok%  and
                      parent::node[@cat="top"] and
                      not(%topcontainsquestionmark%) and
                      not(%topcontainsperiodmark%)) """


It is intended for single verb utterances:

* the verb must be compatible with imperative mood (**wwimpok**)
* the relation that the verb bears must be compatible with imperatives (**imprelok**)
* the parent node must have *cat* equal to *top*
* there must not be a question mark in the utterance
* there must be no period in the utterance.

* **Remark** We must find a way to exclude *kijk* and *kijk eens* as an imperative in most cases, since it should be analysed as a V.U.
* **Remark** We must allow other case forms for *jij* en *u* as subjects in imperatives (but not the reduced variant *je*)
* **remark** There surely is overlap betwen the condition on modal verbs and the conditions imposed by **potentialimpverb**.

* **Schlichting** (p. 62)

  "De kenmerken van de Gebiedende Wijs zijn in het kader van TARSP:

     1. de zin moet altijd beginnen met een werkwoord; dat werkwoord staat meestal in de vorm van de stam van het werkwoord, een enkele maal vinden we Stam+t of de infinitief. (covered except Stam+t)
     2. Er is altijd een niet-vragende intonatie (covered by disallowing a question mark)
     3. Er is vaak een tweede of derde woord in de zin, bijvoorbeeld 'maar', 'even', 'eens'. Covered
     4. Een gebiedende wijs begint nooit met een modaal werkwoord, behalve met 'laten' (covered)

.. _zinsdelen:

Macros for 'Zinsdelen'
""""""""""""""""""""""

The 'zinsdelen' are *B*, *Ond*, *VC* and *W* and they correspond to some extent to  the following language measures, for 'zinsdelen':

* T007: B,  adverbial modifier (see :ref:`T007_B`)
* T063: Ond, subject   (see :ref:`T063_Ond`)
* T097: VC, object or complement (see :ref:`T097_VC`)
* T120: W, verb / predicate (see :ref:`T120_W`)


But the correspondence is only perfect for *B*.

* **Remark** For *Ond* the definitions are different, but it is not clear whether that cannot be avoided.
* **Remark** For *VC* the definitions are also different but perhaps they should be identical.
* **Remark** For *W* there is no immediately obvious correspondence, but perhaps there should be. It looks as if the necessary restrictions have been implemented independently twice.

Out of these language measures, only T120/W occurs in the form ('profielkaart').

Language measures such as *WBVC*, *OndVC*, *OndW*, *OndWB*, *OndWBVC*, and several others are defined  by combinations of the definitions of recurring macros for 'zinsdelen' (and some others conditions). For such language measures, special macros for *Ond*, *VC* and *W* have been defined:

* **Ond**: has a simple definition::

        Ond = """node[%subject%]"""

  where::

        subject = """(@rel="su" and parent::node[(@cat="smain" or @cat="sv1" or @cat="ssub")])"""

Here we only count as subjects those nodes (full or index nodes) that have a finite clause node as parent.
Overt subjects never occur in nonfinite clauses, and subject index nodes should not be counted inside nonfinite clauses. Subject index nodes do occur in finite clauses, e.g., as the "trace" of a wh-movement.

It differs from the definition of :ref:`T063_Ond` because T063 has to cover an additional case (existential *er* as a subject (though maybe that should be included here as well)

* **Tarsp_B**: see :ref:`T007_B`
* **Tarsp_VC**: is defined as follows::

    Tarsp_VC = """((@rel="obj1" or (@rel="pc" and not(%Tarsp_pc_vc_exception%)) or
                    @rel="predc" or @rel="ld" or @rel="obj2" or %Tarsp_finvc% or
                    %Tarsp_vcvnw% or (@rel="svp" and @pt!="vz")) and
                   not(%Tarsp_B%) )"""

  So, it covers:

    * direct objects (*obj1*)
    * prepositional complements that are not **Tarsp_pc_vc_exception** (*pc*)
    * predicative complements (*predc*)
    * locative/directional complements (*ld*)
    * indirect objects (*obj2*)
    * finite verbal complements (macro **Tarsp_finvc**)
    * pronouns with relation *vc*, this is for sluiced subordinate clauses as in *ik weet* **wat**, *effe kijken* **waar**
    * separable particles of a verb that are not adpositions (*svp*)

    and we exclude all cases that can be analysed as an adverbial modifier (**Tarsp_B**, see :ref:`T007_B`)

    The macro **Tarsp_pc_vc_exception** is generated in the *generatemacros* module on the basis of a list of  pairs (verb, adposition), e.g. (*slaan*, *op*) in which Alpino analyzes the adposition as the head of a prepositional complement (pc), but where it should be considered the head of a modifier. See :ref:`generatemacros` for more details.

* **Tarsp_W**: It is defined as::

    Tarsp_W = """node[@rel="hd" and @pt="ww"]"""

  Nonfinite verbs are not excluded by this definition but they are excluded by the mood conditions. For language measure T120, *W*, the macro **Tarsp_coreW** is used.


Macros for Counts of 'zinsdelen'
""""""""""""""""""""""""""""""""

Many composed language measures differ only in the number of complements or adverbial modifiers required. For example *Tarsp_OndWB* and *Tarsp_OndWBB* differ only in the number of adverbial modifiers that should be present (one, resp, two).
This requires conditions on the number of such complements or modifiers.
Note that one cannot simply include two expressions joined by *and* in an Xpath query (e.g. *%Tarsp_B% and %Tarsp_B%*) to cover the *BB* part of the language measure *Tarsp_OndWBB*. The reason is that in XPath such a query will then still match with  a structure containing a single adverbial modifier. We therefore use the Xpath function *count* in composed language measures.

Adverbial modifiers and complements can occur not only under the node where the subject and verb occur but also inside a nonfinite verbal complement, so we gather both in a node set, union (|) these node sets and count the number of elements in the union. This leads to the following formulations::

    Tarsp_B_X_count = """count(node[%Tarsp_B%] | node[%nonfinvc%]/node[%Tarsp_B%]) """
    Tarsp_VC_X_count = """count(node[%Tarsp_VC%] | node[%nonfinvc%]/node[%Tarsp_VC%]) """

Definitions for **Tarsp_B** and **Tarsp_VC** were provided above.

We must also have counts for the overall number of "zinsdelen" in the clause. This is taken care of by the macro *realcomplormodnodecount*. It counts occurrences of *realcomplormodnode* in the current node or in a nonfinite complement::


    realcomplormodnodecount = """count(%realcomplormodnode% | node[%nonfinvc%]/%realcomplormodnode%)"""
    realcomplormodnode = """node[%realcomplormod%]"""

The macro **realcomplormod** is defined as follows::

    realcomplormod = """(not(%particlesvp%) and not(%indexnode%) and not(%nonfinvc%) and not(@rel="hd"))"""


Here we exclude:

* adpositional separable verb particles (**particlesvp**). These are considered to be part of the verb::

    particlesvp = """(@rel="svp" and @pt="vz")"""

* index nodes  (**indexnode**). We do not want to include nodes that do not cover lexical material::

    indexnode = """(@index and not (@cat or @pt or @pos))"""

* nonfinite verbal complements, using the macro **nonfinvc** defined above
* the head verb (*not(@rel="hd")*). We exclude this because there can be multiple verbs in a clause but they should always count as one 'zinsdeel', viz. predicate. The value that   **realcomplormodnodecount** is compared with is therefore always one lower than one would expect, because the predicate is assumed to be always present, and is not counted by **realcomplormodnodecount** . For example, for *OndWBB*, with 4 'zinsdelen', the value that **realcomplormodnodecount** must have is equal to **3**, not **4**.


Concrete Example: **Tarsp_OndWBB**
""""""""""""""""""""""""""""""""""

Given all of the above, it should be clear why the definition of **Tarsp_OndWBB** is as follows::

    Tarsp_OndWBB = """(%declarative% and
                      %Ond% and
                      %Tarsp_W% and
                      %Tarsp_B_X_count% = 2 and
                      %realcomplormodnodecount% = 3)"""




Language Measures
~~~~~~~~~~~~~~~~~


T001: (Vr)WOnd+
"""""""""""""""


* **Name**: (Vr)WOnd+.
* **Category**: Zinsconstructies
* **Subcat**: Vragen
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 60
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**




* **Schlichting**: "Vraagwoordzin waarbij het vraagwoord is weggelaten. Het werkwoord +, meestal, het Onderwerp zijn gerealiseerd. Daarna kunnen nog één of meer Zinsdelen volgen."



T003: 6+
""""""""


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

.. autofunction:: Sziplus::sziplus6

* **Schlichting**: "6 Zinsdelen of meer in een zin"


T004: Aan/uit
"""""""""""""


* **Name**: Aan/uit.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 57;58
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**



* **Schlichting**: "Soms wordt een zinsdeel aan het begin of aan het einde van de zin met andere woorden herhaald. Die herhaling noemen we ‘Aanloop’ aan het begin van een zin en ‘Uitloop’ aan het einde van de zin."




T005: als
"""""""""


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

* **Remark**: Fully covered but it is unclear whether *als* as used in comparisons also should be included. All Schlichting's examples concern conditional *als*. So maybe this query should be restricted somewhat.



T006: Avn
"""""""""


* **Name**: Avn. (Aanwijzend Voornaamwoord als nomen)
* **Category**: Voornaamwoorden
* **Subcat**:
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 79
* **Implementation**: Xpath
* **Query** defined as::

    AVn = """(%coreavn% or %avnrel%)""""
    coreavn = """(@pt="vnw"  and @vwtype="aanw" and @lemma!="hier" and @lemma!="daar" and @lemma!="er" and @rel!="det" and (not(@positie) or @positie!="prenom") )"""
    avnrel = """(%diedatrel% and parent::node[@cat="rel" and @rel!="mod"])"""
    diedatrel = """(@pt="vnw" and @vwtype="betr" and @rel="rhd" and (@lemma="die" or @lemma="dat"))"""

The query for *AVn* consists of two subcases: the core case, and the case of *die* and * dat* incorrectly analysed as a relative pronoun in an independent relative clause.

The core case (*coreavn*):

* which has pt equal to *vnw* and vwtype equal to *aanw* selects demonstrative pronouns, but
* these include R-pronouns, so they are explicitly excluded
* the relation must not be *det* (otherwise the pronouns are not used independently)
* and if a *position* attribute is present it should not have the value *prenom* (otherwise it is not used independently)

The relative case (*avnrel*) covers the relative pronouns *die* and *dat* (*diedatrel*) in an independent relative clause (i.e. *rel* is not equal to *mod*).

* **Schlichting**: "Aanwijzend Voornaamwoord: 'die', 'dit', 'deze', 'dat' zelfstandig gebruikt." Fully covered.


.. _T007_B:

T007: B
"""""""


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

The definition of this macro is as follows::

    Tarsp_B = """(
                  ((((@rel="mod" or @rel="ld" or @rel="predm") and
                     (not(@cat) or @cat!="conj") and
                     (not(@pt) or @pt!="tsw")
                    )or
                    (%predcB%)
                   ) and
                   (../node[@pt="ww" and @rel="hd"])
                  ) or
                  ((@pt="vz" or @pt="bw" or %Rpronoun%) and (@rel="dp" or @rel="--" or @rel="nucl" or @rel="body") and %notonlyrealnode%) or
                  (@cat="pp" and (@rel="--" or @rel="dp") and %notonlyrealnode%) or
                  (@rel="pc" and ../node[@rel="hd" and %locverb%]) or
                  (@rel="cnj" and parent::node[@rel="mod" or @rel="ld" or @rel="predm"]) or
                  (@rel="mod" and @pt="bw" and parent::node[@cat="np"] ) or
                  %Tarsp_nonmodadvcp% or
                  %Tarsp_pc_vc_exception%
                 )"""

Explanation: Adverbial modifiers are:

* Case 1:

    * Nodes with grammatical relation  *mod*, *ld* or *predm*
        * but if the node is a phrase, it should not have the value *conj* for the attribute *cat*. In a conjunction the whole conjunction is not considered an adverbial modifier. The individual conjuncts are, see below.
        * if the node is a word, it should not be an interjection

    * Nodes that meet the conditions of the macro **predcB**. This macro is defined below.

  but only if they modify a verb
* Case 2: adpositions, adverbs and R-pronouns that bear one of the relations *dp*, *--*, *nucl* or *body*, if they are not the only real node in the structure. The macro **notonlyrealnode** is defined below.
* Case 3: adpositional phrases with grammatical relation *dp* or *--* if they are not the only realnode
* Case 4: adpositional complements to a verbs that meets the requirements of the macro **locverb**. Verbs that have a locative interpretation often also have use where they are combined with a particular adposition (e.g. *staan + op*). This often leads to an ambiguity, and Alpino very often selects the *pc* analysis. However, very young children do not know these uses yet, but almost always intend the locative use. This part of the query corrects for Alpino's disambiguation strategy.
* Case 5: A conjunct if its parent node has a grammatical relation from *mod*, *ld* or *predm*
* Case 6: adverbs that are a modifier inside an NP. Probably because Alpino analyses ambiguous cases by including the adverb in the NP.
* Case 7: nodes that meet the requirements of the macro **Tarsp_nonmodadvcp**.
* Case 8: nodes that meet the conditions of the macro **tarsp_pc_vc_exception**. See section :ref:`generatemacros`




The macro **predcB** is defined as follows::

    predcB = """(@rel="predc" and
                 (@pt="adj" or @pt="bw" or @cat="ap" or @cat="advp") and
                 ../node[@rel="obj1"]
                )"""

The idea is that *predc* nodes that do not occur with a copula are covered here.

The macro **notonlyrealnode** is defined as follows::

    notonlyrealnode = """(parent::node[count(node[%realnode%])>1])"""

where **realnode** excludes interpunction signs, interjections, or nodes without any pos or category label:

    realnode = """((not(@pt) or (@pt!="let" and @pt!="tsw")) and (not(@postag) or @postag!="NA()"))"""


The macro **locverb** is defined as follows::

   locverb = """(@lemma="staan" or @lemma="zitten" or @lemma="rijden" or
                 @lemma="vallen" or @lemma="doen" or @lemma="gaan" or
                 @lemma="komen" or @lemma="zijn"  or %locmodalverb% )"""
   locmodalverb = """ (@lemma="kunnen" or @lemma="moeten" or
                       @lemma="hoeven" or @lemma="willen" or
                       @lemma="mogen")"""

The macro **Tarsp_nonmodadvcp** is defined as follows::

  Tarsp_nonmodadvcp = """(@cat="cp" and
                          (@rel="dp" or @rel="--") and
                          node[@pt="vg" and @conjtype="onder" and
                               fBas@lemma!="dat" and @lemma!="of" ] )"""

covering cp-nodes that could not be integrated in the whole structure (hence relation *dp* or *--*) and contain a subordinate conjunction other than *dat* or *of*.


* **Schlichting**: "De bijwoordelijke bepaling zegt iets over de hele inhoud van de zin of iets over het werkwoord, een bijwoord of een bijvoeglijk naamwoord. Een zin kan meer dan één bijwoordelijke bepaling hebben." Basically covered.

* **Remark** The **locverb** macro very probably has overlap with or is subsumed by the generated macro **Tarsp_pc_vc_exception**
* **Remark** Case 5 does not cover conjuncts under a node *conj* that meets the requirements of **predcB**, e.g *ik vind haar* **mooi en aardig**
* **Remark** The macro **predcB** does not cover cases where the object is absent due to topic drop (e.g. *vind ik* **mooi**). We could include a condition which includes cases where surely non-copular verbs (such as *vinden*) are listed, as was done in ASTA.

T010: BBBv
""""""""""


* **Name**: BBBv. (Bijwoord + Bijwoord + Bijvoeglijk woord, adverb + adverb + adjective)
* **Category**: Woordgroepen
* **Subcat**: Ov
* **Level**: Wg
* **Original**: yes
* **In form**: no
* **Page**: 70
* **Implementation**: Xpath
* **Query** defined as::

    //node[@cat="ap" and
    node[@rel="mod" and (@cat="ap" or @cat="advp") and
        node[@rel="mod" or @rel="me" ] and
        node[@rel="hd" ] and count(.//node)=2] and
    node[@rel="hd" and @pt="adj"] and count(node) =2]


* **Schlichting**: "Bijwoord + Bijwoord + Bijvoeglijk Woord. Deze constructie heeft een Bijvoeglijk woord als kern. Het is eigenlijk een BBv/B voorafgegaan door een bijwoord.

The first adverb is analysed as a modifier or measure expression of the second adverb. Together they form a phrase of category *ap* or *advp* that cooccurs with a head *adj*. Both phrases mentioned can contain only two nodes as children. This analysis contradicts the analysis by Schlichting, which suggest that the first adverb modifies the combination of the second adverb with the adjective. But an analysis that matches with the query given seems the most plausible analysis for the second example (*hij is veel te hoog*). As for the first example (*een kindje is nog te klein voor*), a more plausible analysis has *nog* as a sentential modifier, and that is how Alpino analyses it.


T011: Bbijzin
"""""""""""""


* **Name**: Bbijzin. Bijwoordelijke Bijzin (adverbial subordinate clause)
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Sz
* **Original**: yes
* **In form**: yes
* **Page**: 57
* **Implementation**: Xpath
* **Query** defined as::

    //node[@rel="mod"and
           @cat="cp" and
           node[@rel="body" and node[@pt="ww" and @pvagr and @rel="hd"]]]


* **Schlichting**: "Bijwoordelijke bijzin met verbindingswoord. Dit is dus een ondergeschikte zin die in de hoofdzin de functie van bijwoordelijke bepaling heeft. Het verbindingswoord is in deze Fase meestal *als*",.

A straightforward query for a cp ("complementizer phrase") with grammatical relation *mod*. The condition that the *body* must contain a finite verb is necessary because a *cp* can also have other phrases (e.g. *np*) as complement.



T012: BBv/B
"""""""""""


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

This query is straightforward implementation of an adverb modifying an adjective or adverb functioning as a head. It makes use of the macro *adjoradv* (twice), which is defined as follows:

* adjoradv = """(@pt="bw" or @pt="adj" or (@pt="vnw" and (@pos="adj" or @pos="adv")))"""

The macro covers not only words with the value *adj* or *bw* for *pt* but also words with *pt=vnw* where the Alpino *pos* attribute has the value *adj* or *adv*. The latter is needed for a word such *veel* and for R-words such as *daar*.

* **Schlichting**: "Bijwoord + Bijvoeglijk woord of Bijwoord. De eerste B is vaak een bijwoord van graad, of zegt in ieder geval iets van het tweede woord in deze woordgroep. Het tweede woord is meestal cde kern van de woordgroep."


T013: BBvZn
"""""""""""


* **Name**: BBvZn.
* **Category**: Woordgroepen
* **Subcat**: Ov
* **Level**: Wg
* **Original**: yes
* **In form**: no
* **Page**: 70
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**




* **Schlichting**: "Bijwoord + Bijvoeglijk woord + Zelfstandig naamwoord"




T014: BBX
"""""""""


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


The macro **Tarsp_BBX** is defined as follows::

    Tarsp_BBX = """((@cat="top" and
                     count(.//node[@pt!='let' and @pt!='vg'])=3 and
                     count(.//node[@special="er_loc" or @pt="bw" or
                                   @pt="vz" or (@pt="adj" and @rel="dp" ) ])=2 and
                          .//node[@pt="n" or (@pt="vnw" and not(@special="er_loc")) ]
                    ) or
                    ((@cat="sv1" or @cat="smain") and not(%basicimperative%) and
                      not(%ynquery%) and not(%Ond%) and  %Tarsp_W% and
                      count(.//node[%Tarsp_B%]) = 2 and %realcomplormodnodecount% = 2
                    )
                   )"""

Explanation: there is match if either cas 1 holds or Case2:

* Case 1: the utterance contains:

    * anywhere in the stucture exactly 3 real nodes, and
    * anywhere in the structure 2 adverbs, adverbial pronouns, adpositions, or grammatically isolated (*rel* = *dp*) adjectives, and
    * anywhere in the structure a noun, or a pronoun that is not an R-pronoun

* Case 2: there is a clause with category *sv1* or *smain*

    * that is not an imperative clause, and
    * that is not  yes-no question,  and
    * that does not contain a subject, and
    * that does contain a head verb, and
    * that does contain 2 adverbial modifiers, and
    * that contains exactly 2 real complements or modifiers

* **Schlichting**: "Bijwoordelijke bepaling + Bijwoordelijke bepaling + een ander zinsdeel (Ond of W of VC of B)"



T015: BepBvZn
"""""""""""""


* **Name**: BepBvZn.
* **Category**: Woordgroepen
* **Subcat**:
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 71
* **Implementation**: Xpath
* **Query** defined as::

    //node[@cat="np" and
           node[@rel="det" ] and
           node[@rel="mod" and @pt="adj"] and
           node[@rel="hd" and @pt="n"]
          ]


Straightforward implementation of noun phrase with a determiner, a modifying adjective and a head noun

* **Schlichting**: "Bepaler + Bijvoeglijk woord + Zelfstandig naamwoord"

* **Remark**: does not cover numerals, which also fall under "bijvoeglijk". Probably best to make a macro for "bijvoeglijk woord"
* **Remark**: restrict this to exactly 3 nodes under NP.




T016: BepZnBv
"""""""""""""


* **Name**: BepZnBv.
* **Category**: Woordgroepen
* **Subcat**: Ov
* **Level**: Wg
* **Original**: yes
* **In form**: no
* **Page**: 70
* **Implementation**: Xpath
* **Query** defined as::

    //node[(@cat="ap" or @cat="advp") and node[(@rel="mod" or @rel="me") and @cat="np"]]


* **Schlichting**: "Bepaler + Zelfstandig naamwoord + Bijvoeglijk woord. Soms vindt men een Zn op de plaats van de Bv: *een heleboel water*"

 The current query covers both adjectives and adverbs. Unclear whether that is necessary or desired.

* **Remark**: The  example **een heleboel water** is not covered by this query
* **Remark**: Currently any NP is allowed, this should be restrcted to an NP with only two nodes (determiner or modifier + head)


T017: BezZn
"""""""""""


* **Name**: BezZn.
* **Category**: Woordgroepen
* **Subcat**:
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 68
* **Implementation**: Xpath
* **Query** defined as::

    //node[@cat="np" and
    node[@pdtype="det" and @rel="det" and @positie="prenom"  and @vwtype="bez" and @pt="vnw" ] and
    node[(@pt="n"  or (@pt="adj" and @positie="nom")) and @rel="hd"]]

Straightforward implementation. Also covers substantivised adjectives as a head.

* **Schlichting**: "Bezittelijke voornaamwoord + Zelfstandig naamwoord"

* **Remark**: according to the query, the  NP can consist of more than just the possessive pronoun and the noun. This should be restricted

T018: Bijvoeglijke Bijzin
"""""""""""""""""""""""""


* **Name**: Bijvoeglijke Bijzin.
* **Category**:
* **Subcat**:
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**:
* **Implementation**: Xpath
* **Query** defined as::

    //node[@rel="mod"and @cat="rel" and parent::node[node[@pt="n" and @rel="hd"]]]

We have assumed that this involves relative clauses.

* **Schlichting**: Though "bijvoeglijke bijzin" is mentioned with T020 (p. 53-54) there is to our knowledge no separate description of them.

* **Remark**: Should *whrel* be included here as well, perhaps with a condition that there is also a noun or subtantivised adjective as antecedent?


T019: Bijwoordelijke bepalingwoordgroep
"""""""""""""""""""""""""""""""""""""""


* **Name**: Bijwoordelijke bepalingwoordgroep.
* **Category**: Uitbreiding Zinsdelen
* **Subcat**:
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 75
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**




* **Schlichting**: "Bijwoordelijke bepalingwoordgroep"




T020: Bijzin z Verb
"""""""""""""""""""


* **Name**: Bijzin z Verb.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 53;54
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**




* **Schlichting**: "Bijzin zonder verbindingswoord. De bijzinnen kunnen Bijwoordelijke bijzinnen zijn, VC bijzinnen of Bijvoeglijke bijzinnen."




T023: Bv/B
""""""""""


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

These are single word utterances consisting of an adjective or an adverb, and based on the examples that Schlichting gives (such as *uit*, *op*) adpositions should be included as well. (*uit* is parsed as an adverb by Alpino, but *op* as an adposition).

The condition to restrict it to single word utterances uses the macro *realnode*, which is defined as follows::

    realnode = """((not(@pt) or (@pt!="let" and @pt!="tsw")) and (not(@postag) or @postag!="NA()"))"""

It excludes interpunction symbols, interjections and words not classified for DCOI part of speech by Alpino (i.e., where *postag=NA()*),



* **Schlichting**: "Bijvoeglijke naamwoorden en Bijwoorden"

* **Remark**: R-pronouns (such as *daar*, explictly mentioned by Schlichting) are not covered yet. Perhaps use the macro *adjoradv* here.


T024: Bv z e
""""""""""""


* **Name**: Bv z e.
* **Category**: Woordstructuur
* **Subcat**:
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 87;88
* **Implementation**: Xpath
* **Query** defined as: **not implemented yet**


It is not clear whether predicative adjectives should be covered by this as well. We assume not. Schlichting only discusses attributive uses and only gives examples of attributive uses. A query could be::

    //node[@pt="adj" and @buiging="zonder" and
           (@rel="mod" and
           parent::node[@cat="np" and node[@rel="hd" and (@pt="n" or(@pt="adj" and @positie="nom"))]])]

covering attributive adjectives modifying a noun or a substantivised adjective.     The phenomenon  occurs only once in the VKLTarsp dataset (sample 6, utterance 25) but it has not been annotated as such. It does not occur in [Schlichting 2017].



* **Schlichting**: "Bijvoeglijk naamwoord zonder 'e'-uitgang"



T025: BvBepZn
"""""""""""""


* **Name**: BvBepZn.
* **Category**: Woordgroepen
* **Subcat**:
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 69
* **Implementation**: Xpath
* **Query** defined as::

    //node[@cat="np" and
           node[@rel="det"] and
           node[@rel="mod" and @pt="bw" and (not(@special) or @special!="er")] and
           count(node)=3]


Straightforward implementation, some remarks:

* the conditions on the *special* attribute are intended to exclude adverbial pronouns
* there is no condition on the head. Perhaps a condition allowing only nouns and substantivised adjectives should be added (or should substantivised infinitives be included as well?)
* there is no specific condition on the adverb (e.g. no mention of *nog*), Schlichting's criterion "als het gevolgd kan worden door een telwoord" is difficult to implement.

* **Schlichting**: "Bijvoeglijk woord + bepaler + Zelfstandig naamwoord. Het bijvoeglijk woord is meestal ‘nog’. We beschouwen ‘nog’ alleen als bijvoeglijk woord als het gevolgd kan worden door een telwoord."




T027: BvZn
""""""""""


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


* **Schlichting**: "Bijvoeglijk woord + Zelfstandig naamwoord. Onder een Bijvoeglijk woord (nota bene niet een ‘bijvoeglijk naamwoord’) verstaan we woorden die een eigenschap of een hoeveelheid aangeven:

1.    Bijvoeglijke naamwoordem, bijv. ‘grote’, ‘andere’
2.    Telwoorden, bijvoeglijk gebruikt, bijv. ‘twee’, ‘eerste’
3.    Bijvoeglijke woorden die een hoeveelheid aangeven, bijvoorbeeld ‘meer’, ‘veel’. Ook ‘nog’ wordt tot deze groep van bijvoeglijke woorden gerekend, namelijk dan wanneer het gevolgd kan worden door een telwoord: ‘nog auto’ is dus BvZn"

The query is defined using the macro *BvZn*, which is defined as follows::

      BvZn = """ (count(node)=2 and
                  (  (%headn% and (%coreadjmod% or %corevnwmod% or %corebwmod%))

                  )
                 )
             """


in which four other macros are used:

* **headn**: simple head noun::

     headn = """ ( node[@rel="hd" and @pt="n"] )"""

* **coreadjmod**: adjective or numerals as modifier (note that ordinal numerals are analysed as adjectives by Alpino)::

     coreadjmod = """ (node[@rel="mod" and ( @pt="adj" or @pt="tw")] and not(node[@rel="det"])) """

* **corevnwmod**: indefinite pronouns acting as determiner, excluding genitives such as *iemands*, and  *geen*::

    corevnwmod = """ (node[@rel="det" and
                     (@pt="tw" or (@pt="vnw" and @vwtype="onbep" and @naamval!="gen" and @lemma!="geen"))] )"""

* **corebwmod**: basically any modifying adverb that is quantificational in nature (by the macro **qbwlemma** (so far only *nog*)::

    corebwmod = """ (node[@rel="mod" and @pt="bw" and %qbwlemma%]) """

    qbwlemma = """ (@lemma="nog" ) """






T029: BWondBB
"""""""""""""


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



* **Schlichting**: "Onderwerp + Werkwoord + drie Bijwoordelijke bepalingen."

 Straigthforward implementation using of the macro **Tarsp_BWOndBB**, which is defined as follows::

    Tarsp_BWOndBB = """(%declarative% and %Ond% and
                       %Tarsp_W% and %Tarsp_B_X_count% = 3 and
                       %realcomplormodnodecount% = 4)"""



See section :ref:`composedmeasures` for details.

T030: BX
""""""""


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


Explanation: Alpino cannot deal very well with such structures. If there are additional interjections or interpunction signs, Alpino often creates additional structure (with nodes with category *du*), which makes formulating the query not easy. Furthermore, the X-part of BX can be a full constituent consisting of multiple words, so simple conditions on the number of words will not work here. Two cases are distinguished:

* Case 1: a match is found with a node with *cat* = *top* that does not contain a finite verb (**pv**) nor the word *niet* (*niet* is covered by a different language measure), and that does not contain at any depth a node with relation *dlink*: if such a node is present a full phrase or clause is present as well. If these conditions are met, several subcases are distinguished one of which must evaluate to True:

    * there must be exactly one  node anywhere in the structure with *cat* = *du*, containing exactly 2 realnodes (macro **realnode**), one of which is a single adverb (macro **singlewordbw**, see below)* and the other is a single word or a **corephrase**.  (example: *daar auto*), The macro **corephrase** is defined as follows::

        corephrase = """(@cat="np" or @cat="pp" or @cat="advp" or @cat="ap")"""


    * there is a child node that meets the requirements of the macro **bxnp1**::

        bxnp1 = """(@cat="np" and count(node)=2 and
                    node[@rel="hd" and @pt="ww"] and
                    node[@rel="mod" and @pt])"""

      i.e. a NP that contains a verb as a head and a word that modifies it, and nothing else (example: *even pakken .*).
    * there is  a node with *cat* = *du* that contains exactly one  **realnode** that meets the requirements of the macro **bxnp1**
    * there is a child node that meets the requirements of the macro **bxnp2**, i.e. a noun phrase consisting of a head and a single word  modifier, and nothing else (example: *die hier*)::

        bxnp2 = """(@cat="np" and count(node)=2 and node[@rel="hd"] and node[@rel="mod" and %singlewordbw%])"""

    * there is a node with *cat* = *du* that contains exactly one  **realnode** that meets the requirements of the macro **bxnp2**


* Case 2: the node meets the requirements of the macro **Tarsp_bnonfin**::

    Tarsp_bnonfin = """((@cat="inf" or @cat="ppart") and
                        @rel="vc" and
                        parent::node[@cat="smain" and count(node)=1] and
                        node[%Tarsp_B%] and node[@pt="ww" and @rel="hd"] and
                        count(node[%realcomplormod%])=1 )"""

  This covers cases where a nonfinite verbal complement is the only child of an *smain* category and contains only a head verb and an adverbial modifier (defined by macro **Tarsp_B**, see :ref:`T007_B`). Such structures can only arise after correction through the *smallclauses* module. (See :ref:`smallclauses`).

The macro **singlewordbw** is defined as follows::

    singlewordbw = """ (@pt="bw" or %Rpronoun% or %adjadv%)"""
    adjadv = """(@pt='adj' and (@lemma='wel'))"""

The macro **Rpronoun** simply lists all R-pronouns in a disjunction, and the **adjadv** macro is intended for words that are adverbs but analysed by Alpino (in some cases) as an adjective. So far, we only encountered this for *wel* (or was the **adjoradv** macro intended here?.


* **Schlichting**: "Bijwoordelijke bepaling + een ander Zinsdeel. Dit andere Zinsdeel kan zijn een W, een VC of een B. BW, BVC en BB staan namelijk niet apart op de profielkaart. In de praktijk worden hier ook zinnen gescoord met een B en een ander zinsdeel waarvan men niet weet of het een onderwerp of een VC is. De zin ‘die ook’ bijvoorbeeld, kan betekenen ‘die moet ook’ of ‘die moet je ook daar doen’. Zulke twijfelgevallen kunnen we hier dus ook scoren."
   * Basically covered. if noun or pronoun precedes the adverb SASTA analyses the utterance as a *OndB*, not as a *BX*. That corresponded best to the actual practice in the annotated data received.



T031: C
""""""""


* **Name**: C .
* **Category**: Zinsdelen
* **Subcat**:
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 43;44
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**



* **Schlichting**: "Complement. Een aanvulling van het gezegde. Het Complement kan zijn:

1.    Naamwoordelijk deel van het gezegde. Het naamwoordelijk gezegde bestaat uit een koppelwerkwoord en (meestal) een zelfstandig naamwoord of bijvoeglijk naamwoord. Voorbeelden Zij is *mijn zusje*, Ben je *moe*, Dat is *van hem*
2.    Bepaling van gesteldheid. Deze zegt iets van het werkwoord en van het lijdend voorwerp of het onderwerp. De bepaling van gesteldheid wordt ook wel ‘dubbelverbonden bepaling’ genoemd. Voorbeelden: Die ga ik *groen* kleuren, Dat vind ik *lekker*, hij heeft het *kapot* gemaakt, ik kan dat *alleen*

Bij de analyse worden Voorwerpen en Complementen alle twee ‘VC’ genoemd.
"





T032: de
""""""""


* **Name**: de.
* **Category**: Woordgroepen
* **Subcat**:
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 66
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@cat="np" and
           node[@rel="det" and @lemma="de"] and
           count(node)=2]



* **Schlichting**: "Bepaald lidwoord + enkelvoudig mannelijk of vrouwelijk Zelfstandig naamwoord of meervoudig Zelfstandig naamwoord. De constructies ‘in de mand’ en ‘naar het ziekenhuis’ worden gescoord bij VzBepZn èn bij ‘de’." Covered.



T033: die/dezeZn
""""""""""""""""


* **Name**: die/dezeZn.
* **Category**: Woordgroepen
* **Subcat**:
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 68
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@cat="np" and
           node[@pt="n" and @rel="hd"] and
           node[@pt="vnw" and @vwtype="aanw" and
                @rel="det" and
                (@lemma="die" or @lemma="deze")] and
           count(node)=2]


The query is self-explanatory.

* **Schlichting**: "Aanwijzend Voornaamwoord + Zelfstandig naamwoord in enkelvoud of meervoud". Covered.



T034: dit/datZn
"""""""""""""""


* **Name**: dit/datZn.
* **Category**: Woordgroepen
* **Subcat**:
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 71
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@cat="np" and
           node[@pt="n" and @rel="hd"] and
           node[@pt="vnw" and @vwtype="aanw" and
                @rel="det" and
                (@lemma="dit" or @lemma="dat")] and
           count(node)=2]


The query is self-explanatory.

* **Schlichting**: "Aanwijzend Voornaamwoord + onzijdig Zelfstandig naamwoord. Ook onjuist gebruik mag gescoord worden." Covered.




T035: een
"""""""""


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


The query is self-explanatory.

* **Schlichting**: "Onbepaald lidwoord + Zelfstandig naamwoord. Ook het onbepaalde lidwoord + Bijvoeglijke woord, gebruikt als Zelfstandig naamwoord, wordt hier gescoord, bijvoorbeeld ‘een andere’."

**Remark** Substantivised adjectives are not covered yet.

T036: en
""""""""


* **Name**: en.
* **Category**: Verbindingswoorden
* **Subcat**:
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 77
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@pt="vg" and @lemma="en" and @rel="dlink"]

This query is self-explanatory. The condition on *rel* excludes *en* in conjunctions.


* **Schlichting**: "Het verbindingswoord ‘en’ wordt in deze Fase gebruik om een zinsdeel of een zin te introduceren. In Fase VI wordt ‘en’ gebruikt om twee hoofdzinnen met elkaar te verbinden."




T037: er
""""""""


* **Name**: er.
* **Category**: Voornaamwoorden
* **Subcat**:
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 81
* **Implementation**: Xpath
* **Query** defined as::

    //node[@lemma="er"]


The query is self-explanatory. Note that the condition formulated in terms of the atribute *lemma* ensures that also variants of *er* such as *Er*, *d'r* and even *der* can be dealt with.

* **Schlichting**: "Dit ‘er’ heeft slechts in enkele gevallen het karakter van een voornaamwoord. Het kan als zinsdeel de functie hebben van een bijwoordelijke bepaling: ‘zij komt er wel’, ‘ik heb er nog drie’, of van een onderwerp, bv. In: ‘er stond een plant voor het raam’. Zo’n zin kan dan twee onderwerpen hebben (‘er’ is dan een zgn. plaatsonderwerp, het andere onderwerp is dan het getalsonderwerp, dat wil zeggen dat dat onderwerp in het meervoud kan komen te staan: ‘er staat een kind’, ‘er staan twee kinderen’)"




T038: geen X
""""""""""""


* **Name**: geen X.
* **Category**: Woordgroepen
* **Subcat**:
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 72
* **Implementation**: Xpath
* **Query** defined as::

    //node[@cat="np" and
           node[@pt="vnw" and @rel="det" and @lemma="geen"] and
           node[@pt="n" and @rel="hd"]]


The query is self-explanatory.

* **Schlichting**: "‘geen’ meestal gevolgd door een zelfstandig naamwoord"

* **Remark** perhaps the number of nodes should be restricted to 2? Though *geen N meer* should also be accepted


T039: hè
""""""""


* **Name**: hè.
* **Category**: Zinsconstructies
* **Subcat**: Vragen
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 59;60
* **Implementation**: Xpath
* **Query** defined as::

    //node[ @lemma="hè"]

The query is self-explanatory, but it is perhaps too broad. Occurrences of *hè* at the beginning of an utterance will also be scored now.

* **Schlichting**: "De naklank ‘hè’ in de betekenis van ‘vind je niet?’ of ‘dat vind je toch ook?’ maakt de voorafgaande uiting vragend."



T040: hem
"""""""""


* **Name**: hem.
* **Category**: Voornaamwoorden
* **Subcat**:
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 82
* **Implementation**: Xpath
* **Query** defined as::

    //node[@lemma="hem" and @pt="vnw"]

The query is self-explanatory. It is crucial that the formulation is in terms of *lemma* (and not *word*), otherwise we will miss cases where the word is written with an initial capital (*Hem*) and reduced forms (*'m*).

* **Schlichting**: "Het persoonlijk voornaamwoord ‘hem’, gebruikt als voorwerp.". Covered.



T041: het
""""""""""


* **Name**: het .
* **Category**: Voornaamwoorden
* **Subcat**:
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 80
* **Implementation**: Xpath
* **Query** defined as::

    //node[@lemma="het" and @pt='vnw' ]

The query is self-explanatory. The condition that the *pt* is equal to *vnw* excludes occurrences of *het* as an article (because then *pt* = *lid*). The check on the lemma form allows also reduced forms (*'t*) and occurrences where the word contains capital characters (e.g. *Het*).

* **Schlichting**: "Persoonlijk voornaamwoord ‘het', onder andere als lijdend voorwerp en als onderwerp." Covered.




T042: hetZn
"""""""""""


* **Name**: hetZn.
* **Category**: Woordgroepen
* **Subcat**:
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 71
* **Implementation**: Xpath
* **Query** defined as::

    //node[@cat="np" and
           node[@pt="lid" and @rel="det" and @lemma="het"] and
           node[@rel="hd" and @pt="n"]]

The query is self-explanatory.
* **Remark** We shoud add a condition so that only these two elements are allowed inside the NP.

* **Schlichting**: "Bepaald lidwoord + onzijdig Zelfstandig naamwoord. Ook onjuist gebruik mag gescoord worden. De constructie ‘naar het strand’ wordt gescoord bij VzbepZn èn bij hetZn."



T043: hij
"""""""""


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

The query is self-explanatory. The condition formulated in ters of *lemma* allows reduced forms (*ie*, even *tie* and *-ie*) and occurrences with capital letters (*Hij*)


* **Schlichting**: "‘hij’ en ‘ie’ worden op de profielkaart beide bij ‘hij’ gescoord. ‘ie’ komt vaker voor dan ‘hij’ in deze Fase."


.. _T044_Hwwi:

T044: Hww i
"""""""""""


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

The macro **Tarsp_Hwwi** is defined as follows::

    Tarsp_Hwwi = """(( @pt="ww" and @rel="hd" and @wvorm="pv" and
                       %Tarsp_hww% and
                       ((parent::node[node[@cat="inf"and @rel="vc"]]) or
                        (parent::node[node[@pt="ww" and @rel="vc" and @wvorm="inf"]])
                       )
                      ) or
                      %robusthwwi%
                    )"""

Explanation:

The core case can be described as follows:

* We look for a finite verb acting as a head
* that is an auxiliary verb (macro **Tarsp_hww**)
* and cooccurs with a verbal complement (*rel* = *vc*) that is either an infinitval phrase (*cat* = *inf*) or a bare infinitive (*wvorm* = *inf*)

There is also a second case, for robustness (i.e. if Alpino misanalysed), with the macro **robusthwwi**, defined as follows::

    robusthwwi = """ (@cat="top" and
                      .//node[@pt="ww" and %Tarsp_hww% and @wvorm="pv" and (@rel="--" or @rel="dp")] and
                      .//node[@pt="ww" and @wvorm="inf" and (@rel="--" or @rel="dp")]
                     )"""

This macro searches for a misanalysed (*rel* equal to *--* or *dp*) finite auxiliary verb anywhere in the structure, in combination with a misanalysed infinitive verb anywhere in the structure.


* **Schlichting**: "Hulpwerkwoord gevolgd door een infinitief oftewel het hele werkwoord. De volgende werkwoorden rekenen we tot de hulpwerkwoorden; enkele worden verschillende malen genoemd:

1.    Hebben, zijn, zullen (hulpww van tijd|)
2.    Gaan, komen, zijn, blijven, zitten, liggen lopen, staan (aspect)
3.    Worden, zijn (lijdende vorm)
4.    Kunnen, zullen, mogen, moeten, willen, laten, hoeven, (be)horen (modaliteit)
5.    Doen en laten (causaliteit)
6.    Doen (omschrijving)

De hulpwerkwoorden die gevolgd worden door een infinitief worden niet gescoord bij HwwZ, Stam of Stam+t".


**Remark**: the auxiliary verbs that take *te* plus infinitive are not covered yet

**Remark**: should we count *zitten*, *staan*, *liggen*, etc.  as HwwZ when not followed by infinitive or *te* + infinitive?


T045: Hww Vd
""""""""""""


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

The core case of the query searches for one of the verbs *hebben*, *worden* or *zijn* in combination with a verbal complement that is either a participial phrase (*ppart*) or a bare participle (*wvorm* = *ppart*).

There is also a robust case (macro **robusthwwvd**)::

    robusthwwvd = """ (@cat="top" and
                       .//node[@pt="ww" and %vdhwws% and @wvorm="pv" and (@rel="--" or @rel="dp")] and
                       .//node[@pt="ww" and @wvorm="vd" and (@rel="--" or @rel="dp")]
                      )"""

This macro searches for a misanalysed (*rel* equal to *--* or *dp*) finite auxiliary verb that takes a participial clause (macro **vdhwws**) anywhere in the structure, in combination with a misanalysed participial verb anywhere in the structure. The macro **vdhwwws** is defined as follows::

    vdhwws = """(@lemma="hebben" or @lemma="zijn" or @lemma="worden")"""



* **Schlichting**: "Hulpwerkwoord gevolgd door het Voltooid deelwoord. Hulpwerkwoord + Voltooid deelwoord komt voor bij de voltooide tijd ('jij hebt gemaakt'). Het Voltooid deelwoord wordt apart bij de Woordstructuur gescoord. ook voltooid verleden tijd ('jij had gemaakt') kan hier gescoord worden. dan wordt eveneens bij Verleden tijd en bij Voltooid deelwoord gescoord. Het hulpwerkwoord wordt niet gescoord bij Woordstructuur." Fully covered.

* **Remark** The macro **vdhwws** should also be used in the core case of this query.




T046: HwwZ
""""""""""


* **Name**: HwwZ.
* **Category**: Woordstructuur
* **Subcat**:
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 84-85
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%Tarsp_HwwZ%]



The macro **Tarsp_HwwZ** is defined as follows::

    Tarsp_HwwZ = """(@pt="ww" and @rel="hd" and @wvorm="pv" and
                     ((%Tarsp_hww% or @lemma = "hebben") and
                      not(%Tarsp_vc_sibling%)
                     ) or
                     (@lemma="zijn" and not(%Tarsp_vc_sibling%) and %Tarsp_ld_sibling% )
                    )"""

The query searches for finite forms of a head verb and distinguishes two subcases:

* the finite form is a form of one of the auxiliary verbs that take an infinitival complement, or of the verb *hebben*: in this case no *vc* complement should be present, which is achieved by negting the **Tarsp_vc_sibling** macro, defined as follows::

    Tarsp_vc_sibling = """parent::node[ node[@rel="vc"]]"""

* the finite form is a form of the verb *zijn*: in this case a *vc* complement must be absent but an *ld* sibling must be present. This has been done to exclude regular copular uses of the verb *zijn* (when combined with an adjective (phrase) or noun (phrase) predicate. The presence of the *ld* sibling is ensured by the **Tarsp_ld_sibling** macro::

    Tarsp_ld_sibling = """parent::node[ node[@rel="ld"]]"""


* **Schlichting**: "Hulpwerkwoord Zelfstandig gebruikt. De eerste persoonsvorm die door de kinderen na het koppelwerkwoord geleerd wordt is de tegenwoordige tijd enkelvoud van het hulpwerkwoord, 'zelfstandig' gebruikt, 'Zelfstandig' betekent in dit verband dat het hulpwerkwoord niet gevolgd wordt door een hoofdwerkwoord. Tot deze 'zelfstandig' gebruikte hulpwerkwoorden rekenen we: *blijven, doen, gaan, hebben, hoeven, horen, komen, kunnen, laten, liggen, lopen, moeten, mogen, staan, willen, worden, zijn, zitten, zullen*". The list provided here is identical to the list provided under T044 (see :ref:`T044_Hwwi`),  except that *behoren* is not explicitly mentioned, plus the auxiliaries *hebben*, *zijn* en *worden*." Covered.
   * "Wanneer het hulpwerkwoord wordt gevolgd door een onbepaalde wijs (bijvoorbeeld; 'ik wil fietsen') of door een onvoltooid deelwoord (bijvoorbeeld: 'ze heeft geroepen') wordt het hier niet gescoord (zie Hww i, Fase III en Hww Vd, Fase IV)." Covered
   * "Wanneer het 'zelfstandig'gebruikte hulpwerkwoord in het meervoud staat (bijvoorbeeld: 'nou gaan we') wordt het niet hier gescoord maar bij het Meervoud van de Tegenwoordige Tijd." Not covered
   * "Wanneer het 'zelfstandig' gebruikte hulpwerkwoord in de verleden tijd staat (bijvoorbeedl: 'dat deed jij') wordt het niet hier gescoord maar bij de Verleden tijd." Not Covered
   * "De hulpwerkwoorden die hier gescoord worden, behoeven niet gescoord te worden bij Stam of Stam + t."See under *Stam* and *Stam + t*

* **Remark** the uncovered cases can be improved by adding the following condition: @pvagr!="mv" and @pvtijd!="verl"


T047: ik
""""""""


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

The query is self-explanatory. The condition formulated in terms of *lemma* (instead of *word*) also allows variants in case (*Ik*), reduced variants (*'k*, *k*) en emphasised variants (*ikke*)

* **Schlichting**: "Het persoonlijk voornaamwoord 'ik' wordt meestal in deze Fase ontwikkeld" (It involves Stage III).



T048: Into
""""""""""


* **Name**: Into.
* **Category**: Zinsconstructies
* **Subcat**: Vragen
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 59
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**


Though it is trivial to implement this by looking for the presence of a question mark or exclamation mark, the use of these annotations by annotators appears to be qufaantekeninite inconsistent.


* **Schlichting**: "In Fase II stellen de kinderen alleen vragen door een vraagintonatie te gebruiken. Bij het uitschrijven van het sample wordt die intonatie aangegeven door een vraagteken. Bij het analyseren van een uiting die alleen vraagintonatie heeft maar niet de vorm van de vraag analyseren we de uiting eerst als Mededelende Zin; de aantekening intonatie komt er extra bij. Vraag-Intonatie is dus een extra scoring "





T049: Inv
"""""""""


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
            node[@pt="ww" and @rel="hd" and (not(@stype) or @stype!="imparative") ] and
            node[@rel="su" and number(@end)>../node[@rel="hd"]/@end]
           ) or
           %robustinversion%]

The core case of this query looks for

* *sv1* nodes not dominated by a *whq* node or *smain* node
* that are not imperatives
* in which the finite verb precedes the subject.

The robust case has been implemented by the macro **robustinversion**, defined as follows::

   robustinversion = """(@cat="top" and
                         .//node[@pt="ww"  and @wvorm="pv" and  @rel!="hd" and
        						 (not(@stype) or @stype!="imparative")] and
                         .//node[@pt="vnw" and @naamval="nomin" and @rel!="su" and
                                 @end>..//node[@pt="ww" and @wvorm="pv"]/@end])"""

It searches for wrongly analyzed structures  (cf. the conditions on the grammatical relations) that contain:

* anywhere a non-head finite verb that is not marked for *stype* = *imparative* (Alpino  indeed uses this misspelling of *imperative* as value)
* anywhere a non-subject nominative pronoun
* where the pronoun precedes the verb

* **Schlichting**:
    "Hiermee wordt bedoeld de inversie of omkering van persoonsvorm en onderwerp. In de eerste constructie met onderwerp en persoonsvorm die zij leren, gebruiken de kinderen de volgorde onderwerp - persoonsvorm. heel spoedig daarna leren ze de inversievolgorde"

    Inversie hoeft in principe niet elke keer dat het voorkomt gescoord te worden. Het is van belang dat men bij elke leerling die in de Grammaticale Ontwikkelingsfase III of hoger valt controleert dat het kind twee- of driemaal de inversievolgorde gebruikt. Fouten tegen de regel van inversie worden apart genoteerd, bijvoorbeeld achterop de profielkaart. Het is waarschijnlijk dat in Zuid-Nederland deze Inversie wat later wordt geleerd dan in Noord-Nederland"


* **Remark** It is probably best to restrict Inversion to declarative clauses only. We probably can best use the macro **declarative** for this. Currently we exclude wh-questions and imperatives, but not yes-no questions. That will also make the exclusion of imperatives better and consistent with other language measures.

.. _T050_jij:

T050: jij
"""""""""


* **Name**: jij.
* **Category**: Voornaamwoorden
* **Subcat**:
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 79
* **Implementation**: Xpath
* **Query** defined as::

    //node[@lemma="jij" or
          (@lemma="je"  and (@vwtype="pr" or @vwtype="pers") and (@rel="su" ))]

The reduced form *je* does not have *jij* as its lemma, probably because it is also a reduced form of *jou* and *jouw*. Its lemma is *je*.
The values of *vwtype* can be *pers* (personal pronoun, for *jij*) or *pr* (personal or reflexive pronoun, for *je*).

* **Schlichting**: "We vinden overwegend 'jij' in deze Fase; een enkele maal 'je'." (it concerns Stage III).

* **Remark** use of *jij* as a single word utterance, or as a single word as *dp*, *sat*, or *nucl* is not covered now.

T051: jou
"""""""""


* **Name**: jou.
* **Category**: Voornaamwoorden
* **Subcat**:
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 82
* **Implementation**: Xpath
* **Query** defined as::

    //node[(@lemma="je" or @lemma="jou") and
           (@vwtype="pr" or @vwtype="pers") and
           (@rel="obj1" or @rel="obj2")]

The query is self-explanatory.

* The lemma differs for *jou* and *je*, see also :ref:`T050_jij`
* The *vwtype* for *je* and *jou* differs, so both options must be allowed
* The condition on the *rel* attribute is to exclude the possessive pronoun *je*

* **Remark** It should be checked whether both a condition on *vwtype* and a condition on *rel* are needed
* **Remark**: the query does not account for cases where *jou* is the only word in an utterance, or the only word in a *dp*, *sat* or *nucl* node. Extension of the query is needed. Or when it is a *predc* (*als ik jou was*).

* **Schlichting**: "Het persoonlijk voornaamwoord 'jou' wordt zowel gebruikt als voorwerp als in bepalingen met een voorzetsel."




T052: Kop
"""""""""


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

The macro **Tarsp_Kop** is defined as follows::

    Tarsp_Kop = """(   @pt="ww" and @rel="hd" and not(%Tarsp_hww%) and

                     ((%Tarsp_predc_sibling% and not(%Tarsp_obj1_sibling%)) or
                      (@lemma="zijn" and not(%Tarsp_vc_sibling%)
					   and not(%Tarsp_ld_sibling%) and
					   not(%Tarsp_onlymodR_sibling%))
                     )
                   )"""


Explanation: a node is a copular verb if it is a verb acting as a head but not an auxiliary verb (**Tarsp_hww**), and

   * either it has a *predc* sibling (**tarsp_predc_sibling**) but no direct object (*obj1*) sibling (**Tarsp_obj1_sibling**), or
   * the lemma equals *zijn* and it has no *vc* sibling (**Tarsp_vc_sibling**), no *ld* sibling, and no Rpronoun as modifier if no predicate is present (**Tarsp_onlymodR_sibling**)

The *sibling* macros are defined as follows::

    Tarsp_vc_sibling = """parent::node[ node[@rel="vc"]]"""
    Tarsp_predc_sibling = """parent::node[ node[@rel="predc"]]"""
    Tarsp_obj1_sibling = """parent::node[ node[@rel="obj1"]]"""
    Tarsp_ld_sibling = """parent::node[ node[@rel="ld"]]"""
    Tarsp_onlymodR_sibling = """(parent::node[node[@rel="mod" and %Rpronoun%] and not(node[@rel="predc"])])"""

* **Remark** These definition could be simplified by replacing *parent::node[node* by *../node*

The definition of *zijn* as a copula does not require the presence of a predicate, it rather excludes complements and modifiers that indicate a  different usage of *zijn* (e.g., as an auxiliary verb, or as an independent verb of location). This has been done because in incomplete sentences or misanalysed sentences containing *zijn*, the most probable interpretation of *zijn* is  in most cases as a copula (with a left-out or unpronounced predicate).

The query does not list the copulas explicitly because there are many more copulas than traditionally assumed and also many more than [Schlichting 2005:47] mentions for child language (e.g. *gaan*, *aanvoelen*, *raken*, etc).



* **Schlichting**: "Koppelwerkwoord. We onderscheiden twee soorten gezegdes:"

    1. "Werkwoordelijke, bijvoorbeeld 'zij *werkt* 's morgens'"
    2. "Naamwoordelijke gezegdes, bijvoorbeeld 'hij *is tuinman*' en 'jij *bent moe*'."

       "Naamwoordelijke gezegdes bestaan uit een koppelwerkwoord en een naamwoordelijk deel van  het gezegde. Het koppelwerkwoord heeft niet veel betekenis van zichzelf. het vormt de koppeling tussen het onderwerp en het naamwoordelijk deel van het gezegde. Het meest gebruikte koppelwerkwoord, ook in de kindertaal, is 'zijn'. Andere voorkomende koppelwerkwoorden zijn 'worden', 'blijven' en 'lijken'.

       "Aanvankelijk wordt alleen de vorm 'is' nog gebruikt. Het Koppelwerkwoord wordt geanalyseerd als speciaal Zinsdeel 'W-Kop'en wordt apart bij de Zinsdelen in Fase II gescoord."

* **Note** In Sasta a copular verb is annotated by the code *Kop*, **not** by *W-Kop*. Since it is also a verb, two codes are used: *W,Kop*

T053: maar
""""""""""


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

The first part of this query is self-explanatory, the second part has been included because Alpino often analyses an sentence-initial *maar* as an adverb instead of conjunction

* **Schlichting**: "Het Verbindinsgwoord 'maar'. Dit wordt introducerend gebruikt en om twee hoofdzinnen te verbinden."



T054: Sv1
"""""""""


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


This is not a language measure of Tarsp, but it has been defined to identify verb-initial clauses (for development purposes)




T055: Mededelende Zin
"""""""""""""""""""""


* **Name**: Mededelende Zin.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 44;45
* **Implementation**: none
* **Query** defined as: **not implemented**


This is not really a language measure, but rather a class of language measures that apply to declarative sentences.





T056: mij
"""""""""


* **Name**: mij.
* **Category**: Voornaamwoorden
* **Subcat**:
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 81
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[(@lemma="me" or @lemma="mij") and
           (@vwtype="pr" or @vwtype="pers")]

* The lemma differs for *mij* and *me*, see also :ref:`T050_jij`
* The *vwtype* for *mij* and *me* differs, so both options must be allowed




* **Schlichting**: "Persoonlijk voornaamwoord 'mij', 'me', gebruikt als voorwerp en na een voorzetsel"




T057: MvTT
""""""""""


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

The query is self-explanatory.

* **Schlichting**: "Meervoud van de tegenwoordige Tijd. Het gaat hier om congruentie tussen Onderwerp en Werkwoord in het meervoud van de 1e, 2e en 3e persoon van de tegenwoordige tijd van het werkwoord, ook van het hulpwerkwoord. We bedoelen hier constructies als 'ze komen', 'wij spelen'. Het moet duidelijk zijn dat het werkwoord geen infinitief is. Ook de congruentie tussen persoonsvorm en naamwoordelijk deel van het gezegde wordt hier gescoord"


* **Remark** Though Schlichting refers to "congruentie"(agreement), the query can be formulated in terms of properties of the finite verb alone.

T058: MvZn
""""""""""


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


The query is self-explanatory.

* **Schlichting**: "Meervoudig Zelfstandig naamwoord. Zowel meervoudsvormen op '-en' als op '-s' komen voor. Wanneer kinderen een meervoud van de zelfstandige naamwoorden gebruiken betekent dit nog niet altijd dat zij de meervoudsregel begrepen hebben. Het woord 'schoenen' bijvoorbeeld kan heel goed alleen in het meervoud gebruikt worden door het kind. Daarom is het van belang dat men aantekent op de profielkaart welke meervoudsvormen men gevonden heeft. Zodra er een meervoudsvorm is gevonden van een woord dat waarschijnlijk ook in het enkelvoud is aangeboden, is het extra aantekenen niet meer nodig."

* **Remark** The plural forms are currently not put into the form, and it is not tracked whether a singular form has already occurred.


T059: Nabep
"""""""""""


* **Name**: Nabep.
* **Category**: Woordgroepen
* **Subcat**:
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 73
* **Implementation**: Xpath
* **Query** defined as::

    // node[@rel="mod" and
            (not(@lemma) or (@lemma!="ook" and @lemma!="dan")) and
            parent::node[@cat="np" and node[@rel="hd" and @pt!="ww"]] and
            @begin >= ../node[@rel="hd"]/@end]

Explanation:

* the node must be a modifier, and either a phrase, or if it is a single word it should not be *ook* or *dan*
* it must modify a head that is not a verb inside an NP
* the node must follow the head

* **Schlichting**: "In 'de grote plant' zijn 'de' en 'grote' bepalende woorden bij 'plant', in 'de plant met de grote bladeren'is 'met de grote bladeren'een bepaling bij 'plant, maar deze bepaling staat na het kernwoord. Dit noemen we een 'nabepaling'."

* **Remark** Alpino (incorrectly) analyses many verbless utterances as involving a nabepaling (e.g., *ladder hier*). We try to reanalyse these in the module :ref:`smallclauses`.




T060: Nevens
""""""""""""


* **Name**: Nevens.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Sz
* **Original**: yes
* **In form**: yes
* **Page**: 56
* **Implementation**: Xpath
* **Query** defined as::

    //node[node[@rel="cnj" and (@cat="smain" or @cat="sv1")] and
           node[@rel="crd" ]]


Explanation:

* the node must contain an smain or sv1 with grammatical relation *cnj*, and
* it must contain a coordinator


* **Schlichting**: "Nevenschikkende zin met Verbindingswoord, dus twee hoofdzinnen verbonden door 'en', 'maar', 'want', 'of', of 'dus'." Covered.




T061: Nevenschikkende
"""""""""""""""""""""


* **Name**: Nevenschikkende.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 54
* **Implementation**: Xpath
* **Query** defined as: **not implemented yet**

This is actually not a language measure but  subclass of "samengestelde zinnen".





T062: Ombep
"""""""""""


* **Name**: Ombep.
* **Category**: Woordgroepen
* **Subcat**:
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 74
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

Alpino does not analyse the only example given (*geen* ... *meer*) as single constituent. So far we did not encounter any examples. It does not occur in [Schlichting 2017].

* **Schlichting**: "Omsluitende bepaling: een gedeelte van de bepaling staat vóór  het kernwoord, een gedeelte erachter."



.. _T063_Ond:

T063: Ond
"""""""""


* **Name**: Ond.
* **Category**: Zinsdelen
* **Subcat**:
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 41
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%FullOnd%]

Here, **FullOnd** is defined as::

    FullOnd = """(%subject% or %erx%)"""


where **subject** (see :ref:`zinsdelen`) and **erx** are defined as::

    subject = """(@rel="su" and parent::node[(@cat="smain" or @cat="sv1" or @cat="ssub")])"""
    erx = """((@rel="mod" and @lemma="er" and ../node[@rel="su" and @begin>=../node[@rel="mod" and @lemma="er"]/@end]) or
              (@rel="mod" and @lemma="er" and ../node[@rel="su" and not(@pt) and not(@cat)])
             )
          """


The **erx** macro is to ensure that so-called *expletive er* also counts a subject. We implemented this in the following manner: *er* is considered (also) expletive (and thus must count as a subject):

* if it precedes the subject  (as in **er** *kwam iemand binnen*), or
* if there is an empty subject, to cover cases such as *wie zwom* **er**. Note that in *wie heeft* **er** gezwommen* this *er* is considered a subject because of the empty subject of the participial clause, which is perhaps not what we want.




* **Schlichting**: "Dit is de persoon of de zaak die de handeling van het werkwoord uitvoert. Wanneer het onderwerp van een zin in het meervoud staat, staat de persoonsvorm van die zin ook in het meervoud."



T064: OndB
""""""""""


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


Straightforward implementation::

    Tarsp_OndB = """(%Ond% and
                     node[%Tarsp_Basic_B%]  and
                     count(node) = 2)"""

See :ref:`smallclauses` for details.

* **Schlichting**: "Onderwerp + Bijwoordelijke Bepaling"



T065: OndBVC
""""""""""""


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


Straightforward implementation::


    Tarsp_OndBVC = """(%Ond% and
                       node[%Tarsp_Basic_B%]  and
                       node[%Tarsp_Basic_VC%]  and
                       count(node) = 3) """

See :ref:`smallclauses` for details.

* **Schlichting**: "Onderwerp + Bijwoordelijke Bepaling + Voorwerp of Complement"


T066: Onderbr
"""""""""""""


* **Name**: Onderbr.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 58
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

This is not really a language measure. It is rather an indication of how sentences containing an interruption by another sentence or phrase should be analysed.


* **Schlichting**: "Soms wordt de zin onderbroken met een korte zin of een Zinsdeel. Beide zinnen worden ook apart geanalyseerd"





T067: Onderschikkend: B
"""""""""""""""""""""""


* **Name**: Onderschikkend: B.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 42;55;56
* **Implementation**: Xpath with macros
* **Query** defined as::

     Tarsp_B = """(
                   ((((@rel="mod" or @rel="ld" or @rel="predm") and
                      (not(@cat) or @cat!="conj") and
                      (not(@pt) or @pt!="tsw")
                     )or
                     (%predcB%)
                    ) and
                    (../node[@pt="ww" and @rel="hd"])
                   ) or
                   ((@pt="vz" or @pt="bw" or %Rpronoun%) and
                    (@rel="dp" or @rel="--" or @rel="nucl" or @rel="body") and
                    %notonlyrealnode%) or
                   (@cat="pp" and (@rel="--" or @rel="dp") and %notonlyrealnode%) or
                   (@rel="pc" and ../node[@rel="hd" and %locverb%]) or
                   (@rel="cnj" and parent::node[@rel="mod" or @rel="ld" or @rel="predm"]) or
                   (@rel="mod" and @pt="bw" and parent::node[@cat="np"] ) or
                   %Tarsp_nonmodadvcp% or
                   %Tarsp_pc_vc_exception%
                  )

               """

The query distinguishes several subcases as alternatives (joined by *or*):

* Any node with one of the grammatical relations *mod*, *ld* or *predm* provided:

  * the category, if present, is not equal to *conj* (the individual conjuncts do count, see below.
  * if the node is for a word, the word should not be an interjection
  * it has a head verb as sibling

* Any adverbial predicate that has a head verb as sibling. Adverbial predicates are defined by the macro **predcB**::

    predcB = """(@rel="predc" and
                 (@pt="adj" or @pt="bw" or @cat="ap" or @cat="advp") and
                 ../node[@rel="obj1"]
                )"""

  so these are *predc* nodes with a direct object as sibling

* **Remark** We now miss cases where the object is absent due to  Topic drop (e.g. *vind ik goed*). Maybe replace it by disallowing real copulas.

* Any adpositon, adverb or Rpronoun not in a core grammatical relation but with any of the relations *dp*, *--*, *nucl*, *body* provided that they are not the only  realnode present, where a real node is any node that is not a interjection, interpunction sign or of unknown part of speech tag::

    realnode = """((not(@pt) or (@pt!="let" and @pt!="tsw")) and (not(@postag) or @postag!="NA()"))"""
    notonlyrealnode = """(parent::node[count(node[%realnode%])>1])"""

* Any *PP* with any of the grammatical relations *--* or *dp* if it is not the only real node.
* Any adpositional complement to a locative verb. Alpino analyses locative and directional complements to a locative verb often as an adpositional complement. That is often correct but not for very young children that Tarsp addresses. This part of the query corrects for that.
* Any conjunct (relation *cnj*) in a conjunction that bears the grammatical relation *mod*, *ld* or *predm*.
* Any adverb inside an NP with relation *mod*. This is especially for adverbs such as *ook*, *nog*, *niet*, *alleen*, but also for adverbs inside NPs with a substantivised verb as a head (e.g. *even pakken*).
* Adverbial clauses that occur independently (e.g. *als mama thuiskomt*), as defined by the macro **Tarsp_nonmodadvcp**::

      Tarsp_nonmodadvcp = """(@cat="cp" and (@rel="dp" or @rel="--") and
                              node[@pt="vg" and @conjtype="onder" and
                              @lemma!="dat" and @lemma!="of" ] )"""

* **remark** I am not sure that this should be kept. Maybe move it to Bbijzin

* Adpositional complements that should have been analysed as adverbial modifiers. Achieved by the macro **Tarsp_pc_vc_exception**, explained elsewhere (see section :ref:`generatemacros`).
     * **Remark** There is overlap with the condition on locative verbs above. It has to be found out how big the overlap is, and whether this can be simplified.

* **Schlichting**: "De bijwoordelijke bepaling zegt iets over de hele inhoud van de zin of iets over het werkwoord, een bijwoord of bijvoeglijk naamwoord. Een zin kan meer dan één bijwoordelijke bepaling hebben"





T068: Onderschikkend: VC
""""""""""""""""""""""""


* **Name**: Onderschikkend: VC.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 43-44;55
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%complement% and parent::node[(@cat="smain" or @cat="sv1" or @cat="ssub" or @cat="inf" or @cat="ppart") ]]

This is not a language measure that occurs in the form. The macro **complement** is defined as follows::

    complement = """((@rel="obj1" or @rel="obj2") or
                 (@rel="predc" and not(%predcB%)) or
                 (@rel="pobj1" and not(%pobj1B%) ) or
                 %verbalcomplement%
                )"""

    verbalcomplement = """(@rel="vc" and (@cat="cp" or @cat="whq" or @cat="whsub"))"""

    predcB = """(@rel="predc" and
               (@pt="adj" or @pt="bw" or @cat="ap" or @cat="advp") and
               ../node[@rel="obj1"]
             )"""

    pobj1B = """(@rel="pc" and ../node[@rel="hd" and %locverb%])"""

* **Remark** The differences with **Tarsp_VC** (see :ref:`zinsdelen`) should be studied, and we should probably make them equal. T068 has not been maintained systematically, so very likely **Tarsp_VC** is the best one.

* **Schlichting**: "Lijdend Voorwerp, Meewerkend Voorwerp en Voorzetselvoorwerp worden alle drie afgekort ot V. Dit betekent dat ze na de analyse alle drie onder V gescoord worden. Een Complement is een aanvulling van het gezegde. Het complement kan zijn: (1) naamwoordelijk deel van het gezegde; (2) bepaling van gesteldheid"

* **Remark** Schlichting's example 'Ik kan dat *alleen*' is not a complement, in my view, but a modifier (secondary predicate).


    Bij de analyse worden Voorwerpen (V) en Complementen (C) alle twee 'VC' genoemd. Dit doen we omdat het, vooral bij de tweewoordzinnen, niet altijd mogelijk is de Voorwerpen en de Complementen te onderscheiden. Bovendien wordt hierdoor het aantal constructies beperkt."




T069: Onderschikkende
"""""""""""""""""""""


* **Name**: Onderschikkende.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 54;55
* **Implementation**:
* **Query** not implemented

This is mot really a query, but rather a class of clauses: subordinate clauses.




* **Schlichting**: "Bijzinnen horen meestal bij een hoofdzin. Men kan een bijzin herkennen aan de plaats waar de persoonsvorm staat, dat is namelijk helemaal of bijna helemaal achteraan in de zin."




T070: Onderwerpswoordgroep
""""""""""""""""""""""""""


* **Name**: Onderwerpswoordgroep.
* **Category**: Uitbreiding Zinsdelen
* **Subcat**:
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 75
* **Implementation**: Xpath
* **Query** defined as::

    //node[@rel="su" and @cat]


* **Schlichting**: " Bij het behandelen van de Woordgroepen hebben we gezien dat een zinsdeel uitgebreid kan zijn tot een woordgroep."

* **Remark** We currently do not underline these phrases, nor do we circle the utterance id in the form.




T071: OndVC
"""""""""""


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

Straightforward implementation::


    Tarsp_OndVC = """(%Ond% and
                       node[%Tarsp_Basic_VC%]  and
                       count(node) = 2) """



where::

    Tarsp_BasicVCW = """(node[@pt="ww" and @rel="hd"] and
                         node[%Tarsp_Basic_VC%] and
                         count(%fillednode%)=2)"""

See section :ref:`smallclauses` for details.


* **Schlichting**: "Onderwerp + voorwerp of Complement"











T072: OndW
""""""""""


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


Straightforward implementation::

    Tarsp_OndW = """(%declarative% and
                    %Ond% and
                    (%Tarsp_W%  or node[%Tarsp_onlyWinVC%]) and
                    %realcomplormodnodecount% = 1 )"""

See section :ref:`composedmeasures` for details.

The only special part here is the macro **Tarsp_onlyWinVC**, defined as follows::

    Tarsp_onlyWinVC = """(@rel="vc" and node[@rel="hd" and @pt="ww" and %realcomplormodnodecount% = 0])"""


This covers cases in which the predicate is a nonfite verb. See :ref:`smallclauses` for clarification.

* **Schlichting**: "Onderwerp + Werkwoord"


T073: OndWB
"""""""""""


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


Straightforward implementation::

    Tarsp_OndWB = """(%declarative% and
                      %Ond% and
                      %Tarsp_W% and
                      %Tarsp_B_X%  and
                      %realcomplormodnodecount% = 2 )"""

See section :ref:`composedmeasures` for details.

* **Schlichting**: "Onderwerp + Werkwoord + Bijwoordelijke Bepaling"



T074: OndWBB
""""""""""""


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

Straightforward implementation::


    Tarsp_OndWBB = """(%declarative% and
                       %Ond% and
                       %Tarsp_W% and
                       %Tarsp_B_X_count% = 2 and
                       %realcomplormodnodecount% = 3)"""


See section :ref:`composedmeasures` for details.

* **Schlichting**: "Onderwerp + Werkwoord + Bijwoordelijke Bepaling + Bijwoordelijke Bepaling"



T075: OndWBVC
"""""""""""""


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

Straightforward implementation::


    Tarsp_OndWBVC = """(%declarative% and
                        %Ond% and
                        %Tarsp_W% and
                        %Tarsp_B_X% and
                        %Tarsp_VC_X% and
                        %realcomplormodnodecount% = 3 )"""


See section :ref:`composedmeasures` for details.

* **Schlichting**: "Onderwerp + Werkwoord + Bijwoordelijke Bepaling + lijdend voorwerp of voorzetselvoorwerp of Complement"

* **Remark** Should indirect objects not be included (we did, Schlichting does  not mention it, though she states that it hardly occurs on p. 53 in Stage V)?



T076: OndWVC
""""""""""""


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

Straightforward implementation::

    Tarsp_OndWVC = """(%declarative% and
                       %Ond% and
                       %Tarsp_W%  and
                       %Tarsp_VC_X% and
                       %realcomplormodnodecount% = 2 )
                   """

See section :ref:`composedmeasures` for details.

* **Schlichting**: "Onderwerp + Werkwoord  + lijdend voorwerp of voorzetselvoorwerp of Complement""




T077: OndWVCVC(X)
"""""""""""""""""


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

Straightforward implementation::

    Tarsp_OndWVCVCX = """(%declarative% and
                          %Ond% and
                          %Tarsp_W% and
                          %Tarsp_VC_X_count% = 2  and
                          %realcomplormodnodecount% <= 4 )"""


See section :ref:`composedmeasures` for details.

* **Schlichting**: "Deze constructie bestaat uit vier of vijf Zinsdelen: Onderwerp,+ Werkwoord + twee VC's (+ een ander Zinsdeel). De VC's zijn meestal lijdend voorwerp, bepaling van gesteldheid, of naamwoordelijk deel van het gezegde."



T078: Ov2
"""""""""


* **Name**: Ov2.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 48
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**



* **Schlichting**: " "





T079: Ov3
"""""""""


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


    Tarsp_Ov3 = """(%declarative% and
                   not(%Tarsp_OndWVC%) and
                   not(%Tarsp_OndWB%) and
                   not(%Tarsp_BBX%)and
                   not(%Tarsp_WBVC%) and
                   not(%Tarsp_OndB%) and
                   not(%Tarsp_OndVC%) and
                   %realcomplormodnodecount% = 2) """


The definition is straightforward, and mostly negative:

* declarative clauses
* with two complements or modifiers
* but not any of OndWVC, OndWB, BBX, WBVC, OndB, or OndVC

* **Schlichting**: "behalve de genoemde zeven constructirs in Fase III van de Mededelende zin vinden we nog enkele constructies die bestaan uit drie zinsdelen, die minder voorkomen."

* **Remark** **OndBVC** is missing here


T080: Ov7
"""""""""


* **Name**: Ov7.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 58
* **Implementation**: Xpath
* **Query** defined as: **not implemented yet**



* **Schlichting**: " "





T081: OvWg7
"""""""""""


* **Name**: OvWg7.
* **Category**: Woordgroepen
* **Subcat**:
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 74
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**




* **Schlichting**: " "




T082: OvVerb6
"""""""""""""


* **Name**: OvVerb6.
* **Category**: Verbindingswoorden
* **Subcat**:
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 78
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**



* **Schlichting**: " "





T083: Ov4
"""""""""


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

The macro **Tarsp_Ov4** is defined as follows::


    Tarsp_Ov4 = """(%declarative% and
                   %realcomplormodnodecount% = 3 and
                   not(%Tarsp_OndWBVC%) and
                   not(%Tarsp_OndWBB%) and
                   not(%Tarsp_OndWVCVCX%))"""


The definition is straightforward:

* declarative clauses
* with three complements or modifiers (and a verb as the fourth 'zinsdeel')
* but not any of *OndWBVC*, *OndWBB*, or *OndWVCVCX*.

* **Schlichting**: "Overige constructies mededelende zin Fase IV, bestaande uit vier Zinsdelen"



T084: Ov5
"""""""""


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

The macro **Tarsp_Ov5** is defined as follows::


    Tarsp_Ov5 = """(%declarative% and %realcomplormodnodecount% = 4 and
                    not(%Tarsp_VCWOndBB%) and
                    not(%Tarsp_OndWVCVCX%) and
                    not(%Tarsp_BWOndBB%) )"""

The definition is straightforward:

* declarative clauses
* with four complements or modifiers (and a verb as the fifth 'zinsdeel')
* but not any of *VCWOndBB*, *OndWVCVCX*, or *BWOndBB*.


* **Schlichting**: "overige constructies met vijf zinsdelen."



T085: Overige
"""""""""""""


* **Name**: Overige.
* **Category**: Voornaamwoorden
* **Subcat**:
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 82
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@lemma="alles"  or
           @lemma="niets" or
           @lemma="niks" or
           (@lemma="wat" and @vwtype= "onbep") or
           @lemma="u" or
           @lemma="ons"  or
           @lemma="zelf"]


* **Schlichting**: "*zelf*, *niets/niks*, *alles*, *ons*, *wat*, *u*"

* **Remark** We probably should exclude *ons* as a possessive pronoun here.




T086: SamZn
"""""""""""


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


* **Schlichting**: " "


.. _T087_Stam:

T087: Stam
""""""""""


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



* **Schlichting**: "Stam van het zelfstandig werkwoord (uitgezonderd die in de gebiedende Wijs)"

* the stem of the verb is identical to the present tense singular form first person: in DCOI features: @pvtijd="tgw" and @pvagr="ev"
* we must exclude auxiliary verbs that are scored under Hww i (p. 65), Hww Vd (p. 69) or Hww Z (p. 85)
* we must exclude the use of *kijk* as a V.U. We do so though the macro **Tarsp_kijkVU**. it basically allows any occurrence of *kijk* that does not have a PP complement or modifier, nor a *vc* complement::

    Tarsp_kijkVU = """(@pt="ww" and
                       @lemma="kijken" and
                       @wvorm="pv" and
                       @pvagr="ev" and
                       @pvtijd="tgw" and
                       not(../node[%Tarsp_pporvc%]))"""

    Tarsp_pporvc = """ (((@rel="pc" or @rel="mod" or @rel="ld") and @cat="pp")  or @rel="vc")"""




T088: Stam+t
""""""""""""


* **Name**: Stam+t.
* **Category**: Woordstructuur
* **Subcat**:
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 86
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@pt="ww" and @pvagr="met-t" and
           not(%Tarsp_hww% or
               @lemma = "hebben" or
               @lemma = "worden" or
               @lemma = "zijn"
              )
          ]



* **Schlichting**: "Stam van het zelfstandige werkwoord, gevolgd door een toegevoegde, hoorbare 't'."

The definition is straightforward:

* in D-Coi the value *met-t* is only applied in case there really is a 't' in addition to the stem (as in *hij loopt, hij doodt*, but not in *hij verlaat haar*). The 't' in *doodt* is "toegevoegd", but not "hoorbaar", SASTA counts it as as *Stam + t*. The samples support this: VKLtarsp 01 (*vindt*), VKLTarsp 07 (*houdt*), TD22 (*vindt*, 4x) are all marked as *Stam + t*
* Auxiliary verbs that are scored under Hww i (p. 65), Hww Vd (p. 69) or Hww Z (p. 85) should not be marked for Stam + t



T089: Sz2+
""""""""""


* **Name**: Sz2+.
* **Category**:
* **Subcat**:
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as::

       //node[@cat="top" and
	          count(.//node[@cat="smain" or @cat="cp" or @cat="whsub" or
			                @cat="rel" or @cat="whrel"  or @cat="whq" or @cat="whsub" or
                            ( @cat="sv1" and not(parent::node[@cat="whq"]))
                           ]
                    ) >= 2]

Unclear whether this measure exists at all.

* **Schlichting**: " "




T090: Sz3+
""""""""""


* **Name**: Sz3+.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Sz
* **Original**: yes
* **In form**: yes
* **Page**: 57
* **Implementation**: Xpath with macros
* **Query** defined as::

       //node[@cat="top" and
	          count(.//node[@cat="smain" or @cat="cp" or @cat="whsub" or
			        @cat="rel" or @cat="whrel"  or @cat="whq" or @cat="whsub" or
                    ( @cat="sv1" and not(parent::node[@cat="whq"]))
                             ]
                   ) >= 3]

The query counts the number of clauses in the whole tree. If 3 or more, a match is found. A node with *cat*=*sv1* can be a clause of a clause body. It is a clause body if dominated by a node with category *whq*, so *sv1* nodes are counted in only if they are not dominated by a node with category *whq*.


* **Schlichting**: "Samengestelde zin die bestaat uit drie of meer zinnen. Dit kunnen drie hoofdzinnen zijn of een combinatie van hoofd- en bijzinnen. Na drie hoofdzinnen begint er een nieuwe uiting"

* **Remark** We better define a macro for clauses and clause bodies and use that in this query.

T091: V (lijdend)
"""""""""""""""""


* **Name**: V (lijdend).
* **Category**: Zinsdelen
* **Subcat**:
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 42
* **Implementation**: not implemented
* **Query** defined as: **not implemented**

Not implemented because they are subsumed under *VC*

* **Schlichting**: "Het lijdend voorwerp van een zin kan meestal gevonden worden door een vraag te stellen met 'wat' betreffende het onderwerp en het werkwoord van de zin. [...] Het lijdend voorwerp van de bedrijvende vorm wordt het onderwerp van dezelfde zin in de lijdende vorm."





T092: V (meewerkend)
""""""""""""""""""""


* **Name**: V (meewerkend).
* **Category**: Zinsdelen
* **Subcat**:
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 42;43
* **Implementation**: not implemented
* **Query** defined as: **not implemented**

Not implemented because they are subsumed under *VC*



* **Schlichting**: "Het meewerkend voorwerp kan bijna altijd voorafgeaan worden door 'aan' of 'voor'. Dit 'voor'kan altijd vervangen worden door 'ten behoeve van'. Het meewerkend voorwerp komt niet zo vaak voor. Het wordt gebruikt bij werkwoorden als 'geven' en 'kopen' en 'schrijven' of 'mededelen'."



T093: V (Voorzetselvoorwerp)
""""""""""""""""""""""""""""


* **Name**: V (Voorzetselvoorwerp).
* **Category**: Zinsdelen
* **Subcat**:
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 43
* **Implementation**: not implemented
* **Query** defined as: **not implemented**

Not implemented because they are subsumed under *VC*

* **Schlichting**: "Wanneer een werkwoord gebruikt wordt met een vast voorzetsel is het zinsdeel dat begint met dat voorzetsel het voorzetselvoorwerp. Ook een werkwoordelijke uitdrukking kan gebruikt worden met een voorzetselvoorwerp."



T094: V.U. Divers
"""""""""""""""""


* **Name**: V.U. Divers.
* **Category**: V.U.
* **Subcat**:
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 37
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[ (@lemma!="ja" and @lemma!="nee" and @word!="xxx" and
	         @lemma != "mama" and @word!="xx" and
             ((@pt="tsw" and @lemma!="hè") or
              (@pt="tsw" and @lemma="hè" and @rel="tag"
			   and number(@end)<=number(../node[@rel="nucl"]/@begin)) or
               ((@lemma="au" or @lemma="hoepla" or @lemma="dag" or
			     @lemma="kijk" or @lemma="hap" or @lemma="aai" ) and
                 (@rel="--" or @rel="sat" or @rel="tag")
			   )
             )
            )    or
            %Tarsp_kijkVU%  or
            %Tarsp_hehe%
          ]

The query distinguishes three subcases:

* **Case 1**: interjections or otherwise specifically mentioned extragrammatical words
    * It excludes 'ja'and 'nee' (these fall under T150) and the CHAT code 'xxx' and the (wrong) CHAT code 'xx, as well as the lemma 'mama'
    * the word must be a 'tsw' but not 'hè', or
    * the word must be a 'tsw' with lemma= 'hè', provided that this *hè* occurs as a tag to the left of a nucleus
* **Case 2**: the word 'kijk' as a VU. This is achieved by the macro **Tarsp_kijkVU**, defined in :ref:`T087_Stam`.
* **Case 3**: the combination of words *hè, hè*, defined by the macro **Tarsp_hehe**, which basically searches for the bigram *hè hè*::

    Tarsp_hehe = """ (@lemma="hè" and
                      @end = ancestor::node[@cat="top"]/descendant::node[@lemma="hè"]/@begin)"""


* **Schlichting**: "Diverse Sociale Uitdrukkingen. hieronder vallen de uitingen die in het sociale verkeer veel gebruikt worden zoals 'dag', 'hallo', 'goedemorgen', 'au', 'hoepla' etc. Ook 'hoor'('die is van mij, hoor'), 'kijk' ('kijk, dat is hem') en 'hè' in de betekenis van 'wat zeg je'of 'hè, hè' worden hier gescoord. Verder vinden we in deze categorie de klanknabootsingen als 'boem' en 'tingeling'"

* **Remarks** There is also a macro for *kijkeens* (**Tarsp_kijkeens**), but I am not sure it is used anywhere now




T095: V.U. Soc. AangP
"""""""""""""""""""""


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

The query selects nouns that bear the grammatical relation *tag*. It excludes *hè* (apparently sometimes analysed as a noun) and (wrong) CHAT codes.

* **Schlichting**: "Aangesproken persoon, bijvoorbeeld 'mama', 'Peter'"



T096: V.U. Ster
"""""""""""""""


* **Name**: V.U. Ster.
* **Category**: V.U.
* **Subcat**:
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 38;39
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**





* **Schlichting**: "Hieronder verstaan we uitingen die in hun geheel worden geleerd, zoals:

    1. Spreekwoorden en uitdrukkingen, bijvoorbeeld 'bezint eer ge begint' en regels uit versjes of liedjes, bijv. 'alle eendjes zwemmen in het water'
    2. Ook gewone spreektaalzinnen die het kind in zijn geheel leert scoren we hier en verder niet meer. Nemen we bijvoorbeeld de uiting 'weet ik niet'. Wanneer we deze uiting vinden in een taalsample waarin verder geen 'ik' wordt gebruikt, of geen inversie van onderwerp en persoonsvorm voorkomt, dan is de zin waarschijnlijk als Stereotiepe Uitdrukking geleerd.
    3. Opsommingen, bijv. 'een, twee, drie, vier, vijf.'
    4. Zelfherhalingen. Men scoort hier wanneer een kind een uiting van zichzelf onmiddellijk herhaalt met precies dezelfde woorden.



.. _T097_VC:

T097: VC
""""""""


* **Name**: VC.
* **Category**:
* **Subcat**:
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 42-44
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[%complement% and
	       parent::node[(@cat="smain" or @cat="sv1" or
		                 @cat="ssub" or @cat="inf" or
						 @cat="ppart") ]]


Here the macro **complement** is defined as follows::

    complement = """((@rel="obj1" or @rel="obj2") or
                     (@rel="predc" and not(%predcB%)) or
                     (@rel="pobj1" and not(%pobj1B%) ) or
                     %verbalcomplement%
                    )"""

So, it covers:

* direct objects (*obj1*)
* indirect objects (*obj2*)
* predicative complements (*predc*), at least if they are not predicates that are considered adverbial modifiers in Tarsp (*predcB*)
* prepositional complements (*pc*) if they are not considere adverbial complements in Tarsp(*pobj1B*)
* and verbals complements (**verbal complement**).

The latter is defined as follows::


    verbalcomplement = """(@rel="vc" and (@cat="cp" or @cat="whq" or @cat="whsub"))"""

So it excludes nonfinite verbal complements such as *inf*, *teinf*, *ppart*, etc.

Predicates that cooccur with a transitive verb are considered modifiers in Tarsp. We exclude them by checking for the presence of a direct object::

    predcB = """(@rel="predc" and
               (@pt="adj" or @pt="bw" or @cat="ap" or @cat="advp") and
               ../node[@rel="obj1"]
             )"""

* **Remark** that fails if the direct object is left out (e.g. by topic drop).

Prepositional complements should be considered modifiers if they cooccur with a verb that can also take locative or directional complements. This has been implemented by **pob1B**::

    pobj1B = """(@rel="pc" and ../node[@rel="hd" and %locverb%])"""
    locverb = """(@lemma="staan" or @lemma="zitten" or @lemma="rijden" or
	              @lemma="vallen" or @lemma="doen" or @lemma="gaan" or
				  @lemma="komen" or @lemma="zijn"  or %locmodalverb% )"""

    locmodalverb = """ (@lemma="kunnen" or @lemma="moeten" or
	                    @lemma="hoeven" or @lemma="willen" or
						@lemma="mogen")"""



* **Remark** This language measure is not in the form and has not been kept up to date. In particular, it should be investigated to what extent it differs from the macro **Tarsp_VC** used in the composed language measures. See :ref:`composedmeasures`.

* **Schlichting** discusses several cases of  "Voorwerpen" and "Complementen" separately:

 * "**Lijdend Voorwerp**. Het lijdend voorwerp kan meestal gevonden worden door een vraag te stellen met 'wat' betreffende het onderwerp en het werkwoord van de zin. [...] Het lijdend voorwerp van bedrijvende vorm wordt het onderwerp van dezelfde zin in de lijdende vorm." Covered
 * "**Meewerkend Voorwerp**. Het meewerkend voorwerp kan bijna altijd voorafgegaan worden door 'aan' of 'voor'. Dit 'voor' kan altijd vervangen worden door 'ten behoeve van'. Het meewerkend voorwerp komt niet zo veel voor. Het wordt gebruikt bij werkwoorden als 'geven' en 'kopen', en 'schrijven' of 'mededelen'. Covered
 * "**Voorzetselvoorwerp**. Wanneer een werkwoord gebruikt wordt met een vast voorzetsel is het zinsdeel dat begin met dat voorzetsel het voorzetselvoorwerp. Ook een werkwoordelijke uitdrukking kan gebruikt worden met een voorzetselvoorwerp (*een hekel hebben aan*)." Covered.
 * "**Complement**. Een aanvulling van het gezegde. het complement kan  zijn:
    1. naamwoordelijk deel van het gezegde. Het naamwoordelijk gezegde bestaat uit een koppelwerkwoord en (meestal) een zelfstandig naamwoord of bijvoeglijk naamwooord." (maar ook een voorbeeld met een PP wordt gegeven). Covered
    2. Bepaling van gesteldheid. Deze zegt iets van het werkwoord en van het onderwerp of lijdend voorwerp. de bepaling van gesteldheid wordt ook wel 'dubbelverbonden bepaling' genoemd." This covers primary predicates (which Alpino consideres *predc*) but also *secondary predicates* (in Alpino: *predm*, e.g in *ik kan dat* **alleen**). Mostly covered.

* **Remark** we do not treat secondary predicates  such as *ik kan dat* **alleen** as complements, but as adverbial modifiers.

T098: Vcbijzin
""""""""""""""


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

Alpino does not have clauses with grammatical relation *obj1* or *obj2*: instead clause have the grammatical relation *vc*.

A clause acting as an adpositional complement also has the grammatical relation *vc*, so is also covered.

The macro **directerede_vcbijzin** is used as weel, but I do not understand or remember why. (was it intended for ASTA?). It is defined as follows::

    directerede_vcbijzin = """( %clausecat% and not(@rel="cnj") and
                                (preceding-sibling::node[%metasmain%] or
                                 following-sibling::node[%metasv1%]))"""

and it uses several other macros::

    clausecat = """(@cat="smain" or @cat="whq" or %baresv1% )"""
    metaverb = """(@lemma="zeggen" or @lemma="denken" or
	               @lemma="vinden" or @lemma="vragen" or
				   @lemma="schreeuwen" or @lemma="fluisteren" )"""
    metasmain = """(@cat="smain" and not(@rel="cnj") and node[@rel="hd" and %metaverb%]) """
    metasv1 = """(@cat="sv1" and not(@rel="cnj") and node[@rel="hd" and %metaverb%]) """

    baresv1 = """( @cat="sv1" and not(parent::node[(@cat="whq" or @cat="whrel")]))"""


* **Schlichting**: "Ondergeschikte zin die in de hoofdzin de functie heeft van een lijdend voorwerp, een voorzetselvoorwerp of meewerkend voorwerp of een complementsbijzin: deze laatste heeft de functie van een naamwoordelijk deel van het gezegde of van een bepaling van gesteldheid."

* **Remark** A clause with grammatical relation *predc* does occur, but is currently not covered.
* **Remark** Nodes with category *cp* are not necessarily clauses. That is only so if they also contain a *ssub* node. This should be adapted. It is especially important for *cp* with grammatical relation *predc*.

T099: VCW
"""""""""


* **Name**: VCW.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 46
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**

For infinitival constructons, this can be dealt with by using the smallclauses module (See :ref:`smallclauses`).

For finite constructions, we can cover *is* + Noun or NP, but what else can occur has to be investigated. There are many examples in the Auris data.

* **Schlichting**: "Voorwerp of Complement + Werkwoord"





T100: VCWOndBB
""""""""""""""


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

Straightforward implementation::

    Tarsp_VCWOndBB = """(%declarative% and
                         %Ond% and
                         %Tarsp_W% and
                         %Tarsp_B_X_count% = 2 and
                         %Tarsp_VC_X% and
                         %realcomplormodnodecount% = 4)"""


* **Schlichting**: "Onderwerp + Werkwoord + VC + twee Bijwoordelijke bepalingen"



T101: VCWoordgroep
""""""""""""""""""


* **Name**: VCWoordgroep.
* **Category**: Uitbreiding Zinsdelen
* **Subcat**:
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 75
* **Implementation**: Xpath
* **Query** defined as::

    //node[@cat and
	       ((@rel="obj1" or @rel="obj2" or @rel="pc" or
		     @rel="predc" or @rel="ld" or
			 (@rel="vc" and (@cat="cp" or @cat="whq" or @cat="whsub"))
			) and
			parent::node[(@cat="smain" or @cat="sv1" or
			              @cat="ssub" or @cat="inf" or
						  @cat="ppart") ])]


The query selects nodes for phrases (@cat) and with a grammatical relatoin for objects and complements that occur in a clause or clause body.



* **Schlichting**: "<no text>"

* **Remark** It is not obvious to me that the condition on being contained in a clause is really needed. A simple test on the VKLtarsp data suggests that it is not.


T102: Verb Ov
"""""""""""""


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
            (@pt="vnw" and @vwtype="vb")
           ) and
           parent::node[(@cat="whsub" or @cat="ssub" or @cat="rel" or @cat="cp" or @cat="whrel") and @rel!="nucl"]
      ]

The query selects

*  the conjunctions *dat*, *of*, *toen*, and
*  wh-pronouns

provided that they are dominated by a clause that does not bear the grammatical relation 'nucl'


* **Schlichting**: "Overige onderschikkende verbindingswoorden: 'waar', 'dat', 'toen', 'of', 'wat', 'hoe'."




T103: Vergr trap
""""""""""""""""


* **Name**: Vergr trap.
* **Category**: Woordstructuur
* **Subcat**:
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 88
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**, but it could be //node[@graad="comp"]




In the VKLTarsp dataset this only occurs with *meer*, mostly  in a combination with a negative word (*niet meer*, *nergens meer*, *geen  ... meer*), but also  in *nog meer kindjes*. Should these be included?
No annotations for this measure occur in the Auris TD and DTD data. The language measure is absent in [Schlichting 2017].

* **Schlichting** "Vergrotende trap van het bijvoeglijk naamwoord."



T104: Verkl
"""""""""""


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

The query is self-explanatory.

* **Schlichting**: "Verkleinwoord van zelfstandige naamwoorden. Sommige woorden hebben als meeste gebruikte of enig gebruikte vorm het verkleinwoord, bijvoorbeeld 'meisje', 'kopje', 'koekje'. Deze worden niet gescoord bij verkleinwoord."

* **Remark**: *meisje* is correctly not counted (because Alpino does not analyse it as a diminutive), but *koekje* en *kopje* are incorrectly counted.


T105: Verl Tijd
"""""""""""""""


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



* **Schlichting**: "De Verleden Tijd van Koppelwerkwoord, Hulpwerkwoord en soms het onregelmatige zelfstandige werkwoord. Zowel enkelvoud als meervoud worden hier gescoord. de verleden tijd van de regelmatige werkwoorden wordt in Fase VI nog niet gebruikt."

* **Remark** We have no exceptions for regular verbs. We interpret Schlichting's text as follows: Past tenses of regular verbs should be counted, but they occur only rarely.

T106: Vo/bij
""""""""""""


* **Name**: Vo/bij.
* **Category**: Woordgroepen
* **Subcat**:
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 71
* **Implementation**: Python function
* **Query** defined as::

    voslashbij

.. autofunction:: queryfunctions::voslashbij

* **Schlichting**: "Voornaamwoordelijk bijwoord, gesplitst. Het gesplitste voornaamwoordelijk bijwoord behoeft niet gescoord te worden bij Vobij, kolom Voornaamwoorden in Fase IV, alleen hier bij de Woordgroepen in Fase V."

* **Remark** Schlichting only gives examples with nonadjacent Rpronouns and adpositions. We agreed with Rob Zwitserlood that adjacent R-pronoun + adposition, even if written separately, is to be counted under *Vobij*. However, the notion "adjacent" is not so easy to define in  inflated tree structures. This has been done in a python function *adjacent* in the module treebankfunctions, and for this reason this query must also be defined as a python function.




T107: Vobij
"""""""""""


* **Name**: Vobij.
* **Category**: Voornaamwoorden
* **Subcat**:
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 80
* **Implementation**: Python function
* **Query** defined as::

    vobij

.. autofunction:: queryfunctions::vobij




* **Schlichting**: "Voornaamwoordelijk bijwoord. Het voornaamwoordelijk bijwoord is een combinatie van 'er', 'daar', 'hier', 'waar' met een voorzetsel (bijv. 'aan', 'bij', 'voor') of een bijwoord ('af', 'heen', 'toe')"

* **Remark** Separately wiritten but adjacen R-pronoun + adposition cases are also considered *Vobij*
* **Remark** Alpino considers words such as 'af', 'heen', and 'toe' as postpositions, not as adverbs.





T108: Volt dw
"""""""""""""


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

The query is self-explanatory

* **Schlichting**: "Voltooid deelwoord. Bij het vroege gebruik van het Voltooid deelwoord wordt 'ge' nog wel eens weggelaten. Bij woorden als 'vallen' of 'maakt' zal men alleen uit de situatie kunnen opmaken of het een voltooid deelwoord betreft of een andere vorm. Ook zonder het voorvoegsel 'ge' mogen de voltooide deelwoorden gescoord worden."

* **Remark** Wrongly formed forms without *ge* can only be dealt with if they are dealt with by the *deregularise* module.

T109: Voltd fg
""""""""""""""


* **Name**: Voltd fg.
* **Category**: Woordstructuur
* **Subcat**:
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 88
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**


* **Schlichting**: "Voltooid deelwoord, fout gevormd. In deze Fase (VII) beginnen de kinderen de regel voor het maken van een voltooid deelwoord door te krijgen. Dit blijkt uit het gebruik van fout gevormde voltooide deelwoorden. Natuurlijk komt deze constructie nooit als leerdoel in een behandelingsplan."

* **Remark** Can  be dealt with via the module *deregularise*.




T110: Vr
""""""""


* **Name**: Vr.
* **Category**:
* **Subcat**:
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**:
* **Implementation**: Xpath
* **Query** defined as::

    //node[ @cat="whq"]


This language measure actually does not exist. It has been included and implemented because the code *Vr* occurs in the Schlichting appendix  (example 20, p. 91, and example 22, p. 92). Example 20 should have been annotated as *Vr(XY)*, and example 22 as *Vr4*.

.. _VrXY:

T111: Vr(XY)
""""""""""""


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


Straightforward implementation::

    Tarsp_VrXY = """(%Tarsp_whq% and
        node[%Tarsp_whqhead%] and
        node[%whqbody%   and %realcomplormodnodecount% <= 1])"""

where *Tarsp_whqhead* and *whqbody* cover both wh-questions (main and subordinate) and independent relatives::

    Tarsp_whqhead = """(@rel="whd" or @rel="rhd") """
    whqbody = """((@cat="sv1" or @cat="ssub") and @rel="body")"""

See section :ref:`composedmeasures` for details.

* **Schlichting**

    * "Vraagwoord (+ een of twee Zinsdelen)."Covered
    * Het Vraagwoord zonder meer, of gevolgd door één Zinsdeel komt niet vaak voor. We vinden meestal Vr + X + Y." **Not currently covered**
    * "'Wat is dat?' is bij sommige kinderen als Vaste Uitdrukking geleerd. We scoren deze dan bij Stereotiepe Uitdrukkingen". **Not covered**


T112: Vr4
"""""""""


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

* **Schlichting** "Vraagwoord + drie Zinsdelen." Covered.

Straightforward implementation::

    Tarsp_Vr4 = """(%Tarsp_whq% and
        node[%Tarsp_whqhead%] and
        node[%whqbody%  and %realcomplormodnodecount% = 2])"""

For *Tarsp_whqhead* and *whqbody*, see :ref:`VrXY`


See section :ref:`composedmeasures` for details.



T113: Vr5+
""""""""""


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


Straightforward implementation::

    Tarsp_Vr5plus = """(%Tarsp_whq% and
        node[%Tarsp_whqhead%] and
        node[%whqbody%  and %realcomplormodnodecount% > 2])"""



For *Tarsp_whqhead* and *whqbody*, see :ref:`VrXY`

See section :ref:`composedmeasures` for details.

* **Schlichting** "Vraagzinnen die beginnen met een vraagwoord en behalve dat Vraagwoord nog vier of meer Zinsdelen hebben." Covered.

* **Remark** There is also an older implementation as a Python function in the module *SZiplus*


T114: VzB
"""""""""


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
                  (%Rpronoun% and @begin=../node[@rel="hd"]/@end)
                )
               ]
          ]

The query selects a node that contains

* an adposition as head, and
* a direct object, which can be
    * an adposition, or
    * an adverb, or
    * an Rpronoun, provided that it follows the adposition (so *van hier* is ok, *hier van* not)

* **Schlichting**: "Voorzetsel + Bijwoord"



T115: VzBepBvZn
"""""""""""""""


* **Name**: VzBepBvZn.
* **Category**: Woordgroepen
* **Subcat**:
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 74
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**




* **Schlichting**: "Voorzetsel + Bepaler + Bijvoeglijk woord + Zelfstandig naamwoord."




T116: VzBepZn
"""""""""""""


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

The query searches for a PP that contains a direct object that contains a determiner.

* **Schlichting**: "Voorzetsel + Bepaler + Zelfstandig naamwoord"


* **Remark** Maybe we must restrict the content of the object to determiner + Noun and nothing else.

T117: VzN
"""""""""


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

The macro **Tarsp_VzN** is defined as follows::

    Tarsp_VzN = """(%vzn1xpath% or %vzn2xpath% ) """

    vzn1xpath = """(@cat="pp" and
                   (node[@pt="vz"] and
                    node[(@pt="n" or @pt="vnw") and
                    not (%Rpronoun%) and @rel="obj1"] and
                    not(node[@pt="vz" and @vztype="fin"])
                   ))"""
    vzn2xpath = """(node[@lemma="in" and @rel="mwp"] and
                   node[@lemma="deze" and @rel="mwp"])"""


The macro distinguishes two subcases:

* a PP with a preposition but no postposition and a direct object that is a noun or a pronoun but no R-pronoun.
* the combination *in deze*, which has an idiosyncratic parse in Alpiono

* **Schlichting**: "Voorzetsel + Zelfstandig naamwoord of Voornaamwoord. In Fase III vinden we hoofdzakelijk Vz + Zn"




T118: VzZnAz
""""""""""""


* **Name**: VzZnAz.
* **Category**: Woordgroepen
* **Subcat**: Ov
* **Level**: Wg
* **Original**: yes
* **In form**: no
* **Page**: 70
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**



* **Schlichting**: "Voorzetsel + Zelfstandig naamwoord + achterzetsel"





T119: S1W
"""""""""


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


* **Schlichting**: "Werkwoord. De kinderen gebruiken inde éénwoordfase een aantal werkwoorden in de onbepaalde wijs."

* **Remark** Schlichting does not distinguish a code for a verb as a single word utterance, and a verb or predicate in a full sentence. We introduced a different code for a verb as a single word utterance.

.. _T120_W:

T120: W
"""""""


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

The macro **Tarsp_coreW** is defined as follows::

    Tarsp_coreW = """ ( @pt="ww" and
                       (@wvorm="pv" or parent::node[@rel!="vc"] or %Tarsp_BarenonfinW%) and
                       not(%Tarsp_kijkVU%) and
                       not((@lemma="zijn" or @lemma="worden") and parent::node[node[@rel="vc"]]) )"""


The query selects:

* nodes with *pt* equal to *ww** (verbs)
* that are
    * finite (*@wvorm* equal to *pv*), or
    * whose parent node does not bear the grammatical relation *vc* (because then a higher verb should count as *W*), or
    * or whose parent node does bear the grammtical relation *vc* but that parent is the only node under an smain node. This is for utterance that contain an infiitive or past particple only (e.g. *boekje lezen*). See the module :ref:`smallclauses`. This is achieved by the macro **Tarsp_BarenonfinW**::

        Tarsp_BarenonfinW = """parent::node[@rel="vc" and
                                            parent::node[@cat="smain" and count(node)=1]]"""


* that is not a VU *kijk*, by the macro **tarsp_kijkVU**, defined under @@, and
* that is not a form  of 'zijn' or 'worden' with a *vc*-sibling. I think that this is to exclude *zijn* as a W in e.g. *hij kan gekomen zijn*. In *hij is gekomen*, *is* does count because it is finite.




* **Schlichting**: "Werkwoord"

* **Remark** I do not really understand the last condition concerning *zijn* and * worden*, should *hebben* not be added here as well?



T121: W(X)
""""""""""


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



It has been implemented by means of a Python function **wx**.


.. autofunction:: imperatives::wx

In a later stage  a query with macros was defined for it, but  the Python function has not been replaced yet.

The query has a straightforward implementation::

    wx = """(%basicimperative% and
             %realcomplormodnodecount% <= 1)"""

See section :ref:`composedmeasures` for details.


* **Remark** Experiment with replacing the wx function by the query with macros

* **Schlichting** "De Gebiedende Wijszinnen bestaan in deze Fase uit één of twee zinsdelen." Covered


T122: PV-loos
"""""""""""""


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


This is not a language measure but has been added for development purposes.




T123: waarschijnlijk fout geanalyseerde nevenschikking
""""""""""""""""""""""""""""""""""""""""""""""""""""""


* **Name**: waarschijnlijk fout geanalyseerde nevenschikking.
* **Category**:
* **Subcat**:
* **Level**: Zc
* **Original**: no
* **In form**: no
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**



This is not a language measure but has been added for development purposes.





T124: want
""""""""""


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

The query is self-explanatory.

* **Schlichting**: "'want' verbindt twee hoofdzinnen. Soms wordt het introducerend gebruikt."




T125: WBVC
""""""""""


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

Straightforward implementation::

    Tarsp_WBVC = """(%declarative%  and
                     %Tarsp_W% and
                     %Tarsp_B_X% and
                     %Tarsp_VC_X% and
                     %realcomplormodnodecount% = 2 )"""


See section :ref:`composedmeasures` for details.

* **Schlichting** "Werkwoord + Bijwoordelijke bepaling + Voorwerp of Complement." Covered

T126: Wdeel
"""""""""""


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

The query searches for a head verb that contains an underscore in its lemma and that has an *svp* node as a sibling.

* **Schlichting**: "Werkwoord + Scheidbaar deel"




T127: Werkwoordswoordgroep
""""""""""""""""""""""""""


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


* **Schlichting**: "<no text>"

* **Remark** The given query finds the first verb of the verbal group. Note that Alpino (correctly) does not consider verbal groups to be phrases. if we want to identify all elements of the verbal group, a different query will have to be formulated, one that yields multiple nodes as single result.




T128: wij
"""""""""


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


The query is self-explanatory.

* **Schlichting**: "Persoonlijk voornaamwoord 'wij', 'we'."




T129: Wond(X)
"""""""""""""


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


Straightforward implementation::

    Tarsp_WOndX = """(%ynquery% and
                      not(%basicimperative%) and
                      %topcontainsquestionmark% and
                      %Tarsp_W% and
                      %Ond% and
                      %realcomplormodnodecount% <= 2)"""

See section :ref:`composedmeasures` for details.

* **Schlichting** "Werkwoord + Onderwerp, meestal gevolgd door een derde zinsdeel." Covered.


T130: WOnd4
"""""""""""


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


Straightforward implementation::

    Tarsp_WOnd4 = """(%ynquery% and
                      not(%basicimperative%) and
                      %topcontainsquestionmark% and
                      %Tarsp_W% and
                      %Ond% and
                      %realcomplormodnodecount% = 3)"""

See section :ref:`composedmeasures` for details.

* **Schlichting** "Werkwoord + Onderwerp + twee Zinsdelen." Covered.

T131: WOnd5+
""""""""""""


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

Straightforward implementation::

    Tarsp_WOnd5plus = """(%ynquery% and
                          not(%basicimperative%) and
                          %topcontainsquestionmark% and
                          %Tarsp_W% and
                          %Ond% and
                          %realcomplormodnodecount% =4)"""

See section :ref:`composedmeasures` for details.

* **Schlichting** "Vraagzinnen die beginnen met een Werkwoord en een Onderwerp en daarbij nog drie of meer Zinsdelen hebben." Covered.

* **Remark** Maybe *= 4* should be *>= 4*


T132: woordgroep(onderstrepen)
""""""""""""""""""""""""""""""


* **Name**: woordgroep(onderstrepen).
* **Category**: Zinsdelen
* **Subcat**:
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 63-64
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[(@cat="ap" or @cat="advp" or @cat="np" or @cat="pp" or
       node[@rel="vc" and (@cat="inf" or @cat="ppart")]) and parent::node[count(node[@cat or @pt!="let"])>1]]


* **Schlichting**: "Elk zinsdeel kan, zoals gezegd, ook uit meerdere woorden bestaan. [...] Bij de analyse worden de woordgroepen onderstreept, het nummer van de uiting wordt omcirkeld."

* **Remark** We can identify the word groups, but they are not undelined in the annotation form, and the utterance id is currently not surrounded by a circle.


T133: WVz
"""""""""


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

The query search for a verb that has a *pc* as sibling if that *pc* node is not an adverbial modifier.

* **Schlichting**: "Werkwoord + Voorzetselvoorwerp waarbij het vast voorzetsel gerealiseerd is"



T134: WW
""""""""


* **Name**: WW.
* **Category**: Woordgroepen
* **Subcat**:
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 73
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**



* **Schlichting**: "Werkwoord + Werkwoord. Deze constructie omvat een hulpwerkwoord + twee infinitieven. Ook werkwoordelijke uitdrukkingen zoals 'nodig hebben', 'het koud hebben'worden hier gescoord"





T135: WXY
"""""""""


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

Straightforward implementation::

    wxy = """(%basicimperative% and
              %realcomplormodnodecount% = 2)"""

See section :ref:`composedmeasures` for details.

* **Schlichting** "Werkwoord + twee Zinsdelen". Covered


T136: WXYZ
""""""""""


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

Straightforward implementation::

    wxyz = """(%basicimperative% and
               %realcomplormodnodecount% = 3)"""

See section :ref:`composedmeasures` for details.

* **Schlichting** "Werkwoord + drie Zinsdelen". Covered


T137: WXYZ5*
""""""""""""


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

Straightforward implementation::

    wxyz5 = """(%basicimperative% and
                %realcomplormodnodecount% = 4)"""


See section :ref:`composedmeasures` for details.

* **Remark** The label should be chaned to *WXY5*, the varinat with the asterisk should be an alternative.

* **Schlichting** "Werkwoord + vier Zinsdelen". Covered



T138: X en X (en X)
"""""""""""""""""""


* **Name**: X en X (en X).
* **Category**: Woordgroepen
* **Subcat**:
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 72
* **Implementation**: Python function
* **Query** defined as::

    xenx

.. autofunction:: xenx::xenx


* **Schlichting**: "Dit zijn twee woorden van dezelfde woordsoort, verbonden door 'en', die samen één Zinsdeel vormen, soms worden drie elementen verbonden. Ook woordgroepen kunnen op een dergelijke wijze verbonden worden. Behalve door 'en' kunnen de woorden of woordgroepen ook verbonden worden door 'of'."




T139: X(W)deel
""""""""""""""


* **Name**: X(W)deel.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 48;49
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**




* **Schlichting**: "De X kan hier elk willekeurig Zinsdeel zijn behalve de W. De X is dus een Ond, een VC, of een B. (W)deel is het scheidbare deel van een samengesteld werkwoord. In 'Ik doe de jas uit' is 'uit' het scheidbare deel van het samengestelde werkwoord 'uitdoen'. In de (W)deelconstructies zien we wel het scheidbare deel maar niet het werkwoord. daarom staat de W tussen haakjes. "

* **Remark** Dubious analysis. Most of these, if not all, can also be analysed as *OndB* or as *BX*




T140: Xneg
""""""""""


* **Name**: Xneg.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 49;50
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[(@rel='--' or @rel="nucl") and
           count(node) = 2 and
           node[ @lemma!="niet"] and
           (node[@lemma="niet" ] or
            node[@cat="advp" and node[@lemma="niet"]]
           )
          ]

The query searches for a node:

* with grammatical relation *--* or *nucl*
* containing exactly two nodes
* one of which is not equal to the word *niet*
* and the other one is  node for the word *niet* or and adverbial phrase containing the word *niet*.

* **Schlichting**: "Deze constructie bestaat uit een Zinsdeel dat verder niet benoemd wordt + een negatief, ontkennend woord, meestal 'niet'. Het eerst Zinsdeel, dat verder niet benoemd wordt, noemen we 'X'. het kan een Onderwerp zijn, een Werkwoord, een VC of een Bijwoordelijke bepaling. [...] Wanneer 'niet' voorkomt in constructiees van meer dan twee Zinsdelen wordt 'niet'weer gewoon als B geanalyseerd."



T141: XY(W)deel
"""""""""""""""


* **Name**: XY(W)deel.
* **Category**: Zinsconstructies
* **Subcat**: Mededelende Zin
* **Level**: Zc
* **Original**: yes
* **In form**: no
* **Page**: 51
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**




* **Schlichting**: "Deze constructie bestaat uit twee Zinsdelen + het 'deeltje' van een scheidbaar samengesteld werkwoord (e.g. *Marije strijkbout vast*"




T142: ze
""""""""


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

The query is self-explanatory. With plural *ze*, the attribute *persoon* can only have the values *3* or 3p*.

* **Schlichting**: "Persoonlijk voornaamwoord 'ze', meervoud mannelijk en vrouwelijk. 'ze' komt veel vaker voor dan 'zij'. In het begin wordt 'ze' vooral in de functie van onderwerp gebruikt."



T143: zelf
""""""""""


* **Name**: zelf.
* **Category**: Voornaamwoorden
* **Subcat**: Ov
* **Level**: VVW
* **Original**: yes
* **In form**: no
* **Page**:
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**


 *zelf* is mentioned on p.82 under *Overige*, together with *niets* and *niks*. It should be covered there.

* **Schlichting**: " "




T144: zij
"""""""""


* **Name**: zij.
* **Category**: Voornaamwoorden
* **Subcat**:
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 82
* **Implementation**: Xpath with macros
* **Query** defined as::


        //node[@pt="vnw"  and @vwtype="pers" and
               @getal="ev" and @genus="fem"  and
               @pdtype="pron"]

The query allows *zij* and *ze*, but also *zijzelf* (though I believe that is a misspelling for *zij zelf*)

* **Schlichting**: "Persoonlijk voornaamwoord derde persoon enkelvoud, vrouwelijk"






T145: Zn
""""""""


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
           (node[@pt="n" or
                 (@pt="tw" and @numtype="hoofd") or
                 (@lemma="paar" and @pt="lid")
                ] or
            node[@cat="du" and
                 node[@pt="n" or
                 (@pt="tw" and @numtype="hoofd") or
                 (@lemma="paar" and @pt="lid")]
                ]
            ) and
            count(.//node[%realnode%])=1
           ]

The query search for a *top* node that contains only one real node and has as a child:

    * a nominal node
    * a *du* node that contains a nominal node

where a *nominal* node is a node:

    * that is a noun, or
    * that is a substantively used numeral, or
    * that has as lemma *paar* with *pt* *lid*.


* **Schlichting**: "Hiertoe worden gerekend de zelfstandige naamwoorden, de eigennnamen, en de getalsnamen vwanneer ze zelfstandig gebruikt worden, dus bijvoorbeeld: 'boek', 'oma', 'Jantien', 'twee'"

* **Remark** I do not know why *paar* with *pt* *lid* was added, there are no such cases. *paar* is never analysed as an article in the TARSP samples, Lassy Klein or CGN.


T147: ZnZn
""""""""""


* **Name**: ZnZn.
* **Category**: Woordgroepen
* **Subcat**:
* **Level**: Wg
* **Original**: yes
* **In form**: yes
* **Page**: 69
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@cat="top" and
           .//node[node[@pt="n" and @rel="hd"] and node[@pt="n" and not(@rel="hd")] ] or
           node[@cat="du" and count(node[@rel="dp" and @pt="n"])>=2]
          ]

The query searches for a *top* node:

* that contains a node (anywhere in the structure) which contains a head noun and a non-head noun, or
* that contains a *du* node as a child which as two *n* children.


* **Schlichting**: "Zelfstandig naamwoord + Zelfstandig naamwoord. Deze combinatie van twee Zelfstandige naamwoorden kan een bezitsrelatie uitdrukken, bijvoorbeeld '*oma's tas*' of de '*tas van oma*', maar kan ook een andere combinatie van twee Zn's tot een woordgroep vormen, bijvoorbeeld 'stukje koek'. "

* **Remark** The query searches for a *top* node, but it should not do that but search for the first noun of the two nouns. It covers *stukje kaas* or  *opa baardje* but not *vaders huis*, however, Alpino analyses *opa* as a pronoun in the construction *opa's huis*  (idem for *oma*, *papa* and probably more words). It does not correctly analyse *Jans huis*, *Piets huis* or *tantes huis*.



T148: Znx
"""""""""


* **Name**: Znx.
* **Category**: Woordgroepen
* **Subcat**:
* **Level**: Wg
* **Original**: yes
* **In form**: no
* **Page**: 40
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**




* **Schlichting**: "Hiertoe worden gerekend de zelfstandige naamwoorden, de eigennnamen, en de getalsnamen wanneer ze zelfstandig gebruikt worden, dus bijvoorbeeld: 'boek', 'oma', 'Jantien', 'twee'"

T150: V.U. Nee/ja
"""""""""""""""""


* **Name**: V.U. Nee/ja.
* **Category**: V.U.
* **Subcat**:
* **Level**: Zc
* **Original**: yes
* **In form**: yes
* **Page**: 38
* **Implementation**: Xpath
* **Query** defined as::

    //node[@lemma="ja" or @lemma="nee"]

The implementation is self-explanatory.

* **Schlichting**: "Nee/ja"





T151: V.U. Totaal
"""""""""""""""""


* **Name**: V.U. Totaal.
* **Category**: Aggregate
* **Subcat**:
* **Level**:
* **Original**: yes
* **In form**: yes
* **Page**: 39
* **Implementation**: Python function
* **Query** defined as::

    vutotaal


.. autofunction:: TARSPpostfunctions::vutotaal

* **Schlichting**: "Hier noteren we het totaal aantal Sociale en Stereotype Uitdrukkingen"


.. _G_Totaal:

T152: G Totaal
""""""""""""""


* **Name**: G Totaal.
* **Category**: Aggregate
* **Subcat**:
* **Level**:
* **Original**: yes
* **In form**: yes
* **Page**: 20
* **Implementation**: Python function
* **Query** defined as::

    gtotaal

.. autofunction:: TARSPpostfunctions::gtotaal



* **Schlichting**: "We gaan uit van het Totaal aantal gescoorde uitingen. Hiervan trekken we af:

   - het aantal Afvallers: A totaal
   - het aantal vaste Uitdrukking: V.U. totaal

   Dit levert het aantal Analyse-eenheden op, dat is het aantal uitingen dat grammaticaal geanalyseerd is, oftewel G totaal."



T153: G.O Fase
""""""""""""""


* **Name**: G.O Fase. (Grammaticale Ontwikkelingsfase)
* **Category**: Aggregate
* **Subcat**:
* **Level**:
* **Original**: yes
* **In form**: yes
* **Page**: 20
* **Implementation**: Python function
* **Query** defined as::

    gofase

.. autofunction:: TARSPpostfunctions::gofase

* **Schlichting**: Eerst wordt *G totaal* berekend. Zie hiervoor :ref:`G_Totaal`. "We berekenen hoeveel Zinsconstructies per Fase zijn gescoord. We letten hiervoor uitsluitend op de vakken van de Zinsconstructies: Mededelende zin, Vraag, en Gebiedende wijs. Per Fase noteren we het aantal Zinsconstructies in de eerste kolom bóven de Fase-aanduiding (niet meegeteld worden Intonatie en Koppelwerkwoord in Fase II, en 'hè' en Inversie in Fase III). Bij een bepaald percentage Zinsconstructies kunnen we zeggen dat het kind zich in die Fase aan het ontwikkelen is. De regel is dat 5% van de Analyse-eenheden van het taalsample in een Fase bij de Zinsconstructies gescoord moet zijn om het kind in die Fase te kunnen plaatsen.





T154: PFII
""""""""""


* **Name**: PFII.
* **Category**: Aggregate
* **Subcat**:
* **Level**:
* **Original**: yes
* **In form**: yes
* **Page**: 23
* **Implementation**: Python function
* **Query** defined as::

    pf2


.. autofunction:: TARSPpostfunctions::pf2



* **Schlichting**: "Profielscore voor Fase II"



T155: PFIII
"""""""""""


* **Name**: PFIII.
* **Category**: Aggregate
* **Subcat**:
* **Level**:
* **Original**: yes
* **In form**: yes
* **Page**: 23
* **Implementation**: Python function
* **Query** defined as::

    pf3


.. autofunction:: TARSPpostfunctions::pf3


* **Schlichting**: "Profielscore voor Fase III"




T156: OvZnBv4
"""""""""""""


* **Name**: OvZnBv4.
* **Category**: Woordgroepen
* **Subcat**:
* **Level**: WG
* **Original**: yes
* **In form**: yes
* **Page**: 69
* **Implementation**: Xpath with macros
* **Query** defined as: **not implemented yet**




* **Schlichting**: "Overige Zn- en Bv-woordgroepen Fase IV"




T157: Screening
"""""""""""""""


* **Name**: Screening.
* **Category**: Aggregate
* **Subcat**:
* **Level**:
* **Original**: no
* **In form**: no
* **Page**: 94-97
* **Implementation**: Python function
* **Query** defined as::

    tarsp_screening


* **Schlichting**: "De TARSP-Screening us een methode om de Grammatical Ontwikkelingsfase van de spontane taal vast te stellen, zonder een analyse te maken."




T158: PFIV
""""""""""


* **Name**: PFIV.
* **Category**: Aggregate
* **Subcat**:
* **Level**:
* **Original**: yes
* **In form**: yes
* **Page**: 23
* **Implementation**: Python function
* **Query** defined as::

    pf4


.. autofunction:: TARSPpostfunctions::pf4


* **Schlichting**: "Profielscore voor Fase IV"




T159: PFV
"""""""""


* **Name**: PFV.
* **Category**: Aggregate
* **Subcat**:
* **Level**:
* **Original**: yes
* **In form**: yes
* **Page**: 23
* **Implementation**: Python function
* **Query** defined as::

    pf5

.. autofunction:: TARSPpostfunctions::pf5



* **Schlichting**: "Profielscore voor Fase V"




T160: PFVI
""""""""""


* **Name**: PFVI.
* **Category**: Aggregate
* **Subcat**:
* **Level**:
* **Original**: yes
* **In form**: yes
* **Page**: 23
* **Implementation**: Python function
* **Query** defined as::

    pf6


.. autofunction:: TARSPpostfunctions::pf6


* **Schlichting**: "Profielscore voor Fase VI"




T161: PFVII
"""""""""""


* **Name**: PFVII.
* **Category**: Aggregate
* **Subcat**:
* **Level**:
* **Original**: yes
* **In form**: yes
* **Page**: 23
* **Implementation**: Python function
* **Query** defined as::

    pf7

.. autofunction:: TARSPpostfunctions::pf7


* **Schlichting**: "Profielscore voor Fase VII"




T162: PF
""""""""


* **Name**: PF.
* **Category**: Aggregate
* **Subcat**:
* **Level**:
* **Original**: yes
* **In form**: yes
* **Page**: 23
* **Implementation**: Python function
* **Query** defined as::

    pf


.. autofunction:: TARSPpostfunctions::pf


* **Schlichting**: " Profielscore. Een tweede mogelijkheid om twee samples meer in detail te vergelijken is de Profielscore (PF). De Profielscore is het totaal aantal constructies waarbij een of meermalen gescoord is. Bij het vergelijken van twee taalsamples door middel van de Profielscore moeten de samples eenzelfde aantal Analyse-eenheden bevatten. De Fase I constructies worden voor de Profielscore niet meegeteld". Ook de constructies met twee ** tellen niet mee (Bijzin zonder verbindingswoord en de Vraagwoordconstructie zonder vraagwoord: ((Vr)WOnd+). *OndVC* telt men, indien deze niet in het taalsample voorkomt, wel mee als tenminste bij *OndWVC* of *OndWBVC* gescoord is. *XNeg* mag meegeteld worden indien een langere uiting met 'niet' gescoord is. Hetzelfde principe geldt voor *OndB*, *VCW* en *BX*. De vraagintonatie 'Into' mag meegeteld worden indien ergens anders in de vraagkolom gescoord is. In het meest linkse vak op de profielkaart staat het aantal constructies vermeld dat in een Fase ontwikkeld wordt. Hier kan men het gescoorde aantal constructies per Fase noteren. De Profielscore wordt genoteerd naast de G.O. Fase, bij PF. De maximale Profielscore is 100.




T165: Formulier
"""""""""""""""


* **Name**: Formulier.
* **Category**: Forms
* **Subcat**:
* **Level**:
* **Original**: yes
* **In form**: yes
* **Page**: 31-36
* **Implementation**: Python function
* **Query** defined as::

    mktarspform



* **Schlichting**: "Profielkaart"



















TARSP Language Measures
-----------------------

We will describe here all Tarsp language measures, in the order of the identifiers assigned to them. However, a few language measures are special in that they systematically composed out of recurring macros. See  :ref:`TarspAnnotation` for more on these language measures, which we will call *composed language measures*. We will discuss the most important macros that are used in the queries for such language measures first, in section :ref:`composedmeasures`. 


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

    Tarsp_whq = """((@cat="whq" and @rel="--") or (@cat="whsub"))"""
    
covering both main clauses (*whq*) and subordinate clauses (*whsub*).


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
* the parent nod must have *cat* equal to *top*
* there must not be a question mark in the utterance
* there must be no period in the utterance.

* **Remark** We must find a way to exclude *kijk* and *kijk eens* as an imperative in most cases, since it should be analysed as a V.U.

* **Schlichting** (p. 62) 

  "De kenmerken van de Gebiedende Wijs zijn in het kader van TARSP:
     
     1. de zin moet altijd beginnen met een werkwoord; dat werkwoord staat meestal in de vorm van de stam van het werkwoord, een enekel maal vinden we stam +t of de infinitief. (covered except stam +t)
     2. Er is altijd een niet-vragende intonatie (covered by disallowing a question mark)
     3. Er is vaak een tweed of derde woord in de zin, bijvoorbeeld 'maar', 'even', 'eens'. Covered
     4. Een gebideden wijs begint nooit met een modaal werkwoord, behalve met 'laten' (covered)

.. _zinsdelen:

Macros for 'Zinsdelen'
""""""""""""""""""""""

The 'zinsdelen'are *B*, *Ond*, *VC* and *W* and they correspond to some extent to  the following language measures, for 'zinsdelen':

* T007: B,  adverbial modifier (see :ref:`T007_B`)
* T063: Ond, subject   (see :ref:`T063_Ond`)
* T097: VC, verbal complement (see :ref:`T097_VC`)
* T120: W, verb 


But the correspondenc is only perfect for *B*. For *Ond* the definitions are different, but it is not clear whether that cannot be avoided. For *VC* the definitions are also different but perhaps they should be identical. 
For *W* there is no correspondence.
Out of these language measures, only T120/W occurs in the form ('profielkaart'), but it has a different interpretation than *W* in the composed language measures. *W* in the composed language measures means *predicate*, but language measure T120 with code *W* means *verb*. For example, in the sentence *Hij heeft gezwommen* there are two verbs (*heeft*, en *gezwommen*) but only one predicate (i.e *heeft gezwommen*). 

Language measures such as *WBVC*, *OndVC*, *OndW*, *OndWB*, *OndWBVC*, and several others are defined  by combinations of the definitions of recurring macros for 'zinsdelen'(and some others conditions). For such language measures, special macros of for Ond, VC and W have been defined:

* **Ond**: has a simple definition::

        Ond = """node[%subject%]"""
    
  where::
    
        subject = """(@rel="su")"""


It differs from the definition of :ref:`T063_Ond` because T063 has to exclude subjects of nonfinite nodes (which is covered in the composed language measures by the conditions on mood) and to cover an additional case (existential *er* as a subject (though maybe that should be included here as well) 
   
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
    * finite verbal complement (macro **Tarsp_finvc**)
    * pronouns with relation *vc*, this is for sluiced subordinate clauses as in *ik weet* **wat**, *effe kijken* **waar**
    * separable particles of a verb that are not adpositions (*svp*)
    
    and we exclude all cases that can be analysed as an adverbial modifier (**Tarsp_B**, see :ref:`T007_B`)
    
    The macro **Tarsp_pc_vc_exception** is generated in the *generatemacros* module on the basis of a list of  pairs (verb, adposition), e.g. (*slaan*, *op*) in which Alpino analyzes the adposition as the head of an prepositional complement (pc), but where it should be considered the head of a modifier. See :ref:`generatemacros` for more details.
    
* **Tarsp_W**: It is defined as:: 

    Tarsp_W = """node[@rel="hd" and @pt="ww"]"""
    
  Nonfinite verbs are not excluded by this definition but they are excluded by the mood conditions.


Macros for Counts of 'zinsdelen'
""""""""""""""""""""""""""""""""

Many composed language measures differ only in the number of complements or adverbial modifiers required. For example *Tarsp_OndWB* and *Tarsp_OndWBB* differ only in the number of adverbial modifiers that should be present (one, resp, two).
This requires conditions on the number of such complements or modifiers.
Note that one cannot simply include two expressions joined by *and* in an Xpath query (e.g. *%Tarsp_B% and %Tarsp_B%*) to cover the *BB* part of the language measure *Tarsp_OndWBB*. The reason is that in XPath such a query will then still match with  a structure containing a single adverbial modifier. We therefore use the predicate *count* in composed language measures. 

Adverbial modifiers and complements can occur not only under the node where the subject and verb occur but also inside a nonfinite verbal complement, so we gather both in a node set, union these nodesets and count the number of elements in the union. This leads to the following formulations::

    Tarsp_B_X_count = """count(node[%Tarsp_B%] | node[%nonfinvc%]/node[%Tarsp_B%]) """
    Tarsp_VC_X_count = """count(node[%Tarsp_VC%] | node[%nonfinvc%]/node[%Tarsp_VC%]) """

Definitions for *Tarsp_B* and *Tarsp_VC* were provided above.

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

@@todo@@

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

    //node[@pt="vnw"  and @vwtype="aanw" and @lemma!="hier" and @lemma!="daar" and @lemma!="er" and 
    @rel!="det" and (not(@positie) or @positie!="prenom") ]


* The query with pt equal to *vnw* and vwtype equal to *aanw* selects demonstrative pronouns, but
* these include R-pronouns, so they are explicitly excluded
* the relation must not be *det* (otherwise the pronouns are not used independently)
* and if a *position* attribute is present it should not have the value *prenom* (otherwise it is not used independently)

* **Schlichting**: "Aanwijzend Voornaamwoord: 'die', 'dit', 'deze', 'dat' zelfstandig gebruikt." fully covered.


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
        * but if the node is a phrase, it should not have the value *conj* for the attribute *cat*. In a conjunction the whole conjuction is not considered an adverbial modifier. The individual conjuncts are, see below.
        * if the node is a word, it should not be an interjection
        
    * Nodes that meet the conditions of the macro **predcB**. This macro is defined below.
      
  but only if they modify a verb
* Case 2: adpositions, adverbs and R-pronouns that bear one of the relations *dp*, *--*, *nucl* or *body*, if they are not the only real node in the structure. The macro **notonlyrealnode** is defined below.
* Case 3: adpositional phrases with grammatical relation *dp* or *--* if they are not the only realnode
* Case 4: adpositional complements to a verbs that meets the requirements of the macro **locverb**. Verbs that have a locative interpretation often also have use where they are combined with a particular adposition (e.g. *staan + op*). This often leads to asn ambiguity, and Alpino very often selects the *pc* analysis. However, very young children do not know these uses yet, but almost always intend the locative use. This part of the query corrects for Alpino's strategy.
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


                 
* **Schlichting**: "De bijwoordelijke bepaling zegt iets over de hele inhoud van de zin of iets over het werkwoord, een bijwoord of een bijvoeglijk naamwoord. Een zin kan meer dan één bijwoordelijke bepaling hebben."Basically covered.

* **Remark** The **locverb** macro very probably has overlap with or is subsumed by the generated macro **Tarsp_pc_vc_exception**
* **Remark** Case 5 does not cover conjuncts under a node *conj* that meets the requirements of **predcB**, e.g *ik vind haar* **mooi en aardig**
* **Remark** The macro **predcB** does not cover cases where the object is absent due to topic drop (e.g. *vind ik* **mooi**). We could include a condition which includes cases where surely non-copular verbs (such as *vinden*) are listed, as was done in ASTA.

T010: BBBv
""""""""""


* **Name**: BBBv. (Bijwoord + Bijwoord + Bijvoeglijk woord, adverb + adverb + adjective
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

    //node[@rel="mod"and @cat="cp" and node[@rel="body" and node[@pt="ww" and @pvagr and @rel="hd"]]]


* **Schlichting**: "Bijwoordelijke bijzin met verbindingswoord. Dit is dus een ondergeschikte zin die in de hoofdzin de functie van bijwoordelijke bepaling heeft. Het verbindingswoord is in deze fase meestal *als*",.

A straightforward query for a cp ("complementizer phrase") with grammatical relation *mod*. The condition that the *body* must contain a finite verb is necessary because a *cp* can als have other phrases (e.g. *np*) as complement.



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


@@todo@@

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
    node[@rel="hd" and @pt="n"]]


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
  
These are single word utterances consisting of an adjective or an adverb, and based on the examples that Schlichting gives (such as *uit*, *op*) adpositions should be included as well. (*uit* is parsed as an adverb by Alpino, but *op* as a adposition).

The condition to restruct it to single word utterances use the macro *realnode*, which is defined as follows::

    realnode = """((not(@pt) or (@pt!="let" and @pt!="tsw")) and (not(@postag) or @postag!="NA()"))"""

It excludes interpunction symbols, interjections and words not classified for DCOI part of speech by Alpino (i.e., where *pos=NA()*),



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
    
* **corbwmod**: basically any modifying adverb that is quantificational in nature (by the macro **qbwlemma** (so far only *nog*)::

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
    * there is  node with *cat* = *du* that contains exactly one  **realnode** that meets the requirements of the macro **bxnp1**
    * there is a child node that meets the requirements of the macro **bxnp2**, i.e. a noun phrase consisting of a head and a single word  modifier, and nothing else (example: *die hier*)::
        
        bxnp2 = """(@cat="np" and count(node)=2 and node[@rel="hd"] and node[@rel="mod" and %singlewordbw%])"""
        
    * there is  node with *cat* = *du* that contains exactly one  **realnode** that meets the requirements of the macro **bxnp2**


* Case 2: the node meets the requirements of the macro **Tarsp_bnonfin**::

    Tarsp_bnonfin = """((@cat="inf" or @cat="ppart") and 
                        @rel="vc" and 
                        parent::node[@cat="smain" and count(node)=1] and 
                        node[%Tarsp_B%] and node[@pt="ww" and @rel="hd"] and 
                        count(node[%realcomplormod%])=1 )"""

  This covers cases where a nonfinite verbal complement is the only child of an *smain* category and contains only a head verb and an adverbial modifier (defined by macro **Tarsp_B**, see :ref:`T007_B`). Such structures can only arise after correction throgh the *smallclauses* module. (See :ref: `smallclauses`).

The macro **singlewordbw** is defined as follows::
      
    singlewordbw = """ (@pt="bw" or %Rpronoun% or %adjadv%)"""
    adjadv = """(@pt='adj' and (@lemma='wel'))"""

The macro **Rpronoun** simply lists all R-pronouns in a disjunction, and the **adjadv** macro is intended for words that are adverbs but analysed by Alpino (in some cases) as an adjective. So far, we only encountered this for *wel* (or was the **adjoradv** macro intended here?.


* **Schlichting**: "Bijwoordelijke bepaling + een ander Zinsdeel. Dit andere Zinsdeel kan zijn een W, een VC of een B. BW, BVC en BB staan namelijk niet apart op de profielkaart. In de praktijk worden hier ook zinnen gescoord met een B en een ander zinsdeel waarvan men niet weet of het een onderwerp of een VC is. De zin ‘die ook’ bijvoorbeeld, kan betekenen ‘die moet ook’ of ‘die moet je ook daar doen’. Zulke twijfelgevallen kunenn we hier dus ook scoren." 
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

    //node[@cat="np" and node[@rel="det" and @lemma="de"] and count(node)=2]



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

    //node[@cat="np" and node[@pt="n" and @rel="hd"] and node[@pt="vnw" and @vwtype="aanw" and @rel="det" and (@lemma="die" or @lemma="deze")] and count(node)=2]


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

    //node[@cat="np" and node[@pt="n" and @rel="hd"] and node[@pt="vnw" and @vwtype="aanw" and @rel="det" and (@lemma="dit" or @lemma="dat")] and count(node)=2]


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

This query is self-explanatory. The condition on *rel* excluded *en* en conjunctions.
 

* **Schlichting**: "Het verbindingswoord ‘en’ wordt in deze fase gebruik om een zinsdeel of een zin te introduceren. In fase VI wordt ‘en’ gebruikt om twee hoofdzinnen met elkaar te verbinden."




T037: er
""""""""


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


The query is self-explanatory. Note that the condition formulated in terms of the atribute *lemma* ensures that also variants of *er* such as *Er*, *d'r* and even *der* can be dealt with.

* **Schlichting**: "Dit ‘er’ heeft slechts in enkele gevallen het karakter van een voornaamwoord. Het kan als zinsdeel de functie hebben van een bijwoordelijke bepaling: ‘zij komt er wel’, ‘ik heb er nog drie’, of van een onderwerp, bv. In : ‘er stond een plant voor het raam’. Zo’n zin kan dan twee onderwerpen hebben (‘er’ is dan een zgn. plaatsonderwerp, het andere onderwerp is dan het getalsonderwerp, dat wil zeggen dat dat onderwerp in het meervoud kan komen te staan: ‘er staat een kind’, ‘er staan twee kinderen’"




T038: geen X
""""""""""""


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


The query is self-explanatory.

* **Schlichting**: "‘geen’ meestal gevolgd door een zelfstandig naamwoord"

* **remark** perhaps the number of nodes should be restricted to 2? Though *geen N meer* should also be accepted


T039: hè
""""""""


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

The query is self-explanatory, but it is perhaps too broad. Also occurrences of *hè* at the beginning of an utterance will also be scored now.

* **Schlichting**: "de naklank ‘hè’ in de betekenis van ‘vind je niet?’ of ‘dat vind je toch ook?’ maakt de voorafgaande uiting vragend."



T040: hem
"""""""""


* **Name**: hem.
* **Category**: Voornaamwoorden
* **Subcat**: 
* **Level**: VVW
* **Original**: yes
* **In form**: yes
* **Page**: 82
* **Implementation**: Xpath with macros
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
* **Implementation**: Xpath with macros
* **Query** defined as::

    //node[@lemma="het" and @pt='vnw' ]

The query is self-explanatory. The condition that the *pt* is equal to *vnw* excludes occurrences of *het* as an article (because then *pt* = *lid*). The check on the lemma form allows also reduced forms (*'t) and occurerences where the word conatins capital characters (e.g. *Het*).

* **Schlichting**: " Persoonlijk voornaamwoord ‘het, onder andere als lijdend voorwerp en als onderwerp." Covered.




T042: hetZn
"""""""""""


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


* **Schlichting**: "‘hij’ en ‘ie’ worden op de profielkaart beide bij ‘hij’ gescoord. ‘ie’ komt vaker voor dan ‘hij’ in deze fase."




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
* that is a auxiliary verb (macro **Tarsp_hww**)
* and cooccurs with a verbal complement (*rel* = *vc*) that is either an infinitval phrase (*cat = *inf*) or a bare infinitive (*wvorm* = *inf*)

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

De hulpwerkwoorden die gevolgd worden door een infinitief worden niet gescoord bij HwwZ, Stam of Stam+t"


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




* **Schlichting**: "Hulpwerkwoord gevolgd door het Voltooid deelwoord. Hulpwerkwoord + Voltooid deelwoord komt voor bij de voltooide toijd ('jij hebt gemaakt'). het Voltooid deelwoord wordt apart bij de Woordstructuur gescoord. ook voltooid verleden tijd ('jij had gemaakt') kan hier gescoord worden. dan wordt eveneens bij Verleden tijd en bij Voltooid deelwoord gescoord. het hulpwerkwoord wordt niet gescoord bij Woordstructuur."




T046: HwwZ
""""""""""


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



* **Schlichting**: " "



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



* **Schlichting**: " "



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

    

* **Schlichting**: " "





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
      node[@pt="ww" and @rel="hd" and (not(@stype) or @stype!="imparative") ] and node[@rel="su" and number(@end)>../node[@rel="hd"]/@end]) or 
      %robustinversion%]



* **Schlichting**: " "



T050: jij
"""""""""


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



* **Schlichting**: " "



T051: jou
"""""""""


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



* **Schlichting**: " "




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



* **Schlichting**: " "



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



* **Schlichting**: " "



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



* **Schlichting**: " "



T055: Mededelende Zin
"""""""""""""""""""""


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

    //node[(@lemma="me" or @lemma="mij") and (@vwtype="pr" or @vwtype="pers")]







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






T059: Nabep
"""""""""""


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
""""""""""""


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
"""""""""""""""""""""


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

    """((%subject% and (@pt or @cat) ) or %erx%)"""


where **subject** and **erx** are defined as::

    subject = """(@rel="su")"""
    erx = """((@rel="mod" and @lemma="er" and ../node[@rel="su" and @begin>=../node[@rel="mod" and @lemma="er"]/@end]) or
              (@rel="mod" and @lemma="er" and ../node[@rel="su" and not(@pt) and not(@cat)])
             )
          """
          
The condition on the presence of *pt* or *cat* is present to exclude (empty) subject of infinitives and participle clauses, e.g. in *Hij heeft gezwommen* *hij* is an antecedent of an (empty) node acting as the subejct of the past participle *gezwommen*, and we do not want to include that.

The **erx** macro is to ensure that so-called *expletive er* also counts a subject. We implemented this in the following manner. *  *er* is considered (also) expletive (and thus must count as a subject):

* if it precedes the subject  (as in **er** *kwam iemand binnen*, or
* if there is an empty subject, to cover cases such as *wie zwom* **er**. Note that in *wie heeft* **er** gezwommen* this *er* is considered a subject beacuse of the empty subject of the participial clause, which is perhaps not what we want.
 

**Remark**: The condition on the presence of *pt* or *cat* incorrectly excludes *wie* in *wie doet dat*, *wie heeft dat gedaan*: *wie* is a *whd* an an antecedent to  an index node with grammatical relation *su* (see e.g. VKLTarsp, sampl 3, utterance 25 *weet ik niet* **wie** daarin zit. It has no consequences for the scores because *Ond* is not in the form and because in language measures such as OndWB etc a different definition of subject is used. It probably is better to replace the condition on *pt* and *cat* by a condition on the parent node, viz. that it must have as value for the *cat* attribute one of the values from *smain*, *sv1*, or *ssub* (categories for finite clauses or finite clause bodies).



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

    






T067: Onderschikkend: B
"""""""""""""""""""""""


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
""""""""""""""""""""""""


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
"""""""""""""""""""""


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
""""""""""""""""""""""""""


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
                    %realcomplormodnodecount% = 0 )"""

See section :ref:`composedmeasures` for details.

The only special part here is the macro **Tarsp_onlyWinVC**, defined as follows::

    Tarsp_onlyWinVC = """(@rel="vc" and node[@rel="hd" and @pt="ww" and %realcomplormodnodecount% = 0])"""


This covers cases in which the predicate is a nonfite verb. See :ref:`smallclauses` for clarification.

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






T080: Ov7
"""""""""


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

    //node[@lemma="alles"  or @lemma="niets" or @lemma="niks" or (@lemma="wat" and @vwtype= "onbep") or @lemma="u" or @lemma="ons"  or @lemma="zelf"]






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

    //node[@pt="ww" and @pvagr="met-t" and not(%Tarsp_hww% or
     @lemma = "hebben" or
     @lemma = "worden" or
     @lemma = "zijn"   
     ) ]






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

       //node[@cat="top" and count(.//node[@cat="smain" or @cat="cp" or @cat="whsub" or @cat="rel" or @cat="whrel"  or @cat="whq" or @cat="whsub" or 
                                       ( @cat="sv1" and not(parent::node[@cat="whq"]))
                             ]
                     )>=2]






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

       //node[@cat="top" and count(.//node[@cat="smain" or @cat="cp" or @cat="whsub" or @cat="rel" or @cat="whrel"  or @cat="whq" or @cat="whsub" or 
                                       ( @cat="sv1" and not(parent::node[@cat="whq"]))
                             ]
                     )>=3]






T091: V (lijdend)
"""""""""""""""""


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
""""""""""""""""""""


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
""""""""""""""""""""


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

    //node[ (@lemma!="ja" and @lemma!="nee" and @word!="xxx" and @lemma != "mama" and @word!="xx" and 
       ((@pt="tsw" and @lemma!="hè") or
        (@pt="tsw" and @lemma="hè" and @rel="tag" and number(@end)<=number(../node[@rel="nucl"]/@begin)) or
        ((@lemma="au" or @lemma="hoepla" or @lemma="dag" or @lemma="kijk" or @lemma="hap" or @lemma="aai" ) and
         (@rel="--" or @rel="sat" or @rel="tag"))           
         ) )    or  %Tarsp_kijkVU%     or %Tarsp_hehe%
          ]






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

    






T150: V.U. Nee/ja
"""""""""""""""""


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

    //node[%complement% and parent::node[(@cat="smain" or @cat="sv1" or @cat="ssub" or @cat="inf" or @cat="ppart") ]]


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

Predicates that cooccur with a transitive verb are considered modifiers in Tarsp. We exclude them by checking for the presenece of direct object::

    predcB = """(@rel="predc" and 
               (@pt="adj" or @pt="bw" or @cat="ap" or @cat="advp") and
               ../node[@rel="obj1"]
             )"""
             
* **Remark** that fails if the direct object is left out (e.g. by topic drop).

Prepositional complements should be considered modifiers if they cooccur with a verb that can also take locative or directional complements. This has been implemented by **pob1B**::
             
    pobj1B = """(@rel="pc" and ../node[@rel="hd" and %locverb%])"""
    locverb = """(@lemma="staan" or @lemma="zitten" or @lemma="rijden" or @lemma="vallen" or @lemma="doen" or @lemma="gaan" or @lemma="komen" or @lemma="zijn"  or %locmodalverb% )"""

    locmodalverb = """ (@lemma="kunnen" or @lemma="moeten" or @lemma="hoeven" or @lemma="willen" or @lemma="mogen")"""



* **Remark** This language measure is not in the form and has not been kept up to date. In particular, it should be investogated to what extent it differs from the macro **Tarsp_VC** used in the composed language measures. See :ref:`composedmeasures`. 

* **Schlichting** discusses several cases "Voorwerpen" and "Complementen" separately:

 * "**Lijdend Voorwerp**. Het lijdend voorwerp kan meestal gevonden worden door een vraag te stellen met 'wat' betreffende het onderwerp en het werkwoord van de zin. [...] Het lijdend voorwerp van bedrijvende vorm wordt het onderwerp van dezelfde zin in de lijdende vorm." Covered
 * "**Meewerkend Voorwerp**. Het meewerrkend voorwerp kan bijna altijd voorafgegaan worden door 'aan'of 'voor'. Dit 'voor' kan altijd vervangen worden door 'ten behoeve van'. Het meewerkend voorwerp komt niet zo veel voor. het wordt gebruikt bij werkwoorden als 'geven' en 'kopen', en 'schrijven'of 'mededelen'. Covered
 * "**Voorzetselvoorwerp**. Wanneer een werkwoord gebruikt wordt met een vast voorzetselis het zinsdeel dat begin met dat voorzetsel het voorzetselvoorwerp. ook een werkwoordelijke uitdrukking kan gebruikt worden met een voorzetselvoorwerp (*een hekel hebben aan*)." Covered. 
 * "**Complement**. Een aanvulling van het gezegde. het complement kan  zijn:
    1. naamwoordelijk del van het gezegde. Het naamwoordelijk gezegde bestaat uit een koppelwerkwoord en (meestal) een zelfstandig naamwoord of bijvoeglijk naamwooord." (maar ook een voorbeeld met een PP wordt gegeven). Covered
    2. Bepaling van gesteldheid. Deze zegt iets van het werkword en van het onderwerp of lijdend voorwerp. de bepaling van gesteldheid wordt ook wel 'sdubbelverbonden bepaling'genoemd." This covers primary predicates (which Alpino consideres *predc*) but also *secondary predicates* (in Alpino: *predm*, e.g in *ik kan dat* **alleen**). Mostly covered.
    
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



T101: VCWoordgroep
""""""""""""""""""


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
       (@pt="vnw" and @vwtype="vb")) and
       parent::node[(@cat="whsub" or @cat="ssub" or @cat="rel" or @cat="cp" or @cat="whrel") and @rel!="nucl"]
      ]






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
No annotations for this measure occur in the Auris TD and DTD data. The language meausre is absent in [Schlichting 2017].

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






T106: Vo/bij
""""""""""""


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
"""""""""""


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
                     node[@rel="whd"] and
                     node[@cat="sv1" and 
                          @rel="body"  and 
                          %realcomplormodnodecount% = 1
                         ])"""


See section :ref:`composedmeasures` for details.

* **Schlichting**
 
    * "Vraagwoord (+ een of twee Zinsdelen)."Covered
    * Het Vraagwoord zonder meer, of gevolgd door één Zinsdeel komt niet vaak voor. We vinden meestal Vr + X + Y." **Not currently covered**
    * "'Wat is dat?'is bij sommige kinderen als Vaste Uitdrukking geleerd. We scoren deze dan bij Stereotiepe Uitdrukkingen". **Not covered**


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
                    node[@rel="whd"] and
                    node[@cat="sv1" and 
                         @rel="body"  and 
                         %realcomplormodnodecount% = 2
                        ])"""



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
                        node[@rel="whd"] and
                        node[@cat="sv1" and 
                             @rel="body"  and 
                             %realcomplormodnodecount% > 2
                            ])"""



See section :ref:`composedmeasures` for details.

* **Schlichting** "Vraagzinnen die beginnen met een vraagwoord en behalve dat Vraagwoord nog vier of meer Zinsdelen hebben." Covered.


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
              (%Rpronoun% and @begin=../node[@rel="hd"]/@end)) ]]






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
@@add description@@

In a later stage  a query with macros was defined for it, but  the Python function has not been replaced yet.

The query has a straightforward implementation::

    wx = """(%basicimperative% and 
             %realcomplormodnodecount% <= 1)"""

See section :ref:`composedmeasures` for details.


* **Remark** Experiment with replaceing the wx function by the query with macros

* **Schlichting** "de Gebiedende Wijszinnen bestaan in deze fase uit één of twee zinsdelen." Covered


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


T132: woordgroep(onderstrepen)
""""""""""""""""""""""""""""""


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
* **Implementation**: Xpath with macros
* **Query** defined as::

    xenx






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

    //node[(@rel='--' or @rel="nucl") and count(node) = 2 and node[ @lemma!="niet"] and 
       (node[@lemma="niet" ] or 
        node[@cat="advp" and node[@lemma="niet"] ]
       )
      ]






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

    
        //node[@pt="vnw"  and @vwtype="pers" and @getal="ev" and @genus="fem"   and @pdtype="pron"]







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
      (node[@pt="n" or (@pt="tw" and @numtype="hoofd") or (@lemma="paar" and @pt="lid")] or 
       node[@cat="du" and node[@pt="n" or (@pt="tw" and @numtype="hoofd") or (@lemma="paar" and @pt="lid")]]) and 
      count(.//node[%realnode%])=1]






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

    //node[@cat="top" and .//node[node[@pt="n" and @rel="hd"] and node[@pt="n" and not(@rel="hd")] ] or
          node[@cat="du" and count(node[@rel="dp" and @pt="n"])>=2]
          ]






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

    






T151: V.U. Totaal
"""""""""""""""""


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
""""""""""""""


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
""""""""""""""


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
""""""""""


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
"""""""""""


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

    






T157: Screening
"""""""""""""""


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
""""""""""


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
"""""""""


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
""""""""""


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
"""""""""""


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
""""""""


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
"""""""""""""""


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






















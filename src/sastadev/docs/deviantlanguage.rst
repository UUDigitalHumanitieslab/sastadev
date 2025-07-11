Deviant Language
================

The input for SASTA contains a lot of deviant language. Language is of course deviant when it does not adhere to the rules of the Dutch language. 
But since in SASTA Alpino is the approximation of these rules, what really counts as deviant is what is deviant relative to the Alpino grammar. We will see several examples of this below.

Deviant language can be avoided by using CHAT-annotations. But CHAT-annotations are not always used, and even if they are  used, they are not used 
systematically and consistently. 

We will first describe the general strategy that SASTA follows to deal with deviant language.

General Strategy
----------------


We first give a global overview of the strategy followed, and illustrate it with a simple example. This involves the following steps:

#. It is assumed that the whole sample has been parsed as is, and has resulted in a treebank.
#. An attempt is made to identify a deviant configuration in each utterance in the treebank that has to be analysed. This is usually done by identifying specific patterns in the input string. The procedure can also investigate the syntactic structure, and this is used, but its use is limited because the syntactic structure is usually not very informative exactly because of the deviancy in the utterance. For example, in the utterance *bij die varken*, SASTA should identify deviant language (the *de*-word *die* is immediately followed by a *het*-word (*varken*).
#. SASTA attempts to make a correction, or even multiple alternative corrections. So *bij die varken* is replaced by *bij dat varken*, with *die* replaced by *dat*. SASTA also adds metadata to reflect this correction. These corrections can involve replacements of one word by another word, insertions of a word, deletions of a word or word sequence, or expansion of a word into a sequence of words. Of course, multiple corrections can be applied to a single utterance.
#. SASTA parses the corrected utterance(s).
#. It then evaluates the original and corrected utterances, by a complex evaluation measure, which involves inter alia the degree of grammatical cohesion, the number of deviant configurations present, and the number of unknown words present.
#. SASTA selects the best one, with its metadata
#. SASTA then replaces the corrections by the original words, sometimes with the properties of the original word in the parse of the corrected utterance. In the example, the correction *dat* is replaced by the original word *die* (and its grammatical properties), so that the utterance has the syntactic structure of the utterance  *bij dat varken*, but contains the word *die* (with its properties) instead of *dat* (and its properties).
#. The grammatical analysis of the relevant method is applied, in the normal way.  
#. SASTA generates, on the basis of the metadata produced,  an error report, which specifies each error that has been found, how it has been corrected, and some additional information.
#. SASTA also generates an error logging file, which specifies all the alternatives that have been considered, and which one is considered the best one according to the evaluation criterion.

A corrected treebank is generated by a call in *sastadev* to the function *correcttreebank* in the module *correcttreebank*:

.. autofunction:: sastadev.correcttreebank::correcttreebank

Each syntactic structure in the input treebank is corrected by the function *correct_stree* in the module *correcttreebank*.

.. autofunction:: sastadev.correcttreebank::correct_stree

Since in the corrected utterance multiple words may have to be inserted or removed, and since the linear order in Alpino syntactic structures is indicated by means of *begin* and *end* attributes (see :ref:`alpinoparser`), SASTA uses "inflated" syntactic structures, i.e syntactic structures in which the *begin* attribute of the first original word has the value *'10'*, and the *begin* attribute of the next word has the value *'20'*. The values of the *end* attribute are equal to str(int(begin) + 1 ), as usual. This enables one to delete and insert nodes for words without having to adapt the *begin* and *end* values of each node. Inflating a syntactic structure in this way is done by the function *treeinflate* in the module treebankfunctions.

.. autofunction:: sastadev.treebankfunctions::treeinflate

Various Types of Deviant Language 
---------------------------------

Deviant language occurs in many different forms. We discuss the most important ones here.


Deviant Transcriptions
^^^^^^^^^^^^^^^^^^^^^^

We give the transcription, the correct transcription after a slash, a translation between round brackets, 
the reason why the transcription is deviant, and how and where this is dealt with

Final n not pronounced after schwa
""""""""""""""""""""""""""""""""""

Example: *mouwe* /	*mouwen* (sleeves): This is dealt with in the function *getalternativetokenmds* in the module corrector. For any unknown word that ends in *e* an alternative is generated with an *n* attached, if the resulting word is a known word. 

Dee
"""

The string *dee* must sometimes be interpreted as *deze* (this), sometimes as *deed* (did). Both alternatives are generated in the function *getalternativetokenmds* in the module corrector.

Moe
"""

The string *moe* must sometimes be interpreted literally  as *moe* (tired), sometimes as *moet* (must). If *moe* is used as *moet* in an utterance, Alpino usually cannot make anything of it.  We have defined a query to identify occurrences of *moe* that has no grammatical connections, and then replace it with *moet* as one alternative. 

**Remark** This should be generalised, because *moe* that should be interpreted as *moet* sometimes does have grammatical relations with other words

Basic Replacements
""""""""""""""""""

For an utterance that contains a word that occurs with a deviant spelling (e.g. *as* instead of *als*) an alternative variant is generated containing the correct spelling ("als") and with metadata about this replacement. This is done in function *getalternativetokenmds* in the module *corrector* by checking whether the word occurs in the dictionary *basicreplacements*:

.. autodata:: sastadev.basicreplacements::basicreplacements
   :no-value:
   
Basic Expansions
""""""""""""""""
For an utterance that contains a contracted word (e.g. *das* instead of *dat is*) an alternative variant is generated containing the expansion ("dat is") and with metadata about this replacement. This is done in function *getalternatives* in the module *corrector* by applying the function *getexpansions*:

.. autofunction:: sastadev.corrector::getexpansions


Verb form + *ie* written as one word
""""""""""""""""""""""""""""""""""""

Example: *gaatie*	/ *gaat ie* (goes he): probably written as one word because it is pronounced as one word. This is dealt with by the *gaatie* function in the corrector module:

  * .. autofunction:: sastadev.corrector::gaatie

Dehyphenation
"""""""""""""
* *zie-ken-huis* / *ziekenhuis* (hospital):	syllables pronounced separately (used mostly in ASTA). This is dealt with in  the function *getalternativetokenmds* in the module corrector by a call to the function *fullworddehyphenate*:

   * .. autofunction:: sastadev.stringfunctions::fullworddehyphenate 


(Regional) informal spoken language
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _ie-diminutives:

*ie*-diminutives
""""""""""""""""

.. automodule::  sastadev.iedims




Incorrect possessive pronouns
"""""""""""""""""""""""""""""

Often *me* and *ze* (sometimes spelled as *su*) are used as possessive pronouns, a phenomenon typical for informal spoken Dutch.
Alpino can deal with *me* as a possessive pronoun, so we need not do anything. It is treated as if there were "m'n".
Alpino cannot deal with *ze* or *su* as a possessive pronoun, so we replace *ze* if followed by a word that can be a noun by "z'n", and return this as an alternative to be considered.

**Remark** There are some conditions on the relation that *ze* bears in the syntactic tree. I am not sure this necessary or desirable.

.. _initdevoicing:

Initial Devoicing of fricatives
"""""""""""""""""""""""""""""""

The voiced fricative consonants /v/ and /z/) are often pronounced voiceless, and this is often reflected in the transcript. Examples are *sit* instead of *zit*, *fan* instead of *van*, etc. An alternative with a voiced initial fricative is generated by the function *initdevoicing* from the module *corrector*. This function is called both for /f/-/v/ and for /s/-/z/:

.. autofunction:: sastadev.corrector::initdevoicing

Wrong pronunciation of content words in the transcript
""""""""""""""""""""""""""""""""""""""""""""""""""""""




@@to be added@@

.. _grammaticalerrors:

Grammatical Errors
^^^^^^^^^^^^^^^^^^

.. _detagreementerrors:

Determiner agreement errors
"""""""""""""""""""""""""""

Determiner Agreement errors (e.g. *de huis* instead of *het huis*) are dealt with by the function *getwrongdetalternatives* from the module *corrector*.

.. autofunction:: sastadev.corrector::getwrongdetalternatives


  

.. _subjectverbagreement:

Subject Verb Agreement
""""""""""""""""""""""

.. _overgeneralisation:

(Wrong) Overgeneralisation
""""""""""""""""""""""""""

Children often overgeneralise when inflecting words. SASTA contains facilities for identifying such overgeneralisations (e.g. *gekijkt*) and replace them by the correct forms (e.g. *gekeken*). The overgeneralisations are sometimes also wrong overgeneralisations (e.g. *gekeekt*), and transcripts can contain spelling errors in such overgeneralised form (*gevalt* instead of *gevald* is a case we encountered), or reflect a particular pronunciation (*ekeekt* instead of *gekeekt*).

SASTA currently only covers overgeneralisations of verbs. The matter is not completely trivial, because apart from the app. 200 irregular simplex verbs (e.g. *slapen*, *kopen*) there are many more consisting of a prefix in combination with an irregular verb. The prefix can be a separable prefix (e.g. *uitslapen*, *inkopen*) or an inseparable prefix (e.g. *verslapen*, *verkopen*), or even both (e.g. *doorverkopen*). In verbs with a non-separable prefix such as *ver*  or *be* one must take into account that the past participle prefix *ge* cannot appear (cf. *gekocht*, *ingekocht* v. *verkocht*, *doorverkocht*).

This is dealt with in the function *getalternativetokenmds* of the module *corrector* by a call to the function *correctinflection* of the module *deregularise* applied to a word that is unknown.

.. autofunction:: sastadev.deregularise::correctinflection


For more details, see the module  :ref:`deregularise`.

.. _disambiguatingwords:

Disambiguating words
^^^^^^^^^^^^^^^^^^^^

Certain words are ambiguous but have one reading that is most plausible or even the only one possible for young children. For example, the word *dicht* can be an adjective ('closed') for an inflected form of the word *dichten* ('to write poetry'). 

We gathered a list of words with such ambiguities, and manually selected the most plausible one. We later checked that these words  indeed do not occur in the top 3000 words used by young children under their less plausible reading.

In order to prevent an analysis with the less plausible reading by Alpino we replace the relevant words by a diferent non-ambiguous word with the same grammatical properties as the word under the most plausible reading. For example, the word *dicht* is replaced by the word *mooi*, which is also an adjective but has no verbal (or other) reading. Since this lack of ambiguity is typical for young children, this replacement is only done for the methods TARSP and STAP.

The replacement is carried out in the function *getalternativetokenmds* of module *corrector* by checking whether the word occurs in the *disambiguationdict* and replacing it by the replacement specified there.

.. autodata:: sastadev.corrector::disambiguationdict
    :no-value:
 

.. _limitationsofalpino:

Limitations of Alpino
^^^^^^^^^^^^^^^^^^^^^

.. _smallclauses:

Small clauses
"""""""""""""

.. automodule:: sastadev.smallclauses

.. vz+defdet:

Adposition plus demonstrative pronoun
"""""""""""""""""""""""""""""""""""""

Alpino cannot deal with combinations of adposition + a substantively used demonstrative pronoun (e.g. *naar dit*, *over dat*, *naar deze*, *tegen die*).
It can deal with the (very formal) combination *in deze*, which it treats as a multiword unit.

This is reasonable for adult language, since most often an R-pronoun + an adposition are used instead of adposition + demonstrative pronoun. But in children's language this is different: the combinations occur frequently.

SASTA replaces a demonstrative pronoun immediately preceded by an adposition by the pronoun *hem*, then parses the new string, and replaces *hem* and its properties in the parse by the original demonstrative pronoun and its properties.

SASTA cannot always determine upon the substitution whether the demonstrative pronoun has been used substantively or attributively. It does a replacement, and assumes that sentences with attributive demonstrative pronouns replaced by *him* will yield a worse parse than  a sentence with an unreplaced attributive demonstrative pronoun.

Examples: 

* For the utterance *maar eigenlijk mag niet mensen opeten van* **deze** *?* an alternative is generated *maar eigenlijk mag niet mensen opeten van* **hem** *?*. The alternative gets a better parse and is selected.

* For the utterance *is helemaal veilig bij* **dat** *varken* an alternative is generated *is helemaal veilig bij* **hem** *varken* but that sentence gets a worse parse than the original utterance, so this proposed correction is rejected.

These replacements are done in the function *getalternatives* from the module *corrector* by a call to the function *correctPdit*.

.. autofunction:: sastadev.corrector::correctPdit
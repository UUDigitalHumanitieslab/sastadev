Implementation of the methods
=============================

The selection of the utterances to be analyzed  is currently not done by SASTA (though it probably is possible, and it is planned to experiment with it).
 
Each method is described by a set of language measures. Each language measure has a number of properties, the most prominent one of which is   the query. Each method is represented as a table in an Excel document, in a subfolder *methods* in the code folder, with the language measures in the rows and the language measure properties in the columns.

Each language measure has the following properties:

* **ID** Each language measure has an ID, which consists one one letter and 3 digits. Tarsp IDs start with T, ASTA IDs start with A, and STAP IDs start with S.
* **Category**: Each language measure can belong to a category, for example Zinsconstructies, Verbindingswoorden, Woordgroepen in TARSP.
* **Subcat**: Each language measure can belong to a subcategory, e.g. Vragen, Mededelende Zinnen in TARSP.
* **Level**: Each language measure can belong to a level. In Tarsp this is usually an abbreviation for the Category property, e.g. Zc, Sz, VVW.
* **Item**: the code to use to annotate the language measure, e.g. Avn, BBX in TARSP, M, N, LEX in ASTA, VT, VN, SGG in STAP. Case is never significant in codes.
* **Altitems**: alternative codes that one can use to annotate the language measure, e.g. hwwi next to hww i, hww Z next to hwwZ (TARSP), del lidwoord next to dellid (ASTA), . In this way we are robust to variant notations and frequently made typo’s (e.g., BIJZ, BIJZN, BIJZIJN for BIJZIN in ASTA)
* **Implies**: Especially relevant in TARSP to cover specific ways of coding. Using a particular code implies that some other codes are also implicitly coded. See below for explanation. Example: coding OndWB implies coding Ond, W and B.
* **Original**: Possible values are yes or no. We sometimes make language measures that are not original to the method, for research or development purposes. For example, in TARSP we defined a language measure for verb-initial utterances (T054, Sv1) and for utterances without a finite verb (T122, PV-loos). This property is used to distinguish these from original language measures
* **Pages**: mentions the pages in the book or article that describes the method where this language measure is described.
* **Fase**: (used in TARSP only): stage that the language measure belongs to
* **Query**: the query that implements the language measure
* **Inform**: specifies whether the language measure appears in the form associated with the method. See below for more explanation.
* **Screening**: (relevant for Tarsp only) whether the query is relevant for the TARSP Screening procedure.
* **Process**: Language measures come in 4 process categories. Language measures with the same process category are applied in an indeterminate order and they cannot use results of other language measures from this process category. The four process categories are:

  * **Pre**: Prequeries: these are performed first
  * **Core**: Core queries: these are performed next, and they can make use of the results of the prequeries;
  * **Post**: Postqueries: these are performed next, and they can make use of the results of the prequeries and the postqueries, and are generally used to aggregate results;
  * **Form**: Form queries: these are performed last, can make use of results obtained so far, usually do some further aggregation and  they make the forms.

* **Special1**: Originally intended for future extensions. Currently in use for marking Star1 and Star2 language measures in TARSP (e..g T001, (Vr)WOnd+ occurs in Schlichting(2005) as (Vr)WOnd+** (with two stars), and therefore it has been marked as Star2. @@
* **Special2**: Originally intended for future extensions. Currently in use for filtering or allowing certain results depending on the function specified (see passfilter below), used to deal with certain interdependencies between prequery and corequery language measures.
* **Comments**: for any comments
    
The language measures with  their properties are internally stored in a QueryDict: a dictionary with as key the QueryId, and as value a Query object

A special class *Method* has been defined in the module methods.py. 

.. autoclass:: methods::Method




A method is read in by the read_method function in the readmethod.py module. 

Queries
-------

Queries take as input a syntactic structure for an utterance with utterance id *uttid*, implemented in sastadev as an lxml.etree Element.
They return a list of syntactic structures (the ones that match with the query), each an lxml.etree Element. Code around the application of a query turns this list of syntactic structures into a Counter with *(uttid, position)* as keys. The position is equal to the value of the *end* attribute of the leftmost word of the matching syntactic structure, or *0* if no match with a specific word can be indicated (in case of deleted or absent words). Such results are called *exact results* because they align the query to a particular word in the utterance. A Counter for a given query is stored in a dictionary with the query id as key and the Counter as value.

Actual comparisons with references to compute performance do not take the alignment into account, so the exact results are turned into (inexact) results which is a Counter with *uttid* as key. However, comparisons with references for development and debugging purposes (e.g. to create the "platinum check" files) do take the alignment into account. 


Queries can be formulated in three different ways:

* Using pure Xpath
* Using Xpath queries in combination with macros.
* Python functions

We will discuss each of them in a separate subsection.

Xpath
^^^^^

This is an example of an Xpath query, it is the query for the language measure T015 (BepBvZn) in TARSP::

	//node[@cat="np" and
		node[@rel="det" ] and
		node[@rel="mod" and @pt="adj"] and
		node[@rel="hd" and @pt="n"]]

It searches for a node (*node*) anywhere in the structure (*//*) where attribute (*@*) *cat* (category) has the value (*=*)  *np* (“*np*”, noun phrase), and that contains (at least) three nodes:

* A node with attribute *rel* set to *det* (determiner)
* A node with attribute *rel* set to *mod* (modifier) and attribute *pt* (part of speech) set to *adj* (adjective)
* A node with attribute *rel* set to *hd* (head) and attribute *pt* set to *n* (noun)

An Xpath query in SASTA  must start with *//* (it is necessary in the query and it distinguishes Xpath queries from python functions here). *//* means: search anywhere in the tree.

Note that inside the Sasta code each Xpath query gets “.” (meaning: from this point on) put in front of it. This is needed because in SASTA (like in GrETEL and in contrast to PaQu) there is only a single document for the whole treebank (but no documents for the individual utterances), and // would cause a search in the whole treebank, not only in the current utterance.

Macros 
^^^^^^

Xpath is a very simple language, and many things that you want to express in it can only be expressed in a very cumbersome manner. Furthermore, certain parts of queries recur in multiple queries, and these should be defined only once to keep them compatible. For example, the definition of auxiliary verb occurs both in *Hww i* and in *HwwZ*, and that definition is pretty cumbersome, in part because Alpino does not itself have the notion of auxiliary verb, in part because of the limited expressivity of Xpath.

Xpath is so simple in part because it is usually used inside Xquery programs. Xquery is a full-fledged programming language with good expressivity. But in the GrETEL and SASTA context we do not have Xquery.
In order to avoid these problems we introduced macros, inspired by their use in the PaQu and GRETEL applications. A macro is nothing more than a string to abbreviate another string. A macro in SASTA (and in GrETEL, and in PaQu) is surrounded by % signs.

Macros are defined in text files inside a subfolder named macros of the code folder. Currently three macrofiles exist, but they should be reorganised into 4 files: one for general macros, and one for each method. These macro files are read in, parsed and stored for use in the macro expansion function every time Sasta is run, as defined in the module macros.py.  

This is an example of a macro definition::

   nonfinvc = """(@rel="vc" and %nonfincat%) """

Here the macro *nonfinvc* is defined as (*=*) *(@rel="vc" and %nonfincat%)*.

As one can see this macrodefinition contains another macro, *nonfincat*, between % signs. That macro is defined as::

   nonfincat = """(@cat="inf" or @cat="ppart")"""

where the definition only contains pieces of Xpath-code.

Inside SASTA an Xpath query is first expanded so that all macros have been replaced by pieces of Xpath code. Only then is the query launched. 
The module that takes care of macros is the module macros.py:

.. automodule:: macros

The expansion function in this module  is called *expandmacros*. It takes as input a string and outputs a string with the macros expanded:

.. autofunction:: macros::expandmacros

Expanding the following Xpath expression::

   //node[%nonfinvc%]

Results in::

   //node[(@rel="vc" and (@cat="inf" or @cat="ppart")) ]

It is often desirable to test the correctness of the definition of a macro before it is included in the SASTA system. In the SASTA scripts there is a script *expandquery.py* which takes as input a query and puts the expansion in a 
file called *expandedqueries.txt*. The expanded query can then be copied and pasted in GrETEL (which contains an Xpath parser and reports any errors) or any other Xpath validation programme, and can be tested in GrETEL.
This is the usage information of the expandquery.py script::

	Usage: expandquery.py [options]
	Options:
	  -h, --help            show this help message and exit
	  -f INFILENAME, --file=INFILENAME
							File that contains the query to be expanded
	  -q QUERY, --query=QUERY
							query as a string

It is strongly recommended to have macro definitions begin and end with round brackets to avoid any operator priority issues. And generally, macros for conditions on nodes are often more reusable than macros for full nodes.
If one looks in the macro files, one quickly sees that many macros are defined in terms of multiple other macros, e.g. the definition of Tarsp_OndWBVC uses 6 macros in its definition::

	Tarsp_OndWBVC = """
	(%declarative% and %Ond% and  %Tarsp_W% and %Tarsp_B_X% and %Tarsp_VC_X% and %realcomplormodnodecount% = 3 )
	"""

.. _generatemacros:

Generation of macros
""""""""""""""""""""

Macros make writing queries much simpler and makes it easier to maintain them. But in some cases macros are not enough, e.g. if a macro expansion is very large but built up in a regular way. One such case is dealt with by the module generatemacros.py:

.. automodule:: generatemacros

Python functions
----------------

In some cases formulating the query in Xpath is too cumbersome (even with macros). For such cases we can fall back on queries formulated in Python.

In the definition of the query one includes the name of the Python function, for example (from TARSP): *sziplus6*.
This function must be defined somewhere, of course. This can be done in any python module.

.. automodule:: external_functions




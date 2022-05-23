CHAT-annotations
================

SASTA supports input in the CHAT format and it can deal with the CHAT annotations in utterances.

The CHAT format in general and in particular its metadata are dealt with by the chamd module, which is part of the DH Lab github repository `chamd <https://github.com/UUDigitalHumanitieslab/chamd>`_.

The CHAT annotations have changed slightly over time, and the CHILDES website only contains the latest version of the documentation. Two versions of the CHAT manual are available in the `SASTA Documentation Google Drive <https://drive.google.com/drive/folders/1N0uz92GkyOdZMc-d3dVKQG9kBh53uTPf?usp=sharing>`_: chat.pdf is the 2015 version of the CHAT manual, chat2020-06-19.pdf is the version of 2020-06-19.

SASTA actually uses two different modules to deal with CHAT annotations. The first one was developed outside of SASTA in the context of the AnnCor project, and is also used in GrETEL.
This module is based on the 2015 version of the CHAT manual. [#fn4]_ It is included in the DH Lab GitHub  repository chamd, as the module cleanCHILDESMD.py. It deals with the CHAT annotations by removing them or applying them, in accordance with the conventions for generating MOR and GRA tiers. [#fn5]_ The relevant function is cleantext::

   cleantext (utt: str, repkeep:bool) -> str

Where utt is the parameter for the input string, and the boolean parameter repkeep is for an alternative option of cleaning but it must always be False in the SASTA context.  
This module generates output that is compatible with PaQu Enhanced Plain (`PEP <https://paqu.let.rug.nl:8068/info.html#cormeta>`_) text format, which is used in PaQu and GrETEL for uploading corpora with metadata.  The name PEP-text is not a standard name but was invented by Jan Odijk for this format.

The second module has been developed in SASTA, and it has the same functionality as cleanCHILDESMD.py, but it translates the annotations into metadata, so that queries on CHILDES annotations can be done using Xpath. In addition, the output can be either a string or a list of tokens. The output is therefore a Tuple of  cleaned text and metadata. The relevant module is cleanCHILDEStokens.py, and the relevant function::

  cleantext(utt: str, repkeep: bool, tokenoutput: bool=False) ->  Tuple[CleanedText, Metadata]:

Where:

* CleanedText = Union[List[Token], str], where Token is defined in the module sastatoken.py
* Metadata = List[Meta], where Meta is defined in the module metadata.py

The second module is used in the modules to correct the syntactic structures, and it yields output that is not compatible with PEP text format, because the PEP text format is too simple for this.

In the future we must consult with Gertjan van Noord to extend the PEP text format somewhat so that it can accommodate these metadata and then GrETEL and PaQu should be updated accordingly.

.. rubric:: Footnotes
.. [#fn4] However, the code for lengthened syllables (‘:’) was not dealt with because it was rarely used in Dutch CHILDES corpora, and it caused many problems for the use of ‘:’ as a regular interpunction sign.
.. [#fn5] With some alternative options, e.g., false starts (retracings with correction) can be removed or kept.
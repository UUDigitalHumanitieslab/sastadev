Methods
=======

SASTA supports multiple methods, and has concrete implementations for TARSP, STAP (Van Ierland et al. 2008, Verbeek et al 2007), and ASTA.

Some of these methods have variants, in particular for TARSP there are TARSP2005 (Schlichting 2005),  TARSP2017_1-4, and TARSP2017_4-6 (Schlichting 2017); for ASTA there is ASTABasic (Boxum et al. 2013, ASTA Appendix), and ASTAExtended (Boxum et al. 2019). [#f1]_

Currently SASTA only supports one variant for each method, viz. TARSP2005 and ASTAExtended.  Support for the other variants requires some extensions, both to describe them as variants, and for implementing them (esp. TARSP2017).

These methods consist of multiple components. They prescribe how a sample should be collected, what size it is, and what it should contain. They also prescribe how the sample should be split up into utterances. SASTA does nothing for these aspects, this is the responsibility of the linguist.

SASTA prescribes how the sample should look like. Supported input formats are a SASTA-specific Word file (docx) or CHAT (MacWhinney 2000).

The linguist has to indicate via metadata which utterances should be analysed. Multiple options are offered for that. It is planned to have the relevant utterances selected automatically by SASTA, but this is currently not the case yet.

It is desirable to include in a sample not only the utterances of the target child or the person with Aphasia (PMA) but also the utterances of the interviewer or other participants in the session. However, the latter is not obligatory.

Each method defines so-called language measures. A transcript of a spontaneous language session is annotated with codes to indicate which language measures are applicable in which utterance. Sometimes the codes are aligned with specific words, but that is often not the case.  


TARSP Annotations
-----------------

SASTA outputs only codes for  language measures that are included in the method-specific form.

The TARSP language measures for ‘Zinsdelen’ are Ond, W, VC, and B. Of these, only W occurs in the form.

There are a lot of language measures in TARSP that have a code that combines Ond, W, VC and or B, e.g. OndWVC, BWOndBB, etc. These are all included in the form. Many annotators split up codes such as OndWVC into three codes Ond, W and VC and align these to the relevant words. This is e.g. the case in Schlichting’s (2005, 2017) appendix. It was also the case in many of the data supplied by the VKL members. However, this is not the way it should be done. One always has to specify codes such as OndWVC, BWOndBB, etc. as a single code either unaligned, or under the first word where it applies. 

These codes have a different meaning than the separate codes,e.g.:

* Separate codes Ond, W, and VC mean that there is a subject, a predicate (‘gezegde’) and a verbal complement  in the utterance, 
* The code OndWVC states this as well, but in addition

  *  that these are contained in a declarative clause
  * And that Ond, W and VC have a direct grammatical relation to each other (Ond is the subject of W, and VC is a verbal complement to W)

One can also specify the individual codes Ond, B, and VC, but that is not obligatory. W, however, should be specified. If none of the individual codes Ond, B, VC and W are annotated, one should use the -i (implies) option of sastadev. 

The imply method currently does not work properly for codes such as Hww i, HwwZ, and HwwVd. If we mark them to imply the code W, we will get too many W codes if e.g. OndWVC is also present; if we do not mark them as such, we will miss cases where Hww i occurs but no OndWVC or similar code (this is currently the case). We should introduce a different coding for such cases. And then adapt the imply method.

.. rubric:: Footnotes
.. [#f1] The labels for these variants are not standard and have been invented here.

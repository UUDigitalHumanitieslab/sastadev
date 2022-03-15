from lxml import etree
from treebankfunctions import showtree
from asta_queries import asta_bijzin

streestrings = {}

streestrings[0] = """
<alpino_ds version="1.3">
  <metadata>
<meta type="text" name="charencoding" value="UTF8"/>
<meta type="text" name="childage" value=""/>
<meta type="text" name="childmonths" value=""/>
<meta type="text" name="session" value="ASTA_sample_05"/>
<meta type="text" name="origutt" value="uh dus sinds ik hier ben heb ik logo omdat ik "/>
<meta type="text" name="parsefile" value="Unknown_corpus_ASTA_sample_05_u00000000006.xml"/>
<meta type="text" name="speaker" value="PMA"/>
<meta type="int" name="uttendlineno" value="17"/>
<meta type="int" name="uttid" value="4"/>
<meta type="int" name="uttstartlineno" value="17"/>
<meta type="text" name="name" value="pma"/>
<meta type="text" name="SES" value=""/>
<meta type="text" name="age" value=""/>
<meta type="text" name="custom" value=""/>
<meta type="text" name="education" value=""/>
<meta type="text" name="group" value=""/>
<meta type="text" name="language" value="nld"/>
<meta type="text" name="months" value=""/>
<meta type="text" name="role" value="Other"/>
<meta type="text" name="sex" value=""/>
<meta type="text" name="xsid" value="4"/>
<meta type="int" name="uttno" value="6"/>
<xmeta annotatedposlist="[10]" annotatedwordlist="['uh']" annotationposlist="[10]" annotationwordlist="['uh']" atype="text" backplacement="0" cat="Syntax" name="ExtraGrammatical" penalty="10" source="SASTA" subcat="None" value="Filled Pause"/><xmeta annotatedposlist="[]" annotatedwordlist="[]" annotationposlist="[]" annotationwordlist="['uh', 'dus', 'sinds', 'ik', 'hier', 'ben', 'heb', 'ik', 'logo', 'omdat', 'ik']" atype="list" backplacement="0" cat="None" name="tokenisation" penalty="10" source="CHAT/Tokenisation" subcat="None" value="['uh', 'dus', 'sinds', 'ik', 'hier', 'ben', 'heb', 'ik', 'logo', 'omdat', 'ik']"/><xmeta annotatedposlist="[]" annotatedwordlist="[]" annotationposlist="[]" annotationwordlist="['uh', 'dus', 'sinds', 'ik', 'hier', 'ben', 'heb', 'ik', 'logo', 'omdat', 'ik']" atype="list" backplacement="0" cat="None" name="cleanedtokenisation" penalty="10" source="CHAT/Tokenisation" subcat="None" value="['uh', 'dus', 'sinds', 'ik', 'hier', 'ben', 'heb', 'ik', 'logo', 'omdat', 'ik']"/><xmeta annotatedposlist="[]" annotatedwordlist="[]" annotationposlist="[10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110]" annotationwordlist="[10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110]" atype="list" backplacement="0" cat="None" name="cleanedtokenpositions" penalty="10" source="CHAT/Tokenisation" subcat="None" value="[10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110]"/><xmeta annotatedposlist="[]" annotatedwordlist="[]" annotationposlist="[]" annotationwordlist="dus sinds ik hier ben heb ik logo omdat ik" atype="text" backplacement="0" cat="Correction" name="parsed_as" penalty="10" source="SASTA" subcat="None" value="dus sinds ik hier ben heb ik logo omdat ik"/></metadata>
<node begin="10" cat="top" end="111" id="0" rel="top">
    <node begin="100" conjtype="onder" end="101" frame="complementizer" id="1" lcat="--" lemma="omdat" pos="comp" postag="VG(onder)" pt="vg" rel="--" root="omdat" sense="omdat" word="omdat"/>
    <node begin="10" end="11" frame="--" genus="zijd" getal="ev" graad="basis" his="skip" id="1" lcat="--" lemma="uh" naamval="stan" ntype="soort" pos="--" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="--" root="uh" sense="uh" word="uh"/>
    <node begin="20" cat="du" end="111" id="2" rel="--">
      <node begin="20" cat="du" end="91" id="3" rel="dp">
        <node begin="20" end="21" frame="complementizer(root)" id="4" lcat="du" lemma="dus" pos="comp" postag="BW()" pt="bw" rel="dlink" root="dus" sc="root" sense="dus" word="dus"/>
        <node begin="30" cat="smain" end="91" id="5" rel="nucl">
          <node begin="30" cat="cp" end="61" id="6" rel="mod">
            <node begin="30" end="31" frame="complementizer" id="7" lcat="cp" lemma="sinds" pos="comp" postag="VZ(init)" pt="vz" rel="cmp" root="sinds" sense="sinds" vztype="init" word="sinds"/>
            <node begin="40" cat="ssub" end="61" id="8" rel="body">
              <node begin="40" case="nom" def="def" end="41" frame="pronoun(nwh,fir,sg,de,nom,def)" gen="de" getal="ev" id="9" lcat="np" lemma="ik" naamval="nomin" num="sg" pdtype="pron" per="fir" persoon="1" pos="pron" postag="VNW(pers,pron,nomin,vol,1,ev)" pt="vnw" rel="su" rnum="sg" root="ik" sense="ik" status="vol" vwtype="pers" wh="nwh" word="ik"/>
              <node begin="50" end="51" frame="er_loc_adverb" getal="getal" id="10" lcat="advp" lemma="hier" naamval="obl" pdtype="adv-pron" persoon="3o" pos="adv" postag="VNW(aanw,adv-pron,obl,vol,3o,getal)" pt="vnw" rel="ld" root="hier" sense="hier" special="er_loc" status="vol" vwtype="aanw" word="hier"/>
              <node begin="60" end="61" frame="verb(unacc,sg1,ld_adv)" id="11" infl="sg1" lcat="ssub" lemma="zijn" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="ben" sc="ld_adv" sense="ben" tense="present" word="ben" wvorm="pv"/>
            </node>
          </node>
          <node begin="70" end="71" frame="verb(hebben,sg1,transitive_ndev)" id="12" infl="sg1" lcat="smain" lemma="hebben" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="heb" sc="transitive_ndev" sense="heb" stype="declarative" tense="present" word="heb" wvorm="pv"/>
          <node begin="80" case="nom" def="def" end="81" frame="pronoun(nwh,fir,sg,de,nom,def)" gen="de" getal="ev" id="13" lcat="np" lemma="ik" naamval="nomin" num="sg" pdtype="pron" per="fir" persoon="1" pos="pron" postag="VNW(pers,pron,nomin,vol,1,ev)" pt="vnw" rel="su" rnum="sg" root="ik" sense="ik" status="vol" vwtype="pers" wh="nwh" word="ik"/>
          <node begin="90" end="91" frame="noun(het,count,sg)" gen="het" genus="onz" getal="ev" graad="basis" id="14" lcat="np" lemma="logo" naamval="stan" ntype="soort" num="sg" pos="noun" postag="N(soort,ev,basis,onz,stan)" pt="n" rel="obj1" rnum="sg" root="logo" sense="logo" word="logo"/>
        </node>
      </node>
      <node begin="110" case="nom" def="def" end="111" frame="pronoun(nwh,fir,sg,de,nom,def)" gen="de" getal="ev" id="15" lcat="np" lemma="ik" naamval="nomin" num="sg" pdtype="pron" per="fir" persoon="1" pos="pron" postag="VNW(pers,pron,nomin,vol,1,ev)" pt="vnw" rel="dp" rnum="sg" root="ik" sense="ik" status="vol" vwtype="pers" wh="nwh" word="ik"/>
    </node>
  </node>
  <sentence sentid="4">uh dus sinds ik hier ben heb ik logo omdat ik</sentence><comments>
    <comment>Q#ng1647271273|dus sinds ik hier ben heb ik logo omdat ik|1|3|-0.6490448165400009</comment>
  </comments>
</alpino_ds>
"""


strees = {}
for x in streestrings:
    strees[x] = etree.fromstring(streestrings[x])

thequery = """
.//node[
    ( (@word="geboren")  or
      
    (@pt="adj" and 
     (@rel="mod" and 
      parent::node[@cat="np"] and 
      ../node[@rel="hd" and (@pt="n" or @pt="vnw" or @cat="mwu")] and
	  (not(@begin < ../node[@rel="det" and (@pt="lid" or @pt="vnw")]/@begin) or @lemma='heel' or @lemma='geheel')
	 )
	)
 or
     
   (@pt="adj" and
    (@rel="hd" and
     parent::node[@cat="ap" and parent::node[@cat="np"] and 
     ../node[@rel="hd" and (@pt="n" or @pt="vnw" or @cat="mwu")]]
	 )
	)
 or
     
   (@pt="tw" and @numtype="rang")
 or
      
   (@pt="adj" and @rel="hd" and parent::node[@cat="np"])
 or
     
    (
   (@pt="tw" and @numtype="rang")
 and @positie = "nom" )
 or
	 
   (@pt="ww" and @wvorm="vd" and @rel="mod" and parent::node[@cat="np"])
 or
	 
   (@pt="ww" and @wvorm="od" and @rel="mod" and parent::node[@cat="np"])
 or
	 
     (@pt="adj" and  ( (@rel="predc" or @rel="predm" )  and ../node[ (@pt="ww" and @rel="hd" and @lemma!="uit_zien" and @lemma!="heten" and @lemma!="gaan" and @lemma!="zitten" and (contains(@frame, "copula") or not(@stype="topic_drop")) and parent::node[node[@rel="predc"] and not(node[@rel="obj1"]) ] )])
)
 or
	 
     (@pt="adj" and @rel="hd" and parent::node[@cat="ap" and  ( (@rel="predc" or @rel="predm" )  and ../node[ (@pt="ww" and @rel="hd" and @lemma!="uit_zien" and @lemma!="heten" and @lemma!="gaan" and @lemma!="zitten" and (contains(@frame, "copula") or not(@stype="topic_drop")) and parent::node[node[@rel="predc"] and not(node[@rel="obj1"]) ] )])
])
 or
	  (@rel="det" and @pt="vnw" and @vwtype="onbep")
 
	)
]
"""

#matches = strees[0].xpath(thequery)
matches = asta_bijzin(strees[0])
for m in matches:
    showtree(m)
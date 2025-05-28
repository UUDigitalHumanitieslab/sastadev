from sastadev.conf import settings
from lxml import etree

sentence = "daarnaast daarnaast doe ik ook 's avonds of in het weekend extra diensten"

origutt = "daarnaast daarnaast doe ik ook ’s avonds of in het weekend extra diensten"

parse = settings.PARSE_FUNC

tree = parse(sentence)
md = etree.Element('metadata')
origuttmeta = etree.Element('meta', attrib={'name':'origutt', 'type':'text', 'value': origutt})
md.append(origuttmeta)
tree.append(md)

treebank = etree.Element('treebank')
treebank.append(tree)

fulltreebank = etree.ElementTree(treebank)
treebankfullname = 'apostroftest.xml'
fulltreebank.write(treebankfullname, encoding="UTF8", xml_declaration=False,
                   pretty_print=True)




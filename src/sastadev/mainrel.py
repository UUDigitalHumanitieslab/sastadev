
mainrelxpath = './/node[@rel="--" and @cat="rel"]'


def mainrelcount(stree: SynTree) -> int:
    mainrels = stree.xpath(mainrelxpath)
    result = len(mainrels)
    return result

Criterion('mainrelcount', mainrelcount, negative, 'Dislike main relative clauses')
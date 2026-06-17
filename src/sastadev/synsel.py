from sastadev.filefunctions import get_corrected_tree_fullname
from sastadev.sastatypes import SynTree
from sastadev.macros import expandmacros
from sastadev.test_functions import test_f
from sastadev.treebankfunctions import getattval as gav
from typing import List

synsel = {('doen', 'ww') : [['su', 'obj1'], ['su', 'vc']],
          ('hebben', 'ww'): [['su', 'obj1'], ['su', 'vc']],
          ('zijn', 'ww'): [['su', 'predc'], ['su', 'pc'], ['su', 'vc' ]],
          ('willen', 'ww'): [['su', 'obj1'], ['su', 'vc'], ['su', 'ld'], ['su', 'mod']],
          ('kennen', 'ww'): [['su', 'obj1']],
         ('kunnen', 'ww'):  [['su', 'obj1'], ['su', 'vc'], ['su', 'ld'], ['su', 'mod']],
          ('uit_blazen', 'ww'): [['su', 'obj1']]
}

parent_imperative_xpath = expandmacros('./parent::node[%basicimperative%]')


def omitted_phrase(stree: SynTree) -> List[SynTree]:
    results = []
    heads = stree.xpath('.//node[@word and @rel="hd"]')
    for head in heads:
        # exclude imperatives
        imperatives = head.xpath(parent_imperative_xpath)
        if imperatives != []:
            continue
        head_lemma = gav(head, 'lemma')
        head_pt = gav(head, 'pt')
        if (head_lemma, head_pt) in synsel:
            syns = synsel[(head_lemma, head_pt)]
            overall_ok = False
            for syn in syns:
                syn_result = all([head.xpath(f'../node[@rel="{rel}"]') != [] for rel in syn])
                if syn_result:
                    overall_ok = True
            if not overall_ok:
                results.append(head)
    return results


test_utts = [('vklstap', 'stap_02', '10'),
                ('vklstap', 'stap_02', '12'),
                ('vklstap', 'stap_02', '21'),
                ('vklstap', 'stap_02', '25'),
                ('vklstap', 'stap_02', '35'),
                ('vklstap', 'stap_02', '44')
            ]


def main():
    selected_test_utts = test_utts # [test_utts[5]]
    test_f(selected_test_utts, omitted_phrase)



if __name__ == '__main__':
    main()




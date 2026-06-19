import copy
from dataclasses import dataclass
from sastadev.filefunctions import get_corrected_tree_fullname
from sastadev.sastatypes import SynTree
from sastadev.macros import expandmacros
from sastadev.test_functions import test_f
from sastadev.treebankfunctions import getattval as gav
from typing import Callable, List


@dataclass
class Selection_Item:
    rel: str
    cond: str = ""

def si(rel: str, cond: str="") -> Selection_Item:
    return Selection_Item(rel, cond=cond)

su = si('su')
ld = si('ld')
mod = si('mod')
obj1 = si('obj1')
pc = si('pc')
predc = si('predc')
predm = si('predm')
vc = si('vc')

defpron = """(@lemma="dit" or @lemma="dat" or @lemma="het")"""

synsel = {('doen', 'ww') : [[su, obj1], [su, vc], [su, si('mod', '@lemma="zo"')], [su, predc] ],
          ('hebben', 'ww'): [[su, obj1], [su, vc], [su, si('svp', '@lemma="vrij"')]],
          ('zijn', 'ww'): [[su, predc], [su, pc], [su, vc ], [su, ld],
                           [su, si('mod', '%new_STAP_BB_p%')], [su, predm],
                           [si('su', f'{defpron}'), si('mod', '@cat="cp"')]],
          ('willen', 'ww'): [[su, obj1], [su, vc], [su, ld], [su, mod]],
          ('kennen', 'ww'): [[su, obj1]],
         ('kunnen', 'ww'):  [[su, obj1], [su, vc], [su, ld], [su, mod]],
          ('uit_blazen', 'ww'): [[su, obj1]]
}

parent_imperative_xpath = expandmacros('./parent::node[%basicimperative%]')

def extend_syns(syns, head) -> dict:
    head_wvorm = gav(head, 'wvorm')
    if head_wvorm not in  ['inf', 'vd']:
        return syns
    new_syns = copy.deepcopy(syns)
    for syn in syns:
        new_syn = [syn_item for syn_item in syn if syn_item != su]
        new_syns.append(new_syn)
    return new_syns



def omitted_phrase(stree: SynTree) -> List[SynTree]:
    results = []
    heads = stree.xpath('.//node[@word and @rel="hd"]')
    for head in heads:
        # exclude imperatives
        imperatives = head.xpath(parent_imperative_xpath)
        if imperatives != []:
            continue
        head_lemma = gav(head, 'original_lemma') if gav(head, 'original_lemma') != '' else gav(head, 'lemma')
        head_pt = gav(head, 'pt')
        if (head_lemma, head_pt) in synsel:
            base_syns = synsel[(head_lemma, head_pt)]
            syns = extend_syns(base_syns, head)
            overall_ok = False
            for syn in syns:
                all_items_found_so_far = True
                for item in syn:
                    rel = item.rel
                    cond = f'and {expandmacros(item.cond)}' if item.cond != "" else ""
                    item_result = head.xpath(f'../node[@rel="{rel}" {cond}]') != []
                    all_items_found_so_far = all_items_found_so_far and item_result
                    if not all_items_found_so_far:
                        continue
                if all_items_found_so_far:
                    overall_ok = True
                    break
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




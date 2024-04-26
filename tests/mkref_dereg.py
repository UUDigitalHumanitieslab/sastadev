from deregularise_test import thelist
from sastadev.deregularise import correctinflection

for wrong, good in thelist:
    cands = correctinflection(wrong)
    for cand, m in cands:
        print(f"('{wrong}', '{good}', '{m}')"  )

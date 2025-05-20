import itertools

stage2 = 2
stage3 = 3
stage4 = 4
stage5 = 5
stage6 = 6
stage7 = 7

anymood = 0
decl = 1
question = 2
imp = 3

VBcombinations = {}
Vcombinations = {}

stage2noVcombinations = ['T030', 'T064', 'T140']
Vcombinations[(stage2, decl)] = ['T030', 'T071', 'T072','T099', 'T140']
VBcombinations[(stage2, decl)] = ['T030', 'T064']

Vcombinations[(stage3, question)] = ['T001' ]
Vcombinations[(stage3, imp)] = ['T121']
Vcombinations[(stage3, decl)] = ['T014', 'T065', 'T073', 'T076', 'T079', 'T125', 'T141']
VBcombinations[(stage3, decl)] = ['T014', 'T065', 'T073', 'T125']   # should T079 Ov3 be here?

Vcombinations[(stage4, question)] = ['T111', 'T129']
Vcombinations[(stage4, imp)] = ['T135']
Vcombinations[(stage4, decl)] = ['T074', 'T075', 'T083']
VBcombinations[(stage4, decl)] = ['T074', 'T075', 'T083']

Vcombinations[stage5, question] = ['T112', 'T130']
Vcombinations[(stage5, imp)] = ['T136']
Vcombinations[(stage5, decl)] = ['T029', 'T077', 'T084', 'T100', ]
VBcombinations[(stage5, decl)] = ['T029', 'T100', 'T136']

Vcombinations[(stage6, question)] = ['T113', 'T131']
Vcombinations[(stage6, imp)] = ['T137']
Vcombinations[(stage6, decl)] = ['T003']
VBcombinations[(stage6, question)] = [ 'T113', 'T131' ]
VBcombinations[(stage6, imp)] = [ 'T137' ]
VBcombinations[(stage6, decl)] = ['T003']

Vcombinations[(stage7, anymood)] = ['T080', 'T090']
VBcombinations[(stage7, anymood)] = ['T080', 'T090']

# Vcombinationsbystage = {}
# Vcombinationsbystage[stage2] = [code for ]
# Vcombinations[stage3] = stage3V_Decl_combinations + stage3V_Imp_combinations + stage3V_Question_combinations
# Vcombinations[stage4] = stage4V_Decl_combinations + stage4V_Imp_combinations + stage4V_Question_combinations
# Vcombinations[stage5] = stage5V_Decl_combinations + stage5V_Imp_combinations + stage5V_Question_combinations
# Vcombinations[stage6] = stage6V_Decl_combinations + stage6V_Imp_combinations + stage6V_Question_combinations
# Vcombinations[stage7] = stage7V_combinations


allVcombinations = list(itertools.chain.from_iterable([Vcombinations[tuple] for tuple in Vcombinations]))

allVBcombinations = list(itertools.chain.from_iterable([VBcombinations[tuple] for tuple in VBcombinations]))

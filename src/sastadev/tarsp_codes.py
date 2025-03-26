

stage2noVcombinations = ['T030', 'T064', 'T140']
stage2Vcombinations = ['T030', 'T071', 'T072','T099', 'T140']

stage3V_Question_combinations = ['T001' ]
stage3V_Imp_combinations = ['T121']
stage3V_Decl_combinations = ['T014', 'T065', 'T073', 'T076', 'T079', 'T125', 'T141']

stage4V_Question_combinations = ['T111', 'T129']
stage4V_Imp_combinations = ['T135']
stage4V_Decl_combinations = ['T074', 'T075', 'T083']

stage5V_Question_combinations = ['T112', 'T130']
stage5V_Imp_combinations = ['T136']
stage5V_Decl_combinations = ['T029', 'T077', 'T084', 'T100', ]

stage6V_Question_combinations = ['T113', 'T131']
stage6V_Imp_combinations = ['T137']
stage6V_Decl_combinations = ['T003']

stage7V_combinations = ['T080', 'T090']

stage3Vcombinations = stage3V_Decl_combinations + stage3V_Imp_combinations + stage3V_Question_combinations
stage4Vcombinations = stage4V_Decl_combinations + stage4V_Imp_combinations + stage4V_Question_combinations
stage5Vcombinations = stage5V_Decl_combinations + stage5V_Imp_combinations + stage5V_Question_combinations
stage6Vcombinations = stage6V_Decl_combinations + stage6V_Imp_combinations + stage6V_Question_combinations

allV_combinations = stage2Vcombinations + stage3Vcombinations + stage4Vcombinations + \
                    stage5Vcombinations + stage6Vcombinations + stage7V_combinations
moresubbst = [('əs', 'eens'),
              ('moetə', 'moeten'),
              ('moetə' , 'moet'),
              ("'s", "is"),
              ('pot', 'kapot'),
              ('almaal', 'allemaal')
              ('knorrens', 'varkens')
              ]

dupvowel = '[aeou]'
aasre = rf'{dupvowel}\1s$'
# Lauraas -> Laura's; autoos -> auto's
if not known_word(token.word) and token.word[-3:] in {'aas', 'oos', 'ees', 'uus'} and known_word(token.word[:-2]):
    newword = f"{token.word[:-2]}'s"
    newtokenmds = updatenewtokenmds(newtokenmds, token, [newword], beginmetadata,
                                    name='Spelling Correction', value='Missing Apostrophe',
                                    cat='Spelling', backplacement=bpl_word, penalty=penalty)



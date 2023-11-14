from iedims import getjeforms


iewords = ['poppie', 'kassie', 'boekie']

for ieword in iewords:
    jewords = getjeforms(ieword)
    print(jewords)
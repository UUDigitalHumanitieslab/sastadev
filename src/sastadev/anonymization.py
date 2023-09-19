'''
reimplements SASTA anonymization json data
See https://github.com/UUDigitalHumanitieslab/sasta/blob/develop/backend/anonymization.json


'''

import json
import re

vertbar = '|'

anonymisationtablejsonstr = """ 
[
    {
        "category": "place",
        "codes": ["PLAATS", "PLAATSNAAM", "WOONPLAATS"],
        "common": ["Utrecht", "Breda", "Leiden", "Maastricht", "Arnhem"]
    },
    {
        "category": "lastname",
        "codes": ["ACHTERNAAM"],
        "common": ["Jansen", "Hendriks", "Dekker", "Dijkstra", "Veenstra"]
    },
    {
        "category": "person",
        "codes": ["NAAM", "BROER", "ZUS", "KIND", "VADER", "MOEDER"],
        "common": ["Maria", "Jan", "Anna", "Esther", "Pieter", "Sam"]
    },
    {
        "category": "profession",
        "codes": ["BEROEP"],
        "common": ["timmerman", "chirurgh", "leraar", "ober", "verslaggever"]
    },
    {
        "category": "country",
        "codes": ["LAND"],
        "common": ["Duitsland", "Nederland", "Japan", "Kameroen", "India"]
    },
    {
        "category": "education",
        "codes": ["STUDIE", "OPLEIDING"],
        "common": [
            "bedrijfskunde",
            "informatica",
            "filosofie",
            "rechtsgeleerdheid",
            "werktuigbouwkunde"
        ]
    },
    {
        "category": "institution",
        "codes": ["ZORGINSTELLING", "INSTELLING", "ZIEKENHUIS"],
        "common": [
            "Diakonessenhuis",
            "Rijnstate",
            "Vogellanden",
            "HagaZiekenhuis",
            "Slingeland"
        ]
    }
]
"""

anonymisationlist = json.loads(anonymisationtablejsonstr)

anonymisationdict = {key: dct["common"] for dct in anonymisationlist for key in dct["codes"] }

#: The constant *sasta_pseudonyms* list the strings that replace names for
#: pseudonymisation purposes.
sasta_pseudonyms = [key for key in anonymisationdict]

#: The constant *pseudonym_patternlist* contains regular expressions for pseudonyms
#: based on elements from the *sasta_pseudonyms* (pseudonym + number).
pseudonym_patternlist = [r'^{}\d?$'.format(el) for el in sasta_pseudonyms]
pseudonym_pattern = vertbar.join(pseudonym_patternlist)
pseudonymre = re.compile(pseudonym_pattern)


junk = 0

def getname(rawcode: str) -> str:
    code = rawcode.upper()    # the code must be in all uppercase otherwise we do too much
    if code == '':
        return rawcode
    if code[-1] in '01234':
        prefix = code[:-1]
        suffix = code[-1]
        suffixint = int(suffix)
    else:
        return rawcode
    if prefix in anonymisationdict:
        result = anonymisationdict[prefix][suffixint]
    else:
        result = rawcode
    return result

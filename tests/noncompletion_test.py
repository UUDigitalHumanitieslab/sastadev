import re

re1 = '^(.*)\((.*?)\)(.*)$'

teststrings = ['stapel(bed)', 'he(vi)g', '(aan)val']

for teststr in teststrings:
    annotated = re.sub(re1, r'\1\3', teststr)
    annotation = re.sub(re1, r'\1\2\3', teststr)
    print(teststr, annotated, annotation)
target_intarget, target_xsid, target_all, target_byrole, target_bysyn, target_stapvu = 0, 1, 2, 3, 4, 5
intargetxpath = '//meta[@name="intarget"]'
xsidxpath = '//meta[@name="xsid"]'
intargetvalxpath = './/meta[@name="intarget"]/@value'
xsidvalxpath = './/meta[@name="xsid"]/@value'
synxpath = './/meta[@name="syn"]'

rolevalxpath = './/meta[@name="role"]/@value'

targetroles = ['target_child', 'target', 'target_adult']
stapvuxpath = './/meta[@name="origutt" and contains(@value, "[+ VU]")]'

def get_targets(treebank, methodname):
    xsids = treebank.xpath(xsidxpath)
    intargets = treebank.xpath(intargetxpath)
    roles = treebank.xpath(rolevalxpath)
    targetrolesfound = any(map(lambda x: x.lower() in targetroles, roles))
    synannotations = treebank.xpath(synxpath)
    stapvus = treebank.xpath(stapvuxpath)
    if synannotations != []:
        result = target_bysyn
    elif xsids != []:
        result = target_xsid
    elif intargets != []:
        result = target_intarget
    elif methodname == 'stap' and stapvus != []:
        result = target_stapvu
    elif targetrolesfound:
        result = target_byrole
    else:
        result = target_all
    return result


def get_mustbedone(syntree, targets):
    if targets == target_bysyn:
        syns = syntree.xpath(synxpath)
        result = syns != []
    elif targets == target_intarget:
        intargetvals = syntree.xpath(intargetvalxpath)
        result = intargetvals != [] and intargetvals[0] == 'yes'
    elif targets == target_xsid:
        xsids = syntree.xpath(xsidvalxpath)
        result = xsids != []
    elif targets == target_byrole:
        rolevals = syntree.xpath(rolevalxpath)
        result = any(map(lambda x: x.lower() in targetroles, rolevals))
    elif targets == target_stapvu:
        syns = syntree.xpath(stapvuxpath)
        result = syns != []
    else:
        result = True
    return result

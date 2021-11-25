from math import log


class MethodInfo:
    def __init__(self, path, basenamemodel, silverpath, silvertemplate, deffn):
        self.path = path
        self.basenamemodel = basenamemodel
        self.silverpath = silverpath
        self.silvertemplate = silvertemplate
        self.definitionfn = deffn


asta_path = r'D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\astadata\ASTA'
asta_basemodel = 'ASTA_sample_{}'
asta_model = 'ASTA_sample_{}_analysis'
asta_silverpath = r'D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\astadata\Silver'
asta_silvertemplate = r'{}'
asta_def_fn = r'D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\ASTA\ASTA Index Current.xlsx'

stap_path = r'D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\stapdata'
stap_basemodel = r'STAP_{}'
stap_model = r'STAP_{}_analysis'
stap_silverpath = r'D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\STAP\Zilver'
stap_silvertemplate = '{}'
stap_def_fn = r'D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\STAP\STAP_Index_Current.xlsx'


tarsp_path = r'D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\tarspdata\tarsp'
tarsp_basemodel = 'TARSP_{}'
tarsp_model = 'TARSP_{}_analysis'
tarsp_silverpath = r'D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\TARSP\Zilver'
tarsp_silvertemplate = r'{}'
tarsp_def_fn = r'D:\jodijk\Dropbox\jodijk\Utrecht\Projects\CLARIAH CORE\WP3\VKL\tarspdata\TARSP Index Current.xlsx'

knownmethods = dict()
knownmethods['ASTA'] = MethodInfo(asta_path, asta_basemodel, asta_silverpath, asta_silvertemplate, asta_def_fn)
knownmethods['STAP'] = MethodInfo(stap_path, stap_basemodel, stap_silverpath, stap_silvertemplate, stap_def_fn)
knownmethods['TARSP'] = MethodInfo(tarsp_path, tarsp_basemodel, tarsp_silverpath, tarsp_silvertemplate, tarsp_def_fn)


def isknownmethod(mname):
    if mname is None:
        result = False
    else:
        result = mname.upper() in knownmethods
    return result


def getfnbases(method, maxval):
    model = knownmethods[method].basenamemodel
    width = max([2, int(log(maxval, 10)) + 1])
    results = []
    for i in range(1, maxval + 1):
        istr = str(i).rjust(width, '0')
        result = model.format(istr)
        results.append(result)
    return results

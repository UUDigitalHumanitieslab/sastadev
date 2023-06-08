import pytest

from sastadev.astaforms import (AstaFormData, ExcelForm, make_astaform, scores,
                                tabel)


@pytest.mark.skip(reason='test code gives errors')
def test_astaform():
    astadata = AstaFormData({'boek': 2, 'huis': 3}, {'lopen': 2})
    theform = ExcelForm(tabel, scores)
    theworkbook = make_astaform(theform, astadata, 'astaformulier.xlsx')

    theworkbook.close()

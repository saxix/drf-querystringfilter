import pytest

from drf_querystringfilter.exceptions import InvalidPattern
from drf_querystringfilter.filters import RexList


def test_rexlist():
    ll = RexList()
    ll.append('.*')
    assert 1 in ll
    assert '1' in ll

    ll = RexList()
    ll.append(r'a?')
    ll.append(r'b*')
    assert 'c' not in ll
    assert 'b' in ll
    assert 'aa' in ll
    assert '^baa' not in ll

    ll = RexList()
    ll.append(r'.*__')
    assert 'join__field' in ll

    with pytest.raises(InvalidPattern):
        ll.append('[*')

    ll = RexList(['.*'])
    ll[0] = '.*'
    with pytest.raises(InvalidPattern):
        ll[0] = '[*'

    with pytest.raises(InvalidPattern):
        RexList(['.*', []])

import os
import sys
import pytest

from ..exceptions import *
from ..filter_constructor import get_filter
from ..ugly import check


def test_check():

    HERE = os.path.abspath(os.path.dirname(__file__))

    out_name = os.path.join(HERE, 'out.txt')
    ref_name = os.path.join(HERE, 'ref.txt')

    filters = [get_filter(abs_tolerance=0.1)]
    check(filters, out_name=out_name, ref_name=ref_name, verbose=False)

    filters = [get_filter()]
    with pytest.raises(FilterKeywordError) as e:
        check(filters, out_name=out_name, ref_name=ref_name, verbose=False)
    assert 'ERROR: for floats you have to specify either rel_tolerance or abs_tolerance\n' in str(e.value)

    filters = [get_filter(rel_tolerance=0.01)]
    with pytest.raises(TestFailedError) as e:
        check(filters, out_name=out_name, ref_name=ref_name, verbose=False)
    assert 'ERROR: test %s failed\n' % out_name in str(e.value)
    with open(os.path.join(HERE, 'out.txt.diff'), 'r') as f:
        assert f.read() == '''
.       1.0 2.0 3.0
ERROR           ### expected: 3.05 (rel diff: 1.64e-02)\n'''

    filters = [get_filter(abs_tolerance=0.01)]
    with pytest.raises(TestFailedError) as e:
        check(filters, out_name=out_name, ref_name=ref_name, verbose=False)
    assert 'ERROR: test %s failed\n' % out_name in str(e.value)
    with open(os.path.join(HERE, 'out.txt.diff'), 'r') as f:
        assert f.read() == '''
.       1.0 2.0 3.0
ERROR           ### expected: 3.05 (abs diff: 5.00e-02)\n'''

    filters = [get_filter(abs_tolerance=0.01, ignore_sign=True)]
    with pytest.raises(TestFailedError) as e:
        check(filters, out_name=out_name, ref_name=ref_name, verbose=False)
    assert 'ERROR: test %s failed\n' % out_name in str(e.value)
    with open(os.path.join(HERE, 'out.txt.diff'), 'r') as f:
        assert f.read() == '''
.       1.0 2.0 3.0
ERROR           ### expected: 3.05 (abs diff: 5.00e-02 ignoring signs)\n'''


def test_check_bad_filter():

    HERE = os.path.abspath(os.path.dirname(__file__))

    out_name = os.path.join(HERE, 'out.txt')
    ref_name = os.path.join(HERE, 'ref.txt')

    filters = [get_filter(from_string='does not exist', num_lines=4)]
    with pytest.raises(BadFilterError) as e:
        check(filters, out_name=out_name, ref_name=ref_name, verbose=False)
    assert 'ERROR: filter [4 lines from "does not exist"] did not extract anything from file %s\n' % out_name in str(e.value)

    filters = [get_filter(from_string='does not exist', to_string="either")]
    with pytest.raises(BadFilterError) as e:
        check(filters, out_name=out_name, ref_name=ref_name, verbose=False)
    assert 'ERROR: filter ["does not exist" ... "either"] did not extract anything from file %s\n' % out_name in str(e.value)


def test_check_different_length():

    HERE = os.path.abspath(os.path.dirname(__file__))

    out_name = os.path.join(HERE, 'out2.txt')
    ref_name = os.path.join(HERE, 'ref.txt')

    filters = [get_filter(abs_tolerance=0.1)]
    with pytest.raises(TestFailedError) as e:
        check(filters, out_name=out_name, ref_name=ref_name, verbose=False)
    assert 'ERROR: test %s failed\n' % out_name in str(e.value)
    with open(os.path.join(HERE, 'out2.txt.diff'), 'r') as f:
        assert f.read() == '''ERROR: extracted sizes do not match
own gave 4 numbers:
1.0 2.0 3.0 4.0

reference gave 3 numbers:
1.0 2.0 3.05
\n'''


def test_bad_keywords():
    from ..filter_api import recognized_kw

    with pytest.raises(FilterKeywordError) as e:
        _ = get_filter(raboof=0, foo=1)
    exception = '''ERROR: keyword(s) (foo, raboof) not recognized
       available keywords: ({0})\n'''.format(', '.join(recognized_kw))
    assert exception in str(e.value)

    with pytest.raises(FilterKeywordError) as e:
        _ = get_filter(from_string='foo', from_re='foo', to_string='foo', to_re='foo')
    assert "ERROR: incompatible keyword pairs: [('from_re', 'from_string'), ('to_re', 'to_string')]\n" in str(e.value)


def test_only_string():

    HERE = os.path.abspath(os.path.dirname(__file__))

    out_name = os.path.join(HERE, 'only_string_out.txt')
    ref_name = os.path.join(HERE, 'only_string_ref.txt')

    filters = [get_filter(string='raboof')]
    check(filters, out_name=out_name, ref_name=ref_name, verbose=False)

    filters = [get_filter(string='foo')]
    with pytest.raises(BadFilterError) as e:
        check(filters, out_name=out_name, ref_name=ref_name, verbose=False)
    assert 'ERROR: filter [1 lines from "foo"] did not extract anything from file %s\n' % out_name in str(e.value)

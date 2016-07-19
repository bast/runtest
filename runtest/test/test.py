import os
import sys
import pytest

from ..classes import Filter
from ..exceptions import *


def test_filter_file():
    from ..main import _filter_file

    text = '''
1.0 2.0 3.0
1.0 2.0 3.0
1.0 2.0 3.0
1.0 2.0 3.0
1.0 2.0 3.0
1.0 2.0 3.0
1.0 2.0 3.0
raboof 1.0 3.0 7.0
       1.0 3.0 7.0
       1.0 3.0 7.0
       1.0 3.0 7.0
       1.0 3.0 7.0
       1.0 3.0 7.0
       1.0 3.0 7.0
       1.0 3.0 7.0'''

    f = Filter()
    f.add(rel_tolerance=1.0e-5, from_re='raboof', num_lines=5)

    res = _filter_file(f=f.filter_list[0], file_name='raboof', output=text.splitlines())
    assert res == ['raboof 1.0 3.0 7.0', '       1.0 3.0 7.0', '       1.0 3.0 7.0', '       1.0 3.0 7.0', '       1.0 3.0 7.0']


def test_check():

    HERE = os.path.abspath(os.path.dirname(__file__))

    out_name = os.path.join(HERE, 'out.txt')
    ref_name = os.path.join(HERE, 'ref.txt')

    f = Filter()
    f.add(abs_tolerance=0.1)
    f.check(work_dir='not used', out_name=out_name, ref_name=ref_name, verbose=False)

    f = Filter()
    f.add()
    with pytest.raises(FilterKeywordError) as e:
        f.check(work_dir='not used', out_name=out_name, ref_name=ref_name, verbose=False)
    assert 'ERROR: for floats you have to specify either rel_tolerance or abs_tolerance\n' in str(e.value)

    f = Filter()
    f.add(rel_tolerance=0.01)
    with pytest.raises(TestFailedError) as e:
        f.check(work_dir='not used', out_name=out_name, ref_name=ref_name, verbose=False)
    assert 'ERROR: test %s failed\n' % out_name in str(e.value)
    with open(os.path.join(HERE, 'out.txt.diff'), 'r') as f:
        assert f.read() == '''
.       1.0 2.0 3.0
ERROR           ### expected: 3.05 (rel diff: 1.64e-02)\n'''

    f = Filter()
    f.add(abs_tolerance=0.01)
    with pytest.raises(TestFailedError) as e:
        f.check(work_dir='not used', out_name=out_name, ref_name=ref_name, verbose=False)
    assert 'ERROR: test %s failed\n' % out_name in str(e.value)
    with open(os.path.join(HERE, 'out.txt.diff'), 'r') as f:
        assert f.read() == '''
.       1.0 2.0 3.0
ERROR           ### expected: 3.05 (abs diff: 5.00e-02)\n'''

    f = Filter()
    f.add(abs_tolerance=0.01, ignore_sign=True)
    with pytest.raises(TestFailedError) as e:
        f.check(work_dir='not used', out_name=out_name, ref_name=ref_name, verbose=False)
    assert 'ERROR: test %s failed\n' % out_name in str(e.value)
    with open(os.path.join(HERE, 'out.txt.diff'), 'r') as f:
        assert f.read() == '''
.       1.0 2.0 3.0
ERROR           ### expected: 3.05 (abs diff: 5.00e-02 ignoring signs)\n'''


def test_check_bad_filter():

    HERE = os.path.abspath(os.path.dirname(__file__))

    out_name = os.path.join(HERE, 'out.txt')
    ref_name = os.path.join(HERE, 'ref.txt')

    f = Filter()
    f.add(from_string='does not exist', num_lines=4)
    with pytest.raises(BadFilterError) as e:
        f.check(work_dir='not used', out_name=out_name, ref_name=ref_name, verbose=False)
    assert 'ERROR: filter [4 lines from "does not exist"] did not extract anything from file %s\n' % out_name in str(e.value)

    f = Filter()
    f.add(from_string='does not exist', to_string="either")
    with pytest.raises(BadFilterError) as e:
        f.check(work_dir='not used', out_name=out_name, ref_name=ref_name, verbose=False)
    assert 'ERROR: filter ["does not exist" ... "either"] did not extract anything from file %s\n' % out_name in str(e.value)


def test_check_different_length():

    HERE = os.path.abspath(os.path.dirname(__file__))

    out_name = os.path.join(HERE, 'out2.txt')
    ref_name = os.path.join(HERE, 'ref.txt')

    f = Filter()
    f.add(abs_tolerance=0.1)
    with pytest.raises(TestFailedError) as e:
        f.check(work_dir='not used', out_name=out_name, ref_name=ref_name, verbose=False)
    assert 'ERROR: test %s failed\n' % out_name in str(e.value)
    with open(os.path.join(HERE, 'out2.txt.diff'), 'r') as f:
        assert f.read() == '''ERROR: extracted sizes do not match
own gave 4 numbers:
1.0 2.0 3.0 4.0

reference gave 3 numbers:
1.0 2.0 3.05
\n'''


def test_bad_keywords():

    f = Filter()
    with pytest.raises(FilterKeywordError) as e:
        f.add(raboof=0, foo=1)
    exception = '''ERROR: keyword(s) (foo, raboof) not recognized
       available keywords: (from_re, to_re, re, from_string, to_string, string, ignore_below, ignore_above, ignore_sign, mask, num_lines, rel_tolerance, abs_tolerance)\n'''
    assert exception in str(e.value)

    f = Filter()
    with pytest.raises(FilterKeywordError) as e:
        f.add(from_string='foo', from_re='foo', to_string='foo', to_re='foo')
    assert "ERROR: incompatible keyword pairs: [('from_re', 'from_string'), ('to_re', 'to_string')]\n" in str(e.value)


def test_only_string():

    HERE = os.path.abspath(os.path.dirname(__file__))

    out_name = os.path.join(HERE, 'only_string_out.txt')
    ref_name = os.path.join(HERE, 'only_string_ref.txt')

    f = Filter()
    f.add(string='raboof')
    f.check(work_dir='not used', out_name=out_name, ref_name=ref_name, verbose=False)

    f = Filter()
    f.add(string='foo')
    with pytest.raises(BadFilterError) as e:
        f.check(work_dir='not used', out_name=out_name, ref_name=ref_name, verbose=False)
    assert 'ERROR: filter [1 lines from "foo"] did not extract anything from file %s\n' % out_name in str(e.value)

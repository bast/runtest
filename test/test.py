import os
import sys
import runtest

# ------------------------------------------------------------------------------


def test_extract_numbers():
    """
    Tests extract_numbers.
    """

    text = '''<<A( 3),B( 3)>> - linear response function (real):
-----------------------------------------------------------------------------------------------
   A - Z-Dipole length      B1u  T+
   B - Z-Dipole length      B1u  T+
-----------------------------------------------------------------------------------------------
 Frequency (real)     Real part                                     Convergence
-----------------------------------------------------------------------------------------------
  0.00000000 a.u.   -1.901357604797 a.u.                       3.04E-07   (converged)
-----------------------------------------------------------------------------------------------
----------------------------------------------------------------------------


                         +--------------------------------+
                         ! Electric dipole polarizability !
                         +--------------------------------+


 1 a.u =   0.14818471 angstrom**3


@   Elements of the electric dipole polarizability tensor

@   xx            1.90135760 a.u.   (converged)
@   yy            1.90135760 a.u.   (converged)
@   zz            1.90135760 a.u.   (converged)

@   average       1.90135760 a.u.
@   anisotropy    0.000      a.u.

@   xx            0.28175212 angstrom**3
@   yy            0.28175212 angstrom**3
@   zz            0.28175212 angstrom**3

@   average       0.28175212 angstrom**3
@   anisotropy    0.000      angstrom**3'''

    f = runtest.Filter()
    f.add()

    numbers, locations = runtest.extract_numbers(f.filter_list[0], text.splitlines())

    assert numbers == [0.0, -1.901357604797, 3.04e-07, 1, 0.14818471, 1.9013576, 1.9013576, 1.9013576, 1.9013576, 0.0, 0.28175212, 0.28175212, 0.28175212, 0.28175212, 0.0]
    assert locations == [(7, 2, 10), (7, 20, 15), (7, 63, 8), (17, 1, 1), (17, 11, 10), (22, 18, 10), (23, 18, 10), (24, 18, 10), (26, 18, 10), (27, 18, 5), (29, 18, 10), (30, 18, 10), (31, 18, 10), (33, 18, 10), (34, 18, 5)]

# ------------------------------------------------------------------------------


def test_compare_numbers_abs():

    f = runtest.Filter()
    f.add(abs_tolerance=0.01)

    l1 = [0.0, 1.0, 2.0, -3.0]
    l2 = [0.0, 1.0, 2.0, -3.0]
    l3 = [0.0, 1.0, 2.1, -3.0]

    res = runtest.compare_numbers(f.filter_list[0], l1, l2)
    assert res == [1, 1, 1, 1]

    res = runtest.compare_numbers(f.filter_list[0], l1, l3)
    assert res == [1, 1, 0, 1]

# ------------------------------------------------------------------------------


def test_compare_numbers_abs_ignore_sign():

    f = runtest.Filter()
    f.add(abs_tolerance=0.01, ignore_sign=True)

    l1 = [0.0, 1.0, 2.0, -3.0]
    l2 = [0.0, 1.0,-2.0, -3.0]

    res = runtest.compare_numbers(f.filter_list[0], l1, l2)
    assert res == [1, 1, 1, 1]

# ------------------------------------------------------------------------------


def test_compare_numbers_rel():

    f = runtest.Filter()
    f.add(rel_tolerance=0.1)

    l1 = [0.0, 1.0, 2.0, -3.0]
    l2 = [0.0, 1.0, 2.0, -3.0]
    l3 = [0.0, 1.0, 2.1, -3.0]
    l4 = [0.0, 1.0, 2.5, -3.0]

    res = runtest.compare_numbers(f.filter_list[0], l1, l2)
    assert res == [1, 1, 1, 1]

    res = runtest.compare_numbers(f.filter_list[0], l1, l3)
    assert res == [1, 1, 1, 1]

    res = runtest.compare_numbers(f.filter_list[0], l1, l4)
    assert res == [1, 1, 0, 1]

# ------------------------------------------------------------------------------


def test_compare_numbers_int():

    f = runtest.Filter()
    f.add()

    l1 = [0, 1, 3, 7]
    l2 = [0, 2, 3, 7]

    res = runtest.compare_numbers(f.filter_list[0], l1, l2)
    assert res == [1, 0, 1, 1]

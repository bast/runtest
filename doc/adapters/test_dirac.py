#!/usr/bin/env python

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from runtest_dirac import Filter, TestRun

test = TestRun(__file__, sys.argv)

f = Filter()
f.add(from_string   = '@   Elements of the electric dipole',
      to_string     = '@   anisotropy',
      rel_tolerance = 1.0e-5)
f.add(from_string   = '************ Expectation values',
      to_string     = 's0 = T : Expectation value',
      rel_tolerance = 1.0e-5)

test.run(['PBE0gracLB94.inp', 'GLLBsaopLBalpha.inp'], ['Ne.mol'], f)

sys.exit(test.return_code)

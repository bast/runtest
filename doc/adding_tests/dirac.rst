

.. _adding_tests_dirac:

Adding tests in DIRAC
=====================

The runtest_dirac.py is an extension of the runtest library.  The runtest
library is a low-level program-independent library that provides infrastructure
for running calculations and extracting and comparing numbers against reference
outputs.


Reference outputs
-----------------

Reference outputs are placed in directory "result/".


Easy example
------------

Let us look at an easy example.

First we load some standard modules and import functionality from the library
(highlighted lines). This part is generic to all DIRAC tests.

.. code-block:: python
   :emphasize-lines: 3-9

   #!/usr/bin/env python

   import os
   import sys

   sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
   from runtest_dirac import Filter, TestRun

   test = TestRun(__file__, sys.argv)

   f = Filter()
   f.add(from_string = '@   Elements of the electric dipole',
         to_string   = '@   anisotropy')
   f.add(from_string = '************ Expectation values',
         to_string   = 's0 = T : Expectation value')

   test.run(['PBE0gracLB94.inp', 'GLLBsaopLBalpha.inp'], ['Ne.mol'], f)

   sys.exit(test.return_code)

Then we construct the filter object. It consists of two filter tasks. We can construct
as many filter objects as we like and each can consist of as many tasks as we like.

.. code-block:: python
   :emphasize-lines: 11-15

   #!/usr/bin/env python

   import os
   import sys

   sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
   from runtest_dirac import Filter, TestRun

   test = TestRun(__file__, sys.argv)

   f = Filter()
   f.add(from_string = '@   Elements of the electric dipole',
         to_string   = '@   anisotropy')
   f.add(from_string = '************ Expectation values',
         to_string   = 's0 = T : Expectation value')

   test.run(['PBE0gracLB94.inp', 'GLLBsaopLBalpha.inp'], ['Ne.mol'], f)

   sys.exit(test.return_code)

With test.run we really run the job.
Note how we pass the filter object. If we omit to pass it, then the
calculations will be run but not verified. This is useful for multi-step jobs.
Also observe how we give a list of input files and molecule files (in this case
two input files and one molecule file). The test library will run and test all
input/molecule file combinations (in this case two).  We could have executed
them separately in two lines. This would make no difference, just more typing.

.. code-block:: python
   :emphasize-lines: 19

   #!/usr/bin/env python

   import os
   import sys

   sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
   from runtest_dirac import Filter, TestRun

   test = TestRun(__file__, sys.argv)

   f = Filter()
   f.add(from_string = '@   Elements of the electric dipole',
         to_string   = '@   anisotropy')
   f.add(from_string = '************ Expectation values',
         to_string   = 's0 = T : Expectation value')

   test.run(['PBE0gracLB94.inp', 'GLLBsaopLBalpha.inp'], ['Ne.mol'], f)

   sys.exit(test.return_code)

Finally on the last line we exit with test.return_code. This is important.
The integer test.return_code equals the number of failed test runs. It is zero if the test
is successful.


Multi-step tests
----------------

Here is an example for a multi-step test.
Note how only every second run is actually verified by passing the filter object.

.. code-block:: python
   :emphasize-lines: 19,23,27

    #!/usr/bin/env python

    import os
    import sys
    import shutil

    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from runtest_dirac import Filter, TestRun

    test = TestRun(__file__, sys.argv)

    f = Filter()
    f.add(from_string = 'Energy at final geometry is',
          num_lines   = 3,
          tolerance   = 1.0e-4)

    test.run(['O.inp'], ['O.mol'], args='--get=DFCOEF')
    shutil.copy('DFCOEF', 'DFPROJ')
    test.run(['H2O.inp'], ['H2O.mol'], f, args='--copy=DFPROJ')

    test.run(['O.2c_iotc.inp'], ['O.mol'], args='--get=DFCOEF')
    shutil.copy('DFCOEF', 'DFPROJ')
    test.run(['H2O.2c_iotc.inp'], ['H2O.mol'], f, args='--copy=DFPROJ')

    test.run(['O.2c_iotc_noamfi.inp'], ['O.mol'], args='--get=DFCOEF')
    shutil.copy('DFCOEF', 'DFPROJ')
    test.run(['H2O.2c_iotc_noamfi.inp'], ['H2O.mol'], f, args='--copy=DFPROJ')

    # cleanup
    os.unlink('DFCOEF')
    os.unlink('DFPROJ')

    sys.exit(test.return_code)

The other runs only serve to prepare files and are not checked (no filter passed as argument).

.. code-block:: python
   :emphasize-lines: 17,21,25

    #!/usr/bin/env python

    import os
    import sys
    import shutil

    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from runtest_dirac import Filter, TestRun

    test = TestRun(__file__, sys.argv)

    f = Filter()
    f.add(from_string = 'Energy at final geometry is',
          num_lines   = 3,
          tolerance   = 1.0e-4)

    test.run(['O.inp'], ['O.mol'], args='--get=DFCOEF')
    shutil.copy('DFCOEF', 'DFPROJ')
    test.run(['H2O.inp'], ['H2O.mol'], f, args='--copy=DFPROJ')

    test.run(['O.2c_iotc.inp'], ['O.mol'], args='--get=DFCOEF')
    shutil.copy('DFCOEF', 'DFPROJ')
    test.run(['H2O.2c_iotc.inp'], ['H2O.mol'], f, args='--copy=DFPROJ')

    test.run(['O.2c_iotc_noamfi.inp'], ['O.mol'], args='--get=DFCOEF')
    shutil.copy('DFCOEF', 'DFPROJ')
    test.run(['H2O.2c_iotc_noamfi.inp'], ['H2O.mol'], f, args='--copy=DFPROJ')

    # cleanup
    os.unlink('DFCOEF')
    os.unlink('DFPROJ')

    sys.exit(test.return_code)


Passing arguments to pam
------------------------

This can be done with args. Example:

.. code-block:: python

   test.run(['O.inp'], ['O.mol'], args='--get=DFCOEF')


Catching expected errors
------------------------

We have tests which fail with MPI or integer(4) compilation
in a predictable and controlled way. In this case we don't want
to see the test failing, but we want it to pass.

Example:

.. code-block:: python
   :emphasize-lines: 18,19

    #!/usr/bin/env python

    import os
    import sys

    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from runtest_dirac import Filter, TestRun

    test = TestRun(__file__, sys.argv)

    f = Filter()
    f.add(string = 'Number of determinants/combinations')
    f.add(string = ' Final energy')

    test.run(['He.inp'],
             ['He.mol'],
             f,
             accepted_errors=['memory off-set too big for INTEGER*4',
                              'FATAL ERROR for LUCITA runs: memory offset (dynamic memory - static memory) is too big for i*4'])

    sys.exit(test.return_code)

When we run this test as separate script, we see::

  $ ./test -b ~/dirac/build/

  running test: He He
  found error which is expected/accepted: FATAL ERROR for LUCITA runs: memory offset (dynamic memory - static memory) is too big for i*4

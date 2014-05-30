

Adding tests in Dalton
======================


Reference outputs
-----------------

Reference outputs are placed in directory "result/".


Creating test scripts
---------------------

First follow the documentation for DIRAC, see :ref:`adding_tests_dirac`.

A difference with respect to DIRAC is that in Dalton we do pass a suffix-filter
dictionary in order to be able to test different output files.

Let us look at an example. Observe how we create a filter for "out", and another
filter for "stdout", which we pass as a dictionary (curly brackets):

.. code-block:: python
   :emphasize-lines: 11-14,16-20

   #!/usr/bin/env python

   import os
   import sys

   sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
   from runtest_dalton import Filter, TestRun

   test = TestRun(__file__, sys.argv)

   f_out = Filter()
   f_out.add(from_string = 'Final results from SIRIUS',
             num_lines   = 11,
             tolerance   = 1.0e-7)

   f_stdout = Filter()
   f_stdout.add(from_string  = 'beta = -Efff',
                num_lines    = 10,
                tolerance    = 1.0e-7,
                ignore_below = 1.0e-7)

   test.run(['hf.dal', 'hf_2np1.dal'], ['h2o2.mol'], {'out': f_out, 'stdout': f_stdout})

   sys.exit(test.return_code)


Updating tests
--------------

In most cases it is sufficient to update/replace the reference output.

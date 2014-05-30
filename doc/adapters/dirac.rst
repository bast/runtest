

Adapter for DIRAC
-----------------

In runtest_dirac.py we have subclassed
TestRun to override the execute method for convenience:

.. literalinclude:: runtest_dirac.py

This has the advantage that we can run and check a series of input file tuples
with the same filter set as demonstrated here:

.. literalinclude:: test_dirac.py

Note that the filter argument is optional which allows us to run calculations
which are not tested (we need this in multi-step jobs where not all the steps
are tested).

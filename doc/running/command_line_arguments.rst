

Command-line arguments
======================


-h, --help
----------

Show help message and exit.


-b BINARY_DIR, --binary-dir=BINARY_DIR
--------------------------------------

Directory containing the binary/launcher.
By default it is the directory of the test script which is executed.


-w WORK_DIR, --work-dir=WORK_DIR
--------------------------------

Working directory where all generated files will be written to.
By default it is the directory of the test script which is executed.


-l LAUNCH_AGENT, --launch-agent=LAUNCH_AGENT
--------------------------------------------

Prepend a launch agent command (e.g. "mpirun -np 8" or
"valgrind --leak-check=yes").
By default no launch agent is prepended.


-v, --verbose
-------------

Give more verbose output upon test failure (by default False).


-s, --skip-run
--------------

Skip actual calculation(s), only compare numbers. This is useful
to adjust the test script for long calculations.


-n, --no-verification
-----------------------

Run calculation(s) but do not verify results. This is useful to
generate outputs for the first time.

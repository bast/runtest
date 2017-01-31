

General tips
============

How to add a new test
---------------------

Test scripts are python scripts which return zero (success)
or non-zero (failure). You define what success or failure means.
The runtest library helps you with basic tasks but you are free
to go beyond and define own tests with arbitrary complexity.


Strive for portability
----------------------

Avoid shell programming or symlinks in test scripts otherwise the tests are not
portable to Windows. Therefore do not use ``os.system()`` or ``os.symlink()``. Do not
use explicit forward slashes for paths, instead use ``os.path.join()``.


Always test that the test really works
--------------------------------------

It is easy to make a mistake and create a test which is always "successful".
Test that your test catches mistakes. Verify whether it extracts the right
numbers.


Never commit functionality to the main development line without tests
---------------------------------------------------------------------

If you commit functionality to the main development line without tests then
this functionality will break sooner or later and we have no automatic
mechanism to detect it. Committing new code without tests is bad karma.


Never add inputs to the test directories which are never run
------------------------------------------------------------

We want all inputs and outputs to be accessile by the default test
suite. Otherwise we have no automatic way to detect that some inputs or outputs
have degraded. Degraded inputs and outputs are useless and confusing.



Example: Adding a test in the DIRAC code
========================================

Easy example
------------

Let us look at an easy example.

First we import modules that we need (highlighted lines):

.. code-block:: python
  :emphasize-lines: 3-8

  #!/usr/bin/env python

  import os
  import sys
  sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

  from runtest import version_info, get_filter, cli, run
  from runtest_config import configure

  assert version_info.major == 2

  f = [
      get_filter(from_string='@   Elements of the electric dipole',
                 to_string='@   anisotropy',
                 rel_tolerance=1.0e-5),
      get_filter(from_string='************ Expectation values',
                 to_string='s0 = T : Expectation value',
                 rel_tolerance=1.0e-5),
  ]

  options = cli()

  ierr = 0
  for inp in ['PBE0gracLB94.inp', 'GLLBsaopLBalpha.inp']:
      for mol in ['Ne.mol']:
          ierr += run(options,
                      configure,
                      input_files=[inp, mol],
                      filters={'out': f})

  sys.exit(ierr)

Then we construct a list of filters. We can construct as many lists as we like and they can contain as many filters as we like.

.. code-block:: python
  :emphasize-lines: 12-19

  #!/usr/bin/env python

  import os
  import sys
  sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

  from runtest import version_info, get_filter, cli, run
  from runtest_config import configure

  assert version_info.major == 2

  f = [
      get_filter(from_string='@   Elements of the electric dipole',
                 to_string='@   anisotropy',
                 rel_tolerance=1.0e-5),
      get_filter(from_string='************ Expectation values',
                 to_string='s0 = T : Expectation value',
                 rel_tolerance=1.0e-5),
  ]

  options = cli()

  ierr = 0
  for inp in ['PBE0gracLB94.inp', 'GLLBsaopLBalpha.inp']:
      for mol in ['Ne.mol']:
          ierr += run(options,
                      configure,
                      input_files=[inp, mol],
                      filters={'out': f})

  sys.exit(ierr)

After we use the command line interface to generate options, we really run the test.
Note how we pass the configure option to the run function:

.. code-block:: python
  :emphasize-lines: 26-29

  #!/usr/bin/env python

  import os
  import sys
  sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

  from runtest import version_info, get_filter, cli, run
  from runtest_config import configure

  assert version_info.major == 2

  f = [
      get_filter(from_string='@   Elements of the electric dipole',
                 to_string='@   anisotropy',
                 rel_tolerance=1.0e-5),
      get_filter(from_string='************ Expectation values',
                 to_string='s0 = T : Expectation value',
                 rel_tolerance=1.0e-5),
  ]

  options = cli()

  ierr = 0
  for inp in ['PBE0gracLB94.inp', 'GLLBsaopLBalpha.inp']:
      for mol in ['Ne.mol']:
          ierr += run(options,
                      configure,
                      input_files=[inp, mol],
                      filters={'out': f})

  sys.exit(ierr)

Note how we pass the filter list as a dictionary. If we omit to pass it, then
the calculations will be run but not verified. This is useful for multi-step
jobs.  From the dictionary, the library knows that it should execute the filter
list "f" on output files with the suffix "out".


.. _example-test-script:

Example test script
===================

Let us consider a relatively simple annotated example.

First we import modules that we need (highlighted lines):

.. code-block:: python
  :emphasize-lines: 3-16

  #!/usr/bin/env python

  # provides os.path.join
  import os

  # provides exit
  import sys

  # we make sure we can import runtest and runtest_config
  sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

  # we import essential functions from the runtest library
  from runtest import version_info, get_filter, cli, run

  # this tells runtest how to run your code
  from runtest_config import configure

  # we stop the script if the major version is not compatible
  assert version_info.major == 2

  # construct a filter list which contains two filters
  f = [
      get_filter(from_string='@   Elements of the electric dipole',
                 to_string='@   anisotropy',
                 rel_tolerance=1.0e-5),
      get_filter(from_string='************ Expectation values',
                 to_string='s0 = T : Expectation value',
                 rel_tolerance=1.0e-5),
  ]

  # invoke the command line interface parser which returns options
  options = cli()

  ierr = 0
  for inp in ['PBE0gracLB94.inp', 'GLLBsaopLBalpha.inp']:
      for mol in ['Ne.mol']:
          # the run function runs the code and filters the outputs
          ierr += run(options,
                      configure,
                      input_files=[inp, mol],
                      filters={'out': f})

  sys.exit(ierr)

Then we construct a list of filters. We can construct as many lists as we like
and they can contain as many filters as we like.  The list does not have to be
called "f". Give it a name that is meaningful to you.

.. code-block:: python
  :emphasize-lines: 21-29

  #!/usr/bin/env python

  # provides os.path.join
  import os

  # provides exit
  import sys

  # we make sure we can import runtest and runtest_config
  sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

  # we import essential functions from the runtest library
  from runtest import version_info, get_filter, cli, run

  # this tells runtest how to run your code
  from runtest_config import configure

  # we stop the script if the major version is not compatible
  assert version_info.major == 2

  # construct a filter list which contains two filters
  f = [
      get_filter(from_string='@   Elements of the electric dipole',
                 to_string='@   anisotropy',
                 rel_tolerance=1.0e-5),
      get_filter(from_string='************ Expectation values',
                 to_string='s0 = T : Expectation value',
                 rel_tolerance=1.0e-5),
  ]

  # invoke the command line interface parser which returns options
  options = cli()

  ierr = 0
  for inp in ['PBE0gracLB94.inp', 'GLLBsaopLBalpha.inp']:
      for mol in ['Ne.mol']:
          # the run function runs the code and filters the outputs
          ierr += run(options,
                      configure,
                      input_files=[inp, mol],
                      filters={'out': f})

  sys.exit(ierr)

After we use the command line interface to generate options, we really run the
test.  Note how we pass the configure function to the run function. Also note how
we pass the filter list as a dictionary. If we omit to pass it, then the
calculations will be run but not verified. This is useful for multi-step jobs.
From the dictionary, the library knows that it should execute the filter list
"f" on output files with the suffix "out". It is no problem to apply different
filters to different output files, for this add entries to the `filters`
dictionary.

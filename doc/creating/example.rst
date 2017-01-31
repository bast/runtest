

Example: Adding a test in the DIRAC code
========================================

Creating a link between runtest and the code you want to test
-------------------------------------------------------------

The runtest library is a low-level program-independent library that provides
infrastructure for running calculations and extracting and comparing numbers
against reference outputs. The library does not know anything about your code.

The library requires that you define a configure function which defines how to
handle a list of input files and extra arguments and which also defines the
launcher of your code, full launch command, output prefix, and relative
reference path where reference outputs are stored.

Here is an example module ``runtest_config.py`` which defines such a function:

.. code-block:: python

  def configure(options, input_files, extra_args):
      """
      This function is used by runtest to configure runtest
      at runtime for DIRAC specific launch command and file naming.
      """

      from os import path
      from sys import platform

      launcher = 'pam'
      launcher_full_path = path.normpath(path.join(options.binary_dir, launcher))

      (inp, mol) = input_files

      if platform == "win32":
          exe = 'dirac.x.exe'
      else:
          exe = 'dirac.x'

      command = []
      command.append('python {0}'.format(launcher_full_path))
      command.append('--dirac={0}'.format(path.join(options.binary_dir, exe)))
      command.append('--noarch --nobackup')
      command.append('--inp={0} --mol={1}'.format(inp, mol))
      if extra_args is not None:
          command.append(extra_args)

      full_command = ' '.join(command)

      inp_no_suffix = path.splitext(inp)[0]
      mol_no_suffix = path.splitext(mol)[0]

      output_prefix = '{0}_{1}'.format(inp_no_suffix, mol_no_suffix)

      relative_reference_path = 'result'

      return launcher, full_command, output_prefix, relative_reference_path


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

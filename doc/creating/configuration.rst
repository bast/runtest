

How to hook up runtest with your code
=====================================

The runtest library is a low-level program-independent library that provides
infrastructure for running calculations and extracting and comparing numbers
against reference outputs. The library does not know anything about your code.

In order to tell the library how to run your code, the library requires that
you define a configure function which defines how to handle a list of input
files and extra arguments.  This configure function also defines the launcher
script or binary for your code, the full launch command, the output prefix, and
relative reference path where reference outputs are stored.
The output prefix can also be ``None``.

Here is an example module ``runtest_config.py`` which defines such a function:

.. code-block:: python

  def configure(options, input_files, extra_args):
      """
      This function is used by runtest to configure runtest
      at runtime for code specific launch command and file naming.
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

The function is expected to return ``launcher``, ``full_command``,
``output_prefix``, and ``relative_reference_path``.

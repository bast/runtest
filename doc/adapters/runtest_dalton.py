
import os
import sys
import runtest


class Filter(runtest.Filter):

    def __init__(self):
        runtest.Filter.__init__(self)

    def add(self, *args, **kwargs):
        try:
            runtest.Filter.add(self, *args, **kwargs)
        except runtest.FilterKeywordError, e:
            sys.stderr.write(str(e))
            sys.exit(-1)


class TestRun(runtest.TestRun):

    def __init__(self, _file, argv):
        runtest.TestRun.__init__(self, _file, argv)
        self.return_code = 0

    def run(self, inp_files, mol_files, f=None, args='', accepted_errors=[]):

        launch_script = os.path.normpath(os.path.join(self.binary_dir, 'dalton'))
        if self.skip_run:
            sys.stdout.write('\nskipping actual run\n')
        else:
            if not os.path.exists(launch_script):
                sys.stderr.write('ERROR: launch script %s not found\n' % launch_script)
                sys.stderr.write('       have you set the correct --binary-dir (or -b)?\n')
                sys.stderr.write('       try also --help\n')
                sys.exit(-1)

        launcher = '%s -noarch -nobackup %s' % (launch_script, args)

        for inp in inp_files:
            inp_no_suffix = os.path.splitext(inp)[0]
            for mol in mol_files:
                mol_no_suffix = os.path.splitext(mol)[0]
                output_no_suffix = '%s_%s' % (inp_no_suffix, mol_no_suffix)
                sys.stdout.write('\nrunning test: %s %s\n' % (inp_no_suffix, mol_no_suffix))

                command = launcher + ' %s %s' % (inp_no_suffix, mol_no_suffix)
                try:
                    runtest.TestRun.execute(self,
                                            command=command,
                                            stdout_file_name = '%s.stdout' % output_no_suffix,
                                            accepted_errors=accepted_errors)
                    if f is None:
                        sys.stdout.write('finished (no reference)\n')
                    else:
                        try:
                            # f is a suffix-filter dictionary
                            for suffix in f:
                                out = '%s.%s' % (output_no_suffix, suffix)
                                f[suffix].check(self.work_dir, '%s' % out, 'result/%s' % out, self.verbose)
                            sys.stdout.write('passed\n')
                        except IOError, e:
                            sys.stderr.write('ERROR: could not open file %s\n' % e.filename)
                            sys.exit(-1)
                        except runtest.TestFailedError, e:
                            sys.stderr.write(str(e))
                            self.return_code += 1
                        except runtest.BadFilterError, e:
                            sys.stderr.write(str(e))
                            sys.exit(-1)
                        except runtest.FilterKeywordError, e:
                            sys.stderr.write(str(e))
                            sys.exit(-1)
                except runtest.AcceptedError, e:
                    sys.stdout.write(str(e))
                except runtest.SubprocessError, e:
                    sys.stderr.write(str(e))
                    sys.exit(-1)

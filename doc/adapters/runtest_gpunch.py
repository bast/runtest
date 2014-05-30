
import os
import sys
import runtest


class Filter(runtest.Filter):

    def __init__(self):
        runtest.Filter.__init__(self)

    def add(self, *args, **kwargs):
        try:
            runtest.Filter.add(self, *args, **kwargs)
        except runtest.FilterKeywordError as e:
            sys.stderr.write(e.message)
            sys.exit(-1)


class TestRun(runtest.TestRun):

    def __init__(self, _file, argv):
        runtest.TestRun.__init__(self, _file, argv)
        self.return_code = 0

    def run(self, inp_files, f=None, accepted_errors=[]):

        if sys.platform == "win32":
            executable = 'gpunch.exe'
        else:
            executable = 'gpunch'

        executable = os.path.normpath(os.path.join(self.binary_dir, executable))
        if self.skip_run:
            sys.stdout.write('\nskipping actual run\n')
        else:
            if not os.path.exists(executable):
                sys.stderr.write('ERROR: executable not found in %s\n' % executable)
                sys.stderr.write('       have you set the correct --binary-dir (or -b)?\n')
                sys.stderr.write('       try also --help\n')
                sys.exit(-1)

        for inp in inp_files:
            out = '%s.out' % os.path.splitext(inp)[0]
            sys.stdout.write('\nrunning test: %s\n' % inp)

            command = executable + ' %s %s' % (inp, out)
            try:
                runtest.TestRun.execute(self,
                                        command=command,
                                        accepted_errors=accepted_errors)
                if f is None:
                    sys.stdout.write('finished (no reference)\n')
                else:
                    try:
                        f.check(self.work_dir, '%s' % out, 'reference/%s' % out, self.verbose)
                        sys.stdout.write('passed\n')
                    except IOError as e:
                        sys.stderr.write('ERROR: could not open file %s\n' % e.filename)
                        sys.exit(-1)
                    except runtest.TestFailedError as e:
                        sys.stderr.write(e.message)
                        self.return_code += 1
                    except runtest.BadFilterError as e:
                        sys.stderr.write(e.message)
                        sys.exit(-1)
            except runtest.AcceptedError as e:
                sys.stdout.write(e.message)
            except runtest.SubprocessError as e:
                sys.stderr.write(e.message)
                sys.exit(-1)

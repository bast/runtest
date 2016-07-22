def run(options, get_command, t, f=None, accepted_errors=None):

    import os
    import sys
    import inspect
    import shlex
    import subprocess
    from .exceptions import TestFailedError, BadFilterError, FilterKeywordError
    from .copy import copy_path

    # here we find out where the test script sits
    frame = inspect.stack()[-1]
    module = inspect.getmodule(frame[0])
    caller_file = module.__file__
    caller_dir = os.path.dirname(os.path.realpath(caller_file))

    # if the work_dir is different from caller_dir
    # we copy all files under caller_dir to work_dir
    if options.work_dir != caller_dir:
        copy_path(caller_dir, options.work_dir)

    launcher, command, outputs = get_command(options, t)

    launch_script_path = os.path.normpath(os.path.join(options.binary_dir, launcher))

    if not options.skip_run and not os.path.exists(launch_script_path):
        sys.stderr.write('ERROR: launch script {0} not found in {1}\n'.format(launcher, options.binary_dir))
        sys.stderr.write('       have you set the correct --binary-dir (or -b)?\n')
        sys.stderr.write('       try also --help\n')
        sys.exit(-1)

    sys.stdout.write('\nrunning test with input tuple %s\n' % t)

    if options.skip_run:
        sys.stdout.write('(skipped run with -s|--skip-run)\n')
    else:
        if sys.platform != "win32":
            command = shlex.split(command)

        process = subprocess.Popen(command,
                                   cwd=options.work_dir,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            sys.stdout.write('ERROR: crash during %s\n%s' % (command, stderr))
            sys.exit(1)

    if accepted_errors is not None:
        for error in accepted_errors:
            if error in stderr:
                # we found an error that we expect/accept
                sys.stdout.write('found error which is expected/accepted: %s\n' % error)

    # for dalton?
    # if stdout_file_name != '':
    #     f = open(stdout_file_name, 'w')
    #     f.write(stdout)
    #     f.close()

    if f is None:
        sys.stdout.write('finished (no reference)\n')
    else:
        try:
            for i, output in enumerate(outputs):
                check(f[i], '%s' % output, 'result/%s' % output, options.verbose)
            sys.stdout.write('passed\n')
        except IOError as e:
            sys.stderr.write('ERROR: could not open file %s\n' % e.filename)
            sys.exit(1)
        except TestFailedError as e:
            sys.stderr.write(str(e))
            return 1
        except BadFilterError as e:
            sys.stderr.write(str(e))
            sys.exit(1)
        except FilterKeywordError as e:
            sys.stderr.write(str(e))
            sys.exit(1)
    return 0



def check(filter_list, out_name, ref_name, verbose=False):
    """
    Compares output (work_dir/out_name) with reference (work_dir/ref_name)
    applying all filters tasks from the list of filters.

    Input:
        - work_dir -- working directory
        - out_name -- actual output file name
        - ref_name -- reference output file name
        - verbose  -- give verbose output upon failure

    Returns:
        - nothing

    Generates the following files in work_dir:
        - out_name.filtered  -- numbers extracted from output
        - out_name.reference -- numbers extracted from reference
        - out_name.diff      -- difference between the two above

    Raises:
        - TestFailedError
    """
    import os
    from .tuple_comparison import tuple_matches
    from .extract import extract_numbers
    from .scissors import cut_sections
    from .exceptions import FilterKeywordError, TestFailedError, BadFilterError

    def _tuple_matches(t):
        if f.tolerance_is_relative:
            error_definition = 'relative'
        else:
            error_definition = 'absolute'
        return tuple_matches(t,
                             tolerance=f.tolerance,
                             error_definition=error_definition,
                             ignore_sign=f.ignore_sign,
                             skip_below=f.skip_below,
                             skip_above=f.skip_above)

    log_out = open('%s.filtered' % out_name, 'w')
    log_ref = open('%s.reference' % out_name, 'w')
    log_diff = open('%s.diff' % out_name, 'w')

    for f in filter_list:

        out_filtered = cut_sections(open(out_name).readlines(),
                                    from_string=f.from_string,
                                    from_is_re=f.from_is_re,
                                    to_string=f.to_string,
                                    to_is_re=f.to_is_re,
                                    num_lines=f.num_lines)
        if out_filtered == []:
            if f.num_lines > 0:
                r = '[%i lines from "%s"]' % (f.num_lines, f.from_string)
            else:
                r = '["%s" ... "%s"]' % (f.from_string, f.to_string)
            message = 'ERROR: filter %s did not extract anything from file %s\n' % (r, out_name)
            raise BadFilterError(message)

        log_out.write(''.join(out_filtered))
        out_numbers, out_locations = extract_numbers(out_filtered, f.mask)
        if f.mask is not None and out_numbers == []:
            raise FilterKeywordError('ERROR: mask %s did not extract any numbers\n' % f.mask)

        ref_filtered = cut_sections(open(ref_name).readlines(),
                                    from_string=f.from_string,
                                    from_is_re=f.from_is_re,
                                    to_string=f.to_string,
                                    to_is_re=f.to_is_re,
                                    num_lines=f.num_lines)
        if ref_filtered == []:
            if f.num_lines > 0:
                r = '[%i lines from "%s"]' % (f.num_lines, f.from_string)
            else:
                r = '["%s" ... "%s"]' % (f.from_string, f.to_string)
            message = 'ERROR: filter %s did not extract anything from file %s\n' % (r, ref_name)
            raise BadFilterError(message)

        log_ref.write(''.join(ref_filtered))
        ref_numbers, _ = extract_numbers(ref_filtered, f.mask)
        if f.mask is not None and ref_numbers == []:
            raise FilterKeywordError('ERROR: mask %s did not extract any numbers\n' % f.mask)

        if out_numbers == [] and ref_numbers == []:
            # no numbers are extracted
            if out_filtered != ref_filtered:
                log_diff.write('ERROR: extracted strings do not match\n')
                log_diff.write('own gave:\n')
                log_diff.write(''.join(out_filtered) + '\n')
                log_diff.write('reference gave:\n')
                log_diff.write(''.join(ref_filtered) + '\n')

        # we need to check for len(out_numbers) > 0
        # for pure strings len(out_numbers) is 0
        # TODO need to consider what to do with pure strings in future versions
        if len(out_numbers) == len(ref_numbers) and len(out_numbers) > 0:
            if not f.tolerance_is_set and (any(map(lambda x: isinstance(x, float), out_numbers)) or any(map(lambda x: isinstance(x, float), ref_numbers))):
                raise FilterKeywordError('ERROR: for floats you have to specify either rel_tolerance or abs_tolerance\n')
            l = map(_tuple_matches, zip(out_numbers, ref_numbers))
            matching, errors = zip(*l)  # unzip tuples to two lists
            if not all(matching):
                log_diff.write('\n')
                for k, line in enumerate(out_filtered):
                    log_diff.write('.       %s' % line)
                    for i, num in enumerate(out_numbers):
                        (line_num, start_char, length) = out_locations[i]
                        if line_num == k:
                            if errors[i]:
                                log_diff.write('ERROR   %s%s %s\n' % (' ' * start_char, '#' * length, errors[i]))

        if len(out_numbers) != len(ref_numbers):
            log_diff.write('ERROR: extracted sizes do not match\n')
            log_diff.write('own gave %i numbers:\n' % len(out_numbers))
            log_diff.write(''.join(out_filtered) + '\n')
            log_diff.write('reference gave %i numbers:\n' % len(ref_numbers))
            log_diff.write(''.join(ref_filtered) + '\n')

    log_out.close()
    log_ref.close()
    log_diff.close()

    if os.path.getsize('%s.diff' % out_name) > 0:
        log_diff = open('%s.diff' % out_name, 'r')
        diff = ''
        for line in log_diff.readlines():
            diff += line
        log_diff.close()
        message = "ERROR: test %s failed\n" % out_name
        if verbose:
            message += diff
        raise TestFailedError(message)


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

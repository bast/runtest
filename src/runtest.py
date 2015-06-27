
"""
    runtest - Numerically tolerant test library

    Author:
        Radovan Bast

    License:
        BSD-3
        https://github.com/bast/runtest/blob/master/LICENSE

    Documentation:
        http://runtest.readthedocs.org

    Source:
        https://github.com/bast/runtest

    Issue tracking:
        https://github.com/bast/runtest/issues
"""

import re
import os
import sys
import subprocess
import shlex
import shutil
import string
from optparse import OptionParser


__version__ = '1.3.5'  # http://semver.org


class FilterKeywordError(Exception):
    pass


class TestFailedError(Exception):
    pass


class BadFilterError(Exception):
    pass


class AcceptedError(Exception):
    pass


class SubprocessError(Exception):
    pass

# ------------------------------------------------------------------------------


def is_float(x):
    return isinstance(x, float)

# ------------------------------------------------------------------------------


def is_int(n):
    return isinstance(n, int)

# ------------------------------------------------------------------------------


def tuple_matches(f, tup):

    x, x_ref = tup

    if f.ignore_sign:
        # if ignore sign take absolute values
        x = abs(x)
        x_ref = abs(x_ref)

    if is_int(x) and is_int(x_ref):
        return x == x_ref

    if abs(x_ref) < f.ignore_below:
        return True

    if abs(x_ref) > f.ignore_above:
        return True

    error = x - x_ref
    if f.tolerance_is_relative:
        error /= x_ref
    return abs(error) <= f.tolerance

# ------------------------------------------------------------------------------


def compare_lists(f, l1, l2):
    """
    Input:
        - f -- filter task
        - l1 -- list of numbers
        - l2 -- another list of numbers

    Returns:
        - res -- list that contains ones (pass) or zeros (failures)
                 l1, l2, and res have same length

    Raises:
        - FilterKeywordError
    """

    # FIXME this will move up once the caller is unit-tested
    # if we have any float in there then tolerance must be set
    if not f.tolerance_is_set and (any(map(is_float, l1)) or any(map(is_float, l2))):
        raise FilterKeywordError('ERROR: for floats you have to specify either rel_tolerance or abs_tolerance\n')
    return map(lambda t: tuple_matches(f, t), zip(l1, l2))

# ------------------------------------------------------------------------------


def extract_numbers(f, text):
    """
    Input:
        - f -- filter task
        - text -- list of lines where we extract numbers from

    Returns:
        - numbers -- list of numbers
        - locations -- locations of each number, list of triples
                      (line, start position, length)
    """

    numeric_const_pattern = r"""
    [-+]? # optional sign
    (?:
        (?: \d* \. \d+ ) # .1 .12 .123 etc 9.1 etc 98.1 etc
        |
        (?: \d+ \.? ) # 1. 12. 123. etc 1 12 123 etc
    )
    # followed by optional exponent part if desired
    (?: [EeDd] [+-]? \d+ ) ?
    """

    pattern_int = re.compile('^-?[0-9]+$', re.VERBOSE)
    pattern_float = re.compile(numeric_const_pattern, re.VERBOSE)
    pattern_d = re.compile(r'[dD]')

    numbers = []
    locations = []

    for n, line in enumerate(text):
        i = 0
        for w in line.split():
            # do not consider words like TzB1g
            # otherwise we would extract 1 later
            if re.match(r'^[0-9\.eEdD\+\-]*$', w):
                i += 1
                if (f.use_mask) and (i not in f.mask):
                    continue
                is_integer = False
                if len(pattern_float.findall(w)) > 0:
                    is_integer = (pattern_float.findall(w) == pattern_int.findall(w))
                # apply floating point regex
                for m in pattern_float.findall(w):
                    index = line.index(m)
                    # substitute dD by e
                    m = pattern_d.sub('e', m)
                    if is_integer:
                        numbers.append(int(m))
                    else:
                        numbers.append(float(m))
                    locations.append((n, index, len(m)))

    return numbers, locations

# ------------------------------------------------------------------------------


def parse_args(input_dir, argv):

    parser = OptionParser(description='runtest %s - Numerically tolerant test library.' % __version__)
    parser.add_option('--binary-dir',
                      '-b',
                      action='store',
                      default=input_dir,
                      help='directory containing the binary/launcher [default: %default]')
    parser.add_option('--work-dir',
                      '-w',
                      action='store',
                      default=input_dir,
                      help='working directory [default: %default]')
    parser.add_option('--verbose',
                      '-v',
                      action='store_true',
                      default=False,
                      help='give more verbose output upon test failure [default: %default]')
    parser.add_option('--skip-run',
                      '-s',
                      action='store_true',
                      default=False,
                      help='skip actual calculation(s) [default: %default]')
    parser.add_option('--debug',
                      '-d',
                      action='store_true',
                      default=False,
                      help='print verbose debug information [default: %default]')
    parser.add_option('--log',
                      '-l',
                      action='store',
                      default=None,
                      help='log file [default: no logging]')
    (options, args) = parser.parse_args(args=argv[1:])

    if sys.platform == "win32":
        # on windows we flip possibly wrong slashes
        options.binary_dir = string.replace(options.binary_dir, '/', '\\')
        options.work_dir = string.replace(options.work_dir, '/', '\\')

    return options


# ------------------------------------------------------------------------------

def copy_path(root_src_dir, root_dst_dir, exclude_files=[]):
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for f in files:
            if f not in exclude_files:
                src_file = os.path.join(src_dir, f)
                dst_file = os.path.join(dst_dir, f)
                shutil.copy(src_file, dst_file)


# ------------------------------------------------------------------------------

def underline(f, start_char, length, reference, number, is_integer):
    """
    Input:
        - f -- filter task
        - start_char -- position of start character
        - length -- underline length
        - reference -- reference number
        - number -- obtained (calculated) number
        - is_integer -- whether reference number is integer

    Returns:
        - s -- underline string with info about reference and tolerance
    """

    s = ''
    for i in range(start_char):
        s += ' '
    for i in range(length):
        s += '#'
    s += ' expected: %s' % reference

    if not is_integer:
        if f.tolerance_is_set:
            if f.tolerance_is_relative:
                s += ' (rel diff: %6.2e)' % abs(1.0 - number / reference)
            else:
                if f.ignore_sign:
                    s += ' (abs diff: %6.2e ignoring signs)' % abs(abs(number) - abs(reference))
                else:
                    s += ' (abs diff: %6.2e)' % abs(number - reference)

    return s + '\n'


# ------------------------------------------------------------------------------

class TestRun:

    def __init__(self, _file, argv):

        self.input_dir = input_dir = os.path.dirname(os.path.realpath(_file))

        options = parse_args(input_dir, argv)
        self.binary_dir = options.binary_dir
        self.work_dir = options.work_dir
        self.verbose = options.verbose
        self.skip_run = options.skip_run
        self.debug = options.debug
        self.log = options.log

        if self.work_dir != self.input_dir:
            copy_path(self.input_dir, self.work_dir)

        os.chdir(self.work_dir)  # FIXME possibly problematic

    def execute(self,
                command,
                stdout_file_name='',
                accepted_errors=[]):
        """
        Runs the command.

        Raises:
            - AcceptedError
            - SubprocessError
        """
        if self.skip_run:
            return

        if sys.platform != "win32":
            command = shlex.split(command)

        if self.debug:
            print('\nlaunching command: %s' % ' '.join(command))

        process = subprocess.Popen(command,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if self.debug:
            print('\nstdout:\n%s' % stdout)
            if stderr != '':
                print('\nstderr:\n%s' % stderr)

        for error in accepted_errors:
            if error in stderr:
                # we found an error that we expect/accept
                raise AcceptedError('found error which is expected/accepted: %s\n' % error)
        if process.returncode != 0:
            raise SubprocessError('ERROR: crash during %s\n%s' % (command, stderr))
        if stdout_file_name != '':
            f = open(stdout_file_name, 'w')
            f.write(stdout)
            f.close()


class _SingleFilter:

    def __init__(self, **kwargs):
        recognized_keywords = ['from_re',
                               'to_re',
                               're',
                               'from_string',
                               'to_string',
                               'string',
                               'ignore_below',
                               'ignore_above',
                               'ignore_sign',
                               'mask',
                               'num_lines',
                               'rel_tolerance',
                               'abs_tolerance']

        # check for unrecognized keywords
        for key in kwargs.keys():
            if key not in recognized_keywords:
                available_keywords = (', ').join(recognized_keywords)
                message = 'ERROR: keyword "%s" not recognized\n       ' % key
                message += 'available keywords: %s\n' % available_keywords
                raise FilterKeywordError(message)

        # check for incompatible keywords
        self._check_incompatible_keywords('from_re', 'from_string', kwargs)
        self._check_incompatible_keywords('to_re', 'to_string', kwargs)
        self._check_incompatible_keywords('to_string', 'num_lines', kwargs)
        self._check_incompatible_keywords('to_re', 'num_lines', kwargs)
        self._check_incompatible_keywords('string', 'from_string', kwargs)
        self._check_incompatible_keywords('string', 'to_string', kwargs)
        self._check_incompatible_keywords('string', 'from_re', kwargs)
        self._check_incompatible_keywords('string', 'to_re', kwargs)
        self._check_incompatible_keywords('string', 'num_lines', kwargs)
        self._check_incompatible_keywords('re', 'from_string', kwargs)
        self._check_incompatible_keywords('re', 'to_string', kwargs)
        self._check_incompatible_keywords('re', 'from_re', kwargs)
        self._check_incompatible_keywords('re', 'to_re', kwargs)
        self._check_incompatible_keywords('re', 'num_lines', kwargs)
        self._check_incompatible_keywords('rel_tolerance', 'abs_tolerance', kwargs)

        # now continue with keywords
        self.from_string = kwargs.get('from_string', '')
        self.to_string = kwargs.get('to_string', '')
        self.ignore_sign = kwargs.get('ignore_sign', False)
        self.ignore_below = kwargs.get('ignore_below', sys.float_info.min)
        self.ignore_above = kwargs.get('ignore_above', sys.float_info.max)
        self.num_lines = kwargs.get('num_lines', 0)

        if 'rel_tolerance' in kwargs.keys():
            self.tolerance = kwargs.get('rel_tolerance')
            self.tolerance_is_relative = True
            self.tolerance_is_set = True
        elif 'abs_tolerance' in kwargs.keys():
            self.tolerance = kwargs.get('abs_tolerance')
            self.tolerance_is_relative = False
            self.tolerance_is_set = True
        else:
            self.tolerance_is_set = False

        self.mask = kwargs.get('mask', [])
        if self.mask == []:
            self.use_mask = False
        else:
            self.use_mask = True
            for i in self.mask:
                if i < 1:
                    raise FilterKeywordError('ERROR: mask starts counting from 1 (first word)\n')

        self.from_is_re = False
        from_re = kwargs.get('from_re', '')
        if from_re != '':
            self.from_string = from_re
            self.from_is_re = True

        self.to_is_re = False
        to_re = kwargs.get('to_re', '')
        if to_re != '':
            self.to_string = to_re
            self.to_is_re = True

        only_string = kwargs.get('string', '')
        if only_string != '':
            self.from_string = only_string
            self.num_lines = 1

        only_re = kwargs.get('re', '')
        if only_re != '':
            self.from_string = only_re
            self.num_lines = 1
            self.from_is_re = True

    def _check_incompatible_keywords(self, kw1, kw2, kwargs):
        if kw1 in kwargs.keys() and kw2 in kwargs.keys():
            raise FilterKeywordError('ERROR: incompatible keywords: "%s" and "%s"\n' % (kw1, kw2))


class Filter:

    def __init__(self):
        self.filter_list = []

    def add(self, *args, **kwargs):
        """
        Adds filter task to list of filters.

        Raises:
            - FilterKeywordError
        """
        self.filter_list.append(_SingleFilter(*args, **kwargs))

    def check(self, work_dir, out_name, ref_name, verbose=False):
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

        log_out = open('%s.filtered' % out_name, 'w')
        log_ref = open('%s.reference' % out_name, 'w')
        log_diff = open('%s.diff' % out_name, 'w')

        for f in self.filter_list:

            out_filtered = self._filter_file(f, out_name)
            log_out.write(''.join(out_filtered))
            out_numbers, out_locations = extract_numbers(f, out_filtered)
            if f.use_mask and out_numbers == []:
                raise FilterKeywordError('ERROR: mask %s did not extract any numbers\n' % f.mask)

            ref_filtered = self._filter_file(f, ref_name)
            log_ref.write(''.join(ref_filtered))
            ref_numbers, ref_locations = extract_numbers(f, ref_filtered)
            if f.use_mask and ref_numbers == []:
                raise FilterKeywordError('ERROR: mask %s did not extract any numbers\n' % f.mask)

            if out_numbers == [] and ref_numbers == []:
                # no numbers are extracted
                if out_filtered != ref_filtered:
                    log_diff.write('ERROR: extracted strings do not match\n')
                    log_diff.write('own gave:\n')
                    log_diff.write(''.join(out_filtered) + '\n')
                    log_diff.write('reference gave:\n')
                    log_diff.write(''.join(ref_filtered) + '\n')

            if len(out_numbers) == len(ref_numbers):
                l = compare_lists(f, out_numbers, ref_numbers)
                if not all(l):
                    log_diff.write('\n')
                    for k, line in enumerate(out_filtered):
                        log_diff.write('.       %s' % line)
                        for i, num in enumerate(out_numbers):
                            (line_num, start_char, length) = out_locations[i]
                            if line_num == k:
                                if not l[i]:
                                    is_integer = isinstance(num, int)  # FIXME use is_int()
                                    log_diff.write('ERROR   %s' % underline(f, start_char, length, ref_numbers[i], out_numbers[i], is_integer))

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

    def _filter_file(self, f, file_name):
        """
        Input:
            - f -- filter task
            - file_name -- the output file to filter

        Returns:
            - output_filtered -- the filtered output

        Raises:
            - BadFilterError
        """

        output = open(file_name).readlines()

        output_filtered = []

        for i in range(len(output)):
            start_line_matches = False
            if f.from_is_re:
                start_line_matches = re.match(r'.*%s' % f.from_string, output[i])
            else:
                start_line_matches = (f.from_string in output[i])
            if start_line_matches:
                if f.num_lines > 0:
                    for n in range(i, i + f.num_lines):
                        output_filtered.append(output[n])
                else:
                    for j in range(i, len(output)):
                        f.end_line_matches = False
                        if f.to_is_re:
                            f.end_line_matches = re.match(r'.*%s' % f.to_string, output[j])
                        else:
                            f.end_line_matches = (f.to_string in output[j])
                        if f.end_line_matches:
                            for n in range(i, j + 1):
                                output_filtered.append(output[n])
                            break

        if output_filtered == []:
            if f.num_lines > 0:
                r = '[%i lines from "%s"]' % (f.num_lines, f.from_string)
            else:
                r = '["%s" ... "%s"]' % (f.from_string, f.to_string)
            message = 'ERROR: filter %s did not extract anything from file %s\n' % (r, file_name)
            raise BadFilterError(message)

        return output_filtered

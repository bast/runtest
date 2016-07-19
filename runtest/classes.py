from .exceptions import FilterKeywordError, SubprocessError


def _check_for_unknown_kw(kwargs):
    """Checks whether there are any unknown keywords.

    Args:
        kwargs: keyword arguments

    Returns:
        Error message. None if all keywords are known.
    """
    recognized_kw = ['from_re',
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

    unrecoginzed_kw = [kw for kw in kwargs.keys() if kw not in recognized_kw]
    if unrecoginzed_kw == []:
        return None
    else:
        return 'ERROR: keyword(s) ({unrecognized}) not recognized\n       available keywords: ({available})\n'.format(unrecognized=(', ').join(sorted(unrecoginzed_kw)),
                                                                                                                      available=(', ').join(recognized_kw))


def _check_for_incompatible_kw(kwargs):
    """Checks whether there are any incompatible keyword pairs.

    Args:
        kwargs: keyword arguments

    Returns:
        Error message. Empty if all keywords are compatible.
    """
    incompatible_pairs = [('from_re', 'from_string'),
                          ('to_re', 'to_string'),
                          ('to_string', 'num_lines'),
                          ('to_re', 'num_lines'),
                          ('string', 'from_string'),
                          ('string', 'to_string'),
                          ('string', 'from_re'),
                          ('string', 'to_re'),
                          ('string', 'num_lines'),
                          ('re', 'from_string'),
                          ('re', 'to_string'),
                          ('re', 'from_re'),
                          ('re', 'to_re'),
                          ('re', 'num_lines'),
                          ('rel_tolerance', 'abs_tolerance')]

    incompatible_kw = [(kw1, kw2) for (kw1, kw2) in incompatible_pairs if kw1 in kwargs.keys() and kw2 in kwargs.keys()]
    if incompatible_kw == []:
        return None
    else:
        return 'ERROR: incompatible keyword pairs: {0}\n'.format(incompatible_kw)


class TestRun:

    def __init__(self, _file):
        import os
        import sys
        from .cli import parse_args
        from .copy import copy_path

        self.input_dir = input_dir = os.path.dirname(os.path.realpath(_file))

        options = parse_args(input_dir, sys.argv)
        self.binary_dir = options.binary_dir
        self.work_dir = options.work_dir
        self.verbose = options.verbose
        self.skip_run = options.skip_run

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
        import shlex
        import subprocess
        import sys

        if self.skip_run:
            return

        if sys.platform != "win32":
            command = shlex.split(command)

        process = subprocess.Popen(command,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

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
        import sys

        error = _check_for_unknown_kw(kwargs)
        if error:
            raise FilterKeywordError(error)

        error = _check_for_incompatible_kw(kwargs)
        if error:
            raise FilterKeywordError(error)

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

        self.mask = kwargs.get('mask', None)

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

    # FIXME work_dir is not used
    def check(self, work_dir, out_name, ref_name, verbose=False):
        from .main import _check
        _check(self.filter_list, out_name, ref_name, verbose)

def cli():

    from optparse import OptionParser
    import sys
    import os
    import inspect
    from .version import __version__ as _version

    frame = inspect.stack()[-1]
    module = inspect.getmodule(frame[0])
    caller_file = module.__file__
    caller_dir = os.path.dirname(os.path.realpath(caller_file))

    parser = OptionParser(description='runtest {0} - Numerically tolerant test library.'.format(_version))

    parser.add_option('--binary-dir',
                      '-b',
                      action='store',
                      default=caller_dir,
                      help='directory containing the binary/launcher [default: %default]')
    parser.add_option('--work-dir',
                      '-w',
                      action='store',
                      default=caller_dir,
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

    (options, args) = parser.parse_args(args=sys.argv[1:])

    return options

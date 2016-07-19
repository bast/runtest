def parse_args(input_dir, argv):

    from optparse import OptionParser
    from runtest import __version__

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

    return options

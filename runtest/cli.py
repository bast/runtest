def parse_args(input_dir, argv):

    from optparse import OptionParser
    from runtest import __version__

    parser = OptionParser(description='runtest {0} - Numerically tolerant test library.'.format(__version__))

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

    (options, args) = parser.parse_args(args=argv[1:])

    return options


def test_parse_args():

    input_dir = '/raboof/mytest'
    argv = ['./test', '-b', '/raboof/build/']

    options = parse_args(input_dir, argv)
    assert options == {'verbose': False, 'work_dir': '/raboof/mytest', 'binary_dir': '/raboof/build/', 'skip_run': False, 'debug': False}

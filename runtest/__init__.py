from .ugly import get_filter, execute, copy_and_chdir, check, run
from .cli import cli
from .exceptions import FilterKeywordError, TestFailedError, BadFilterError

__author__ = ('Radovan Bast <radovan.bast@uit.no>')

__version__ = '2.0.0-alpha-x'

__all__ = [
    'get_filter',
    'check',
    'execute',
    'cli',
    'run',
]

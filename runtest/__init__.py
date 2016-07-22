from .filter_constructor import get_filter
from .ugly import run
from .version import version_info, version
from .cli import cli

__author__ = ('Radovan Bast <radovan.bast@uit.no>')

__version__ = version

__all__ = [
    'get_filter',
    'version_info',
    'run',
    'cli',
]

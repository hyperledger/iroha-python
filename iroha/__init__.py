import sys

if sys.version_info[0] < 3:
    raise Exception(
    	'Python 3 or a more recent version is required. Python 2 is not supported.')

from .iroha import *
name = 'iroha'

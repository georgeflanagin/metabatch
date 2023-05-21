# -*- coding: utf-8 -*-
import typing
from   typing import *

min_py = (3, 8)

###
# Standard imports, starting with os and sys
###
import os
import sys
if sys.version_info < min_py:
    print(f"This program requires Python {min_py[0]}.{min_py[1]}, or higher.")
    sys.exit(os.EX_SOFTWARE)

###
# Other standard distro imports
###
import argparse
import contextlib
import getpass
import logging
import signal
mynetid = getpass.getuser()

###
# From hpclib
###
import linuxutils
from   urdecorators import trap

###
# imports and objects that are a part of this project
###
verbose = False
myargs = None

###
# Credits
###
__author__ = 'Alina Enikeeva' 
__copyright__ = 'Copyright 2023'
__credits__ = None
__version__ = 0.1
__maintainer__ = 'Alina Enikeeva' 
__email__ = ['alina@richmond.edu']
__status__ = 'in progress'
__license__ = 'MIT'

@trap
def handler(signum:int, stack:object=None) -> None:
    """
    Universal signal handler.
    """
    global myargs
    handler_logger = logging.getLogger('metabatch').getChild('handler')
    handler_logger.setLevel(myargs.verbose)

    if signum in tuple([signal.SIGHUP, signal.SIGUSR1]):
        handler_logger.debug('Rereading all configuration files.')
        metabatch_main(myargs)

    elif signum in tuple([signal.SIGUSR2, signal.SIGQUIT, signal.SIGTERM, signal.SIGINT]):
        handler_logger.debug('Closing up.')
        uu.fclose_all()
        sys.exit(os.EX_OK)

    else:
        handler_logger.debug(
            f"ignoring signal {signum}. Check list of handled signals."
            )


@trap
def handler_main(myargs:argparse.Namespace) -> int:
    handler(myargs)
    return os.EX_OK


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog="handler", 
        description="What handler does, handler does best.")

    parser.add_argument('-i', '--input', type=str, default="",
        help="Input file name.")
    parser.add_argument('-o', '--output', type=str, default="",
        help="Output file name")
    parser.add_argument('-v', '--verbose', action='store_true',
        help="Be chatty about what is taking place")


    myargs = parser.parse_args()
    verbose = myargs.verbose

    try:
        outfile = sys.stdout if not myargs.output else open(myargs.output, 'w')
        with contextlib.redirect_stdout(outfile):
            sys.exit(globals()[f"{os.path.basename(__file__)[:-3]}_main"](myargs))

    except Exception as e:
        print(f"Escaped or re-raised exception: {e}")


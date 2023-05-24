# -*- coding: utf-8 -*-
import typing
from   typing import *

min_py = (3, 9)

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
mynetid = getpass.getuser()

###
# Installed libraries.
###


###
# From hpclib
###
import linuxutils
import parsec4
from   parsec4 import *
from   urdecorators import trap

###
# imports and objects that are a part of this project
###


###
# Global objects and initializations
###
verbose = False

###
# Credits
###
__author__ = 'George Flanagin'
__copyright__ = 'Copyright 2023'
__credits__ = None
__version__ = 0.1
__maintainer__ = 'George Flanagin'
__email__ = ['gflanagin@richmond.edu']
__status__ = 'in progress'
__license__ = 'MIT'

SBATCH = lexeme(regex('^#SBATCH'))
dash = string('--')
SLURM_PARAM = lexeme(regex('[a-z][a-z-]+'))
OPT = dash >> SLURM_PARAM
eq = lexeme(string(EQ))

@generate
def array():
    yield lbrack
    elements = yield parsec.sepBy(value, comma)
    yield rbrack
    raise EndOfGenerator(elements)


value = quoted ^ array ^ text_shred

@generator
def sbatch_line(s:str):
    
    yield SBATCH
    k = yield OPT
    yield eq
    v = yield value
    raise EndOfGenerator((k, v)) 



@trap
def slurmparse_main(myargs:argparse.Namespace) -> int:
    return os.EX_OK


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog="slurmparse", 
        description="What slurmparse does, slurmparse does best.")

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


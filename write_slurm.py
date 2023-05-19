# -*- coding: utf-8 -*-
import typing
from   typing import *

min_py = (3, 9)

###
# Standard imports, starting with os and sys
###
import os
import sys
if sys.version_info == min_py:
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
# From hpclib
###
import linuxutils
from   urdecorators import trap

###
# imports and objects that are a part of this project
###
from parse_slurm import parse_slurm_file 
verbose = False

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
def write_slurm_to_file(filename, slurm_dct: dict) -> None:
    """
    Rewrites the slurm file based on a dictionary.
    """
    with open(filename, "w") as slurm_mod_file:
        for key, val in slurm_dct.items():
            slurm_mod_file.write(val)    
    return 


@trap
def write_slurm_main(myargs:argparse.Namespace) -> int:
    try:
        slurm_dct = parse_slurm_file(myargs.input)
        write_slurm_to_file(myargs.input, slurm_dct)
    except:
        pass 
    return os.EX_OK


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog="write_slurm", 
        description="What write_slurm does, write_slurm does best.")

    parser.add_argument('-i', '--input', type=str, default="",
        help="Input file name that contains SLURM job.")
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

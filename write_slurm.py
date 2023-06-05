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
from datetime import datetime
import getpass
import time
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
from modify_slurm import modify_slurm_file
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
def write_slurm_to_file(filename: str, slurm_dct_mod: dict) -> None:
    """
    Rewrites the slurm file based on a dictionary.
    """
    with open(filename, "w") as slurm_mod_file:
        for key, val in slurm_dct_mod.items():
            slurm_mod_file.write(val)    
        slurm_mod_file.write(f"\n#modified by metabatch on {datetime.now()}")
        #last_updated_metabatch = time.ctime(os.path.getctime('metabatch.py'))
        slurm_mod_file.write(f"\n#metabatch version {time.ctime(os.path.getctime('metabatch.py'))}")
    return slurm_mod_file 


@trap
def write_slurm_main(myargs:argparse.Namespace) -> int:
    try:
        slurm_dct = modify_slurm_file(myargs.input)
        write_slurm_to_file(myargs.input, slurm_dct)
    except Exception as e:
        print(e)
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


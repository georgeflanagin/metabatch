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
import regex as re
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

read_file_dct = {}

@trap
def parse_slurm_file(slurm_file:str) -> object:
    """
    Parses the slurm file, indentifies SLURM parameters.
    """
    with open(slurm_file, 'r') as read_file:
        contents = read_file.readlines()
        regex_comment_line = re.compile(r'^#(?!SBATCH|\!\/bin\/bash)[a-zA-Z\s]+')        

        # create a dictionary { (# line, type of line) : (line) }
        for line_number, line in enumerate(contents):
            comment_line = re.match(regex_comment_line, line)
            sbatch_line = line.startswith("#SBATCH")
            blank_line = line.startswith("\n")
            
            if comment_line:
                read_file_dct[(line_number, "comment")] = line
            elif sbatch_line:
                read_file_dct[(line_number, "sbatch")] = line
            elif blank_line:
                read_file_dct[(line_number, "blank")] = line
            else:
                read_file_dct[(line_number, "shell")] = line

    return read_file_dct 

@trap
def parse_slurm_main(myargs:argparse.Namespace) -> int:
    #parse_slurm_file(myargs.input)
    return os.EX_OK


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog="parse_slurm", 
        description="What parse_slurm does, parse_slurm does best.")

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


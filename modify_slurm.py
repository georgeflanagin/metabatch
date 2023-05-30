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
from parse_config import parse_config_file
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

progs = {'gaussian': '$GAUSS',
        'qchem': 'qchem',
        'QuantumeExpresso': 'QEPATH',
        'amber': '$AMBER'}

@trap
def xform_blank(s:str) -> str:
    """
    Modifies blank lines.
    """

    return s

@trap
def xform_comment(s:str) -> str:
    """
    Modifies comment lines.
    """
    s = "???????" + s 
    return s


@trap 
def xform_shell(s:str) -> str:
    """
    Modifies shell lines.
    """

    return s

@trap
def xform_sbatch(s:str) -> str:
    """
    Modifies SBATCH lines.
    """

    return s

@trap
def modify_slurm_file(file: object) -> dict:
    """
    Rewrite slurm file based on the business rules and program configurations.
    """
    slurm_dct = parse_slurm_file(file)
    #config = parse_config_file(myargs.config_dir)

    slurm_dct_mod = slurm_dct #that will have to be replaced
    

    # identidy the type of program that the file runs
    prog_run = "" 
    for line in slurm_dct.values():
        for prog, key_word in progs.items():
            if key_word in line:
                prog_run = prog
                break 

    
    # call the functions to modify the lines based on their types
    for k, line in slurm_dct.items():
        print(globals()["xform_"+k[1]](line))
        

    return slurm_dct_mod


@trap
def modify_slurm_main(myargs:argparse.Namespace) -> int:
    modify_slurm_file(myargs.input)
    #print(modify_slurm_file(myargs.input))
    return os.EX_OK


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog="modify_slurm", 
        description="What modify_slurm does, modify_slurm does best.")
    
    parser.add_argument('-c', '--config-dir', type=str, default="/etc/metabatch.d",
        help="Input directory with configuration files.")
    parser.add_argument('-i', '--input', type=str, default="",
        help="Input file name that contains SLURM job.")
    parser.add_argument('-o', '--output', type=str, default="",
        help="Output file name")
    parser.add_argument('-v', '--verbose', type=str, 
        choices=('CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'),
        default='ERROR',
        help="Be chatty or not at the corresponding log level.")




    myargs = parser.parse_args()
    verbose = myargs.verbose

    try:
        outfile = sys.stdout if not myargs.output else open(myargs.output, 'w')
        with contextlib.redirect_stdout(outfile):
            sys.exit(globals()[f"{os.path.basename(__file__)[:-3]}_main"](myargs))

    except Exception as e:
        print(f"Escaped or re-raised exception: {e}")


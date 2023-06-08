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
import random
import string
import tempfile
mynetid = getpass.getuser()

###
# From hpclib
###
from dorunrun import dorunrun
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
def create_mod_file(netid: str, ourtempfile:str, newfile:str) -> None:
    """
    Copy the contents of a tempfile to the new file, so that the user owns it. 
    """
    return dorunrun(f"sudo -u {netid} cp {ourtempfile} {newfile}")

@trap
def write_slurm_to_file(netid: str, filename: str, slurm_dct_mod: dict) -> None:



    #create a temp file and name it with a random prefix
    random_str = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=4)) #random string for the modified file name
    temp = tempfile.NamedTemporaryFile(mode = "w+", suffix = "_"+filename, dir = "/usr/local/sw/metabatch", delete = False)
    print(temp.name)
    for key, val in slurm_dct_mod.items():
        temp.write(f"{val}")
    dorunrun(f"chmod 644 {temp}")
    dorunrun(f"sudo -u {netid} cp {temp} {'/usr/local/sw/metabatch/filename'}")
    temp.close()
    '''
    # write modified contents to the temporary file
    with open(temp.name, "w") as slurm_mod_file:
        for key, val in slurm_dct_mod.items():
            slurm_mod_file.write(val)    
    print(slurm_mod_file)
    '''
    # copy the contents of the temporary file to the newfile, owned by the submitter of the original file
    new_mod_file = create_mod_file(netid, temp, temp.name) # let the new file have the same name as the temporary one
    return new_mod_file 

'''
@trap
def write_slurm_to_file(filename: str, slurm_dct_mod: dict) -> None:
    """
    Rewrites the slurm file based on a dictionary.
    """
    random_str = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=4)) #random string for the modified file name
    with open(filename+random_str, "w") as slurm_mod_file:
        for key, val in slurm_dct_mod.items():
            slurm_mod_file.write(val)    

    return slurm_mod_file 
'''

@trap
def write_slurm_main(myargs:argparse.Namespace) -> int:

    try:
        slurm_dct = modify_slurm_file(myargs.input)
        write_slurm_to_file("ae9qg", myargs.input, slurm_dct)
        print(write_slurm_to_file("ae9qg", myargs.input, slurm_dct))

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


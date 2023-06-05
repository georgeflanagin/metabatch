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
from dorunrun import dorunrun
import fifo
import linuxutils
from   urdecorators import trap

###
# imports and objects that are a part of this project
###
from parse_slurm import parse_slurm_file
from modify_slurm import modify_slurm_file
from write_slurm import write_slurm_to_file
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
def read_pipe(pipe: str) -> None:
    """
    Reads from a file pipe, modifies it and submits the new file to SLURM.
    """
    # read the file once it is submitted to pipe
    p = fifo.FIFO(pipe)

    while True:
        sys.stderr.write("Pipe is open.\n")
        data = p.wait_for_data(60*60*24*7)
        #breakpoint()
        print("dd",data)
        sys.stderr.write(f"{data}")        

        # identify the file and who submitted it
        try:
            netid, data_file = data[0].split(',')
            data_file = data_file.strip()
            print(data_file)
        except Exception as e:
            print(f"Bad message format. Got >>{data[0]}<<")
            continue
        
        # read the slurm file and modify it
        try:
            print("ddd")
            data_mod = modify_slurm_file(data_file) 
            mod_file = write_slurm_to_file(data_file, data_mod)
            # submit the job to SLURM
            print('''dorunrun(f"sudo -u {netid} command sbatch {mod_file}")''')

        except Exception as e:
            print("fff")
            print(f"Exception: {e}")
            print('''dorunrun(f"sudo -u {netid} command sbatch {data_file}")''')
            continue

        
    

@trap
def read_pipe_main(myargs:argparse.Namespace) -> int:
    #read_pipe(myargs.input)    

    return os.EX_OK


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog="read_pipe", 
        description="What read_pipe does, read_pipe does best.")

    parser.add_argument('-i', '--input', type=str, default="metapipe",
        help="Input the name of the pipe.")
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


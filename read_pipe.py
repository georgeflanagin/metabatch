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
def submit_file_to_slurm(filename: str, netid: str) ->  None:
    """
    Submits the modified file to SLURM on behalf of the user.
    This will allow the user (aka orginal author of the file) have all the permissions 
    to the modofied file.
    """
    return dorunrun(f"sudo -u {netid} command sbatch {filename}")

@trap
def read_pipe(pipe: str) -> None:
    """
    Reads from a file pipe, modifies it and submits the new file to SLURM.
    """
    # read the file once it is submitted to pipe

    while True:
        p = fifo.FIFO(pipe, "non_block", reopen = True)
        sys.stderr.write(f"{p=}")

        sys.stderr.write("Pipe is open.\n")
        data = p(60*60*24*7)
        del p

        #breakpoint()
        sys.stderr.write(f"pipe returned {data=}\n")        
        #breakpoint()
        # identify the file and who submitted it
        try:
            netid, data_file = data[0].split(',')
            data_file = data_file.strip()
            #print(data_file)
        except Exception as e:
            sys.stderr.write(f"Bad message format. Got >>{data}<<\n")
            continue
       
        if os.getppid == 1: continue #parent process

        try:
            pid = os.fork()
            if pid: 
                print(pid, "this is parent")
                continue # then it is a parent process, and we want to exit, reopen pipe and read again.

            else: #it is a child process
                print(pid, "this is child")
                data_mod = modify_slurm_file(data_file) 
                mod_file = write_slurm_to_file(netid, data_file, data_mod)
                
                # submit the job to SLURM
                submit_file_to_slurm(mod_file, netid)
                print('''dorunrun(f"sudo -u {netid} command sbatch {mod_file}")''')
        
        except Exception as e:
            print(f"Exception: {e}")
            #modification didn't happen so submit the original file
            submit_file_to_slurm(data_file, netid)
            print('''dorunrun(f"sudo -u {netid} command sbatch {data_file}")''')
            continue


        finally: #make sure the child process is killed after execution
            os._exit(os.EX_OK)
        continue 



        """ 
        # read the slurm file and modify it
        try:
            
            data_mod = modify_slurm_file(data_file) 
            mod_file = write_slurm_to_file(netid, data_file, data_mod)
            # submit the job to SLURM
            submit_file_to_slurm(mod_file, netid)
            #print(netid,  mod_file)
            #dorunrun(f"sudo -u {netid} command sbatch {mod_file}")
            print('''dorunrun(f"sudo -u {netid} command sbatch {mod_file}")''')

        except Exception as e:
            print(f"Exception: {e}")
            #modification didn't happen so submit the original file
            submit_file_to_slurm(data_file, netid)
            print('''dorunrun(f"sudo -u {netid} command sbatch {data_file}")''')
            continue

        """ 
    

@trap
def read_pipe_main(myargs:argparse.Namespace) -> int:
    read_pipe(os.path.join(os.environ.get('METABATCHPATH'), 'metapipe'))    

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


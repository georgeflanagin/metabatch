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
from datetime import datetime
import getpass
import math
import re
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
from parse_config import parse_config_file
from fit_the_job import fit_the_job
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
        'quantumexpresso': '$QEPATH',
        'amber': '$AMBER',
        'unknown': 'unknown',
        'zcat': 'zcat'}

@trap
def convert_to_megabytes(mem: int) -> int:
    """
    Converts different memory to megabytes.
    """
    pattern = re.compile(r"(\d+)(?=(?:\/\d+)*\s*([MGKTmgkt]*[bB]*))")
    mem_regex = re.findall(pattern, mem)

    mem_val = int(mem_regex[0][0])

    # the memory requested 
    try:
        mem_unit = mem_regex[0][1].upper()
        #print(mem_unit) 
    except:
        #the memory is passed without specified unit, so we assume the number is in MB
        mem_unit = "MB"
        
    if mem_unit.startswith("K"): # "KB"
        mem_val = math.ceil(mem_val*0.001)
    elif mem_unit.startswith("M"): # "MB"
        mem_val = mem_val
    elif mem_unit.startswith("G"): # "GB"
        mem_val *= 1000
    elif mem_unit.startswith("T"): # "TB"
        mem_val *= 1000000 
    else:
        mem_val = mem_val 
    return mem_val


@trap
def xform_blank(s:str, limits: list) -> str:
    """
    Modifies blank lines.
    """

    return s

@trap
def xform_comment(s:str, limits: list) -> str:
    """
    Modifies comment lines.
    """
    s = s 
    return s


@trap 
def xform_shell(s:str, limits: list) -> str:
    """
    Modifies shell lines.
    """

    return s

@trap
def xform_sbatch(s:str, limits: list) -> str:
    """
    Modifies SBATCH lines.
    """
    mem_val = 0
    cpu_requested = 0    
    partition_requested = ""


    # changes to CPU
    cpu = re.compile(r"#SBATCH --cpus-per-task=.*")    
    is_cpu_line = re.match(cpu, s)

    
    if is_cpu_line != None:
        cpu_requested = is_cpu_line.group(0).split("=")[1] 
        #if needed, adjust CPU
        if int(cpu_requested) >= int(limits["cpu"]):
            s = "".join((is_cpu_line.group(0).split("=")[0],"=", limits["cpu"], '\n'))
            
     
    # changes to memory
    mem = re.compile(r"#SBATCH --mem=.*") 
    is_mem_line = re.match(mem, s)
    
    pattern = re.compile(r"(\d+)(?=(?:\/\d+)*\s*([MGKTmgkt]*[bB]*))")
    mem_regex = re.findall(pattern, s)
    
    # modify the Sbatch --mem line only
    if is_mem_line != None:
        mem_val = convert_to_megabytes(is_mem_line.group())
        
        #if needed, adjust memory
        if int(mem_val) >= int(limits["memory"]):
            s = "".join(("#SBATCH --mem=", limits["memory"], "\n")) # limits["memory"]) 

    
    # changes to partition and nodelist 
    partition = re.compile(r"#SBATCH --partition=.*")
    is_partition_line = re.match(partition, s)

    nodelist = re.compile(r"#SBATCH --nodelist=.*")
    is_nodelist_line = re.match(nodelist, s)
    
    if is_partition_line != None:
        partition_requested = is_partition_line.group().split('=')[1]
        optimal_node, optimal_partition = fit_the_job(partition_requested, mem_val, cpu_requested) 
        print(optimal_node, optimal_partition)
        s = "".join(("#SBATCH --partition=", optimal_partition, "\n", 
                        "#SBATCH --nodelist=", optimal_node, "\n"))

 
    return s

@trap
def modify_slurm_file(file: object) -> dict:
    """
    Rewrite slurm file based on the business rules and program configurations.
    """
    global myargs

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
            #else:
            #    prog_run = 'unknown'
    if prog_run == "":
        prog_run = "unknown"

    limits = []
    
    # retrieves config information based on the program that the job is executing
    #dir_path = myargs.config_dir+"/config.d/"
    dir_path = os.getcwd()+"/metabatch.d/config.d/" 
    config = parse_config_file(dir_path)
    config_for_prog = {k: v["resource_limits"] for k, v in config.items() if k == dir_path+prog_run+".conf"}
    limits = config_for_prog[dir_path+prog_run+".conf"]
    

    # call the functions to modify the lines based on their types
    for k, line in slurm_dct.items():
        s = globals()["xform_"+k[1]](line, limits)
        slurm_dct_mod[k] = s

    # add lines that signify modification by metabatch in the end of the file
    slurm_dct_mod[(len(slurm_dct)+1, "comment")] = f"\n#modified by metabatch on {datetime.now()}"
    slurm_dct_mod[(len(slurm_dct)+2, "comment")] =f"\n#metabatch version {time.ctime(os.path.getctime('metabatch.py'))}" 

    # return {k: globals()[f'xform_{k[1]}'](line) for k, line in slurm_dct.items() }
    return slurm_dct_mod


@trap
def modify_slurm_main(myargs:argparse.Namespace) -> int:
    #print(convert_to_megabytes('10Gb'))
    #print(convert_to_megabytes('100mb'))
    #print(convert_to_megabytes('10KB'))
    #print(convert_to_megabytes('10G'))
    #print(convert_to_megabytes('3000g'))
    
   


    modify_slurm_file(myargs.input)
    print(modify_slurm_file(myargs.input))
    return os.EX_OK


if __name__ == '__main__':
    myenviron = os.environ.get("METABATCHPATH")   
 
    parser = argparse.ArgumentParser(prog="modify_slurm", 
        description="What modify_slurm does, modify_slurm does best.")
    
    parser.add_argument('-c', '--config-dir', type=str, default="/usr/local/sw/metabatch/metabatch.d",
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


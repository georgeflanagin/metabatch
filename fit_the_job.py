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
import linuxutils
from   urdecorators import trap
from   sloppytree import SloppyTree
###
# imports and objects that are a part of this project
###
from mapper import SeekINFO
verbose = False

###
# Credits
###
__author__ = 'George Flanagin'
__copyright__ = 'Copyright 2022, University of Richmond'
__credits__ = None
__version__ = 0.1
__maintainer__ = 'George Flanagin'
__email__ = 'gflanagin@richmond.edu'
__status__ = 'in progress'
__license__ = 'MIT'

medium_condos = ['spdr09', 'spdr10', 'spdr11', 'spdr12', 'spdr13', 'spdr53', 'spdr55', 'spdr56', 'spdr57', 'spdr58'] 
large_condos = ['spdr14', 'spdr15', 'spdr51', 'spdr52', 'spdr59']

@trap
def find_busiest_node(node_usage) -> str:
    """
    Returns the busiest node 
    """
    busiest_node = max(node_usage.values())
    
    busiest = [k for k,v in node_usage.items() if int(v) == busiest_node]

    return busiest[0]

@trap
def fit_to_memory(requested_mem: int, node_usage: dict) -> None:
    """
    Finds the node that can fit the job memory-wise.
    """
    found_fit = False

    for i in range(len(node_usage)):
    
        if found_fit:
            return busiest_node

        for node, mem_cpu in node_usage.items():
            busiest_node = find_busiest_node(node_usage)        
            
            busiest_node_mem = node_usage.get(busiest_node)
            if busiest_node in medium_condos:
                total_mem = 768000
            elif busiest_node in large_condos:
                total_mem = 1536000
            else:
                total_mem = 384000

            busiest_node_free_mem = int(total_mem) - busiest_node_mem
            if requested_mem <= busiest_node_free_mem: 
                found_fit = True
                break    
            else: #look for another node
                node_usage[busiest_node] = 0 
            
    return None



@trap
def fit_to_cpu(requested_cpu: int, cpu_usage: dict, mem_fit_node: str) -> None:
    """
    Finds the node that can fit the job cpu-wise.
    """
    cpu = cpu_usage[mem_fit_node] 
    if requested_cpu <= cpu: 
        return True
    return False     


@trap
def fit_the_job(requested_mem: int, requested_cpu: int) -> str:
    """
    Finds the busiest node where the job can fit.
    """
    node_usage = {} #usage of memory
    cpu_usage = {} #usage of cpu
    data = SeekINFO()

    for line in ( _ for _ in data.stdout.split('\n')[1:] if _ ):
        node, free, total, status, true_cores, cores = line.split()
        cores = cores.split('/')
        used = int(total) - int(free)
        node_usage[node] = int(used) #usage of memory
        cpu_usage[node] = 52 - int(cores[0]) #find out how many CPUs are available

    # sorted dictionary results in the list of tuples
    node_usage = sorted( ((v, k) for k, v in node_usage.items()), reverse=True)
    # convert the list of tuples into a dictionary
    node_usage = dict( (k,v) for v, k in node_usage)
   
    complete_fit_node = False
 
    for i in range(len(node_usage)):    
        mem_fit_node = fit_to_memory(requested_mem, node_usage)
    
        if mem_fit_node != None: 
            complete_fit_node = fit_to_cpu(requested_cpu, cpu_usage, mem_fit_node)

        if complete_fit_node == True:
            print(f"job that requested {requested_mem, requested_cpu} is allocated to {mem_fit_node}")
            break
        elif mem_fit_node != None:
            del node_usage[mem_fit_node]    
        else:
            print(f"job that requested {requested_mem, requested_cpu} could not be allocated")

    return None 

@trap
def fit_the_job_main(myargs:argparse.Namespace) -> int:
    
    fit_the_job(340000, 150)
    fit_the_job(30000000, 12)
    fit_the_job(240000, 20)
    fit_the_job(20000, 6)
    fit_the_job(600000, 24)
    
    return os.EX_OK


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog="fit_the_job", 
        description="What fit_the_job does, fit_the_job does best.")

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


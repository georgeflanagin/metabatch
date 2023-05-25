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

@trap
def find_busiest_node(node_usage) -> str:
    """
    Returns the busiest node 
    """
    busiest_node = max(node_usage.values())
    
    busiest = [k for k,v in node_usage.items() if int(v) == busiest_node]

    return busiest[0]

@trap
def fit_the_job(requested_mem: int, requested_cpu: int) -> str:
    """
    Finds the busiest node where the job can fit.
    """
    medium_condos = ['spdr09', 'spdr10', 'spdr11', 'spdr12', 'spdr13', 'spdr53', 'spdr55', 'spdr56', 'spdr57', 'spdr58'] 
    large_condos = ['spdr14', 'spdr15', 'spdr51', 'spdr52', 'spdr59']
    found_fit = False
    found_cpu_fit = False
    node_usage = {} #usage of memory
    cpu_usage = {} #usage of cpu
    data = SeekINFO()

    for line in ( _ for _ in data.stdout.split('\n')[1:] if _ ):
        node, free, total, status, true_cores, cores = line.split()
        cores = cores.split('/')
        used = int(total) - int(free)
        #node_usage[node] = int(used), int(cores[0])
        node_usage[node] = int(used) #usage of memory
        cpu_usage[node] = 52 - int(cores[0]) #find out how many CPUs are available

    # sorted dictionary results in the list of tuples
    node_usage = sorted( ((v, k) for k, v in node_usage.items()), reverse=True)
    # convert the list of tuples into a dictionary
    node_usage = dict( (k,v) for v, k in node_usage)
    

    for i in range(len(node_usage)):
    
        ### if we found the memory-wise fit, look for the CPU fit
        if found_fit == True:
            cpu = cpu_usage[busiest_node] 
            if requested_cpu <= cpu: 
                found_cpu_fit = True
        else:   
            found_fit = False
    
        if found_fit and found_cpu_fit:
            print(f"job is allocated to {busiest_node}")
            print(f"job requested {requested_mem, requested_cpu} to the node with {busiest_node_free_mem, cpu_usage[busiest_node]}")
            break

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
            #print("requested: ", requested_mem)
            #print("busiest node used mem: ", busiest_node_mem)
            #print("total: ", total_mem)
            #print("busiest node available mem: ", busiest_node_free_mem)
            if requested_mem <= busiest_node_free_mem: 
                found_fit = True
                break    
            else: #look for another node
                node_usage[busiest_node] = 0 
            
        


    
    #### this is to find what partition requested and what nodes to explore. not working for now
    """
    ### find info about partition
    cmd = 'sinfo -o "%n %P"'
    d = SloppyTree(dorunrun(cmd, return_datatype=dict))
    print(d) 
    for line in ( _ for _ in d.stdout.split('\n')[1:] if _ ):
        n, partition = line.split()
        
    if node == n and n in 
    """

    return node

@trap
def fit_the_job_main(myargs:argparse.Namespace) -> int:
    
    fit_the_job(340000, 17)
    fit_the_job(300000, 12)
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


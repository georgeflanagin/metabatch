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
__author__ = 'Alina Enikeeva'
__copyright__ = 'Copyright 2023, University of Richmond'
__credits__ = None
__version__ = 0.1
__maintainer__ = 'Alina Enikeeva'
__email__ = 'alina.enikeeva@richmond.edu'
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
    node_usage = {}
    data = SeekINFO()
    for line in ( _ for _ in data.stdout.split('\n')[1:] if _ ):
        node, free, total, status, true_cores, cores = line.split()
        cores = cores.split('/')
        used = int(total) - int(free)
        #node_usage[node] = [int(used), int(cores[0])]
        node_usage[node] = int(used)
    #node_usage = sorted(node_usage.items(), reverse=True)

    # node_usage = sorted( ((v, k) for k, v in node_usage.items()), reverse=True)
    print(node_usage)
    


    for i in range(len(node_usage)):
        if found_fit == True:
            print(f"job is allocated to {busiest_node}")
            break

        for node, mem_cpu in node_usage.items():
            busiest_node = find_busiest_node(node_usage)        
            #print(node,mem_cpu)
            #print(busiest_node)     
            #print(requested_mem, node_usage.get(busiest_node))

            #### this is for both memory and cpu. not working for now
            #if requested_mem <= busiest_node[0] and requested_cpu <= int(true_cores)-busiest_node[1]:
            #    print(f"the job is allocated to node {is_busiest}")
            #busiest_node_cpu = node_usage.get(busiest_node[1])
             ####
            
            busiest_node_mem = node_usage.get(busiest_node)
            if busiest_node in medium_condos:
                total_mem = 768000
            elif busiest_node in large_condos:
                total_mem = 1536000
            else:
                total_mem = 384000

            busiest_node_free_mem = int(total_mem) - busiest_node_mem
            print("requested: ", requested_mem)
            print("busiest node used mem: ", busiest_node_mem)
            print("total: ", total_mem)
            print("busiest node available mem: ", busiest_node_free_mem)
            if requested_mem <= busiest_node_free_mem: 
                found_fit = True
                #print(f"job is allocated to {busiest_node}")
                break    
            else:
                #print("looking for another node")
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
    
    fit_the_job(340000, 10)
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


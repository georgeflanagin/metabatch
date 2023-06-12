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
def find_the_node(total_mem:int, partition:list) -> str:
    """
    Finds the fit for the job within the partition specified.
    """
    for i in range(len(node_usage)):
        if found_fit == True:
            print(f"job is allocated to {busiest_node}")
            break

        for node, mem_cpu in node_usage.items():
            busiest_node = find_busiest_node(node_usage)        
            #print(node,mem_cpu)
            #print(busiest_node)     
            #print(requested_mem, node_usage.get(busiest_node))

           
            busiest_node_mem = node_usage.get(busiest_node)
            if busiest_node in medium_partition:
                total_mem = 768000
            elif busiest_node in large_partition:
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
            
     
@trap
def fit_the_job(partition_req: str, requested_mem: int, requested_cpu: int) -> str:
    """
    Finds the busiest node where the job can fit.
    """
    basic_partition = ['spdr01', 'spdr02', 'spdr03', 'spdr04', 'spdr05', 'spdr06', 'spdr07', 'spdr08']
    medium_partition = ['spdr09', 'spdr10', 'spdr11', 'spdr12', 'spdr13', 'spdr53', 'spdr55', 'spdr56', 'spdr57', 'spdr58'] 
    large_partition = ['spdr14', 'spdr15', 'spdr51', 'spdr52', 'spdr59']
    erickson_condo = []
    johnson_condo = []
    parish_condo = []    

    found_fit = False
    data = SeekINFO()
    node_usage = SloppyTree()
    

    for line in ( _ for _ in data.stdout.split('\n')[1:] if _ ):
        node, free, total, status, true_cores, cores = line.split()
        cores = cores.split('/')
        used_mem = int(total) - int(free)
        
        # populate sloppy tree with (node: mem, cpu, partition)
        node_usage[node].mem = used_mem # how much memory is being used
        node_usage[node].cpu = int(cores[0]) # how many cpus are being used
        if node in basic_partition:
            node_usage[node].partition = "basic"
        elif node in medium_partition:
            node_usage[node].partition = "medium"
        elif node in large_partition:
            node_usage[node].partition = "large"
        else:
            node_usage[node].partition = partition_req 
    print(node_usage)
    # sort so that the busiest (in terms of memory) node is the first one in the list
    node_usage = sorted( (((v.mem, v.cpu, v.partition), k) for k, v in node_usage.items()), reverse=True)
    print(node_usage)

    basic_partition = []
    for item in node_usage:
        if node_usage.partition == "basic":
            basic_partition.append(item) 

    print(node_usage)

    sys.exit(os.EX_OK)
   
    partition_optimal = ""

    if partition_req == "basic" or partition_optimal == "basic":
        node = find_the_node(384000, basic_partition) #finds the fit within basic partition
        # if there is no fit within the basic partition, look for the fit in the medium partition
        if node == None:
            partition_optimal = "medium"    

    if partition_req == "medium" or partition_optimal == "medium":
        node = find_the_node(768000, medium_partition) 
        if node == None:
            partition_optimal = "large"

    if partition_req == "large" or partition_optimal == "large":
        node = find_the_node(1536000, large_partition)
        if node == None:
            partition_optimal = partition_req #return the partition that was initially requested
    

    ##### put this in a finction called find_the_node
    '''
    for i in range(len(node_usage)):
        if found_fit == True:
            print(f"job is allocated to {busiest_node}")
            break

        for node, mem_cpu in node_usage.items():
            busiest_node = find_busiest_node(node_usage)        
            #print(node,mem_cpu)
            #print(busiest_node)     
            #print(requested_mem, node_usage.get(busiest_node))

           
            busiest_node_mem = node_usage.get(busiest_node)
            if busiest_node in medium_partition:
                total_mem = 768000
            elif busiest_node in large_partition:
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
            
    ''' 

    
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

    return node, partition

@trap
def fit_the_job_main(myargs:argparse.Namespace) -> int:
    
    print(fit_the_job("somecondo", 340000, 10))
    fit_the_job("medium", 300000, 12)
    #fit_the_job(240000, 20)
    #fit_the_job(20000, 6)
    #fit_the_job(600000, 24)
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


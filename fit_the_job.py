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
import configparser
import getpass
import heapdict
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
from newslurmutils import *
verbose = False
myargs = None
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
def partitions_and_nodes() -> dict:
    """
    Read configuration file and populate the dictionary so that the name of 
    the partition is the key and the nodes that belong to this partition are a list 
    of values.
    The form of the dictionary: {partition: [node, ...]}
    """
    global myargs
    parser = configparser.ConfigParser()
    config_info = {}
    path_to_file = myargs.config
    print(path_to_file)
    try:
        parser.read(path_to_file)
    except Exception as e:
        #parse_logger.error("Error parsing config file {path_to_file}")
        print(e)

    #populate the dictionary
    for sect in parser.sections():
        names = []
        values = []
        for name, value in parser.items(sect):
            names.append(name)
            values.append(value)
        config_info[sect] = dict(zip(names, values))
        #print(sect) 
    if not len(config_info):
        #parse_logger.error(f"No config files found in {config_dir}.")
        print("directory is empty")

    return config_info


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
def fit_to_cpu(requested_cpu: int, cpu_usage: dict, mem_fit_node: str) -> bool:
    """
    Finds the node that can fit the job cpu-wise.
    """
    cpu = cpu_usage[mem_fit_node] 
    if requested_cpu <= cpu: 
        return True
    return False     

@trap 
def fit_to_priority(requested_partition: str, prioritized_partitions: dict) -> str:
    """
    Checks the priority of the node found.
    If the node belongs to the prioritized list, the fit is found. 
    """
    

    return None
 

@trap 
def set_priority(user: str, req_partition:str, other_partitions: dict) -> dict:
    """
    Sets priority for the specific user to the partitions.
    
    The highest priority (1) is given to the node of requested partition.
    The second priority (2) is given to the condos (if one belongs to any).
    The last priority (3, 4, 5) is given to community nodes in the order - basic, medium, large.
    """
    
    priorities = heapdict.heapdict() # set lowest number to the highest priority
    priorities["basic"] = 3
    priorities["medium"] = 4
    priorities["large"] = 5

        #example
    # user_netid = "ab9mh"
    # requested_partition = 100
    # check if has access to any special partitions. If so, give the nodes priority = 70
    # basic = 50
    # medium = 30
    # large = 10
    priorities[f"{req_partition}"] = 1
    
    #see if the user is a part of some condo and if so, set priority 2 for this partition
    user_groups = dorunrun(f"groups {user}", return_datatype = str).split(":")[1]
    #print("groups the user belongs to", user_groups.split(":")[1])
    condos = partitions_and_nodes()
    for condo, val in condos.items():
        if condo!= "sizes":
            allowed_users = condos[condo]['allowed_users']
            #print(user_groups, "--",  allowed_users) 
            overlap = set(user_groups.split()).intersection(allowed_users.split())#[value for value in user_groups if value in allowed_users]
            print(overlap)
            if len(overlap) != 0:
                priorities[f"{condo}"] = 2    
    

    return list(priorities.items())

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

    #print(set_priority("gflanagi", "basic", "smth")) 
    print(parse_node_info())
    print(parse_sinfo())
 
    #fit_the_job(340000, 150)
    #fit_the_job(30000000, 12)
    #fit_the_job(240000, 20)
    #fit_the_job(20000, 6)
    #fit_the_job(600000, 24)
    
    return os.EX_OK


if __name__ == '__main__':
    myenviron = os.environ.get("METABATCHPATH") 
    
    parser = argparse.ArgumentParser(prog="fit_the_job", 
        description="What fit_the_job does, fit_the_job does best.")

    parser.add_argument('-i', '--input', type=str, default="",
        help="Input file name.")
    parser.add_argument('-c', '--config', type=str, default=os.path.join(myenviron, 'nodes.conf'),
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


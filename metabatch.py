# -*- coding: utf-8 -*-

###
# Credits
###
__author__ = 'George Flanagin & Alina Enikeeva'
__copyright__ = 'Copyright 2023'
__credits__ = None
__version__ = 0.1
__maintainer__ = 'George Flanagin & Alina Enikeeva'
__email__ = ['hpc@richmond.edu']
__status__ = 'pre-production'
__license__ = 'MIT'

import typing
from   typing import *

min_py = (3, 8)

###
# Standard imports, starting with os and sys. Check compatibility.
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
import configparser
import contextlib
import getpass
import logging
import regex as re
import signal

###
# From hpclib
###
from   dorunrun import dorunrun
import fifo
import fileutils
import linuxutils
import sloppytree
import slurmutils
from   urdecorators import trap

###
# imports and objects that are a part of this project
###

###
# Globals
###
caught_signals = [  
    signal.SIGINT, 
    signal.SIGQUIT, 
    signal.SIGHUP, 
    signal.SIGTERM,
    signal.SIGUSR1, 
    signal.SIGUSR2, 
    signal.SIGRTMIN+1 ]

myargs = None
mynetid = getpass.getuser()
verbose = False

config_info = {}

       

@trap
def parse_config(config_dir: str) -> dict:
    """
    Parses configuration directory and its files. Returns a nested dictionary with the contents of configuration files.
    """
    global config_info

    parse_logger =  logging.getLogger('metabatch').getChild('parse_config')
    parse_logger.setLevel(myargs.verbose)

    if not os.path.exists(config_dir):
        parse_logger.error(f"Directory {myargs.config_dir} is not found")
        sys.exit(os.EX_CONFIG)        

    if len(os.listdir(config_dir)) == 0:
        parse_logger.debug("Directory is empty. No configuration files were found")
        sys.exit(os.EX_CONFIG)    
 

    #get the contents of the directory with config information
    config_items = os.listdir(config_dir)
 
    for item in config_items:

        parse_logger.info("Reading configuration files")
        path_to_item = config_dir+'/'+item
        
        #loop over files in subdirectory
        if os.path.isdir(path_to_item):
            for filename in os.listdir(path_to_item):
                path_to_file = path_to_item+'/'+filename               
                #create configparser object
                parser = configparser.ConfigParser()
                parser.read(path_to_file)
                
                #populate the dictionary
                config_info[path_to_file]={}
                for sect in parser.sections():
                    names = []
                    values = []
                    for name, value in parser.items(sect):
                        names.append(name)
                        values.append(value)
                    config_info[path_to_file][sect] = dict(zip(names, values))
 
        #loop over files in the directory
        elif os.path.isfile(path_to_item):
            
            #create config parser object
            parser = configparser.ConfigParser()
            parser.read(path_to_item)
            
            #populate the dictionary
            config_info[path_to_item]={}
            for sect in parser.sections():
                names = []
                values = []
                for name, value in parser.items(sect):
                    names.append(name)
                    values.append(value)
                config_info[path_to_item][sect] = dict(zip(names, values)) 
                       
    return config_info
 
@trap
def handler(signum:int, stack:object=None) -> None:
    """
    Universal signal handler.
    """
    global myargs
    handler_logger = logging.getLogger('metabatch').getChild('handler')
    handler_logger.setLevel(myargs.verbose)

    if signum in tuple(signal.SIGHUP, signal.SIGUSR1):
        handler_logger.debug('Rereading all configuration files.')
        metabatch_main(myargs)

    elif signum in tuple(signal.SIGUSR2, signal.SIGQUIT, signal.SIGTERM, signal.SIGINT):
        handler_logger.debug('Closing up.')
        uu.fclose_all()
        sys.exit(os.EX_OK)

    else:
        handler_logger.debug(
            f"ignoring signal {signum}. Check list of handled signals."
            )


@trap
def metabatch_events(submissions:fifo.FIFO) -> int:
    """
    This is the event loop. We read from the FIFO, examine
    the input, and pass it along to sbatch.
    """
    global myargs

    found_stop_event = False
    event_logger = logging.getLogger('metabatch').getChild('events')
    event_logger.setLevel(myargs.verbose)

    while not found_stop_event:
        # Wait a day for someone to submit .. something.
        jobs = submissions(60*60*24) 
        event_logger.debug(jobs)
        
    return os.EX_OK


@trap
def metabatch_main(myargs:argparse.Namespace) -> int:
    """
    Do a little setup, and then start the program as a daemon.
    """
    global config_info 

    mylogger = logging.getLogger('metabatch')
    mylogger.setLevel(myargs.verbose)

    config = sloppytree.SloppyDict()
    p = configparser.ConfigParser()

    #for filename in fileutils.all_files_in(myargs.config_dir):
        #config.update(p.read(filename))

    # traverse all the files and directories in config_dir and, if not empty, read them
    config_info = parse_config(myargs.config_dir)
    print(config_info)  

    # parse slurm parameters in the submitted file
    params = parse_slurm_file('anagrammar.slurm')
    print(params)
    
 
    #submissions = fifo.FIFO(myargs.fifo)

    #not myargs.debug and linuxutils.daemonize_me()
    
    #return metabatch_events(submissions)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog="metabatch", 
        description="What metabatch does, metabatch does best.")

    parser.add_argument('-c', '--config-dir', type=str, default="/etc/metabatch.d",
        help="Input file name.")
    parser.add_argument('-d', '--debug', action='store_true', 
        help="Run program interactively for debugging purposes.")
    parser.add_argument('-f', '--fifo', type=str, default="/usr/local/metabatch/queue",
        help="Name of the FIFO where SLURM jobs are submitted.")
    parser.add_argument('-o', '--output', type=str, default="",
        help="Name of the output (logging) file.")
    parser.add_argument('-v', '--verbose', type=str, 
        choices=('CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'),
        default='ERROR',
        help="Be chatty or not at the corresponding log level.")


    myargs = parser.parse_args()
    verbose = myargs.verbose

    ###
    # If we are running the program from the command line, then it
    # is useful to have ctrl-C interrupt the program. Same if we
    # logoff.
    ###
    if myargs.debug:
        caught_signals.remove(signal.SIGINT)
        caught_signals.remove(signal.SIGHUP)

    for _ in caught_signals:
        try:
            signal.signal(_, handler)
        except OSError as e:
            sys.stderr.write(f'cannot reassign signal {_}\n')
        else:
            sys.stderr.write(f'signal {_} is being handled.\n')
    
    try:
        outfile = sys.stdout if not myargs.output else open(myargs.output, 'w')
        with contextlib.redirect_stderr(outfile):
            sys.exit(globals()[f"{os.path.basename(__file__)[:-3]}_main"](myargs))

    except Exception as e:
        print(f"Escaped or re-raised exception: {e}")


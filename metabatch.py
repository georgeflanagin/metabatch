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

min_py = (3, 9)

###
# Standard imports, starting with os and sys. Check compatibility.
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
from parse_slurm import parse_slurm_file
from parse_config import parse_config_file
from read_pipe import read_pipe
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
mypwd = os.getcwd()

@trap
def handler(signum:int, stack:object=None) -> None:
    """
    Universal signal handler.
    """
    global myargs
    handler_logger = logging.getLogger('metabatch').getChild('handler')
    handler_logger.setLevel(myargs.verbose)

    if signum in tuple((signal.SIGHUP, signal.SIGUSR1)):
        handler_logger.debug('Rereading all configuration files.')
        metabatch_main(myargs)

    elif signum in {signal.SIGUSR2, signal.SIGQUIT, signal.SIGTERM, signal.SIGINT}:
        handler_logger.debug('Closing up.')
        fileutils.fclose_all()
        sys.exit(os.EX_OK)

    else:
        handler_logger.debug(
            f"ignoring signal {signum}. Check list of handled signals."
            )


@trap
def metabatch_main(myargs:argparse.Namespace) -> int:
    """
    Do a little setup, and then start the program as a daemon.
    """
    global config_info 

    mylogger = logging.getLogger('metabatch')
    mylogger.setLevel(myargs.verbose)
    #breakpoint()
    config = sloppytree.SloppyDict()
    p = configparser.ConfigParser()

    #for filename in fileutils.all_files_in(myargs.config_dir):
        #config.update(p.read(filename))

        
    
    #not myargs.debug and linuxutils.daemonize_me()
    os.chdir(mypwd)
    breakpoint()
    read_pipe(myargs.fifo)
    return os.EX_OK


if __name__ == '__main__':
    mypath = os.environ.get("METABATCHPATH","/etc/metabatch.d")

    parser = argparse.ArgumentParser(prog="metabatch", 
        description="What metabatch does, metabatch does best.")

    parser.add_argument('-c', '--config-dir', type=str, default=mypath,
        help="Input file name.")
    parser.add_argument('-d', '--debug', action='store_true', 
        help="Run program interactively for debugging purposes.")
    parser.add_argument('-f', '--fifo', type=str, default="/usr/local/sw/metabatch/metapipe",
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
            print(_)
            #signal.signal(_, handler)
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


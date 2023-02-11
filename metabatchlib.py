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
import logging

###
# From hpclib
###
import linuxutils
from   urdecorators import trap

###
# imports and objects that are a part of this project
###

###
# Global objects.
###
mynetid = getpass.getuser()
verbose = False

###
# Credits
###
__author__ = 'George Flanagin and Alina Enikeeva'
__copyright__ = 'Copyright 2023'
__credits__ = None
__version__ = 0.1
__maintainer__ = 'hpc@richmond.edu'
__email__ = ['hpc@richmond.edu']
__status__ = 'in progress'
__license__ = 'MIT'

event_logger = logging.getLogger('metabatch')


@trap
def examine_job(jobfile:str, netid:str) -> None:
    """
    This is the core function. It examines and potentially re-writes
    the job file using business rules that are unavailable to SLURM.
    """

    jobfile = jobfile.strip()
    if (cards := read_jobfile_with_line_numbers(jobfile, mynetid) is None):
        os._exit(os.EX_NOINPUT)

    slurm_lines = get_slurm_lines(cards)
    event_logger.debug(f"{slurm_lines=}")
    

    data = rebuild_jobfile(cards)
    resubmit_jobfile(data, jobfile, netid)

    os._exit(os.EX_OK)


def get_slurm_lines(cards:dict) -> dict:
    """
    Filter the dictionary on lines that start with #SBATCH
    """
    return {k:v for k, v in cards.items() if v.startswith('#SBATCH')}


@trap
def read_jobfile_with_line_numbers(jobfile:str, netid:str) -> dict:
    """
    return the contents as a dict by line number. If
    the file cannot be read (or does not exist) return None.
    """
    if not os.path.isfile(jobfile):
        event_logger.error(f"Unable to locate {jobfile}")

    try:
        with open(jobfile) as f:
            return {i:line for i, line in enumerate(f.readlines())}

    except Exception as e:
        event_logger.error(f"Unable to read {jobfile}")
        return None
        

@trap
def rebuild_jobfile(cards:dict) -> str:
    """
    Now that the contents have been adjusted/modified, let's
    reassemble them. Note that this syntax allows for the fact
    we may have added a line 6.5 intended to be between 6 and 7.
    """
    return "\n".join( cards[n] for n in sorted(cards.keys()) )


@trap
def resubmit_jobfile(data:str, jobfile:str, netid:str) -> int:
    return os.EX_OK

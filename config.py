# -*- coding: utf-8 -*-
import typing
from   typing import *

min_py = (3, 9)

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
import configparser
import contextlib
import getpass
mynetid = getpass.getuser()

###
# Installed libraries.
###


###
# From hpclib
###
import linuxutils
from   urdecorators import trap

###
# imports and objects that are a part of this project
###


###
# Global objects and initializations
###
verbose = False

###
# Credits
###
__author__ = 'George Flanagin'
__copyright__ = 'Copyright 2023'
__credits__ = None
__version__ = 0.1
__maintainer__ = 'George Flanagin'
__email__ = ['gflanagin@richmond.edu']
__status__ = 'in progress'
__license__ = 'MIT'


@trap
def parse_config(config_dir: str) -> dict:
    """
    Parses configuration directory and its files. Returns a nested dictionary with the contents of configuration files.
    """
    config_info = {}

    parse_logger =  logging.getLogger('metabatch').getChild('parse_config')
    parse_logger.setLevel(myargs.verbose)

    if not os.path.exists(config_dir):
        parse_logger.error(f"Directory {myargs.config_dir} is not found")
        sys.exit(os.EX_CONFIG)        

    #get the contents of the directory with config information
    parse_logger.info("Reading configuration files")
    for path_to_file in fileutils.all_files_in(config_dir):

        parser = configparser.ConfigParser()
        try:
            parser.read(path_to_file)
        except Exception as e:
            parse_logger.error("Error parsing config file {path_to_file}")
        
        #populate the dictionary
        config_info[path_to_file]={}
        for sect in parser.sections():
            names = []
            values = []
            for name, value in parser.items(sect):
                names.append(name)
                values.append(value)
            config_info[path_to_file][sect] = dict(zip(names, values))
 
    if not len(config_info):
        parse_logger.error(f"No config files found in {config_dir}.")

    return config_info


@trap
def config_main(myargs:argparse.Namespace) -> int:
    
    return os.EX_OK


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog="config", 
        description="What config does, config does best.")

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


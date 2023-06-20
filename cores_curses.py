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
import curses
from curses import wrapper
import getpass
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
from mapper import *
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
def map_cores(stdscr: object) -> None:

    #add colors
    # existing colors: black , blue, cyan, green, magenta, red, white, yellow


    # initialize the color, use ID to refer to it later in the code
    # params: ID, font color, background color
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_YELLOW) # 1 is the ID of the color
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_MAGENTA)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    #way 2 to use the color, uses a variable assignment
    BLUE_AND_YELLOW = curses.color_pair(1) 
    CYAN_AND_MAGENTA = curses.color_pair(2)
    BLUE_AND_BLACK = curses.color_pair(3)
    MAGENTA_AND_BLACK = curses.color_pair(4)

    # to get the coordinates of the screen
    # (curses.LINES - 1, curses.COLS - 1)

    # windows are needed so that you can refresh them independently
    # one window will have cpu, another - memory
    #cores_win = curses.newpad((curses.LINES - 1), int((curses.COLS - 1)/2))
    #cores_win = curses.newpad((curses.LINES - 1), int((curses.COLS - 1)/2))

    stdscr.clear()
    
    cores_info = draw_map().get("cores")
    cores="\n".join(sorted(cores_info))

    cols_tot = curses.COLS - 1
    rows_tot = curses.LINES - 1
    cols_mid = int(0.5*cols_tot)   ## middle point of the window
    rows_mid = int(0.5*rows_tot)
    
    cores_pad = curses.newpad(rows_mid, cols_mid)
    mem_pad = curses.newpad(rows_mid, cols_mid)
  
    for k, v in draw_map().items():
        cores_pad.clear()
        #mem_win.clear()

        if k == "cores": 
            #cores_pad.clear()
            v="\n".join(sorted(v))
            cores_pad.addstr(0, 0, v, BLUE_AND_BLACK)
            cores_pad.refresh(0,0, 0,0, rows_tot,cols_mid)
            cores_pad.getch()
            #time.sleep(10)
        else:
            #mem_win.clear()
            v="\n".join(sorted(v))
            mem_pad.addstr(0, 0, v, MAGENTA_AND_BLACK)
            mem_pad.refresh(0,0, 0,cols_mid, rows_tot,cols_tot-1)
            #time.sleep(2)
            mem_pad.addstr("\n")
    cores_pad.refresh(0,0, 0,0, rows_tot,cols_mid)  
    mem_pad.refresh(0,0, 0,cols_mid, rows_tot,cols_tot-1)
    
    stdscr.getch()
   # Check if screen was re-sized (True or False)
    resize = curses.is_term_resized(y, x)

    # Action in loop if resize is True:
    if resize is True:
        y, x = screen.getmaxyx()
        screen.clear()
        curses.resizeterm(y, x)
        screen.refresh()

    pass



@trap
def cores_curses_main(myargs:argparse.Namespace) -> int:
    wrapper(map_cores)
    return os.EX_OK


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog="cores_curses", 
        description="What cores_curses does, cores_curses does best.")

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


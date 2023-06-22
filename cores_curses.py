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
import curses.panel
from curses import wrapper
import getpass
import time
import math
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
def get_mem_info() -> dict:

    data = SeekINFO()
    memory_map = {}
    core_map_and_mem = []
   
    # We don't need the header row here is an example line:
    #
    # spdr12 424105 768000 up 52 12/40/0/52

    #core_map_and_mem.append("Node   Core Usage                                            Used / Total Memory\n")
    for line in ( _ for _ in data.stdout.split('\n')[1:] if _ ):
        node, free, total, status, true_cores, cores = line.split()
        cores = cores.split('/')
        used = (int(total) - int(free))/1000 # GB
        core_map_and_mem.append(f"{node} {scaling.row(cores[0], true_cores)} {math.ceil(used)} / {math.ceil(int(total)/1000)}")

    return core_map_and_mem


@trap
def how_busy(n:str) -> int:
    """
    Returns 0-1, corresponding to the business of the node
    """
    data = SeekINFO()
    busy_cores = 0
    busy_mem = 0
   
    try: 
        n = n.split()[0]

        for line in ( _ for _ in data.stdout.split('\n')[1:] if _ ):
            node, free, total, status, true_cores, cores = line.split()
            if node == n:     
                cores = cores.split('/')
                busy_cores = int(cores[0])/int(true_cores)

                mem_used = int(total) - int(free)
                busy_mem = mem_used/int(total)
                
                break 
    except:
        pass

    return max(busy_cores, busy_mem) #, cores[1], true_cores

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
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(9, curses.COLOR_RED, curses.COLOR_BLACK)

    #way 2 to use the color, uses a variable assignment
    BLUE_AND_YELLOW = curses.color_pair(1) 
    CYAN_AND_MAGENTA = curses.color_pair(2)
    BLUE_AND_BLACK = curses.color_pair(3)
    MAGENTA_AND_BLACK = curses.color_pair(4)
    GREEN_AND_BLACK = curses.color_pair(5)
    BLACK_AND_YELLOW = curses.color_pair(6)
    YELLOW_AND_BLACK = curses.color_pair(7)
    WHITE_AND_BLACK = curses.color_pair(8)
    RED_AND_BLACK = curses.color_pair(9)    

    stdscr.clear()
    
    # resize window if needed
    height,width = stdscr.getmaxyx()

    window2 = curses.newwin(0,0, 1,1)
    
    left_panel = curses.panel.new_panel(window2)

    curses.panel.update_panels()
    curses.doupdate()

    running = True
    x = 0
    while ( running  ):
        
        #display the cores map for each node
        try:
            window2.addstr(0, 0,"Node   Core Usage                                            Used / Total Memory\n", WHITE_AND_BLACK)
            for idx, node in enumerate(get_mem_info()):
                if how_busy(node) >= 0.75: #if node is more than 75% full
                    window2.addstr(idx+1, 0, node, RED_AND_BLACK)
                    window2.refresh()
                else:
                    window2.addstr(idx+1, 0, node, GREEN_AND_BLACK)
                    window2.refresh()
            window2.addstr(len(get_mem_info())+1, 0, "Press q to quit", WHITE_AND_BLACK)
            window2.refresh()
                
        except:
            window2.addstr("debug")
            window2.refresh()
            pass 

        #work around window resize
        k = window2.getch()
        if k == curses.KEY_RESIZE:
            
            height,width = stdscr.getmaxyx()
            window2.resize(height, width)
            left_panel.replace(window2)
            left_panel.move(0,0)
        if k == ord('q'): 
            running = False
            curses.endwin()
        curses.panel.update_panels()
        curses.doupdate()
        stdscr.refresh()
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


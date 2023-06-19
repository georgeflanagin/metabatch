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
def prototype(stdscr: object):
    #add colors
    # existing colors: black , blue, cyan, green, magenta, red, white, yellow


    # initialize the color, use ID to refer to it later in the code
    # params: ID, font color, background color
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_YELLOW) # 1 is the ID of the color
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_MAGENTA)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)

    #way 2 to use the color, uses a variable assignment
    BLUE_AND_YELLOW = curses.color_pair(1) 
    CYAN_AND_MAGENTA = curses.color_pair(2)
    BLUE_AND_BLACK = curses.color_pair(3)

    # to get the coordinates of the screen
    # (curses.LINES - 1, curses.COLS - 1)

    # windows are needed so that you can refresh them independently
    # one window will have cpu, another - memory
    mapper_win = curses.newpad(100, 100)

    for k, v in draw_map().items():
        mapper_win.clear()

        if k == "cores": 
            mapper_win.clear()
            v="\n".join(sorted(v))
            mapper_win.addstr(0, 0, v, BLUE_AND_BLACK)
            mapper_win.refresh(0,0, 0, 0, 25, 75)
            time.sleep(2)
            mapper_win.addstr("\n")
    

    """
    for i in range(2):
        stdscr.clear()
        color = BLUE_AND_YELLOW

        if i%2 == 0:
            color = CYAN_AND_MAGENTA

        stdscr.addstr("changing colors", color)
        stdscr.refresh()    
        time.sleep(1)
    """
    stdscr.getch()



    stdscr.clear() #clear the screen
    stdscr.addstr(10, 2, "hello world") #row to place the string, column, string 
    stdscr.addstr(20, 20, "middle of the screen")
    stdscr.addstr(30, 30, "colors", curses.color_pair(1)) 
    stdscr.addstr(25, 25, "colors", BLUE_AND_YELLOW)
    stdscr.addstr(0, 0, "cyan and magenta", CYAN_AND_MAGENTA)
    #stdscr.addstr(40, 40, "uderlined text", curses.A_REVERSE)

    stdscr.refresh()
    stdscr.getch() # waits for the user to type something

    pass


@trap
def prototype_main(myargs:argparse.Namespace) -> int:
    wrapper(prototype) # does all the initializing for us
    """
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    
    #reminate the curses application
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
   
    #restore the terminal 
    curses.endwin()
    
    """
    return os.EX_OK


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog="prototype", 
        description="What prototype does, prototype does best.")

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


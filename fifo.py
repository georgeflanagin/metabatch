# -*- coding: utf-8 -*-
"""
FIFO is a wrapper around the Linux kernel pipes used for interprocess
communication. 

Usage:

    from fifo import FIFO

    # The mode must be either 'r' or 'w'. In either case, the pipe
    # will be created if it does not already exist.
    mypipe = FIFO(pipe_name, mode)

    # FIFO has a __call__ method that selects read or write based
    # on how the pipe was opened. So, ...

        data = mypipe(timeout_seconds) # reads the pipe

        bytes_written = mypipe('message') # writes message to the pipe.

    The reading and writing is no blocking, and select is used to be
    notified when there is data to be read, so the operation is fairly
    efficient: your reading process goes to sleep and receives a SIGIO
    when there is something in the pipe.

    Pipes only deal with bytes, but this FIFO object uses str and does
    the encode/decode behind the scenes.

    A separator that defaults to ; can be supplied when the pipe
    is opened. The separator can be empty, in which case the 
    data are read out in situ, otherwise the read operation
    returns a list of things found, even if it is a list with only
    one element.
"""

import typing
from   typing import *

# Credits
__author__ = 'George Flanagin'
__copyright__ = 'Copyright 2020, University of Richmond'
__credits__ = None
__version__ = '0.4'
__maintainer__ = 'George Flanagin'
__email__ = 'gflanagin@richmond.edu'
__status__ = 'Working Prototype'
__required_version__ = (3, 6)

__license__ = 'MIT'


import argparse
import contextlib

import io
import os
import select
import stat
import sys

verbose=False

if sys.version_info < __required_version__:
    print(f"This code requires Python version {__required_version__} or later.")
    sys.exit(os.EX_SOFTWARE)

from   urdecorators import trap

class FIFO:
    """
    Wrapper around the internals of pipe based IPC.
    """

    # This class variable is a translation table. NOTE: all pipes
    # are binary. The class methods below will take care of the text
    # to binary translation. 
    modes = {
        "non_block": os.O_RDONLY | os.O_NONBLOCK,
        "block": os.O_RDONLY,
        "w": os.O_WRONLY | os.O_NONBLOCK
        }


    def __init__(self, 
            queue_name:str, 
            mode:str='non_block', 
            delimiter:str=';',
            ignore:str="#"):
        """
        Safely open a new or existing FIFO for reading
        or writing. Note that if the function returns, it
        was successful, otherwise it raises an Exception with
        an appropriate text message.

        queue_name -- the name of the pipe, relative or absolute. 
        mode -- one of the modes we support.
        delimiter -- to mark the boundary between parts of the written
            messages.
        ignore -- to facilitate testing, messages that begin like this
            will be discarded.
        """
    
        self.fifo = None
        self.name = ( queue_name 
            if queue_name.startswith(os.sep) else 
            os.path.join(os.environ.get('PIPEDIR', os.getcwd()), queue_name) )
        self.mode = mode
        self.delimiter = "" if delimiter is None else delimiter
        self.ignore = "#" if ignore is None else ignore

        # Check the mode to make sure it is one we can use. 
        if self.mode not in FIFO.modes: 
            raise Exception(
                f"unknown mode {mode}. must be one of {tuple(FIFO.modes.keys())}."
                )

        try:
            # If the file system entry is already present, and it is a 
            # pipe, try to open it.
            if stat.S_ISFIFO(os.stat(self.name).st_mode):
                self.fifo = os.open(self.name, FIFO.modes[self.mode])
                return

            else:
                # if it is not a pipe, do not allow this to proceed.
                raise Exception(f"{self.name} is not a FIFO.")

        except FileNotFoundError as e:
            # if it is not present, we cannot create it in write mode.
            if self.mode == 'w':
                raise Exception(
                    f"pipe {self.name} does not exist; it must be created by a reader."
                    ) from None
            pass

        except OSError as e:
            # We were trying to open in write, it is there, but there is no reader.
            raise Exception(f'{self.name} is not ready because there is no reader.') from None

        except Exception as e:
            # Something else went wrong. Haven't yet seen this one.
            raise Exception(f"unexpected problem with {self.name}: {str(e)}") from None

        try:
            # We must be the reader, and the pipe does not exist.
            os.mkfifo(self.name, 0o600)
            self.fifo = os.open(self.name, FIFO.modes[self.mode])
        
        except Exception as e:
            # We must not have permissions or something else at the OS level.
            raise Exception(f"Catastrophic failure {str(e)}") from None


    @trap
    def __str__(self) -> str:
        """
        Identify this pipe.
        """
        return f"{self.name} is open {self.mode} using {self.delimiter} to delimit messages."


    @trap
    def __call__(self, argument:Union[int, list]=60) -> Union[list, int]:
        """
        Read or write the pipe, depending on how it is open.

        argument (read)  -- an int number of seconds.
        argument (write) -- a string or list of strings to write.

        returns --  (read) the data
                    (write) the number of bytes written.
        """
        return self.write(argument) if self.mode == 'w' else self.wait_for_data(argument)


    @trap
    def wait_for_data(self, how_long:int) -> List[str]:
        """
        Read all the data found. Split on the semi-colon and return
        a list of the text shreds except for the comments.

        how_long : in seconds, how long to select (wait) on the pipe.
        """

        data = None
        poll = select.poll()
        poll.register(self.fifo, select.POLLIN)

        try:
            sys.stderr.write(f"polling\n")
            if (self.fifo, select.POLLIN) in poll.poll(how_long * 1000):
                sys.stderr.write(f"received SIGPIPE\n")
                data = os.read(self.fifo, io.DEFAULT_BUFFER_SIZE*16).decode('utf-8')
                sys.stderr.write(f"{data=}\n")
                data = [ _ for _ in data.split(self.delimiter) 
                    if _ and not _.startswith(self.ignore) ]
            else:
                sys.stderr.write(f"{self.fifo=} {select.POLLIN=} {poll.poll=}\n")


        except Exception as e:
            sys.stderr.write("Exception in FIFO: {e}")

        finally:
            poll.unregister(self.fifo)
            # if data is None, then the assignment statement above failed
            # when reading from the pipe. This happens when there are no
            # writers to the pipe. So, we reopen and wait.
            if data is None: 
                sys.stderr.write("waited for Godot.")
                sys.exit(os.EX_DATAERR)

            return data
                

    @trap
    def write(self, messages:List[str]) -> int:
        """
        write messages to the fifo.
        """

        # We need to join the list with the delimiter.
        if not isinstance(messages, (list, tuple)): messages = [messages]
        messages = self.delimiter.join(messages)
        try:
            os.write(self.fifo, messages.encode('utf-8'))

        except Exception as e:
            uu.tombstone(str(e))
            return 0

        else:
            return len(messages)


@trap
def fifo_writer(myargs:argparse.Namespace) -> int:
    sys.stderr.write(f"Let's write to {myargs.pipe}")
    p = FIFO(myargs.pipe, 'w')

    while text := input('Shout something into the pipe: '):
        p(text)

    return os.EX_OK    


@trap
def fifo_main(myargs:argparse.Namespace) -> int:

    if myargs.mode == 'w':
        return fifo_writer(myargs)

    sys.stderr.write(f"Let's open {myargs.pipe} with mode {myargs.mode}.\n")
    p = FIFO(myargs.pipe, myargs.mode)
    sys.stderr.write(f"{myargs.pipe} created.\n")

    i = 0
    while i < myargs.count:

        i += 1
        sys.stderr.write(f"Waiting {myargs.time} seconds for message in the pipe.\n")
        data = p(myargs.time)
        sys.stderr.write(f"Read {data=}")
        
    return os.EX_OK if i == myargs.count else os.EX_DATAERR



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog="fifo", 
        description="What fifo does, fifo does best.")

    parser.add_argument('-c', '--count', type=int, default=sys.maxsize,
        help="Number of times to read from the pipe. The default is to read indefinitely many times.")
    parser.add_argument('-m', '--mode', type=str, choices=('non_block', 'block', 'w')),
    parser.add_argument('-o', '--output', type=str, default="",
        help="Output file name")
    parser.add_argument('-p', '--pipe', type=str, required='True',
        help="Input file name.")
    parser.add_argument('-t', '--time', type=int, default=300,
        help="Seconds to wait for data in the pipe.")
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


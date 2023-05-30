#!/bin/sh
#This function overwrites original command sbatch.

function sbatch
{
	if [ -z "$1" ]; then
        echo "syntax ..."
        return
	fi
	
	filename=$(realpath "$1")
 	echo "$(whoami),$filename" > metapipe

}


function readpipe
{
    python -c 'import read_pipe; print(read_pipe.read_pipe('metapipe'))'    
}

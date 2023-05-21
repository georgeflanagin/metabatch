"""
This function overwrites original command sbatch.
It reads the 
"""

function sbtach{
	if [-z $1]; then
	echo “syntax …”
	return
	fi
	
	filename = realpath “$1”
 	echo “$(whoami), $filename” > metapipe
}


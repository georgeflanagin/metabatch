#!/bin/bash

###
# This file was originally created by SLURMwriter, a tool
# written by University of Richmond's High Performance
# Computing group. This file created @ 2022-01-24 11:04:04
# 
# Note: slurm cannot see environment or shell variables. You
# must type in the values you need. You can add them in the 
# `sbatch` line you type in so that they are explicitly provided.
###

###
# Environment setup
###
export JOBID=$SLURM_JOB_ID
export NETID=installer
export JOBNAME=catamaran
export DATADIR="$HOME/catamaran"
export SCRATCH="/localscratch/$NETID/$JOBNAME/$JOBID"
export BIGSCRATCH="/scratch/$NETID/$JOBNAME/$JOBID"

echo DATADIR=$DATADIR
echo SCRATCH=$SCRATCH
echo BIGSCRATCH=$BIGSCRATCH

mkdir -p $SCRATCH
mkdir -p $BIGSCRATCH

###
# Invoke function as a trap on the EXIT signal to ensure
# the node's scratch directory is clean.
###
clean_scratch()
{
    cause=$?
    if [[ cause != 0 ]]; then
        echo "Killed by signal $cause" >> "$HOME/$JOBNAME.$JOBID.err"
    else
        echo "Normal termination." >> "$HOME/$JOBNAME.$JOBID.err"
    fi
    nice cp -r $SCRATCH/* $BIGSCRATCH/.
    rm -fr $SCRATCH
}

#SBATCH --account=installer
#SBATCH --begin=2022-01-24T11:03
#SBATCH --mail-type=ALL
#SBATCH --mail-user="$NETID@richmond.edu"
#SBATCH --mem=16GB
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --partition=basic
#SBATCH --time=01:00:00

#SBATCH -o "$HOME/$JOBNAME.$JOBID.out"
#SBATCH -e "$HOME/$JOBNAME.$JOBID.err"

cd $SLURM_SUBMIT_DIR
echo "I ran on: $SLURM_NODELIST"
echo "Starting at `date`"

########################################################################
# Always a good idea to wipe anything from memory where it
# is allocated. Add other modules here, as well.
########################################################################

export MODULEPATH="$MODULEPATH:/usr/local/sw/modulefiles"



########################################################################
# Copy data from DATADIR to SCRATCH below.
########################################################################
cp -r $DATADIR/* $SCRATCH/.


########################################################################
# Run your job by adding commands below for . 
########################################################################
cd "$SCRATCH"

trap clean_scratch EXIT
 myfile.dat
trap "" EXIT

echo "Finished at `date`"

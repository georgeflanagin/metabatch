#!/bin/bash

###
# This file was originally created by SLURMwriter, a tool
# written by University of Richmond's High Performance
# Computing group. This file created @ 2021-10-22 15:00:33
# 
# Note: slurm cannot see environment or shell variables. You
# must type in the values you need. You can add them in the 
# `sbatch` line you type in so that they are explicitly provided.
###

#SBATCH --account=mdias$
#SBATCH --begin=2021-10-22T15:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=abezerra@richmond.edu
#SBATCH --mem=100GB
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --partition=basic
#SBATCH --time=24:00:00

#SBATCH -o /home/abezerra/anibalqe.txt
#SBATCH -e /home/abezerra/anibalqe.txt.err

cd $SLURM_SUBMIT_DIR
echo "I ran on: $SLURM_NODELIST"
echo "Starting at `date`"

###
# Environment setup
###

NAME=anibalqe

export DATADIR=/home/abezerra
export SCRATCH=/localscratch/abezerra
export BIGSCRATCH=/scratch/abezerra

########################################################################
# Always a good idea to wipe anything from memory where it
# is allocated. Add other modules here, as well.
########################################################################

export MODULEPATH="$MODULEPATH:/usr/local/sw/modulefiles"
module purge


mkdir -p $SCRATCH

########################################################################
# Copy data from DATADIR to SCRATCH below.
#
# Example:  cp $DATADIR/myfile $SCRATCH/myfile
########################################################################


########################################################################
# Run your job by adding commands below for qe. 
# You may need to set some ENV variables, or load 
# additional  modules before you add the executable commands.
########################################################################

/usr/local/sw/qe/6.8/bin/pw.x input_file

########################################################################
# Copy output files from SCRATCH to big storage.
########################################################################

cp -r $SCRATCH/* $BIGSCRATCH/.

 
########################################################################
# Be kind and clean the SCRATCH area.
########################################################################

rm -rf $SCRATCH

echo "Finished at `date`"


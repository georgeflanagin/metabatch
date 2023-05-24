#!/bin/bash

###
# Note: slurm cannot see environment or shell variables. You
# must type in the values you need. You can add them in the 
# `sbatch` line you type in so that they are explicitly provided.
###

#SBATCH --account=securegrp
#SBATCH --begin=2021-10-15T10:31
#SBATCH --mail-type=ALL
#SBATCH --mail-user=installer@richmond.edu
#SBATCH --mem=16GB
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --partition=parish
#SBATCH --time=01:00:00

#SBATCH -o mybigjob1.txt
#SBATCH -e mybigjob1.txt.err

cd $SLURM_SUBMIT_DIR
echo "I ran on: $SLURM_NODELIST"
echo "Starting at `date`"

###
# Environment setup
###

NAME=mybigjob

export DATADIR=/home/installer
export SCRATCH=/localscratch/installer
export BIGSCRATCH=/scratch/installer

########################################################################
# Always a good idea to wipe anything from memory where it
# is allocated. Add other modules here, as well.
########################################################################

module purge

mkdir -p $SCRATCH

########################################################################
# Copy data from DATADIR to SCRATCH below.
#
# Example:  cp $DATADIR/myfile $SCRATCH/myfile
########################################################################


########################################################################
# Run your job by adding commands below for 
# . You may need to set some ENV variables,
# or load some modules before you add the executable commands.
########################################################################

{}

########################################################################
# Copy output files from SCRATCH to big storage.
########################################################################

cp -r $SCRATCH/* $BIGSCRATCH/.

 
########################################################################
# Be kind and clean the SCRATCH area.
########################################################################

rm -rf $SCRATCH

echo "Finished at `date`"


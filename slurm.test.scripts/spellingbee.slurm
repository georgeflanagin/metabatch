#!/bin/bash

###
# This file was originally created by SLURMwriter, a tool
# written by University of Richmond's High Performance
# Computing group. This file created @ 2022-04-19 14:30:59
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
export JOBNAME=spellingbee
export DATADIR="$HOME/spellingbee"
export SCRATCH="/localscratch/$NETID/$JOBNAME/$JOBID"
export BIGSCRATCH="/scratch/$NETID/$JOBNAME/$JOBID"

echo DATADIR=$DATADIR
echo SCRATCH=$SCRATCH
echo BIGSCRATCH=$BIGSCRATCH

mkdir -p $DATADIR
mkdir -p $SCRATCH
mkdir -p $BIGSCRATCH

#SBATCH --account=securegrp
#SBATCH --begin=now
#SBATCH --mail-type=ALL
#SBATCH --mail-user="$NETID@richmond.edu"
#SBATCH --mem=16GB
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=20
#SBATCH --partition=basic
#SBATCH --time=01:00:00

#SBATCH -o "$HOME/$JOBNAME.$JOBID.out"
#SBATCH -e "$HOME/$JOBNAME.$JOBID.err"

cd $SLURM_SUBMIT_DIR
echo "I ran on: $SLURM_NODELIST"
echo "Starting at `date`"


echo "Finished at `date`"

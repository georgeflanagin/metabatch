#!/bin/bash -e
#SBATCH  --account=installer$
#SBATCH  --mail-type=NONE
#SBATCH  --mail-user=installer@richmond.edu
#SBATCH  --job-name=fifteen8
#SBATCH  --cpus-per-task=1
#SBATCH  --output fifteen8.tomb
#SBATCH  -e fifteen8.tomb.err
#SBATCH  --mem=32000M
#SBATCH  --tasks=1
#SBATCH  --partition=basic

cd $SLURM_SUBMIT_DIR
echo "I ran on: $SLURM_NODELIST"
echo "Starting at `date`"

NAME=fifteen8

/usr/bin/time -v /usr/bin/date 

echo "Finished at `date`"


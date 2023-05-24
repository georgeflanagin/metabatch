#!/bin/bash -e
#SBATCH  --account=installer$
#SBATCH  --mail-type=NONE
#SBATCH  --mail-user=installer@richmond.edu
#SBATCH  --job-name=lib64.computenode
#SBATCH  --cpus-per-task=1
#SBATCH  --output lib64.computenode.tomb
#SBATCH  -e lib64.computenode.tomb.err
#SBATCH  --mem=32000M
#SBATCH  --tasks=1
#SBATCH  --partition=basic

cd $SLURM_SUBMIT_DIR
echo "I ran on: $SLURM_NODELIST"
echo "Starting at `date`"

NAME=lib64.computenode

/usr/bin/time -v /usr/bin/date 

echo "Finished at `date`"


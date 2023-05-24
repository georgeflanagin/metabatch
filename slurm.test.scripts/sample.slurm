#!/bin/bash -e
#SBATCH  --account=installer$
#SBATCH  --mail-type=NONE
#SBATCH  --mail-user=installer@richmond.edu
#SBATCH  --job-name=sample
#SBATCH  --cpus-per-task=1
#SBATCH  --output sample.tomb
#SBATCH  -e sample.tomb.err
#SBATCH  --mem=32000M
#SBATCH  --tasks=1
#SBATCH  --partition=basic

cd $SLURM_SUBMIT_DIR
echo "I ran on: $SLURM_NODELIST"
echo "Starting at `date`"

NAME=sample

/usr/bin/time -v /usr/bin/date 

echo "Finished at `date`"


#!/bin/bash -e
#SBATCH  --account=installer$
#SBATCH  --mail-type=NONE
#SBATCH  --mail-user=installer@richmond.edu
#SBATCH  --job-name=basissets1
#SBATCH  --cpus-per-task=1
#SBATCH  --output basissets1.tomb
#SBATCH  -e basissets1.tomb.err
#SBATCH  --mem=32000M
#SBATCH  --tasks=1
#SBATCH  --partition=basic

cd $SLURM_SUBMIT_DIR
echo "I ran on: $SLURM_NODELIST"
echo "Starting at `date`"

NAME=basissets1

/usr/bin/time -v /usr/bin/date 

echo "Finished at `date`"


#!/bin/bash -e
#SBATCH  --account=installer$
#SBATCH  --mail-type=NONE
#SBATCH  --mail-user=installer@richmond.edu
#SBATCH  --job-name=s73
#SBATCH  --cpus-per-task=1
#SBATCH  --output s73.tomb
#SBATCH  -e s73.tomb.err
#SBATCH  --mem=32000M
#SBATCH  --tasks=1
#SBATCH  --partition=basic

cd $SLURM_SUBMIT_DIR
echo "I ran on: $SLURM_NODELIST"
echo "Starting at `date`"

NAME=s73

/usr/bin/time -v /usr/bin/date 

echo "Finished at `date`"


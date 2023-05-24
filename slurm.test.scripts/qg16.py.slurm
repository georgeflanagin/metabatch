#!/bin/bash -e
#SBATCH  --account=installer$
#SBATCH  --mail-type=NONE
#SBATCH  --mail-user=installer@richmond.edu
#SBATCH  --job-name=qg16.py
#SBATCH  --cpus-per-task=1
#SBATCH  --output qg16.py.tomb
#SBATCH  -e qg16.py.tomb.err
#SBATCH  --mem=32000M
#SBATCH  --tasks=1
#SBATCH  --partition=basic

cd $SLURM_SUBMIT_DIR
echo "I ran on: $SLURM_NODELIST"
echo "Starting at `date`"

NAME=qg16.py

/usr/bin/time -v /usr/bin/date 

echo "Finished at `date`"


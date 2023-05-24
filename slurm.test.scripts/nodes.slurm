#!/bin/bash -e
#SBATCH  --account=installer$
#SBATCH  --mail-type=NONE
#SBATCH  --mail-user=installer@richmond.edu
#SBATCH  --job-name=nodes
#SBATCH  --cpus-per-task=1
#SBATCH  --output nodes.tomb
#SBATCH  -e nodes.tomb.err
#SBATCH  --mem=32000M
#SBATCH  --tasks=1
#SBATCH  --partition=basic

cd $SLURM_SUBMIT_DIR
echo "I ran on: $SLURM_NODELIST"
echo "Starting at `date`"

NAME=nodes

/usr/bin/time -v /usr/bin/date 

echo "Finished at `date`"


#!/bin/bash -e
#SBATCH --job-name=YOURJOB
#SBATCH --item=D-HH:MM:SS
#SBATCH --cpus-per-task=10
#SBATCH --mem=100G

#SBATCH --mail-type=ALL
#SBATCH --mail-user="netid@richmond.edu"

echo "I ran on: $SLURM_NODELIST"
echo "Starting at `date`"

cd ~/spellingbee
/usr/bin/time python bee.py --cpus 10 --batch -dictionary 20k.txt

echo "Finished at `date`"









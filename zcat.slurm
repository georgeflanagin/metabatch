#!/bin/bash -e

#SBATCH --job-name=ZCAT_TEST_1
#SBATCH --ntasks=1
#SBATCH --time=00:00:10
#SBATCH --mail-type=ALL
#SBATCH --mail-user=hpc@richmond.edu

#SBATCH --partition=any
#SBATCH --mem=10
#SBATCH --cpus-per-task=2

# Print the simulation start date/time
date

# Print the node the simulation is running on
echo "I ran on:"
echo "SLURM_NODELIST=$SLURM_NODELIST"

# Return the context/PWD to the directory where *this* file is located.
cd $SLURM_SUBMIT_DIR

# Load the necessary program libraries

zcat data.dat.gz 

# Print the simulation end date/time
date




#modified by metabatch on 2023-06-05 16:25:26.727521
#metabatch version Mon Jun  5 15:38:11 2023
#!/bin/bash

#SBATCH --begin=now
#SBATCH --job-name=EmoPW
#SBATCH --output=EmoPW.%j.out
#SBATCH --account=cparish
#SBATCH --partition=parish
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=50
#SBATCH --time=100:00:00

# Print the simulation start date/time
date

# Print the CPU node the simulation is running on
echo "I ran on:"
cd $SLURM_SUBMIT_DIR
echo $SLURM_NODELIST

# Load the necessary program libraries
source /usr/local/sw/amber/amber20/amber.sh
export PYTHONPATH="/usr/local/sw/amber/amber20/lib/python3.8/site-packages:$PYTHONPATH"
export PATH="/usr/local/sw/amber/amber20/bin:$PATH"
export LD_LIBRARY_PATH="/usr/local/sw/amber/amber20/lib:/usr/local/cuda/lib64:/usr/local/cuda/lib64/stubs:$LD_LIBRARY_PATH"

##### show what the values are to assist debugging.
# env | sort

cd /scratch/installer/6lzg_300/Emodin

#Run scripts below
#Pairwise Decomposition Calculations
source mmgbsa_10seed.sh
source Filter_Pairwise_Decomp.sh

# Print the simulation end date/time
date

#!/bin/bash

#SBATCH --job-name=T1_A100
#SBATCH --output=T1_A100.txt
#SBATCH --partition=ML
#SBATCH --gres=gpu:tesla_a100:1
#SBATCH --ntasks=1
#SBATCH --time=00:05:00

# Print the simulation start date/time
date


# Print the GPU node the simulation is running on
echo "I ran on:"
cd $SLURM_SUBMIT_DIR
echo "SLURM_NODELIST=$SLURM_NODELIST"

# Load the necessary program libraries

source /usr/local/sw/amber/amber20/amber.sh
#setenv CUDA_HOME /usr/local/cuda-11.4
export CUDA_HOME="/usr/local/cuda-11.4"
export CUDA_VISIBLE_DEVICES=0
export PYTHONPATH="/usr/local/sw/amber/amber20/lib/python3.8/site-packages:$PYTHONPATH"
export PATH="/usr/local/sw/amber/amber20/bin:$PATH"
export LD_LIBRARY_PATH="/usr/local/sw/amber/amber20/lib:/usr/local/cuda/lib64:/usr/local/cuda/lib64/stubs:$LD_LIBRARY_PATH"

env | sort

# Set the output file directory
#cd /work/ja9ia/Si_POSS/PM6/MethoxyIndene/S1

# Run Amber Jobs
./min.sh
./heat.sh
./eq.sh
./md.sh

# Print the simulation end date/time
date

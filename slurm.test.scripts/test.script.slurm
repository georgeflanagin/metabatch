#!/bin/bash

#SBATCH --job-name=TEST
#SBATCH --output=TEST.txt
#SBATCH --partition=ML
 
#SBATCH --ntasks=1
#SBATCH --time=24:00:00

# Print the simulation start date/time
  date

# Load the necessary program libraries
conda init bash
  conda activate qiime2-2022.2

# Set the output file directory
  cd /home/jbrinker/shared


 # Print the simulation end date/time
  date
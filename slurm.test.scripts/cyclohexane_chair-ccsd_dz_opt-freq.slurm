#!/bin/csh

#SBATCH  --job-name=cyclohexane_chair-ccsd_dz_opt-freq
#SBATCH  --cpus-per-task=1
#SBATCH  --output cyclohexane_chair-ccsd_dz_opt-freq.slurmo
#SBATCH  --mem=60000

# Print the calculation start date/time
date

# Print the GPU node the computation is running on
echo "I ran on:"
cd $SLURM_SUBMIT_DIR
echo $SLURM_NODELIST

# Load necessary programs, environment variables, and libraries
module load qchem/qchem532

/usr/bin/time -v qchem -pbs -np 12 cyclohexane_chair-ccsd_dz_opt-freq.in cyclohexane_chair-ccsd_dz_opt-freq.out 


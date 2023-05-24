#!/usr/bin/csh

#SBATCH  --account=dsiriann
#SBATCH  --job-name=qchem-test
#SBATCH  --cpus-per-task=16
#SBATCH  --output qchem-test.tomb
#SBATCH  --error qchem-test.tomb.err
#SBATCH  --mem=1500G
#SBATCH  --tasks=1
#SBATCH  --partition=large

#SBATCH  --mail-type=ALL
#SBATCH  --mail-user="dsiriann@richmond.edu"

# Print the calculation start date/time
date

# Print the CPU node the computation is running on
echo "I ran on:"
cd $SLURM_SUBMIT_DIR
echo $SLURM_NODELIST

# Load necessary programs, environment variables, and libraries
set QC /usr/local/sw/qchem/qchem53
setenv QC          ${QC}
setenv CPLATFORM   LINUX_Ix86_64
setenv QCAUX       ${QC}/qcaux
setenv QCSCRATCH   /scratch/${USER}
setenv QCRSH       ssh
setenv QCMPI       mpich

prepend-path PATH ${QC}/bin
prepend-path PATH ${QC}/exe


date


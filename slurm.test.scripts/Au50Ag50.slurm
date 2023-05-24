#!/bin/bash

###
# Note: slurm cannot see environment or shell variables. You
# must type in the values you need. You can add them in the 
# `sbatch` line you type in so that they are explicitly provided.
###

#SBATCH --account=mrebello$
#SBATCH --begin=now
#SBATCH --mail-type=ALL
#SBATCH --mail-user=abezerra@richmond.edu
#SBATCH --mem=500GB
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --partition=dias
#SBATCH --time=02:00:00

#SBATCH -o /home/abezerra/Au50Ag50.out
#SBATCH -e /home/abezerra/Au50Ag50.err

cd $SLURM_SUBMIT_DIR
echo "I ran on: $SLURM_NODELIST"
echo "Starting at `date`"

###
# Environment setup
###


PREFIX=Au50Ag50

export DATADIR="/home/abezerra/$PREFIX"
export SCRATCH="/scratch/abezerra/$PREFIX"

#mkdir -p $DATADIR
mkdir -p $SCRATCH

#######################################################################
## Quantum Expresso

export QE_version="6.8"
export QEPATH="/usr/local/sw/qe/$QE_version/bin"

########################################################################
# Always a good idea to wipe anything from memory where it
# is allocated. Add other modules here, as well.
########################################################################

cd $SCRATCH
cp $DATADIR/Al.scf.in $SCRATCH/Al.scf.in

#export MODULEPATH="$MODULEPATH:/usr/local/sw/modulefiles"
module purge
#module load mpich/3.4.2-intel-2021.3.0
module load mpich/3.4.2-gcc-8.4.1
module load intel/2021.3.0
module load gcc/8.4.1
#export LD_LIBRARY_PATH=/usr/local/sw/amber/amber20/miniconda/lib/

echo "$pwd"
echo "Modules loaded"
########################################################################
# Copy data from DATADIR to SCRATCH below.
#
# Example:  cp $DATADIR/myfile $SCRATCH/myfile
########################################################################

srun mpirun -n 1 $QEPATH/pw.x < "Al.scf.in" > "Al.scf.out"
echo "QE ran"
########################################################################
# Run your job by adding commands below for 
# qe. You may need to set some ENV variables,
# or load some modules before you add the executable commands.
########################################################################


########################################################################
# Copy output files from SCRATCH to	 big storage.
########################################################################



 
########################################################################
# Be kind and clean the SCRATCH area.
########################################################################

#rm -rf $SCRATCH

echo "Finished at `date`"


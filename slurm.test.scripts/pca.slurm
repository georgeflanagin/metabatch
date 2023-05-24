#!/bin/bash -e
#SBATCH --account=myang
#SBATCH --job-name=pca_Zind
#SBATCH --cpus-per-task=1
#SBATCH --mem=300G
#SBATCH --partition=yang1

#SBATCH --mail-type=ALL
#SBATCH --mail-user=myang@richmond.edu

#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err

##bwa aln practice

echo "I ran on: $SLURM_NODELIST"
echo "Starting at `date`"

cd /scratch/myang_shared/lab/mel/Zind_proj/pca/
export LD_LIBRARY_PATH="/usr/local/sw/anaconda/anaconda3/envs/treemix/lib/:$LD_LIBRARY_PATH"
##export avoids this error:
##smartpca: error while loading shared libraries: libgsl.so.25: cannot open shared object file: No such file or directory

/usr/bin/time smartpca -p Zind_check_idp4a.par
/usr/bin/time smartpca -p Zind_check_idp4b.par
/usr/bin/time smartpca -p Zind_check_idp8a.par
/usr/bin/time smartpca -p Zind_check_idp8b.par
##/usr/bin/time smartpca -p Zind_check.par

echo "Finished at `date`"


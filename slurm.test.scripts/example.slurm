#!/bin/bash

#SBATCH --account=smehkari$
#SBATCH --begin=now
#SBATCH --mail-type=ALL
#SBATCH --mail-user=smehkari@richmond.edu
#SBATCH --job-name=TRYOUT
#SBATCH --ntasks=1
#SBATCH --time=24:00:00

##################### GPU ############################################
#SBATCH --partition=sci
## SBATCH --partition=ML
#SBATCH --gres=gpu:tesla_a40:1
##SBATCH --gres=gpu:tesla_a100:1
#SBATCH --cpus-per-task=2
##################### END GPU ########################################

#################### NON-GPU #########################################
##SBATCH --partition=basic
##SBATCH --cpus-per-task=50
#################### END NON-GPU #####################################

# Print the simulation start date/time
date


# Print the node the simulation is running on
echo "I ran on:"
echo "SLURM_NODELIST=$SLURM_NODELIST"

############### Put your code here ######################
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/usr/local/sw/anaconda/anaconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/usr/local/sw/anaconda/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/usr/local/sw/anaconda/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/usr/local/sw/anaconda/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
echo `jupyter lab`

echo "Finished at `date`"


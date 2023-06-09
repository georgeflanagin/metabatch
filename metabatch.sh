function trappipe
{
    :   
}

trap trappipe SIGPIPE

function sbatch
{
    if [ -z $1 ]; then
        echo "Usage: sbatch {slurmfile}"
        return
    fi
    myjob=$(realpath $1);
    old_python_path="$PYTHONPATH";
    export PYTHONPATH="$METABATCHPATH:$PYTHONPATH";
    command pushd "$METABATCHPATH" > /dev/null;
    python sbatch.py $myjob;
    command popd > /dev/null;
    export PYTHONPATH="$old_python_path"
}    

#touch sbatch.temp
#    rm -f sbatch.temp
#    echo "$(whoami),$1" > sbatch.temp
#    cat sbatch.temp > metapipe
#}

function pipereader
{
    while :; do
        echo $(< ./metapipe)
    done
}



function trappipe
{
    :   
}

trap trappipe SIGPIPE

function sbatch
{
    touch sbatch.temp
    rm -f sbatch.temp
    echo "$(whoami),$1" > sbatch.temp
    cat sbatch.temp > metapipe
}

function pipereader
{
    while :; do
        echo $(< ./metapipe)
    done
}



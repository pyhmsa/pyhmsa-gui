#!/bin/bash

set -e

if [ ! -d "$HOME/miniconda" ]; then
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
    bash miniconda.sh -b -f -p $HOME/miniconda
    export PATH="$HOME/miniconda/bin:$PATH"
    hash -r
    conda config --set always_yes yes --set changeps1 no
    conda update -q conda
    conda install -n root _license
else
    export PATH="$HOME/miniconda/bin:$PATH"
    conda update -q conda
fi

# Echo info about conda
conda info -a
conda env list

# Setup variables
testenv=testenv$PYTHON_VERSION
echo "Test environment: $testenv"

requirements=`cat requirements.txt | tr '\n' ' ' | sed 's/pyhmsa//g' | sed 's/qtpy//g'`
echo "Conda requirements: $requirements"

# Create environment if needed
if [[ `conda env list` != *"$testenv"* ]]; then
    conda create -q -n $testenv python=$PYTHON_VERSION
    echo "Conda environment $testenv created"
fi

# Activate environement
source activate $testenv
echo "Conda environment $testenv activated"

# Install requirements
conda install $requirements
pip install qtpy pyhmsa

# Install package
python setup.py develop

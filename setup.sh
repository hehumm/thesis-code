#!/bin/bash

# Download and install Miniconda
CONDA_INSTALLER="Miniconda3-latest-Linux-x86_64.sh"
wget https://repo.anaconda.com/miniconda/$CONDA_INSTALLER -O /tmp/$CONDA_INSTALLER
bash /tmp/$CONDA_INSTALLER -b -p $HOME/miniconda

# Initialize conda
eval "$($HOME/miniconda/bin/conda shell.bash hook)"
conda init

# Clean up
rm /tmp/$CONDA_INSTALLER


conda create -n ag python=3.10
conda activate ag
conda install -c conda-forge mamba
mamba install -c conda-forge autogluon "pytorch=*=cuda*"
mamba install -c conda-forge "ray-tune >=2.6.3,<2.7" "ray-default >=2.6.3,<2.7"  # install ray for faster training
mamba install -c conda-forge pandas
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

# Create and activate the conda environment
conda create -n ag python=3.10 -y
conda activate ag

# Install mamba for faster package management
conda install -c conda-forge mamba -y

# Install necessary packages
mamba install -c conda-forge autogluon "pytorch=*=cuda*" -y
mamba install -c conda-forge "ray-tune >=2.6.3,<2.7" "ray-default >=2.6.3,<2.7" -y
mamba install -c conda-forge pandas -y

# Additional steps (if any) can be added here
# Sets base image to Miniconda3
FROM continuumio/miniconda3
# Changes default shell to Bash
SHELL ["/bin/bash", "-c"]
# Copies current directory to /app
COPY . /app
# Sets working directory to /app
WORKDIR /app
# Updates and cleans up system packages
RUN apt update && apt upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*
# Create the environment
RUN conda env create -n genseqn -f genseqn.yaml
# Installs mamba in the base environment
RUN conda install -n base -c conda-forge mamba
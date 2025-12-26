# `genseqn`: Long-Read Assembly Pipeline

**genseqn** (from genome and sequence) is a comprehensive and modular Snakemake-based pipeline for the automated analysis of long-read sequencing data. It supports raw data from Oxford Nanopore Technologies (ONT) and also enables hybrid assembly workflows combining ONT and Illumina reads. This workflow is based on the protocol by Jun Kim and Chuna Kim (2022), “A beginner’s guide to assembling a draft genome and analyzing structural variants with long-read sequencing technologies”.  

Project: **genseqn was developed as part of a university study.**

## Cite genseqn

If you use genseqn in your research, please cite:

Finke, D. (2025). genseqn: A Snakemake-based workflow for sequence generation and analysis.  
GitHub repository: https://github.com/d11ustn/genseqn

---

## Table of contents
1. [Dependencies](#dependencies)  
2. [DAG Plot Example](#dag-plot-example)  
3. [Install Conda](#install-miniconda-and-mamba)  
4. [Create Environment](#create-environment-and-install-workflow)
5. [Start the Workflow](#load-samples-and-start-the-workflow)  
6. [Run with Docker](#run-with-docker)  
7. [Optional Commands](#optional-commands)  
8. [References](#references)

---

## Dependencies

- [Linux (recommended)](https://ubuntu.com/)  
  The pipeline was developed and tested on the Ubuntu distribution. Linux provides a stable, high-performance environment for running computationally intensive bioinformatics workflows and ensures compatibility with most scientific software.

- [Snakemake](https://snakemake.readthedocs.io/en/stable/)  
  Workflow management system for defining, organizing, and executing reproducible and scalable data analyses. Workflows are described in a readable, Python-based language and executed with automatic handling of dependencies, parallelization, and reproducibility across different computing environments.

- [Conda](https://conda.io/en/latest/index.html)  
  Package and environment manager used to install all required software in isolated environments.

- [Python](https://www.python.org/)  
  Interpreted programming language required as the base for Snakemake and many bioinformatics tools. Python provides the scripting capabilities, modularity, and flexibility needed to integrate multiple steps of the workflow.

- [R (Rscript)](https://www.r-project.org/)  
  Statistical programming language used for downstream analysis, data exploration, and visualization. R supports a wide range of packages for generating publication-ready plots and performing advanced statistical evaluations.

---

## DAG Plot Example 

<img src="documentation/images/DAG-Plot.png" alt="DAG Plot" width="700"/>

**Fig. 1**: The Directed Acyclic Graph (DAG) illustrates the structure of the workflow.    
**Note**: Black rectangles indicate rules that are activated when Illumina data is included.

---

## Install Miniconda and Mamba

This workflow was tested on a [Linux (Ubuntu)](https://ubuntu.com/) system.

### Install Miniconda3  

Download and install Miniconda:

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh
```

### Install Mamba (optional but recommended)

If you do not have Mamba installed in your conda environment.

```bash
conda install -c conda-forge mamba
```

---

## Create environment and install workflow

### Create a working directory for your project:

You can name the folder freely (e.g. genseqn_project) and place it wherever you prefer.

```bash
mkdir -p path/to/project-workdir
cd path/to/project-workdir
```

### Download the Snakemake workflow from GitHub

If you don’t have the workflow yet, you can download it from GitHub.  
**Otherwise, if you already have the data locally, you can skip this step.**

Clone the repository into your project directory:  
Alternatively, you can download the ZIP file from GitHub and unzip it manually.

```bash
git clone https://github.com/d11ustn/genseqn.git
```

### Create the Conda environment

Navigate to the folder containing `genseqn.yaml`, `config/`, and `workflow/`.  
Create the environment and install all required packages using Conda:

```bash
conda env create -n genseqn -f genseqn.yaml
conda activate genseqn
```

Alternatively, using Mamba:

```bash
mamba env create -n genseqn -f genseqn.yaml
mamba activate genseqn
```

---

## Load samples and start the workflow

### Configure `config/config.yaml`

Set the path to your sample directory. **Each sample must follow this folder structure**:

```
project_name/
├── smpl_01/
│   ├── ont/ontfile.fastq.gz
│   └── illumina/
│       ├── illuminafile_1.fastq
│       └── illuminafile_2.fastq
├── smpl_02/
│   ├── ont/ontfile.fastq.gz
│   └── illumina/
│       ├── illuminafile_1.fastq
│       └── illuminafile_2.fastq
├── smpl_03/...
```

Update the following fields in `config/config.yaml`:

```yaml
# genseqn; configuration file: config/config.yaml

# General settings
sample_path: /path/to/dataset/ # Path to folder with sample directories (e.g. smpl_01/ont/ontfile.fastq.gz; smpl_01/illumina/illuminafile_1.fastq; smpl_01/illumina/illuminafile_2.fastq)
project_name: project_name # Project name for your samples (e.g. drosophila_samples)
save_dict: true # Save JSON dictionary file with sample information
illumina_data: true # Enable (true) or disable (false) Illumina data usage
fastqc_memory: "12000" # FASTQC memory in MB (minimum recommended: 8000)
pilon_memory: "32G" # Pilon Java heap memory (minimum recommended: 8G)

# Analyse settings
canu_genome_size: "12m" # Canu genomeSize parameter; determines expected genome size
canu_minInputCoverage: "" # Canu minInputCoverage; default = 10 if empty
canu_stopOnLowCoverage: "" # Canu stopOnLowCoverage; default = 0 if empty
canu_grid: "false" # Canu useGrid (true/false); enable cluster execution
busco_mode: "genome" # BUSCO mode; leave as "genome" for genome analyses
busco_lineage: "eukaryota_odb10" # BUSCO lineage dataset (see https://busco.ezlab.org/list_of_lineages.html)
```

---

### Illumina Data (Optional)

If you also use Illumina data, set:

```yaml
# genseqn; configuration file: config/config.yaml

illumina_data: true # Enable (true) or disable (false) Illumina data usage
pilon_memory: "32G" # Pilon Java heap memory (minimum recommended: 8G)
```

Set `illumina_data: false` if you're only using ONT data.

---

### Load Samples and run Workflow

Load samples via Python script:

```bash
python dataframe.py
```

Run the full workflow using all available cores:

```bash
# Preview workflow
snakemake --use-conda --cores all -n

# Run analysis
snakemake --use-conda --cores all
```

The results will be saved in a subfolder named after your `project_name`.

---

## Run with Docker

### Preparation

1. Create a folder for your project (e.g. `<your_main_folder>`)

2. Inside this folder, create two subfolders:
   - `<your_main_folder>/config/`
   - `<your_main_folder>/results/`

3. Download the default `config/config.yaml` file into the `your_main_folder/config` folder:

```bash
wget https://raw.githubusercontent.com/d11ustn/genseqn/master/config/config.yaml -P config/
```

4. Move your sample folder (e.g. `example_data/`) into `<your_main_folder>`

5. Edit `config/config.yaml` accordingly.

**Important:** When using Docker, set:

```yaml
sample_path: /app/<your_sample_folder>
```

### Pull and Start Docker Image

1. Navigate to your `<your_main_folder>` directory

2. Pull the Docker image:

```bash
docker pull d11ustn/genseqn
```

3. Start the container:

```bash
docker run -it --name genseqn \
  -v /host/path/to/<your_main_folder>/results:/app/results \
  -v /host/path/to/<your_main_folder>/<your_sample_folder>:/app/<your_sample_folder> \
  -v /host/path/to/<your_main_folder>/config:/app/config \
  d11ustn/genseqn:latest
```
**Make sure the full paths are entered correctly!**

**Explanation:**

- `--name` gives the container a custom name
- `-v` binds local folders into the container
- `-it` keeps STDIN open and allocates a pseudo-TTY  
- `"host"` refers to the absolute path on your local system

### Start Workflow in Docker

1. Activate the Conda environment:

```bash
conda activate genseqn
```

2. Load your samples and start the workflow: [Load Samples with Python](#load-samples-and-start-the-workflow)

---

## Optional Commands

**Create a DAG plot (workflow overview):**  
Visualizes workflow dependencies and execution order.

```bash
snakemake --dag | dot -Tpdf -o dag_project_name.pdf
```

---

## References

- Kim, J., & Kim, C. (2022). A beginner’s guide to assembling a draft genome with long-read sequencing. *STAR Protocols*. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9254108/
- Köster, J., & Rahmann, S. (2012). Snakemake: A scalable bioinformatics workflow engine. *Bioinformatics*, 28(19), 2520–2522. https://snakemake.readthedocs.io
- Anaconda, Inc. (2012). *Conda: Package, dependency and environment management for any language.* [https://docs.conda.io](https://docs.conda.io)
- Van Rossum, G., & Drake, F. L. (2009). *Python 3 Reference Manual.* CreateSpace, Scotts Valley, CA. https://www.python.org
- R Core Team. (2023). *R: A Language and Environment for Statistical Computing*. R Foundation for Statistical Computing, Vienna, Austria. Available at: https://www.R-project.org/

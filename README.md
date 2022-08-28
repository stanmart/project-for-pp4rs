# project-for-pp4rs

A small project to fulfil the requirements of the 2020 Programming Practices for Research Students course at UZH.

## Data sources

The publicly available GFTS timetable of ZVV for year 2020.

## Output

A pdf file containing some pretty graphs and some meaningless tables about the ZVV's network.

## How to compile

The project is set up so that snakemake handles the installation of the required dependencies into a local virtual environment. The only external dependencies you need to install are the [conda/mamba](https://docs.conda.io/en/latest/) package manager, a TeX distribution with `pdflatex` available on the path, and the [snakemake](https://snakemake.github.io/) workflow management system. The first two can be installed using your preferred method. It is recommended to install snakemake in its own separate conda virtual environment (e.g. `conda create -c conda-forge -c bioconda -n snakemake snakemake `).

The steps to build the project are described in its snakemake file. If snakemake is installed it can be compiled from scratch by running the `snakemake` command in its root directory:
```bash
    cd /path/to/project-for-pp4rs
    conda activate snakemake
    snakemake --cores N --use-conda
```
assuming that snakemake is available in the conda environment names `snakemake`. `N` is the number of jobs you wish to run in parallel.
# project-for-pp4rs

A small project to fulfil the requirements of the 2020 Programming Practices for Research Students course at UZH.

## Data sources

The publicly available GFTS timetable of ZVV for year 2020.

## Output

A pdf file containing some pretty graphs and some meaningless tables about the ZVV's network.

## How to compile

The project has a [snakemake](https://snakemake.readthedocs.io/en/stable/) file. If snakemake is installed it can be compiled from scratch using the `snakemake` command in its root directory.

Required packages can be installed using your package manager of choice from `requirements.txt`. Alternatively, the script `install_requirements.sh` is provided to install all required packages locally in the project folder using conda. After that `conda activate ./venv` has to be issued before running snakemake.

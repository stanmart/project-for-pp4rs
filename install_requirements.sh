conda create --prefix ./venv python=3.7 \
             --file ./requirements.txt \
             --channel conda-forge \
             --channel bioconda \
             --yes && \
conda activate ./venv && \
pip install -r ./pip-requirements.txt

rem T251 installer
set CONDA_PATH=C:\ProgramData\miniforge3\condabin\conda
set CONDA_ENV_PATH=C:\ATTEST\tools\pyenvs\T251\py38_conda_env

call %CONDA_PATH% create -y --prefix=%CONDA_ENV_PATH% python=3.8 --file requirements.txt -c conda-forge -c anaconda
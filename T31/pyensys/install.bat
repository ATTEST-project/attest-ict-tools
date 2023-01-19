set CONDA_PATH=C:\ProgramData\miniforge3\condabin\conda
set CONDA_ENV_PATH=C:\ATTEST\tools\pyenvs\T31\py39_conda_env

call %CONDA_PATH% create -y --prefix=%CONDA_ENV_PATH% python=3.9

call %CONDA_PATH% activate %CONDA_ENV_PATH%

call %CONDA_ENV_PATH%\python -m pip install --upgrade pip

call pip install --upgrade setuptools

call %CONDA_PATH% install -c conda-forge -y glpk

call %CONDA_PATH% install -c conda-forge -y scikit-learn

call %CONDA_PATH% install -c conda-forge -y --file requirements.txt

call pip install .
rem T41V2 installer
set CONDA_PATH=C:\ProgramData\miniforge3\condabin\conda
set JULIA_PATH=C:\ATTEST\julia-167

set CONDA_ENV_PATH=C:\ATTEST\tools\pyenvs\T41V2\py38_conda_env
set JULIA_DEPOT_PATH=C:\ATTEST\tools\juliaenvs\T41V2\.julia
set JULIA_PROJECT=C:\ATTEST\tools\juliaenvs\T41V2\T41V2_JL_ENV

REM ---------------------------------------

set PYTHON=%CONDA_ENV_PATH%\python.exe
set PATH=%JULIA_PATH%\bin;%PATH%

call %CONDA_PATH% create -y --prefix=%CONDA_ENV_PATH% python=3.8

call %CONDA_PATH% activate %CONDA_ENV_PATH%

call %CONDA_ENV_PATH%\python -m pip install --upgrade pip

call pip install --upgrade setuptools

call %CONDA_PATH% install -y ezodf

call julia --project=%JULIA_PROJECT% install_julia_dependencies.jl




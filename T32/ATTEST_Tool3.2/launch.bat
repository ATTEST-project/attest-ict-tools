rem @echo off
rem set these paths to reflect the target environment
set JULIA_PATH=C:\ATTEST\julia-167
set CONDA_PATH=C:\ProgramData\miniforge3\condabin\conda
set TOOL_PATH=C:\ATTEST\tools\WP3\T32


set CONDA_ENV_PATH=C:\ATTEST\tools\pyenvs\T32\py37_conda_env
set JULIA_DEPOT_PATH=C:\ATTEST\tools\juliaenvs\T32\.julia
set JULIA_PROJECT=C:\ATTEST\tools\juliaenvs\T32\T32_JL_ENV

set PYTHON=%CONDA_ENV_PATH%\python.exe
set PATH=%JULIA_PATH%\bin;%PATH%

call cd %TOOL_PATH%
call %CONDA_PATH% activate %CONDA_ENV_PATH%
call python cli.py run_wp6 --input_file %1 || goto :error

call %CONDA_PATH% deactivate
exit /b 0

:error
echo Failed with error #%errorlevel%.
exit /b %errorlevel%
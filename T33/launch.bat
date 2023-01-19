@echo off

set CONDA_PATH=C:\ProgramData\miniforge3\condabin\conda
set CONDA_ENV_PATH=C:\ATTEST\tools\pyenvs\T33\py38_conda_env
set TOOL_PATH=C:\ATTEST\tools\WP3\T33
rem set IPOPT_BIN_PATH=C:\ATTEST\ipopt\Ipopt-3.14.9-win64-msvs2019-md\bin
rem set PATH=%CPLEX_BIN_PATH%;%IPOPT_BIN_PATH%;%PATH%

call cd %TOOL_PATH%
call %CONDA_PATH% activate %CONDA_ENV_PATH%
call python main_int.py -j %1 || goto :error
call %CONDA_PATH% deactivate
exit /b 0

:error
echo Failed with error #%errorlevel%.
exit /b %errorlevel%
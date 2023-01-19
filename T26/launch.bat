@echo off

set CONDA_PATH=C:\ProgramData\miniforge3\condabin\conda
set CONDA_ENV_PATH=C:\ATTEST\tools\pyenvs\T26\py38_conda_env
set TOOL_PATH=C:\ATTEST\tools\WP2\T26

call cd %TOOL_PATH%
call %CONDA_PATH% activate %CONDA_ENV_PATH%
call python main_int.py --json-file %1 || goto :error
call %CONDA_PATH% deactivate
exit /b 0

:error
echo Failed with error #%errorlevel%.
exit /b %errorlevel%
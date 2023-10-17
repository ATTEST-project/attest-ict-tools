@echo off

set CONDA_PATH="C:\ProgramData\miniforge3\condabin\conda"
set CONDA_ENV_PATH="C:\ATTEST\tools\pyenvs\T53\ATTEST_env"
set TOOL_PATH="C:\ATTEST\tools\WP5\T53\main"

call cd %TOOL_PATH%
call %CONDA_PATH% activate %CONDA_ENV_PATH%
call python main_cl_int.py --json-file %1 || goto :error
call %CONDA_PATH% deactivate
exit /b 0

:error
echo Failed with error #%errorlevel%.
exit /b %errorlevel%

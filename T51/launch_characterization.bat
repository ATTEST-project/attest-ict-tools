@echo off
set XYZ_CURRENT_DIR=%cd%

set CONDA_PATH="C:\ProgramData\miniforge3\condabin\conda"
set CONDA_ENV_PATH="C:\ATTEST\tools\pyenvs\T51\ATTEST_env"
set TOOL_PATH="C:\ATTEST\tools\WP5\T51\Software\main"

echo %DATE% %TIME%

call cd %TOOL_PATH%
call %CONDA_PATH% activate %CONDA_ENV_PATH%
call python characterization_cl_int.py --json-file %1 || goto :error
call %CONDA_PATH% deactivate
cd %XYZ_CURRENT_DIR=%
echo %DATE% %TIME%
exit /b 0

:error
set TOOL_ERROR=%errorlevel%
echo Failed with error #%TOOL_ERROR%.
cd %XYZ_CURRENT_DIR=%
echo %DATE% %TIME%
exit /b %TOOL_ERROR%

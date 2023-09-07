@echo off
setlocal

set CONDA_PATH=C:\ProgramData\miniforge3\condabin\conda
set CONDA_ENV_PATH=C:\ATTEST\tools\pyenvs\T252\py38_conda_env
set TOOL_PATH=C:\ATTEST\tools\WP2\T252

REM Please adapt the CPLEX_BIN_PATH and the IPOPT_BIN_PATH
REM to match the real installation paths and versions
REM (note: do not use quotes in these paths)
set CPLEX_BIN_PATH=C:\Program Files\IBM\ILOG\CPLEX_Studio221\cplex\bin\x64_win64
set IPOPT_BIN_PATH=C:\ATTEST\ipopt\Ipopt-3.14.9-win64-msvs2019-md\bin
set PATH=%CPLEX_BIN_PATH%;%IPOPT_BIN_PATH%;%PATH%

echo %DATE% %TIME%

call cd %TOOL_PATH%
call %CONDA_PATH% activate %CONDA_ENV_PATH%
call python main_int.py --json-file %1 || goto :error
call %CONDA_PATH% deactivate
endlocal
echo %DATE% %TIME%
exit /b 0

:error
echo Failed with error #%errorlevel%.
endlocal
echo %DATE% %TIME%
exit /b %errorlevel%
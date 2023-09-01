@echo off
setlocal

set CONDA_PATH=C:\ProgramData\miniforge3\condabin\conda
set CONDA_ENV_PATH=C:\ATTEST\tools\pyenvs\T31V2\py39_conda_env
set TOOL_PATH=C:\ATTEST\tools\WP3\T31V2\pyensys

call cd %TOOL_PATH%
call %CONDA_PATH% activate %CONDA_ENV_PATH%
call pyensys run-dist_invest %* || goto :error
call %CONDA_PATH% deactivate
endlocal
exit /b 0

:error
echo Failed with error #%errorlevel%.
endlocal
exit /b %errorlevel%

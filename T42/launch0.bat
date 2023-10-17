@echo off
setlocal

set JULIA_PATH="C:\ATTEST\Julia-167\bin\julia.exe"
set JULIA_BINS="C:\ATTEST\Julia-167\bin"
set CONDA_PATH="C:\ProgramData\miniforge3\condabin\conda"

REM PLEASE DO NOT WRAP THE AMPL_PATH IN QUOTES OR DOUBLE QUOTES, OTHERWISE THE PATH SETTING DOES NOT WORK
set AMPL_PATH=C:\ATTEST\ampl_t45
set PATH=%AMPL_PATH%;%JULIA_BINS%;%PATH%

set JULIA_DEPOT_PATH=C:\ATTEST\tools\juliaenvs\T42\.julia
set TOOL_PATH="C:\ATTEST\tools\WP4\T42"
set CONDA_ENV_PATH="C:\ATTEST\tools\pyenvs\T42\py38_conda_env"
set JULIA_PROJECT_PATH="C:\ATTEST\tools\juliaenvs\T42\T42_JL_ENV"

echo %DATE% %TIME%

call cd %TOOL_PATH%
call %CONDA_PATH% activate %CONDA_ENV_PATH%

call %TOOL_PATH%\run_script.bat || goto :error

call %CONDA_PATH% deactivate
endlocal
echo %DATE% %TIME%
exit /b 0

:error
echo Failed with error #%errorlevel%.
endlocal
echo %DATE% %TIME%
exit /b %errorlevel%

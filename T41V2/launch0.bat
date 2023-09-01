set JULIA_PATH="C:\ATTEST\Julia-167\bin\julia.exe"
set CONDA_PATH="C:\ProgramData\miniforge3\condabin\conda"

set JULIA_DEPOT_PATH=C:\ATTEST\tools\juliaenvs\T41V2\.julia
set TOOL_PATH="C:\ATTEST\tools\WP4\T41V2"
set CONDA_ENV_PATH="C:\ATTEST\tools\pyenvs\T41V2\py38_conda_env"
set JULIA_PROJECT_PATH="C:\ATTEST\tools\juliaenvs\T41V2\T41V2_JL_ENV"



call cd %TOOL_PATH%
call %CONDA_PATH% activate %CONDA_ENV_PATH%
call %JULIA_PATH% --project=%JULIA_PROJECT_PATH% main_sc_milp.jl || goto :error
call %CONDA_PATH% deactivate

exit /b 0

:error
echo Failed with error #%errorlevel%.
exit /b %errorlevel%
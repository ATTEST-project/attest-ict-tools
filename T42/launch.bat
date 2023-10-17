@echo off
setlocal

set JULIA_PATH="C:\ATTEST\Julia-167\bin\julia.exe"
set CONDA_PATH="C:\ProgramData\miniforge3\condabin\conda"

REM PLEASE DO NOT WRAP THE AMPL_PATH IN QUOTES OR DOUBLE QUOTES, OTHERWISE THE PATH SETTING DOES NOT WORK
set AMPL_PATH=C:\ATTEST\ampl_t45
set PATH=%AMPL_PATH%;%PATH%

set JULIA_DEPOT_PATH=C:\ATTEST\tools\juliaenvs\T42\.julia
set TOOL_PATH="C:\ATTEST\tools\WP4\T42"
set CONDA_ENV_PATH="C:\ATTEST\tools\pyenvs\T42\py38_conda_env"
set JULIA_PROJECT_PATH="C:\ATTEST\tools\juliaenvs\T42\T42_JL_ENV"

echo %DATE% %TIME%

call cd %TOOL_PATH%
call %CONDA_PATH% activate %CONDA_ENV_PATH%

REM WP6 call parconverter.py, to convert the json input file to a properties file
set json_input_file=%1
set "properties_input_file=%json_input_file:.json=.txt%"
call python parconverter.py %json_input_file% %properties_input_file% || goto :error
REM WP6 read the properties file and set variables according to its content
for /f "delims== tokens=1,2" %%G in (%properties_input_file%) do set %%G=%%H


::Transmission network file
REM WP6 - set matpower_network_file="data\\ES_Dx_03_2020.m"

::Daily PV profile
REM WP6 - set PV_production_profile_file=data\PV_production_diagram.xlsx

::T4.1 data
REM WP6 - set flexibity_devices_states_file=data\procured_flexibility\ES_Dx_03_2030_W_Bd_WithoutFlex_output.xlsx

::State estimation in form of T4.3
REM WP6 - set state_estimation_csv_file=data\state_estimation\ES_Dx_03_2030_S_Bd\ES_Dx_03_2030_S_Bd_t1.csv

::Atctivation from T4.5 real-time transmission tool
REM WP6 - set trans_activation_file=trans_decisions.xlsx

::T4.2 parameters
REM WP6 - set current_time_period=t1

REM WP6 - commented this section, like it is commented for the T4.5 tool. It is reasonable to assume that this conversion has already occurred.
::EV_PV file conversion script
REM WP6 - set EV_PV_file=".\\data\\Output_EV-PV-Storage_Data Baraa.xlsx"
REM WP6 - julia --project=%JULIA_PROJECT_PATH% EV-PV_file_conversion_script.jl %EV_PV_file%

::Select network and year from EV_PV file
REM WP6 - set flex_devices_tech_char_file=data\EVPV_files\ES_Dx_03_2030W.xlsx

::Convert matpower network file
REM WP6 replaced by the nect statement:  julia MATPOWER_to_XLSX.jl %matpower_network_file%
REM WP6 added second parameter to the converter script
call %JULIA_PATH% --project=%JULIA_PROJECT_PATH% MATPOWER_to_XLSX.jl %matpower_network_file% %network_file% || goto :error


REM WP6 replaced by the nect statement: ampl main.run
REM WP6 execute the ampl script
call %AMPL_PATH%\ampl.exe main.run || goto :error


call %CONDA_PATH% deactivate
endlocal
echo %DATE% %TIME%
exit /b 0

:error
echo Failed with error #%errorlevel%.
endlocal
echo %DATE% %TIME%
exit /b %errorlevel%

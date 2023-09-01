@echo off
setlocal

set JULIA_PATH="C:\ATTEST\Julia-167\bin\julia.exe"
set CONDA_PATH="C:\ProgramData\miniforge3\condabin\conda"

REM PLEASE DO NOT WRAP THE AMPL_PATH IN QUOTES OR DOUBLE QUOTES, OTHERWISE THE PATH SETTING DOES NOT WORK
set AMPL_PATH=C:\ATTEST\ampl_t45
set PATH=%AMPL_PATH%;%PATH%

set JULIA_DEPOT_PATH=C:\ATTEST\tools\juliaenvs\T45\.julia
set TOOL_PATH="C:\ATTEST\tools\WP4\T45"
set CONDA_ENV_PATH="C:\ATTEST\tools\pyenvs\T45\py38_conda_env"
set JULIA_PROJECT_PATH="C:\ATTEST\tools\juliaenvs\T45\T45_JL_ENV"

call cd %TOOL_PATH%
call %CONDA_PATH% activate %CONDA_ENV_PATH%

REM WP6 call parconverter.py, to convert the json input file to a properties file
set json_input_file=%1
set "properties_input_file=%json_input_file:.json=.txt%"
call python parconverter.py %json_input_file% %properties_input_file% || goto :error
REM WP6 read the properties file and set variables according to its content
for /f "delims== tokens=1,2" %%G in (%properties_input_file%) do set %%G=%%H


::Transmission network file
rem set matpower_network_file="data\\Transmission_Network_PT_2020.m"

REM WP6 added the excel input file as an additional parameter to the AMPL script
::Transmission network file data (this file is the result of the conversion from matpower_network_file)
rem set network_file=C:\ATSIM\T4523098ASD123K\network_data.xlsx

REM WP6 added the output file for the tool
rem set out_file=C:\ATSIM\T4523098ASD123K\outfile2.xlsx

::Daily PV profile
rem set PV_production_profile_file=C:\ATSIM\T4523098ASD123K\PV_production_diagram.xlsx

::T4.4 data
rem set flexibity_devices_states_file=C:\ATSIM\T4523098ASD123K\procured_flexibility_PT_2050_wf.xlsx
rem set DA_curtailment_file=C:\ATSIM\T4523098ASD123K\PT_2050_wf_Normal.xlsx

::State estimation in form of T4.3
rem set state_estimation_csv_file=C:\ATSIM\T4523098ASD123K\state_estimation.csv

::T4.5 parameters
rem set current_time_period=t1
rem set output_distribution_bus=n1

::EV_PV file conversion script
rem set EV_PV_file=".\\data\\EV-PV-Storage_Data_for_Simulations_old.xlsx"
REM WP6 replaced by the nect statement:  julia EV-PV_file_conversion_script.jl %EV_PV_file%
REM call %JULIA_PATH% --project=%JULIA_PROJECT_PATH% EV-PV_file_conversion_script.jl %EV_PV_file% || goto :error

::Select network and year from EV_PV file
rem set flex_devices_tech_char_file=C:\ATSIM\T4523098ASD123K\PT_Tx_2050.xlsx

::Convert matpower network file
REM WP6 replaced by the nect statement:  julia MATPOWER_to_XLSX.jl %matpower_network_file%
REM WP6 added second parameter to the converter script
call %JULIA_PATH% --project=%JULIA_PROJECT_PATH% MATPOWER_to_XLSX.jl %matpower_network_file% %network_file% || goto :error

REM WP6 replaced by the nect statement: ampl main.run
REM WP6 execute the ampl script
call %AMPL_PATH%\ampl.exe main.run || goto :error

call %CONDA_PATH% deactivate
endlocal
exit /b 0

:error
echo Failed with error #%errorlevel%.
exit /b %errorlevel%

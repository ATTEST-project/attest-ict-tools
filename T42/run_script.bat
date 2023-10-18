::Transmission network file
set matpower_network_file="data\\ES_Dx_03_2020.m"

::Daily PV profile
set PV_production_profile_file=data\PV_production_diagram.xlsx

::T4.1 data
set flexibity_devices_states_file=data\procured_flexibility\ES_Dx_03_2030_W_Bd_WithFlex_output.xlsx

::State estimation in form of T4.3
set state_estimation_csv_file=data\state_estimation\ES_Dx_03_2030_W_Bd\ES_Dx_03_2030_W_Bd_t1.csv

::Atctivation from T4.5 real-time transmission tool
set trans_activation_file=data\trans_decisions\trans_decisions_t1.xlsx

::T4.2 parameters
set current_time_period=t1

::EV_PV file conversion script
::set EV_PV_file=".\\data\\Output_EV-PV-Storage_Data Baraa.xlsx"
::julia --project=%JULIA_PROJECT_PATH% EV-PV_file_conversion_script.jl %EV_PV_file%

::Select network and year from EV_PV file
set flex_devices_tech_char_file=data\EVPV_files\ES_Dx_03_2030W.xlsx

::Convert matpower network file
julia --project=%JULIA_PROJECT_PATH% MATPOWER_to_XLSX.jl %matpower_network_file%

ampl main.run
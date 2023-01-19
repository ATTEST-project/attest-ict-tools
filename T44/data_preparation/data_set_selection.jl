# println("")
# println("Please select the Data Set:")
# # println("Nordic32===>type =1")
# # println("PT_Tx_2020=>type =1")
# println("HR_Tx_01_2020_new_Koprivnica=====>type= 1")
# println("HR_Tx_02_2020_new_NW_Croatia_WP4=>type= 2")
# println("HR_Tx_03_2020_new_Zagreb=========>type= 3")
# println("Transmission_Network_UK_v2=======>type= 4")
# println("Transmission_Network_UK_2020=====>type= 5")
# println("PT_Tx_2020=======================>type= 6")
# println("PT_Tx_2030_Active================>type= 7")
# println("PT_Tx_2030_Slow==================>type= 8")
# println("PT_Tx_2040_Active================>type= 9")
# println("PT_Tx_2040_Slow==================>type= 10")
# println("PT_Tx_2050_Active================>type= 11")
# println("PT_Tx_2050_Slow==================>type= 12")
# 
# println("Which Data SET?")
# test_case = readline()
# test_case = parse(Int64, test_case)
# println("The selected Data Set is:")
# if test_case==1
#     show("HR_Tx_01_2020_new_Koprivnica")
#     nam ="HR_Tx_01_2020_new_Koprivnica"
#     load_correction=1
# elseif test_case==2
#     show("HR_Tx_02_2020_new_NW_Croatia_WP4")
#     nam ="HR_Tx_02_2020_new_NW_Croatia_WP4"
#     load_correction=1
# elseif test_case==3
#     show("HR_Tx_03_2020_new_Zagreb")
#     nam ="HR_Tx_03_2020_new_Zagreb"
#     load_correction=1
# elseif test_case==4
#     show("Transmission_Network_UK_v2")
#     nam ="Transmission_Network_UK_v2"
#     load_correction=1
# elseif test_case==5
#     show("Transmission_Network_UK_2020")
#     nam ="Transmission_Network_UK_2020"
#     load_correction=1
# elseif test_case==6
#     show("PT_Tx_2020")
#     nam = "PT_Tx_2020"
#     load_correction=0.01
# elseif test_case==7
#     show("PT_Tx_2030_Active")
#     nam = "PT_Tx_2030_Active"
#     load_correction=0.01
# elseif test_case==8
#     show("PT_Tx_2030_Slow")
#     nam = "PT_Tx_2030_Slow"
#     load_correction=0.01
# elseif test_case==9
#     show("PT_Tx_2040_Active")
#     nam = "PT_Tx_2040_Active"
#     load_correction=0.01
# elseif test_case==10
#     show("PT_Tx_2040_Slow")
#     nam = "PT_Tx_2040_Slow"
#     load_correction=0.01
# elseif test_case==11
#     show("PT_Tx_2050_Active")
#     nam = "PT_Tx_2050_Active"
#     load_correction=0.01
# elseif test_case==12
#     show("PT_Tx_2050_Slow")
#     nam = "PT_Tx_2050_Slow"
#     load_correction=0.01
# end

# filename =      "input_data/$(nam).ods"
# filename_prof = "input_data/$(nam)_PROF.ods"

filename = get(parameters, "network_file", "")
filename_prof = get(parameters, "auxiliary_file", "")
output_files_prefix = get(parameters, "output_files_prefix", "")
load_correction = get(parameters, "load_correction", "")

println("")

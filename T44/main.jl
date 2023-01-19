@time begin
using JuMP,OdsIO,MathOptInterface,Dates,LinearAlgebra
# using Ipopt
# using BenchmarkTools
# using CPLEX
# using SCIP       # It is not useful for our purpose. Mianly deals with the feasibility problem.
# using AmplNLWriter
# using Cbc

#-------------------Accessing current folder directory--------------------------
println(pwd());
cd(dirname(@__FILE__))
println(pwd());

# files = cd(readdir, string(pwd(),"\\Network_Data"))
#--------------------Read Data from the Excel file------------------------------
println(" For Contin Filtering===>type =0")
println(" For AC-OPF=============>type =1")
println(" For AC-SCOPF===========>type =2")
println(" For DC-SCOPF===========>type =3")
println(" For Security Assessment type =4")
println(" Which problem to solve?")
problem = readline()
problem = parse(Int64, problem)
println("The selected problem is:")
if      problem==0
    show("Contingency Filtering")
elseif    problem==1
    show("AC_OPF")
elseif problem==2
    show("AC_SCOPF")
elseif problem==3
    show("DC_SCOPF")
elseif problem==4
    show("Security Assessment")
end


include("data_preparation\\data_set_selection.jl")

# filename = "input_data/case5_bus_new.ods"
filename_scenario= "input_data/scenario_gen.ods"
# filename_scenario= "scenario_gen.ods"
# filename = "case_34_baran_modf.ods"
include("data_preparation/data_types.jl")      # Reading the structure of network related fields

include("data_preparation/data_types_contingencies.jl")

include("data_preparation/data_reader.jl")     # Function setting the data corresponding to each network quantity

include("data_preparation/interface_excel.jl") # Program saving all the inforamtion related to each entity of a power system


#-----------functions---------------------
include("functions/network_topology_functions.jl")

include("functions/AC_SCOPF_functions.jl")

include("functions/PF_functions_common.jl")
include("functions/PF_functions_n.jl")
include("functions/PF_functions_c.jl")

include("functions/tractable_SCOPF_functions.jl")




#----------------------- Formatting of Network Data ----------------------------
include("data_preparation/contin_scen_arrays.jl")

include("data_preparation/node_data_func.jl")

show("Initial functions are compiled. ")
println("")



if problem==0
    include("repos\\contin_filtering_new.jl")
    show("Set of contingencies are added to $(filename_prof) input file.")
elseif    problem==1
    include("repos\\AC_OPF.jl")
    include("repos\\OPF_out.jl")
elseif problem==2
    include("repos\\AC_SC_OPF.jl")
    include("repos\\SC_OPF_out.jl")
elseif problem==3
    include("repos\\DC_SCOPF.jl")
    include("repos\\SC_OPF_out.jl")
elseif problem==4
    include("repos\\Security_Assessment_tool.jl")
end

end
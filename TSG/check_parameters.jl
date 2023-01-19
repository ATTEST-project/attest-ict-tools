println("Inside main file")

println(parameters)

filename = get(parameters, "input_file", "")
output=""
nsc=10

println(filename)

include("scenario_gen_tool.jl")

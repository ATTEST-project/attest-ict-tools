using Pkg
Pkg.status()
print(ENV["PYTHON"])
print(ENV["JULIA_PROJECT"])
Pkg.generate(ENV["JULIA_PROJECT"])
Pkg.activate(ENV["JULIA_PROJECT"])
Pkg.add("ArgParse")
Pkg.add("JSON")
Pkg.add("JuMP")
Pkg.add("Ipopt")
Pkg.add("MathOptInterface")
Pkg.add("Juniper")
Pkg.add("Plots")
Pkg.add("LinearAlgebra")
Pkg.add("Dates")
Pkg.add("AmplNLWriter")
Pkg.add("Cbc")
Pkg.add("XLSX")
Pkg.add("DataFrames")
Pkg.add("OdsIO")
Pkg.build("OdsIO")
Pkg.status() 
exit(); 

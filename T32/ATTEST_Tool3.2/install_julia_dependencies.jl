using Pkg
Pkg.status()
print(ENV["PYTHON"])
print(ENV["JULIA_PROJECT"])
Pkg.activate(ENV["JULIA_PROJECT"])
Pkg.add(name="PyCall")
Pkg.build("PyCall")
Pkg.add(name="Ipopt")
Pkg.add(name="JLD")
Pkg.add(name="JuMP")
Pkg.add(name="JSON")
Pkg.add(name="OdsIO")
#Pkg.build("OdsIO")
Pkg.add("Dates")
Pkg.add("LinearAlgebra")

Pkg.status() 
exit(); 

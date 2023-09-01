using Pkg
Pkg.status()
print(ENV["JULIA_PROJECT"])
Pkg.generate(ENV["JULIA_PROJECT"])
Pkg.activate(ENV["JULIA_PROJECT"])
Pkg.add("ArgParse")
Pkg.add("JSON")
Pkg.add("PowerModels")
Pkg.add("DataFrames")
Pkg.add("XLSX")
Pkg.status() 
exit(); 

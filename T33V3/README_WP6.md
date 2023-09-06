Notes:
- to test the installation:
  launch demno.json
  
Important: cases under data directory include multiple _params.txt files. Each _params.txt declares configurations for the specific network; 
      Among the configurations is the name and the path to the solver executable to be used e.g.,

         solver = "ipopt"
         linear_solver = "ma27"
         solver_path = "C:\ATTEST\optim\dist\bin\ipopt.exe"
      
It could be necessary to edit the _params.txt files, to reflect ipopt/ma27 installations that differs from C:\ATTEST\optim\dist
		 
		 


        
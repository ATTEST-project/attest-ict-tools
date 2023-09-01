# T31V2 


This version of T31V2 allows you to read parameters from a json file.
It allows to specify files with absolute paths so that no outputs are written to the source tree.

Example:
```bash
launch.bat demo_A_KPC_35_v2c.json
```

The json content is equivalent to the parameter specified here
```bash
pyensys run-dist_invest --case A_KPC_35_v2c.m --growth {'Active':{'2020':0,'2030':2.4,'2040':1.7,'2050':3.9},'Slow':{'2020':0,'2030':2.0,'2040':1.0,'2050':1.0}} --Max_clusters 4 --add_load_data 1 --add_load_data_case_name HR_Dx_01_
```


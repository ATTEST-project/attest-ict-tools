import numpy as np
import pandas as pd
import os
import sys
from pulp import *
from model_selector import *
import config


# todo: choose optimization type
# set variables to True to optimize that market, set to False not to optimize


#energy = sys.argv[1]
#secondary = sys.argv[2]
#tertiary = sys.argv[3]

# energy = True
# secondary = False
# tertiary = False

energy = config.json_config['run_energy']
secondary = config.json_config['run_secondary']
tertiary = config.json_config['run_tertiary']

model_selector(energy, secondary, tertiary)





#energy = True
#secondary = True
#tertiary = True

# to optimize secondary and tertiary markets without optimizing, it is necessary to include aditionally
# gen_val.csv / gen_bids.csv in the respective input data  folder

'''
energy = True
secondary = True
tertiary = True
model_selector(energy, secondary, tertiary)

'''
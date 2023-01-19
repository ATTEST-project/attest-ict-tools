from xlrd import *
from numpy import *
from pyomo.environ import *
from math import *
import pandas as pd
import xlwt
import config


def save_results_aggr(m):

    DF_P_w = pd.DataFrame()
    DF_P_g = pd.DataFrame()
    DF_P_aggr_w_up = pd.DataFrame()
    DF_P_aggr_w_down = pd.DataFrame()
    for v in m.component_objects(Var, active=True):
        for index in v:  # index[0, j, i, t]; v = ve_in_hp,...
            if v.name == 'P_w':
                DF_P_w.at[index] = value(v[index])
            if v.name == 'P_g':
                DF_P_g.at[index] = value(v[index])
            if v.name == 'P_aggr_w_up':
                DF_P_aggr_w_up.at[index] = value(v[index])
            if v.name == 'P_aggr_w_down':
                DF_P_aggr_w_down.at[index] = value(v[index])

    print("...Save data...")
    output_path = os.path.join(config.output_dir, "Bids_aggregator.xls")
    with pd.ExcelWriter(output_path) as writer:
        DF_P_w.to_excel(writer, sheet_name='Electricity energy bid')
        DF_P_g.to_excel(writer, sheet_name='Gas energy bid')
        DF_P_aggr_w_up.to_excel(writer, sheet_name='Upward secondary band')
        DF_P_aggr_w_down.to_excel(writer, sheet_name='Downward secondary band')


    return 0





from xlrd import *
from numpy import *
from pyomo.environ import *



def create_variables(m, number_buildings, load_in_bus_w, load_in_bus_g, load_in_bus_h):
    n_type_buildings = 1
    h = 24

    m.E_neg = Var(arange(h), domain=NonNegativeReals)
    m.E_pos = Var(arange(h), domain=NonNegativeReals)
    m.D_RT = Var(arange(h), domain=NonNegativeReals)
    m.U_RT = Var(arange(h), domain=NonNegativeReals)
    m.E_RT = Var(arange(h), domain=Reals)
    m.b_aggr = Var(arange(h), domain=Binary)
    m.V_D = Var(arange(h), domain=NonNegativeReals)
    m.V_U = Var(arange(h), domain=NonNegativeReals)

    m.G_neg = Var(arange(h), domain=NonNegativeReals)
    m.G_pos = Var(arange(h), domain=NonNegativeReals)
    m.G_RT = Var(arange(h), domain=NonNegativeReals)

    m.P_dso = Var(arange(n_type_buildings), arange(len(load_in_bus_w)), arange(h), domain=Reals)
    m.P_dso_gas = Var(arange(n_type_buildings), arange(len(load_in_bus_g)), arange(h), domain=Reals)
    m.P_dso_heat = Var(arange(n_type_buildings), arange(len(load_in_bus_h)), arange(h), domain=Reals)
    m.P_dso_up = Var(arange(n_type_buildings), arange(len(load_in_bus_w)), arange(h), domain=Reals)
    m.P_dso_down = Var(arange(n_type_buildings), arange(len(load_in_bus_w)), arange(h), domain=Reals)
    m.P_dso_gas_up = Var(arange(n_type_buildings), arange(len(load_in_bus_g)), arange(h), domain=Reals)
    m.P_dso_gas_down = Var(arange(n_type_buildings), arange(len(load_in_bus_g)), arange(h), domain=Reals)
    m.P_dso_heat_up = Var(arange(n_type_buildings), arange(len(load_in_bus_h)), arange(h), domain=Reals)
    m.P_dso_heat_down = Var(arange(n_type_buildings), arange(len(load_in_bus_h)), arange(h), domain=Reals)


    m.P_aggr_w = Var(arange(h), domain=Reals)
    m.P_aggr_g = Var(arange(h), domain=Reals)
    m.P_aggr_w_up = Var(arange(len(load_in_bus_w)), arange(h), domain=Reals)
    m.P_aggr_w_down = Var(arange(len(load_in_bus_w)), arange(h), domain=Reals)


    m.P_w = Var(arange(len(load_in_bus_w)), arange(h), domain=Reals)
    m.P_g = Var(arange(len(load_in_bus_g)), arange(h), domain=Reals)
    m.P_h = Var(arange(len(load_in_bus_h)), arange(h), domain=Reals)
    m.P_hp = Var(arange(number_buildings), arange(h), domain=NonNegativeReals)
    m.P_gb = Var(arange(number_buildings), arange(h), domain=NonNegativeReals)
    m.P_dh = Var(arange(number_buildings), arange(h), domain=NonNegativeReals)
    m.P_ac = Var(arange(number_buildings), arange(h), domain=NonNegativeReals)
    m.P_PV = Var(arange(number_buildings), arange(h), domain=NonNegativeReals)
    m.P_PVr = Var(arange(number_buildings), arange(h), domain=NonNegativeReals)
    m.P_PV_cu = Var(arange(number_buildings), arange(h), domain=NonNegativeReals)
    m.P_sto_ch = Var(arange(number_buildings), arange(h + 1), domain=NonNegativeReals)
    m.P_sto_dis = Var(arange(number_buildings), arange(h + 1), domain=NonNegativeReals)
    m.P_soc = Var(arange(number_buildings), arange(h + 1), domain=NonNegativeReals)
    m.P_inf_load_w = Var(arange(number_buildings), arange(h), domain=Reals)


    m.P_hp_up = Var(arange(number_buildings), arange(h), domain=NonNegativeReals)
    m.P_dh_up = Var(arange(number_buildings), arange(h), domain=NonNegativeReals)
    m.P_ac_up = Var(arange(number_buildings), arange(h), domain=NonNegativeReals)
    m.P_PV_up = Var(arange(number_buildings), arange(h), domain=NonNegativeReals)
    m.P_sto_up = Var(arange(number_buildings), arange(h + 1), domain=NonNegativeReals)
    m.P_w_up = Var(arange(len(load_in_bus_w)), arange(h), domain=Reals)
    m.P_h_up = Var(arange(len(load_in_bus_h)), arange(h), domain=Reals)


    m.P_hp_down = Var(arange(number_buildings), arange(h), domain=NonNegativeReals)
    m.P_dh_down = Var(arange(number_buildings), arange(h), domain=NonNegativeReals)
    m.P_ac_down = Var(arange(number_buildings), arange(h), domain=NonNegativeReals)
    m.P_PV_down = Var(arange(number_buildings), arange(h), domain=NonNegativeReals)
    m.P_sto_down = Var(arange(number_buildings), arange(h + 1), domain=NonNegativeReals)
    m.P_w_down = Var(arange(len(load_in_bus_w)), arange(h), domain=Reals)
    m.P_h_down = Var(arange(len(load_in_bus_h)), arange(h), domain=Reals)


    m.temp_building = Var(arange(number_buildings), arange(h + 1), domain=NonNegativeReals)
    m.temp_building_up = Var(arange(number_buildings), arange(h + 1), domain=NonNegativeReals)
    m.temp_building_down = Var(arange(number_buildings), arange(h + 1), domain=NonNegativeReals)
    m.b_heat = Var(arange(number_buildings), arange(h), domain=Binary)
    m.b_cool = Var(arange(number_buildings), arange(h), domain=Binary)

    m.gen_dh_w = Var(arange(len(load_in_bus_h)), arange(h), domain=NonNegativeReals)
    m.gen_dh_w_up = Var(arange(len(load_in_bus_h)), arange(h), domain=NonNegativeReals)
    m.gen_dh_w_down = Var(arange(len(load_in_bus_h)), arange(h), domain=NonNegativeReals)
    m.gen_dh_g = Var(arange(len(load_in_bus_h)), arange(h), domain=NonNegativeReals)


    return m


def create_variables_power_flow(m, h, branch, load_in_bus_w):
    number_scenarios = 1
    m.PF = Var(arange(number_scenarios), arange(len(branch)), arange(h), domain=Reals)  # purchased power
    m.QF = Var(arange(number_scenarios), arange(len(branch)), arange(h), domain=Reals)  # purchased power
    m.V = Var(arange(number_scenarios), arange(len(load_in_bus_w)), arange(h), domain=Reals)
    m.U = Var(arange(number_scenarios), arange(len(load_in_bus_w)), arange(h), domain=NonNegativeReals)
    m.I = Var(arange(number_scenarios), arange(len(branch)), arange(h), domain=Reals)
    m.Pres = Var(arange(number_scenarios), arange(len(load_in_bus_w)), arange(h), domain=Reals)
    m.Qres = Var(arange(number_scenarios), arange(len(load_in_bus_w)), arange(h), domain=Reals)
    m.V_viol = Var(arange(number_scenarios), arange(len(load_in_bus_w)), arange(h), domain=NonNegativeReals)
    m.net_load = Var(arange(number_scenarios), arange(len(load_in_bus_w)-1), arange(h), domain = Reals)
    m.chp_gen_w = Var(arange(number_scenarios), arange(2), arange(h), domain = NonNegativeReals)



    m.P_dso = Var(arange(number_scenarios), arange(len(load_in_bus_w)), arange(h), domain=Reals)
    m.P_dso_up = Var(arange(number_scenarios), arange(len(load_in_bus_w)), arange(h), domain=Reals)
    m.P_dso_down = Var(arange(number_scenarios), arange(len(load_in_bus_w)), arange(h), domain=Reals)


    return m


def create_variables_power_flow_gas(m, branch, load_in_bus_g):
    h = 1
    m.PF_gas = Var(arange(len(branch)), arange(h), domain=NonNegativeReals, bounds=(1e-20,None), initialize=1e-20)  # purchased power
    m.PF_in = Var(arange(len(branch)), arange(h), domain=NonNegativeReals)  # purchased power
    m.PF_out = Var(arange(len(branch)), arange(h), domain=NonNegativeReals)  # purchased power
    m.Pgen_gas = Var(arange(len(load_in_bus_g)), arange(h), domain=NonNegativeReals)

    m.p2 = Var(arange(len(load_in_bus_g)), arange(h), domain=NonNegativeReals)


    m.P_dso_gas = Var(arange(len(load_in_bus_g)), arange(h), domain=NonNegativeReals)
    m.P_dso_gas_up = Var(arange(len(load_in_bus_g)), arange(h), domain=NonNegativeReals)
    m.P_dso_gas_down = Var(arange(len(load_in_bus_g)), arange(h), domain=NonNegativeReals)


    return m



def create_variables_power_flow_heat(m, m_old, h, t, iter, branch, buses, number_buildings):
    m.P_dso_heat = Var(arange(number_buildings), arange(h), domain=NonNegativeReals)
    if iter > 0:
        for i in range(0, number_buildings):
            m.P_dso_heat[i, 0] = m_old[t].P_dso_heat[i, 0].value
    m.P_dso_heat_up = Var(arange(number_buildings), arange(h), domain=NonNegativeReals)
    if iter > 0:
        for i in range(0, number_buildings):
            m.P_dso_heat_up[i, 0] = m_old[t].P_dso_heat_up[i, 0].value
    m.P_dso_heat_down = Var(arange(number_buildings), arange(h), domain=NonNegativeReals)
    if iter > 0:
        for i in range(0, number_buildings):
            m.P_dso_heat_down[i, 0] = m_old[t].P_dso_heat_down[i, 0].value
    m.h = Var(arange(number_buildings), arange(h), domain=NonNegativeReals)

    m.m = Var(arange(len(branch)), arange(h), domain=NonNegativeReals)
    if iter > 0:
        for i in range(0, len(branch)):
            m.m[i, 0] = m_old[t].m[i, 0].value
    m.mq_gen = Var(arange(len(buses)), arange(h), domain=NonNegativeReals)
    if iter > 0:
        for i in range(0, len(buses)):
            m.mq_gen[i, 0] = m_old[t].mq_gen[i, 0].value
    m.mq_load = Var(arange(len(buses)), arange(h), domain=NonNegativeReals)
    if iter > 0:
        for i in range(0, len(buses)):
            m.mq_load[i, 0] = m_old[t].mq_load[i, 0].value
    m.Ts = Var(arange(len(buses)), arange(h), domain=NonNegativeReals)
    if iter > 0:
        for i in range(0, len(buses)):
            m.Ts[i, 0] = m_old[t].Ts[i, 0].value
    m.To = Var(arange(len(buses)), arange(h), domain=NonNegativeReals)
    if iter > 0:
        for i in range(0, len(buses)):
            m.To[i, 0] = m_old[t].To[i, 0].value
    m.Ts_o = Var(arange(len(buses)), arange(h), domain=NonNegativeReals)
    if iter > 0:
        for i in range(0, len(buses)):
            m.Ts_o[i, 0] = m_old[t].Ts_o[i, 0].value
    m.T_start = Var(arange(len(branch)), arange(h), domain=NonNegativeReals)
    if iter > 0:
        for i in range(0, len(branch)):
            m.T_start[i, 0] = m_old[t].T_start[i, 0].value
    m.T_end = Var(arange(len(branch)), arange(h), domain=NonNegativeReals)
    if iter > 0:
        for i in range(0, len(branch)):
            m.T_end[i, 0] = m_old[t].T_end[i, 0].value
    m.p = Var(arange(len(buses)), arange(h), domain=NonNegativeReals)
    if iter > 0:
        for i in range(0, len(buses)):
            m.p[i, 0] = m_old[t].p[i, 0].value

    m.m_return = Var(arange(len(branch)), arange(h), domain=NonNegativeReals)
    if iter > 0:
        for i in range(0, len(branch)):
            m.m_return[i, 0] = m_old[t].m_return[i, 0].value
    m.p_return = Var(arange(len(buses)), arange(h), domain=NonNegativeReals)
    if iter > 0:
        for i in range(0, len(buses)):
            m.p_return[i, 0] = m_old[t].p_return[i, 0].value
    m.Ts_return = Var(arange(len(buses)), arange(h), domain=NonNegativeReals)
    if iter > 0:
        for i in range(0, len(buses)):
            m.Ts_return[i, 0] = m_old[t].Ts_return[i, 0].value
    m.T_start_return = Var(arange(len(branch)), arange(h), domain=NonNegativeReals)
    if iter > 0:
        for i in range(0, len(branch)):
            m.T_start_return[i, 0] = m_old[t].T_start_return[i, 0].value
    m.T_end_return = Var(arange(len(branch)), arange(h), domain=NonNegativeReals)
    if iter > 0:
        for i in range(0, len(branch)):
            m.T_end_return[i, 0] = m_old[t].T_end_return[i, 0].value

    m.mq_gen_return = Var(arange(len(buses)), arange(h), domain=NonNegativeReals)
    if iter > 0:
        for i in range(0, len(buses)):
            m.mq_gen_return[i, 0] = m_old[t].mq_gen_return[i, 0].value
    m.mq_load_return = Var(arange(len(buses)), arange(h), domain=NonNegativeReals)
    if iter > 0:
        for i in range(0, len(buses)):
            m.mq_load_return[i, 0] = m_old[t].mq_load_return[i, 0].value
    return m


def create_variables_power_flow_heat_update(m, m_old, h, t, iter, branch, buses, number_buildings):

    m.P_dso_heat = Var(arange(number_buildings), arange(h), domain=Reals)
    if iter > 0:
        for i in range(0, number_buildings):
            m.P_dso_heat[i, 0] = m_old.P_dso_heat[i, 0].value
    m.P_dso_heat_up = Var(arange(number_buildings), arange(h), domain=Reals)
    if iter > 0:
        for i in range(0, number_buildings):
            m.P_dso_heat_up[i, 0] = m_old.P_dso_heat_up[i, 0].value
    m.P_dso_heat_down = Var(arange(number_buildings), arange(h), domain=Reals)
    if iter > 0:
        for i in range(0, number_buildings):
            m.P_dso_heat_down[i, 0] = m_old.P_dso_heat_down[i, 0].value
    m.h = Var(arange(number_buildings), arange(h), domain=NonNegativeReals)



    m.m = Var(arange(len(branch)), arange(h), domain = NonNegativeReals)
    if iter > 0:
        for i in range(0, len(branch)):
            m.m[i, 0] = m_old.m[i, 0].value
    m.mq_gen = Var(arange(len(buses)), arange(h), domain = NonNegativeReals)
    if iter > 0:
        for i in range(0, len(buses)):
            m.mq_gen[i, 0] = m_old.mq_gen[i, 0].value
    m.mq_load = Var(arange(len(buses)), arange(h), domain = NonNegativeReals)
    if iter > 0:
        for i in range(0, len(buses)):
            m.mq_load[i, 0] = m_old.mq_load[i, 0].value
    m.Ts = Var(arange(len(buses)), arange(h), domain = NonNegativeReals)
    if iter > 0:
        for i in range(0, len(buses)):
            m.Ts[i, 0] = m_old.Ts[i, 0].value
    m.To = Var(arange(len(buses)), arange(h), domain = NonNegativeReals)
    if iter > 0:
        for i in range(0, len(buses)):
            m.To[i, 0] = m_old.To[i, 0].value
    m.Ts_o = Var(arange(len(buses)), arange(h), domain = NonNegativeReals)
    if iter > 0:
        for i in range(0, len(buses)):
            m.Ts_o[i, 0] = m_old.Ts_o[i, 0].value
    m.T_start = Var(arange(len(branch)), arange(h), domain = NonNegativeReals)
    if iter > 0:
        for i in range(0, len(branch)):
            m.T_start[i, 0] = m_old.T_start[i, 0].value
    m.T_end = Var(arange(len(branch)), arange(h), domain = NonNegativeReals)
    if iter > 0:
        for i in range(0, len(branch)):
            m.T_end[i, 0] = m_old.T_end[i, 0].value
    m.p = Var(arange(len(buses)), arange(h), domain = NonNegativeReals)
    if iter > 0:
        for i in range(0, len(buses)):
            m.p[i, 0] = m_old.p[i, 0].value

    m.m_return = Var(arange(len(branch)), arange(h), domain = NonNegativeReals)
    if iter > 0:
        for i in range(0, len(branch)):
            m.m_return[i, 0] = m_old.m_return[i, 0].value
    m.p_return = Var(arange(len(buses)), arange(h), domain=NonNegativeReals)
    if iter > 0:
        for i in range(0, len(buses)):
            m.p_return[i, 0] = m_old.p_return[i, 0].value
    m.Ts_return = Var(arange(len(buses)), arange(h), domain=NonNegativeReals)
    if iter > 0:
        for i in range(0, len(buses)):
            m.Ts_return[i, 0] = m_old.Ts_return[i, 0].value
    m.T_start_return = Var(arange(len(branch)), arange(h), domain = NonNegativeReals)
    if iter > 0:
        for i in range(0, len(branch)):
            m.T_start_return[i, 0] = m_old.T_start_return[i, 0].value
    m.T_end_return = Var(arange(len(branch)), arange(h), domain = NonNegativeReals)
    if iter > 0:
        for i in range(0, len(branch)):
            m.T_end_return[i, 0] = m_old.T_end_return[i, 0].value
    m.mq_gen_return = Var(arange(len(buses)), arange(h), domain = NonNegativeReals)
    if iter > 0:
        for i in range(0, len(buses)):
            m.mq_gen_return[i, 0] = m_old.mq_gen_return[i, 0].value
    m.mq_load_return = Var(arange(len(buses)), arange(h), domain = NonNegativeReals)
    if iter > 0:
        for i in range(0, len(buses)):
            m.mq_load_return[i, 0] = m_old.mq_load_return[i, 0].value

    m.w_mq_load_Ts = Var(arange(len(buses)), arange(h), domain=NonNegativeReals)
    m.w_mq_gen_To = Var(arange(len(buses)), arange(h), domain=NonNegativeReals)
    m.w_m_T_start = Var(arange(len(branch)), arange(h), domain=NonNegativeReals)
    m.w_m_T_end = Var(arange(len(branch)), arange(h), domain=NonNegativeReals)
    m.w_m_T_start_return = Var(arange(len(branch)), arange(h), domain=NonNegativeReals)
    m.w_m_T_end_return = Var(arange(len(branch)), arange(h), domain=NonNegativeReals)

    return m

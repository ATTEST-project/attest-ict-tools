from xlrd import *
from numpy import *
from pyomo.environ import *



def create_variables(m, h, number_buildings, load_in_bus_w, load_in_bus_g, load_in_bus_h):
    n_type_buildings = 1

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


def create_variables_power_flow(m, m_old, h, t, branch, load_in_bus_w, iter):
    number_scenarios = 1
    m.PF = Var(arange(number_scenarios), arange(len(branch)), arange(h), domain=Reals)  # purchased power
    if iter > 0:
        for i in range(0, len(branch)):
            m.PF[0, i, 0] = m_old[t].PF[0, i, 0].value
    m.QF = Var(arange(number_scenarios), arange(len(branch)), arange(h), domain=Reals)  # purchased power
    if iter > 0:
        for i in range(0, len(branch)):
            m.QF[0, i, 0] = m_old[t].QF[0, i, 0].value
    m.V = Var(arange(number_scenarios), arange(len(load_in_bus_w)), arange(h), domain=Reals)
    if iter > 0:
        for i in range(0, len(load_in_bus_w)):
            m.V[0, i, 0] = m_old[t].V[0, i, 0].value
    m.U = Var(arange(number_scenarios), arange(len(load_in_bus_w)), arange(h), domain=NonNegativeReals)
    if iter > 0:
        for i in range(0, len(load_in_bus_w)):
            m.U[0, i, 0] = m_old[t].U[0, i, 0].value
    m.I = Var(arange(number_scenarios), arange(len(branch)), arange(h), domain=Reals)
    if iter > 0:
        for i in range(0, len(branch)):
            m.I[0, i, 0] = m_old[t].I[0, i, 0].value
    m.Pres = Var(arange(number_scenarios), arange(len(load_in_bus_w)), arange(h), domain=Reals)
    if iter > 0:
        for i in range(0, len(load_in_bus_w)):
            m.Pres[0, i, 0] = m_old[t].Pres[0, i, 0].value
    m.Qres = Var(arange(number_scenarios), arange(len(load_in_bus_w)), arange(h), domain=Reals)
    if iter > 0:
        for i in range(0, len(load_in_bus_w)):
            m.Qres[0, i, 0] = m_old[t].Qres[0, i, 0].value
    m.V_viol = Var(arange(number_scenarios), arange(len(load_in_bus_w)), arange(h), domain=NonNegativeReals)
    if iter > 0:
        for i in range(0, len(load_in_bus_w)):
            m.V_viol[0, i, 0] = m_old[t].V_viol[0, i, 0].value
    m.net_load = Var(arange(number_scenarios), arange(len(load_in_bus_w)-1), arange(h), domain = Reals)
    if iter > 0:
        for i in range(0, len(load_in_bus_w)-1):
            m.net_load[0, i, 0] = m_old[t].net_load[0, i, 0].value
    m.chp_gen_w = Var(arange(number_scenarios), arange(2), arange(h), domain = NonNegativeReals)
    if iter > 0:
        for i in range(0, 2):
            m.chp_gen_w[0, i, 0] = m_old[t].chp_gen_w[0, i, 0].value



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



def create_variables_power_flow_heat(m, m_old, m3_h0, h, t, iter, branch, buses, number_buildings):

    if iter == 0 and t > 0:
        iter = 1
        t = 0
        m_old = m3_h0

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



    m.m = Var(arange(len(branch)), arange(h), domain = NonNegativeReals)
    if iter > 0:
        for i in range(0, len(branch)):
            m.m[i, 0] = m_old[t].m[i, 0].value
    m.mq_gen = Var(arange(len(buses)), arange(h), domain = NonNegativeReals)
    if iter > 0:
        for i in range(0, len(buses)):
            m.mq_gen[i, 0] = m_old[t].mq_gen[i, 0].value
    m.mq_load = Var(arange(len(buses)), arange(h), domain = NonNegativeReals)
    if iter > 0:
        for i in range(0, len(buses)):
            m.mq_load[i, 0] = m_old[t].mq_load[i, 0].value
    m.Ts = Var(arange(len(buses)), arange(h), domain = NonNegativeReals)
    if iter > 0:
        for i in range(0, len(buses)):
            m.Ts[i, 0] = m_old[t].Ts[i, 0].value
    m.To = Var(arange(len(buses)), arange(h), domain = NonNegativeReals)
    if iter > 0:
        for i in range(0, len(buses)):
            m.To[i, 0] = m_old[t].To[i, 0].value
    m.Ts_o = Var(arange(len(buses)), arange(h), domain = NonNegativeReals)
    if iter > 0:
        for i in range(0, len(buses)):
            m.Ts_o[i, 0] = m_old[t].Ts_o[i, 0].value
    m.T_start = Var(arange(len(branch)), arange(h), domain = NonNegativeReals)
    if iter > 0:
        for i in range(0, len(branch)):
            m.T_start[i, 0] = m_old[t].T_start[i, 0].value
    m.T_end = Var(arange(len(branch)), arange(h), domain = NonNegativeReals)
    if iter > 0:
        for i in range(0, len(branch)):
            m.T_end[i, 0] = m_old[t].T_end[i, 0].value
    m.p = Var(arange(len(buses)), arange(h), domain = NonNegativeReals)
    if iter > 0:
        for i in range(0, len(buses)):
            m.p[i, 0] = m_old[t].p[i, 0].value

    m.m_return = Var(arange(len(branch)), arange(h), domain = NonNegativeReals)
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
    m.T_start_return = Var(arange(len(branch)), arange(h), domain = NonNegativeReals)
    if iter > 0:
        for i in range(0, len(branch)):
            m.T_start_return[i, 0] = m_old[t].T_start_return[i, 0].value
    m.T_end_return = Var(arange(len(branch)), arange(h), domain = NonNegativeReals)
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

    m.w_mq_load_Ts = Var(arange(len(buses)), arange(h), domain=NonNegativeReals)
    m.w_mq_gen_To = Var(arange(len(buses)), arange(h), domain=NonNegativeReals)
    m.w_m_T_start = Var(arange(len(branch)), arange(h), domain=NonNegativeReals)
    m.w_m_T_end = Var(arange(len(branch)), arange(h), domain=NonNegativeReals)
    m.w_m_T_start_return = Var(arange(len(branch)), arange(h), domain=NonNegativeReals)
    m.w_m_T_end_return = Var(arange(len(branch)), arange(h), domain=NonNegativeReals)


    return m




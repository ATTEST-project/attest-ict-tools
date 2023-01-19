from xlrd import *
from numpy import *
from pyomo.environ import *
from math import *
import pandas as pd


def run_model_buildings(m, t_main, number_buildings, profile_solar, temp_outside, resources_agr,
                        buses_w, buses_g, buses_h, gen_dh, other_h, DA_bids):

    buildings_with_pv = []
    buildings_with_sto = []
    buildings_with_hp_thermal = []
    buildings_with_dh = []
    buildings_with_dh_thermal = []
    for i in range(0, len(resources_agr)):
        if resources_agr[i]['installed']['PV']:
            buildings_with_pv.append(i + 1)
        if resources_agr[i]['installed']['sto']:
            buildings_with_sto.append(i + 1)
        if resources_agr[i]['installed']['dh'] == 0 and resources_agr[i]['thermal']['R'] > 0:
            buildings_with_hp_thermal.append(i + 1)
        if resources_agr[i]['installed']['dh'] == 1:
            buildings_with_dh.append(i + 1)
            if resources_agr[i]['thermal']['R'] > 0:
                buildings_with_dh_thermal.append(i + 1)


    buses_with_w_gen_dh = []
    buses_with_g_gen_dh = []
    buses_with_gen_dh = []
    if other_h['b_network']:
        for i in range(0, len(gen_dh)):
            if gen_dh[i]['type'] == 'w':
                buses_with_w_gen_dh.append(gen_dh[i]['bus_elec'])
            if gen_dh[i]['type'] == 'g':
                buses_with_g_gen_dh.append(gen_dh[i]['bus_gas'])
            buses_with_gen_dh.append(gen_dh[i]['bus_dh'])

    buildings_w_network = []
    for i in range(0, len(buses_w)):
        for j in range(0, len(buses_w[i])):
            buildings_w_network.append(buses_w[i][j])

    building = resources_agr

    h = 1
    for t in range(t_main, 24):
        ###############################################################################################################
        ###############################################################################################################
        # Market trading and energy balance constraints
        ###############################################################################################################
        ###############################################################################################################

        m.c1.add(m.E_neg[t] - m.E_pos[t] == m.E_RT[t] - DA_bids['DA_w'][t])

        m.c1.add(m.E_neg[t] + m.E_pos[t] <= (1 - m.b_aggr[t]) * 100000)
        m.c1.add(m.D_RT[t] + m.U_RT[t] <= m.b_aggr[t] * (DA_bids['DA_w_down'][t] + DA_bids['DA_w_up'][t]))

        m.c1.add(m.V_D[t] == DA_bids['DA_w_down'][t] - m.D_RT[t])
        m.c1.add(m.V_U[t] == DA_bids['DA_w_up'][t] - m.U_RT[t])

        m.c1.add(m.G_neg[t] - m.G_pos[t] == m.G_RT[t] - DA_bids['DA_gas'][t])


        ###############################################################################################################
        ###############################################################################################################
        # Delivery scenarios constraints
        ###############################################################################################################
        ###############################################################################################################

        # ____________ P electricity ____________________
        for n in range(0, len(buses_w)):
            prov_w = 0
            for j in range(0, number_buildings):
                m.c1.add(m.P_inf_load_w[j, t] == float(building[j]["consumption"]['elec'][t]))
                if j + 1 in buses_w[n]:
                    prov_w = prov_w + float(building[j]["consumption"]['elec'][t]) + m.P_hp[j, t] - m.P_PV[j, t] + \
                             m.P_sto_ch[j, t] - m.P_sto_dis[j, t] + m.P_ac[j, t]

            if n in buses_with_w_gen_dh:
                for k in range(0, len(gen_dh)):
                    if gen_dh[k]['bus_elec'] == n:
                        m.c1.add(m.P_w[n, t] == prov_w + m.gen_dh_w[gen_dh[k]['bus_dh'], t])
            else:
                m.c1.add(m.P_w[n, t] == prov_w)

        m.c1.add(m.E_RT[t] == sum(m.P_w[n, t] for n in range(0, len(buses_w))))

        # ____________ P gas ____________________
        for n in range(0, len(buses_g)):
            prov_g = 0
            for j in range(0, number_buildings):
                if j + 1 in buses_g[n]:
                    prov_g = prov_g + float(building[j]["consumption"]['gas'][t]) + m.P_gb[j, t]

            if n in buses_with_g_gen_dh:
                for k in range(0, len(gen_dh)):
                    if gen_dh[k]['bus_gas'] == n:
                        m.c1.add(m.P_g[n, t] == prov_g + m.gen_dh_g[gen_dh[k]['bus_dh'], t])
            else:
                m.c1.add(m.P_g[n, t] == prov_g)

        m.c1.add(m.G_RT[t] == sum(m.P_g[n, t] for n in range(0, len(buses_g))))

        # ____________ P heat ____________________
        if other_h['b_network']:
            for n in range(0, len(buses_h)):
                prov_dh = 0
                for j in range(0, number_buildings):
                    if j + 1 in buses_h[n]:
                        prov_dh = prov_dh + m.P_dh[j, t]

                if n in buses_with_gen_dh:
                    for k in range(0, len(gen_dh)):
                        if gen_dh[k]['bus_dh'] == n and gen_dh[k]['type'] == 'w':
                            m.c1.add(m.P_h[n, t] == prov_dh + m.gen_dh_w[n, t] * gen_dh[k]['rend'])
                        if gen_dh[k]['bus_dh'] == n and gen_dh[k]['type'] == 'g':
                            m.c1.add(m.P_h[n, t] == prov_dh + m.gen_dh_g[n, t] * gen_dh[k]['rend'])
                else:
                    m.c1.add(m.P_h[n, t] == prov_dh)



        # Reserves
        # ____________ P electricity  up ____________________
        for n in range(0, len(buses_w)):
            prov_w = 0
            for j in range(0, number_buildings):
                if j + 1 in buses_w[n]:
                    prov_w = prov_w + m.P_sto_up[j, t] + m.P_PV_up[j, t] + m.P_hp_up[j, t] + m.P_ac_up[j, t]

            if n in buses_with_w_gen_dh:
                for k in range(0, len(gen_dh)):
                    if gen_dh[k]['bus_elec'] == n:
                        m.c1.add(m.P_w_up[n, t] == m.P_w[n, t] - prov_w - m.gen_dh_w_up[gen_dh[k]['bus_dh'], t])
                        m.c1.add(m.P_aggr_w_up[n, t] == prov_w + m.gen_dh_w_up[gen_dh[k]['bus_dh'], t])
            else:
                m.c1.add(m.P_w_up[n, t] == m.P_w[n, t] - prov_w)
                m.c1.add(m.P_aggr_w_up[n, t] == prov_w)

        m.c1.add(m.U_RT[t] == sum(m.P_aggr_w_up[n, t] for n in range(0, len(buses_w))))

        # ____________ P electricity  down ____________________
        for n in range(0, len(buses_w)):
            prov_w = 0
            for j in range(0, number_buildings):
                if j + 1 in buses_w[n]:
                    prov_w = prov_w + m.P_sto_down[j, t] + m.P_PV_down[j, t] + m.P_hp_down[j, t] + m.P_ac_down[j, t]

            if n in buses_with_w_gen_dh:
                for k in range(0, len(gen_dh)):
                    if gen_dh[k]['bus_elec'] == n:
                        m.c1.add(m.P_w_down[n, t] == m.P_w[n, t] + prov_w + m.gen_dh_w_down[gen_dh[k]['bus_dh'], t])
                        m.c1.add(m.P_aggr_w_down[n, t] == prov_w + m.gen_dh_w_down[gen_dh[k]['bus_dh'], t])
            else:
                m.c1.add(m.P_w_down[n, t] == m.P_w[n, t] + prov_w)
                m.c1.add(m.P_aggr_w_down[n, t] == prov_w)

        m.c1.add(sum(m.P_aggr_w_up[n, t] for n in range(0, len(buses_w))) ==
                 2 * sum(m.P_aggr_w_down[n, t] for n in range(0, len(buses_w))))

        m.c1.add(m.D_RT[t] == sum(m.P_aggr_w_down[n, t] for n in range(0, len(buses_w))))


        if len(buses_with_w_gen_dh) > 0:
            # ____________ P heat up ____________________
            for n in range(0, len(buses_h)):
                prov_dh = 0
                for j in range(0, number_buildings):
                    if j + 1 in buses_h[n]:
                        prov_dh = prov_dh + m.P_dh_up[j, t]

                if n in buses_with_gen_dh:
                    for k in range(0, len(gen_dh)):
                        if gen_dh[k]['bus_dh'] == n and gen_dh[k]['type'] == 'w':
                            m.c1.add(m.P_h_up[n, t] == m.P_h[n, t] - prov_dh - m.gen_dh_w_up[n, t] * gen_dh[k]['rend'])
                else:
                    m.c1.add(m.P_h_up[n, t] == m.P_h[n, t] - prov_dh)

            # ____________ P heat down ____________________
            for n in range(0, len(buses_h)):
                prov_dh = 0
                for j in range(0, number_buildings):
                    if j + 1 in buses_h[n]:
                        prov_dh = prov_dh + m.P_dh_down[j, t]

                if n in buses_with_gen_dh:
                    for k in range(0, len(gen_dh)):
                        if gen_dh[k]['bus_dh'] == n and gen_dh[k]['type'] == 'w':
                            m.c1.add(m.P_h_down[n, t] == m.P_h[n, t] + prov_dh + m.gen_dh_w_down[n, t] * gen_dh[k]['rend'])
                else:
                    m.c1.add(m.P_h_down[n, t] == m.P_h[n, t] + prov_dh)



        ###############################################################################################################
        ###############################################################################################################
        # Delivery scenarios constraints
        ###############################################################################################################
        ###############################################################################################################
        # ____________ P aggregator ____________________
        m.c1.add(m.P_aggr_w[t] == sum(m.P_w[n, t] for n in range(0, len(buses_w))))
        m.c1.add(m.P_aggr_g[t] == sum(m.P_g[n, t] for n in range(0, len(buses_g))))


        ###############################################################################################################
        ###############################################################################################################
        # Resources constraints
        ###############################################################################################################
        ###############################################################################################################
        # ____________ hp = load ____________________
        for j in range(0, number_buildings):
            if building[j]['installed']['hp'] == 1:
                rend = building[j]['rend']['hp']
            elif building[j]['installed']['gb'] == 1:
                rend = building[j]['rend']['gb']
            if building[j]['installed']['ac'] == 1:
                rend_ac = building[j]['rend']['ac']

            if j + 1 not in buildings_w_network:
                m.c1.add(m.P_hp[j, t] == 0)
                m.c1.add(m.P_hp_up[j, t] == 0)
                m.c1.add(m.P_hp_down[j, t] == 0)
                m.c1.add(m.P_gb[j, t] == 0)

            elif j + 1 not in buildings_with_dh:
                if j + 1 in buildings_with_hp_thermal:
                    building_r = building[j]['thermal']['R']
                    alpha = exp(-1/(building[j]['thermal']['R'] * building[j]['thermal']['C']))
                    T_init = building[j]['thermal']['T_init']

                    if building[j]['installed']['hp'] == 1:
                        m.c1.add(m.P_hp[j, t] <= building[j]['limits']['hp'] * m.b_heat[j, t])
                        m.c1.add(m.P_hp[j, t] >= 0)
                        m.c1.add(m.P_hp_down[j, t] <= building[j]['limits']['hp'] * m.b_heat[j, t] - m.P_hp[j, t])
                        m.c1.add(m.P_hp_up[j, t] <= m.P_hp[j, t])
                        m.c1.add(m.P_gb[j, t] == 0)
                    elif building[j]['installed']['gb'] == 1:
                        m.c1.add(m.P_gb[j, t] <= building[j]['limits']['hp'] * m.b_heat[j, t])
                        m.c1.add(m.P_gb[j, t] >= 0)
                        m.c1.add(m.P_hp[j, t] == 0)
                        m.c1.add(m.P_hp_up[j, t] == 0)
                        m.c1.add(m.P_hp_down[j, t] == 0)

                    if building[j]['installed']['ac'] == 1:
                        m.c1.add(m.P_ac[j, t] <= building[j]['limits']['ac'] * m.b_cool[j, t])
                        m.c1.add(m.P_ac[j, t] >= 0)
                        m.c1.add(m.P_ac_down[j, t] <= building[j]['limits']['ac'] * m.b_cool[j, t] - m.P_ac[j, t])
                        m.c1.add(m.P_ac_up[j, t] <= m.P_ac[j, t])
                    else:
                        m.c1.add(m.P_ac[j, t] == 0)
                        m.c1.add(m.P_ac_up[j, t] == 0)
                        m.c1.add(m.P_ac_down[j, t] == 0)

                    m.c1.add(m.b_heat[j, t] + m.b_cool[j, t] == 1)
                    m.c1.add(m.b_heat[j, t] == 1)

                    m.c1.add(m.temp_building[j, t] >= building[j]['thermal']['T_min'][t])
                    m.c1.add(m.temp_building[j, t] <= building[j]['thermal']['T_max'][t])
                    m.c1.add(m.temp_building_up[j, t] >= building[j]['thermal']['T_min'][t])
                    m.c1.add(m.temp_building_up[j, t] <= building[j]['thermal']['T_max'][t])
                    m.c1.add(m.temp_building_down[j, t] >= building[j]['thermal']['T_min'][t])
                    m.c1.add(m.temp_building_down[j, t] <= building[j]['thermal']['T_max'][t])

                    if t == 0:
                        if building[j]['installed']['ac'] == 0:
                            m.c1.add(m.temp_building[j, t] == alpha * T_init + (1 - alpha) *
                                    (temp_outside[t] + building_r * rend * (m.P_hp[j, t] + m.P_gb[j, t])))
                        else:
                            m.c1.add(m.temp_building[j, t] == alpha * T_init + (1 - alpha) *
                                     (temp_outside[t] + building_r * rend * (m.P_hp[j, t] + m.P_gb[j, t]) -
                                      building_r * rend_ac * (m.P_ac[j, t])))

                        if building[j]['installed']['hp'] == 1:
                            if building[j]['installed']['ac'] == 0:
                                m.c1.add(m.temp_building_up[j, t] == alpha * T_init + (1 - alpha) *
                                         (temp_outside[t] + building_r * rend * (m.P_hp[j, t] - m.P_hp_up[j, t])))
                                m.c1.add(m.temp_building_down[j, t] == alpha * T_init + (1 - alpha) *
                                         (temp_outside[t] + building_r * rend * (m.P_hp[j, t] + m.P_hp_down[j, t])))
                            else:
                                m.c1.add(m.temp_building_up[j, t] == alpha * T_init + (1 - alpha) *
                                         (temp_outside[t] + building_r * rend * (m.P_hp[j, t] - m.P_hp_up[j, t]) -
                                          building_r * rend_ac * (m.P_ac[j, t] - m.P_ac_up[j, t])))
                                m.c1.add(m.temp_building_down[j, t] == alpha * T_init + (1 - alpha) *
                                         (temp_outside[t] + building_r * rend * (m.P_hp[j, t] + m.P_hp_down[j, t]) -
                                          building_r * rend_ac * (m.P_ac[j, t] + m.P_ac_down[j, t])))


                else:
                    if building[j]['installed']['hp'] == 1:
                        m.c1.add(m.P_hp[j, t] == building[j]["consumption"]['heat'][t] / rend)
                        m.c1.add(m.P_gb[j, t] == 0)
                    elif building[j]['installed']['gb'] == 1:
                        m.c1.add(m.P_gb[j, t] == building[j]["consumption"]['heat'][t] / rend)
                        m.c1.add(m.P_hp[j, t] == 0)

                    if building[j]['installed']['ac'] == 1:
                        m.c1.add(m.P_ac[j, t] == building[j]["consumption"]['cool'][t] / rend_ac)
                    else:
                        m.c1.add(m.P_ac[j, t] == 0)

                    m.c1.add(m.P_hp_up[j, t] == 0)
                    m.c1.add(m.P_hp_down[j, t] == 0)
                    m.c1.add(m.P_ac_up[j, t] == 0)
                    m.c1.add(m.P_ac_down[j, t] == 0)
                    m.c1.add(m.temp_building[j, t] == 0)
                    m.c1.add(m.temp_building_up[j, t] == 0)
                    m.c1.add(m.temp_building_down[j, t] == 0)
            else:
                m.c1.add(m.P_hp[j, t] == 0)
                m.c1.add(m.P_hp_up[j, t] == 0)
                m.c1.add(m.P_hp_down[j, t] == 0)
                m.c1.add(m.P_gb[j, t] == 0)




        # ____________ DH = load ____________________
        for j in range(0, number_buildings):
            if building[j]['installed']['ac'] == 1:
                rend_ac = building[j]['rend']['ac']

            if j + 1 in buildings_with_dh:
                if j + 1 in buildings_with_dh_thermal:
                    building_r = building[j]['thermal']['R']
                    alpha = exp(-1/(building[j]['thermal']['R']*building[j]['thermal']['C']))
                    T_init = building[j]['thermal']['T_init']

                    m.c1.add(m.P_dh[j, t] <= building[j]['limits']['dh'] * m.b_heat[j, t])
                    m.c1.add(m.P_dh[j, t] >= 0)
                    m.c1.add(m.P_dh[j, t] >= 10 * m.b_heat[j, t])
                    if len(buses_with_w_gen_dh) > 0:
                        m.c1.add(m.P_dh_down[j, t] <= building[j]['limits']['dh'] * m.b_heat[j, t] - m.P_dh[j, t])
                        m.c1.add(m.P_dh_up[j, t] <= m.P_dh[j, t])
                    else:
                        m.c1.add(m.P_dh_down[j, t] == 0)
                        m.c1.add(m.P_dh_up[j, t] == 0)

                    if building[j]['installed']['ac'] == 1:
                        m.c1.add(m.P_ac[j, t] <= building[j]['limits']['ac'] * m.b_cool[j, t])
                        m.c1.add(m.P_ac[j, t] >= 0)
                        m.c1.add(m.P_ac_down[j, t] <= building[j]['limits']['ac'] * m.b_cool[j, t] - m.P_ac[j, t])
                        m.c1.add(m.P_ac_up[j, t] <= m.P_ac[j, t])
                    else:
                        m.c1.add(m.P_ac[j, t] == 0)
                        m.c1.add(m.P_ac_up[j, t] == 0)
                        m.c1.add(m.P_ac_down[j, t] == 0)

                    m.c1.add(m.b_heat[j, t] + m.b_cool[j, t] == 1)
                    m.c1.add(m.b_heat[j, t] == 1)

                    m.c1.add(m.temp_building[j, t] >= building[j]['thermal']['T_min'][t])
                    m.c1.add(m.temp_building[j, t] <= building[j]['thermal']['T_max'][t])
                    m.c1.add(m.temp_building_up[j, t] >= building[j]['thermal']['T_min'][t])
                    m.c1.add(m.temp_building_up[j, t] <= building[j]['thermal']['T_max'][t])
                    m.c1.add(m.temp_building_down[j, t] >= building[j]['thermal']['T_min'][t])
                    m.c1.add(m.temp_building_down[j, t] <= building[j]['thermal']['T_max'][t])

                    if t == 0:
                        if building[j]['installed']['ac'] == 0:
                            m.c1.add(m.temp_building[j, t] == alpha * T_init + (1 - alpha) *
                                     (temp_outside[t] + building_r * (m.P_dh[j, t])))
                        else:
                            m.c1.add(m.temp_building[j, t] == alpha * T_init + (1 - alpha) *
                                     (temp_outside[t] + building_r * (m.P_dh[j, t]) -
                                      building_r * rend_ac * (m.P_ac[j, t])))

                        if len(buses_with_w_gen_dh) > 0:
                            if building[j]['installed']['ac'] == 0:
                                m.c1.add(m.temp_building_up[j, t] == alpha * T_init + (1 - alpha) *
                                         (temp_outside[t] + building_r * (m.P_dh[j, t] - m.P_dh_up[j, t])))


                                m.c1.add(m.temp_building_down[j, t] == alpha * T_init + (1 - alpha) *
                                         (temp_outside[t] + building_r * (m.P_dh[j, t] + m.P_dh_down[j, t])))
                            else:
                                m.c1.add(m.temp_building_up[j, t] == alpha * T_init + (1 - alpha) *
                                         (temp_outside[t] + building_r * (m.P_dh[j, t] - m.P_dh_up[j, t]) -
                                      building_r * rend_ac * (m.P_ac[j, t] - m.P_ac_up[j, t])))

                                m.c1.add(m.temp_building_down[j, t] == alpha * T_init + (1 - alpha) *
                                         (temp_outside[t] + building_r * (m.P_dh[j, t] + m.P_dh_down[j, t]) -
                                      building_r * rend_ac * (m.P_ac[j, t] + m.P_ac_down[j, t])))


                else:
                    m.c1.add(m.P_dh[j, t] == building[j]["consumption"]['heat'][t])
                    m.c1.add(m.P_dh_up[j, t] == 0)
                    m.c1.add(m.P_dh_down[j, t] == 0)

                    if building[j]['installed']['ac'] == 1:
                        m.c1.add(m.P_ac[j, t] == building[j]["consumption"]['cool'][t] / rend_ac)
                    else:
                        m.c1.add(m.P_ac[j, t] == 0)
                    m.c1.add(m.P_ac_up[j, t] == 0)
                    m.c1.add(m.P_ac_down[j, t] == 0)

                    m.c1.add(m.temp_building[j, t] == 0)
                    m.c1.add(m.temp_building_up[j, t] == 0)
                    m.c1.add(m.temp_building_down[j, t] == 0)
            else:
                m.c1.add(m.P_dh[j, t] == 0)
                m.c1.add(m.P_dh_up[j, t] == 0)
                m.c1.add(m.P_dh_down[j, t] == 0)





        # ____________ PV limits____________________
        for j in range(0, number_buildings):
            if j + 1 in buildings_with_pv and j + 1 in buildings_w_network:
                m.c1.add(m.P_PVr[j, t] == building[j]['limits']['PV'] * profile_solar[t])

                m.c1.add(m.P_PV_cu[j, t] <= m.P_PVr[j, t])
                m.c1.add(m.P_PV[j, t] == m.P_PVr[j, t] - m.P_PV_cu[j, t])

                m.c1.add(m.P_PV_up[j, t] <= m.P_PV_cu[j, t])
                m.c1.add(m.P_PV_down[j, t] <= m.P_PVr[j, t] - m.P_PV_cu[j, t])
            else:
                m.c1.add(m.P_PVr[j, t] == 0)
                m.c1.add(m.P_PV_cu[j, t] == 0)
                m.c1.add(m.P_PV[j, t] == 0)
                m.c1.add(m.P_PV_up[j, t] == 0)
                m.c1.add(m.P_PV_down[j, t] == 0)

        # ____________ Storage limits____________________
        for j in range(0, number_buildings):
            if j + 1 in buildings_with_sto:
                soc_max = building[j]['limits']['sto_soc_max']
                soc_min = building[j]['limits']['sto_soc_min']
                P_max = building[j]['limits']['sto_P']
                rend = building[j]['rend']['sto']
                soc_init = building[j]['limits']['sto_soc_init']

                m.c1.add(m.P_sto_ch[j, t] <= P_max)
                m.c1.add(m.P_sto_dis[j, t] <= P_max)
                m.c1.add(m.P_soc[j, t] <= soc_max)
                m.c1.add(m.P_soc[j, t] >= soc_min)

                m.c1.add(m.P_sto_up[j, t] <= P_max - m.P_sto_dis[j, t])
                m.c1.add(m.P_sto_down[j, t] <= P_max - m.P_sto_ch[j, t])

                m.c1.add(m.P_sto_up[j, t] <= (m.P_soc[j, t + 1] - soc_min) * rend)
                m.c1.add(m.P_sto_down[j, t] <= (m.P_soc[j, t + 1] - soc_min) * rend)

                m.c1.add(m.P_sto_up[j, t] <= (soc_max - m.P_soc[j, t + 1]) / rend)
                m.c1.add(m.P_sto_down[j, t] <= (soc_max - m.P_soc[j, t + 1]) / rend)

                m.c1.add(sum(m.P_sto_up[j, t1] + m.P_sto_down[j, t1] for t1 in range(t, 24)) <= sum((P_max - m.P_sto_ch[j, t1] - m.P_sto_dis[j, t1])/2 for t1 in range(t, 24)))

                if t == 0:
                    m.c1.add(m.P_soc[j, t + 1] == soc_init + (m.P_sto_ch[j, t] * rend - m.P_sto_dis[j, t] / rend))
                if t > 0:
                    m.c1.add(m.P_soc[j, t + 1] == m.P_soc[j, t] + (m.P_sto_ch[j, t] * rend - m.P_sto_dis[j, t] / rend))
                if t == 24 - 1:
                    m.c1.add(m.P_soc[j, t + 1] == soc_init)


            else:
                m.c1.add(m.P_sto_ch[j, t] == 0)
                m.c1.add(m.P_sto_dis[j, t] == 0)
                m.c1.add(m.P_soc[j, t] == 0)

                m.c1.add(m.P_sto_up[j, t] == 0)
                m.c1.add(m.P_sto_down[j, t] == 0)

        # ____________ Electrical district heating generators limits____________________
        if other_h['b_network']:
            for n in range(0, len(buses_h)):

                if n in buses_with_gen_dh:
                    for j in range(0, len(gen_dh)):
                        if n == gen_dh[j]['bus_dh']:
                            m.c1.add(m.gen_dh_w[n, t] <= gen_dh[j]['P_max'])
                            m.c1.add(m.gen_dh_w_up[n, t] <= gen_dh[j]['P_max'])
                            m.c1.add(m.gen_dh_w_down[n, t] <= gen_dh[j]['P_max'])
                            m.c1.add(m.gen_dh_w_down[n, t] <= gen_dh[j]['P_max'] - m.gen_dh_w[n, t])
                            m.c1.add(m.gen_dh_w_up[n, t] <= m.gen_dh_w[n, t])
                else:
                    m.c1.add(m.gen_dh_w[n, t] == 0)
                    m.c1.add(m.gen_dh_w_up[n, t] == 0)
                    m.c1.add(m.gen_dh_w_down[n, t] == 0)


                if n in buses_with_g_gen_dh:
                    for j in range(0, len(gen_dh)):
                        if n == gen_dh[j]['bus_dh']:
                            m.c1.add(m.gen_dh_g[n, t] <= gen_dh[j]['P_max'])
                else:
                    m.c1.add(m.gen_dh_g[n, t] == 0)


    return m
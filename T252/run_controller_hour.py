from xlrd import *
from numpy import *
from pyomo.environ import *
from math import *
import pandas as pd
from copy import *

from create_variables import *
from power_flow_heat import *
from optimization import *


def run_controller_hour(t_main, m, m3_h, resources_agr, number_buildings, temperature_outside,
                        P_AGC, P_AGC_control, load_in_bus_w, load_in_bus_h,
                        gen_dh, heat_network, other_h, branch_h, load_h, b_prints, P_soc_buildings):
    building = resources_agr
    m3_old = 0

    buildings_with_pv = []
    buildings_with_sto = []
    buildings_with_hp_thermal = []
    buildings_with_dh = []
    buildings_with_dh_thermal = []
    buildings_with_ac = []
    buildings_with_ac_thermal = []
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
        if resources_agr[i]['installed']['ac'] == 1:
            buildings_with_ac.append(i + 1)
            if resources_agr[i]['thermal']['R'] > 0:
                buildings_with_ac_thermal.append(i + 1)

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
    for i in range(0, len(load_in_bus_w)):
        for j in range(0, len(load_in_bus_w[i])):
            buildings_w_network.append(load_in_bus_w[i][j])

    P_control_hour = []
    P_EH_control_hour = [0 for i in range(0, number_buildings)]
    for t in range(0, 360):
        if b_prints: print("Time - hour:", t_main, ", Time step AGC (0-360):", t)
        P_EH_control = []
        P_AC_control = []
        P_sto_control = []
        P_PV_control = []
        P_DH_gen_control = []
        P_control = 0
        if P_AGC_control[t] > 0:
            # ______________________________________________________________________________________________________
            # ______________________________________________________________________________________________________
            if P_AGC[t] >= m.E_RT[t_main].value:
                ###################################################################################################
                # PV
                ###################################################################################################
                for j in range(0, number_buildings):
                    if j + 1 in buildings_with_pv:
                        P_PV_control.append(m.P_PV[j, t_main].value -
                                            min(P_AGC_control[t] * (m.P_PV_down[j, t_main].value / m.D_RT[t_main].value),
                                                m.P_PV_down[j, t_main].value))
                    else:
                        P_PV_control.append(0)
                ###################################################################################################
                # Sto
                ###################################################################################################
                for j in range(0, number_buildings):
                    if j + 1 in buildings_with_sto:
                        P_sto_control.append((m.P_sto_ch[j, t_main].value - m.P_sto_dis[j, t_main].value) +
                                             min(P_AGC_control[t] * (m.P_sto_down[j, t_main].value / m.D_RT[t_main].value),
                                                 m.P_sto_down[j, t_main].value))
                    else:
                        P_sto_control.append(0)
                ###################################################################################################
                # EH
                ###################################################################################################
                for j in range(0, number_buildings):
                    if j + 1 not in buildings_with_dh:
                        if j + 1 in buildings_with_hp_thermal:
                            P_EH_control.append(m.P_hp[j, t_main].value +
                                                min(P_AGC_control[t] * (m.P_hp_down[j, t_main].value / m.D_RT[t_main].value),
                                                    m.P_hp_down[j, t_main].value))
                        else:
                            P_EH_control.append(m.P_hp[j, t_main].value)
                    else:
                        P_EH_control.append(0)
                ###################################################################################################
                # AC
                ###################################################################################################
                for j in range(0, number_buildings):
                    if j + 1 in buildings_with_ac:
                        if j + 1 in buildings_with_ac_thermal:
                            P_AC_control.append(m.P_ac[j, t_main].value +
                                                min(P_AGC_control[t] * (m.P_ac_down[j, t_main].value / m.D_RT[t_main].value),
                                                    m.P_ac_down[j, t_main].value))
                        else:
                            P_AC_control.append(m.P_ac[j, t_main].value)
                    else:
                        P_AC_control.append(0)
                ###################################################################################################
                # EH distric heating
                ###################################################################################################
                if other_h['b_network']:
                    for j in range(0, len(load_in_bus_w)):
                        if j in buses_with_w_gen_dh:
                            for k in range(0, len(gen_dh)):
                                if gen_dh[k]['bus_elec'] == j:
                                    P_DH_gen_control.append(m.gen_dh_w[gen_dh[k]['bus_dh'], t_main].value +
                                                            min(P_AGC_control[t] *
                                                                (m.gen_dh_w_down[gen_dh[k]['bus_dh'], t_main].value / m.D_RT[
                                                                    t_main].value),
                                                                m.gen_dh_w_down[gen_dh[k]['bus_dh'], t_main].value))
                        else:
                            P_DH_gen_control.append(0)

            # ______________________________________________________________________________________________________
            # ______________________________________________________________________________________________________
            elif P_AGC[t] < m.E_RT[t_main].value:
                ###################################################################################################
                # PV
                ###################################################################################################
                for j in range(0, number_buildings):
                    if j + 1 in buildings_with_pv:
                        P_PV_control.append(m.P_PV[j, t_main].value +
                                            min(P_AGC_control[t] * (m.P_PV_up[j, t_main].value / m.U_RT[t_main].value),
                                                m.P_PV_up[j, t_main].value))
                    else:
                        P_PV_control.append(0)
                ###################################################################################################
                # Sto
                ###################################################################################################
                for j in range(0, number_buildings):
                    if j + 1 in buildings_with_sto:
                        P_sto_control.append((m.P_sto_ch[j, t_main].value - m.P_sto_dis[j, t_main].value) -
                                             min(P_AGC_control[t] * (m.P_sto_up[j, t_main].value / m.U_RT[t_main].value),
                                                 m.P_sto_up[j, t_main].value))
                    else:
                        P_sto_control.append(0)
                ###################################################################################################
                # EH
                ###################################################################################################
                for j in range(0, number_buildings):
                    if j + 1 not in buildings_with_dh:
                        if j + 1 in buildings_with_hp_thermal:
                            P_EH_control.append(m.P_hp[j, t_main].value -
                                                min(P_AGC_control[t] * (m.P_hp_up[j, t_main].value / m.U_RT[t_main].value),
                                                    m.P_hp_up[j, t_main].value))
                        else:
                            P_EH_control.append(m.P_hp[j, t_main].value)
                    else:
                        P_EH_control.append(0)
                ###################################################################################################
                # AC
                ###################################################################################################
                for j in range(0, number_buildings):
                    if j + 1 in buildings_with_ac:
                        if j + 1 in buildings_with_ac_thermal:
                            P_AC_control.append(m.P_ac[j, t_main].value -
                                                min(P_AGC_control[t] * (m.P_ac_up[j, t_main].value / m.U_RT[t_main].value),
                                                    m.P_ac_up[j, t_main].value))
                        else:
                            P_AC_control.append(m.P_ac[j, t_main].value)
                    else:
                        P_AC_control.append(0)
                ###################################################################################################
                # EH distric heating
                ###################################################################################################
                if other_h['b_network']:
                    for j in range(0, len(load_in_bus_w)):
                        if j in buses_with_w_gen_dh:
                            for k in range(0, len(gen_dh)):
                                if gen_dh[k]['bus_elec'] == j:
                                    P_DH_gen_control.append(m.gen_dh_w[gen_dh[k]['bus_dh'], t_main].value -
                                                            min(P_AGC_control[t] *
                                                                (m.gen_dh_w_up[gen_dh[k]['bus_dh'], t_main].value / m.U_RT[
                                                                    t_main].value),
                                                                m.gen_dh_w_up[gen_dh[k]['bus_dh'], t_main].value))
                        else:
                            P_DH_gen_control.append(0)
        # ______________________________________________________________________________________________________
        # ______________________________________________________________________________________________________
        else:
            for j in range(0, number_buildings):
                P_PV_control.append(m.P_PV[j, t_main].value)
                P_sto_control.append(m.P_sto_ch[j, t_main].value - m.P_sto_dis[j, t_main].value)
                P_EH_control.append(m.P_hp[j, t_main].value)
                P_AC_control.append(m.P_ac[j, t_main].value)

            if other_h['b_network']:
                for j in range(0, len(load_in_bus_w)):
                    if j in buses_with_w_gen_dh:
                        for k in range(0, len(gen_dh)):
                            if gen_dh[k]['bus_elec'] == j:
                                P_DH_gen_control.append(m.gen_dh_w[gen_dh[k]['bus_dh'], t_main].value)
                    else:
                        P_DH_gen_control.append(0)


        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        # SOC Update
        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        P_soc_buildings_prov = []
        for j in range(0, number_buildings):
            if j + 1 in buildings_with_sto:
                rend = building[j]['rend']['sto']
                soc_max = building[j]['limits']['sto_soc_max']
                soc_min = building[j]['limits']['sto_soc_min']

                if t_main == 0 and t == 0:
                    T_init = building[j]['limits']['sto_soc_init']
                else:
                    T_init = P_soc_buildings[j]

                if P_sto_control[j] > 0:
                    P_soc = T_init + P_sto_control[j] * rend / 360
                    if P_soc > soc_max:
                        P_sto_control[j] = P_sto_control[j] - (P_soc - soc_max)
                        P_soc = soc_max
                    P_soc_buildings_prov.append(P_soc)
                elif P_sto_control[j] < 0:
                    P_soc = T_init + P_sto_control[j] / rend / 360
                    if P_soc < soc_min:
                        P_sto_control[j] = P_sto_control[j] - (soc_min - P_soc)
                        P_soc = soc_min
                    P_soc_buildings_prov.append(P_soc)
                else:
                    P_soc = T_init
                    P_soc_buildings_prov.append(P_soc)
            else:
                P_soc_buildings_prov.append(0)
        P_soc_buildings = deepcopy(P_soc_buildings_prov)



        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        # Thermal buildings Update
        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        for j in range(0, number_buildings):
            if j + 1 not in buildings_with_dh:
                if j + 1 in buildings_with_hp_thermal:
                    P_EH_control_hour[j] = P_EH_control_hour[j] + P_EH_control[j]



        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        # Temperature Update
        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        if other_h['b_network']:
            if P_AGC[t] > 0 and P_AGC[t] < 0:
                for i in range(0, len(gen_dh)):
                    if gen_dh[i]['type'] == 'w':
                        buses_with_w_gen_dh.append(gen_dh[i]['bus_elec'])
                    if gen_dh[i]['type'] == 'g':
                        buses_with_g_gen_dh.append(gen_dh[i]['bus_gas'])
                    buses_with_gen_dh.append(gen_dh[i]['bus_dh'])

                # __________________________________________________________________________________________________
                # New DH generation control

                P_DH_gen_control_h = [0 for i in range(0, len(load_in_bus_h))]
                for i in range(0, len(load_in_bus_h)):
                    for j in range(0, len(gen_dh)):
                        if gen_dh[j]['bus_dh'] == i:
                            P_DH_gen_control_h[i] = P_DH_gen_control[int(gen_dh[j]['bus_elec'])] * gen_dh[j]['rend']

                # __________________________________________________________________________________________________
                # Factor of new generation and old generation
                P_gen_dh = []
                for i in range(0, len(load_in_bus_h)):
                    if i in buses_with_gen_dh:
                        P_gen_dh.append(m3_h[0].P_dso_heat[i, 0].value)
                factor_gen_dh = sum(P_DH_gen_control_h) / sum(P_gen_dh)

                # __________________________________________________________________________________________________
                aux_P_load_flex_new = []
                for i in range(0, number_buildings):
                    if i + 1 in buildings_with_dh_thermal:
                        aux_P_load_flex_new.append(m.P_dh[i, t_main].value * factor_gen_dh)
                    else:
                        aux_P_load_flex_new.append(m.P_dh[i, t_main].value)

                # __________________________________________________________________________________________________
                aux_P_bus_h_load = []
                for i in range(0, len(load_in_bus_h)):
                    aux1 = 0
                    for j in range(0, number_buildings):
                        if j + 1 in load_in_bus_h[i]:
                            aux1 = aux1 + aux_P_load_flex_new[j]
                    aux_P_bus_h_load.append(aux1)

                # __________________________________________________________________________________________________
                # Calculation of heat energy distributed through the district heating
                flag_error = 1
                while flag_error:
                    m3 = ConcreteModel()
                    m3.c1 = ConstraintList()

                    m3 = create_variables_power_flow_heat_update(m3, m3_old, 1, 0, t, branch_h, load_in_bus_h, number_buildings)
                    m3 = power_flow_heat_update(m3, m, t, 0, branch_h, load_h, load_in_bus_h, resources_agr, heat_network,
                                                other_h,
                                                P_DH_gen_control_h)

                    m3, flag_error = optimization_dso_heat_update(m3, m, t_main, t, load_in_bus_h, b_prints, aux_P_bus_h_load,
                                                                  buses_with_gen_dh)
                m3_old = m3

                P_dh_load_control = [0 for i in range(0, number_buildings)]
                for i in range(0, len(load_in_bus_h)):
                    aux_dh_load_fix = 0
                    aux_dh_load_flex = 0
                    for j in range(0, len(load_in_bus_h[i])):
                        for k in range(0, number_buildings):
                            if k + 1 == load_in_bus_h[i][j] and k + 1 not in buildings_with_dh_thermal:
                                aux_dh_load_fix = aux_dh_load_fix + m.P_dh[k, t_main].value
                            elif k + 1 == load_in_bus_h[i][j]:
                                aux_dh_load_flex = aux_dh_load_flex + m.P_dh[k, t_main].value
                    for j in range(0, len(load_in_bus_h[i])):
                        for k in range(0, number_buildings):
                            if k + 1 == load_in_bus_h[i][j] and k + 1 not in buildings_with_dh_thermal:
                                P_dh_load_control[k] = m.P_dh[k, t_main].value
                            elif k + 1 == load_in_bus_h[i][j]:
                                P_dh_load_control[k] = m.P_dh[k, t_main].value * (
                                            m3.P_dso_heat[i, 0].value - aux_dh_load_fix) / (
                                                                   m3_h[0].P_dso_heat[i, 0].value - aux_dh_load_fix)

                # ____________ DH = load ____________________
                for j in range(0, number_buildings):
                    if j + 1 in buildings_with_dh:
                        if j + 1 in buildings_with_dh_thermal:
                            T_init = building[j]['thermal']['T_init']
                            building_r = building[j]['thermal']['R']
                            alpha = exp(- (10 / 3600) / (building[j]['thermal']['R'] * building[j]['thermal']['C']))
                            building[j]['thermal']['t_init'] = alpha * T_init + (1 - alpha) * (
                                        temperature_outside[t_main] + building_r * P_dh_load_control[j])


            else:
                P_dh_load_control = [0 for i in range(0, number_buildings)]
                for i in range(0, len(load_in_bus_h)):
                    for j in range(0, len(load_in_bus_h[i])):
                        for k in range(0, number_buildings):
                            if k + 1 == load_in_bus_h[i][j] and k + 1 not in buildings_with_dh_thermal:
                                P_dh_load_control[k] = m.P_dh[k, t_main].value
                            elif k + 1 == load_in_bus_h[i][j]:
                                P_dh_load_control[k] = m.P_dh[k, t_main].value

                for j in range(0, number_buildings):
                    if j + 1 in buildings_with_dh:
                        if j + 1 in buildings_with_dh_thermal:
                            T_init = building[j]['thermal']['T_init']
                            building_r = building[j]['thermal']['R']
                            alpha = exp(- (10 / 3600) / (building[j]['thermal']['R'] * building[j]['thermal']['C']))
                            building[j]['thermal']['t_init'] = alpha * T_init + (1 - alpha) * (
                                        temperature_outside[t_main] + building_r * P_dh_load_control[j])


        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        # Sum all resources
        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

        for j in range(0, number_buildings):
            if j + 1 in buildings_w_network:
                P_control = P_control + resources_agr[j]["consumption"]['elec'][t_main]
                P_control = P_control - P_PV_control[j]
                P_control = P_control + P_sto_control[j]
                P_control = P_control + P_EH_control[j]
                P_control = P_control + P_AC_control[j]

        if other_h['b_network']:
            for j in range(0, len(load_in_bus_w)):
                P_control = P_control + P_DH_gen_control[j]

        P_control_hour.append(P_control)

    # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    # Thermal buildings Update
    # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

    for j in range(0, number_buildings):
        if building[j]['installed']['hp'] == 1:
            rend = building[j]['rend']['hp']
        elif building[j]['installed']['gb'] == 1:
            rend = building[j]['rend']['gb']
        if building[j]['installed']['ac'] == 1:
            rend_ac = building[j]['rend']['ac']
        if j + 1 not in buildings_with_dh:
            if j + 1 in buildings_with_hp_thermal:
                building_r = building[j]['thermal']['R']
                alpha = exp(- (1) / (building[j]['thermal']['R'] * building[j]['thermal']['C']))
                if building[j]['installed']['ac'] == 0:
                    building[j]['thermal']['T_init'] = alpha * building[j]['thermal']['T_init'] + (1 - alpha) * (
                            temperature_outside[t_main] + building_r *
                            (P_EH_control_hour[j] / 360 + m.P_gb[j, t_main].value))
                else:
                    building[j]['thermal']['T_init'] = alpha * building[j]['thermal']['T_init'] + (1 - alpha) * (
                            temperature_outside[t_main] + building_r *
                            (P_EH_control_hour[j] / 360 + m.P_gb[j, t_main].value) - building_r * rend_ac * (m.P_ac[j, t_main].value))


    return P_control_hour, P_soc_buildings, building




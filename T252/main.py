from xlrd import *
from numpy import *
from pyomo.environ import *
from math import *
import pandas as pd
import csv
from time import *
from copy import *
import sys
#sys.stdout = open('C:\\Users\\amfcc\\OneDrive - INESC TEC\\INESC TEC\\MES\\Tese\\2.4 - Operation of Gas and district heating networks\\MyCode - Limpeza\\Real-Time\\Real-time tool - Cópia\\log.txt', 'w')


from Initialization import initialization
from create_variables import *
from run_model import *
from optimization import *
from power_flow import *
from power_flow_gas import *
from power_flow_heat import *
from calculate_criteria import *
from print_results import *
from save_results import *
from run_controller_hour import *


def main():

    # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    #    Initialize case and settings
    # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    h = 1
    n_scenarios = 3
    b_prints = 1

    electrical_network, gas_network, heat_network, resources, weather, prices, admm, DA_bids, AGC = initialization()


    # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    #    Initial organization
    # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

    branch_w = electrical_network['branch_w']
    load_in_bus_w = electrical_network['load_in_bus_w']
    other_w = electrical_network['other_w']

    other_g = gas_network['other_g']
    if other_g['b_network']:
        branch_g = gas_network['branch_g']
        load_in_bus_g = gas_network['load_in_bus_g']
    else:
        branch_g = []
        load_in_bus_g = []


    other_h = heat_network['other_h']
    if other_h['b_network']:
        branch_h = heat_network['branch_h']
        load_in_bus_h = heat_network['load_in_bus_h']
        gen_dh = heat_network['gen_dh']
    else:
        branch_h = []
        load_in_bus_h = []
        gen_dh = []



    load_w = resources['load_w']
    load_g = resources['load_g']
    load_h = resources['load_h']
    resources_agr = resources['resouces_aggregator']
    number_buildings = len(resources_agr)
    for i in range(0, len(resources_agr)):
        resources_agr[i]['consumption']['elec'] = load_w[i]
        resources_agr[i]['consumption']['gas'] = load_g[i]
        resources_agr[i]['consumption']['heat'] = load_h[i]

    profile_solar = weather['profile_solar']
    temperature_outside = weather['temperature_outside']


    ro = {'ro': admm['ro']}
    criteria_final = admm['criteria_final']

    print("")
    print('...Initialization completed...')
    print("")








    # ##################################################################################################################
    # ##################################################################################################################
    # ##################################################################################################################
    # ##################################################################################################################
    #    Deterministic optimization
    # ##################################################################################################################
    # ##################################################################################################################
    # ##################################################################################################################
    # ##################################################################################################################

    print("")
    print('... Starting ADMM ...')
    print("")
    m_h = []
    m_final_results = []
    P_control_day = []
    P_soc_buildings = 0
    m_h = []
    for t_main in range(0, 24):
        print("#####################################################################################################")
        print("#     Time ", t_main)
        print("#####################################################################################################")

        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        #    ADMM initialization
        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        criteria_h = []
        criteria_dual_h = []

        pi = {'w': [], 'g': [], 'h': [], 'w_up': [], 'g_up': [], 'h_up': [], 'w_down': [], 'g_down': [], 'h_down': []}

        pi['w_up'] = [[0 for i in range(0, h)] for i in range(0, len(load_in_bus_w))]
        pi['w_down'] = [[0 for i in range(0, h)] for i in range(0, len(load_in_bus_w))]
        pi['g'] = [[0 for i in range(0, h)] for i in range(0, len(load_in_bus_g))]
        if other_h['b_network']:
            pi['h'] = [[0 for i in range(0, h)] for i in range(0, len(load_in_bus_h))]
            pi['h_up'] = [[0 for i in range(0, h)] for i in range(0, len(load_in_bus_h))]
            pi['h_down'] = [[0 for i in range(0, h)] for i in range(0, len(load_in_bus_h))]

        Pa = {'w': [], 'g': [], 'h': [], 'w_up': [], 'g_up': [], 'h_up': [], 'w_down': [], 'g_down': [], 'h_down': []}
        Pa['w_up'] = [[1 for i in range(0, h)] for i in range(0, len(load_in_bus_w))]
        Pa['w_down'] = [[1 for i in range(0, h)] for i in range(0, len(load_in_bus_w))]
        Pa['g'] = [[1 for i in range(0, h)] for i in range(0, len(load_in_bus_g))]
        if other_h['b_network']:
            Pa['h'] = [[1 for i in range(0, h)] for i in range(0, len(load_in_bus_h))]
            Pa['h_up'] = [[1 for i in range(0, h)] for i in range(0, len(load_in_bus_h))]
            Pa['h_down'] = [[1 for i in range(0, h)] for i in range(0, len(load_in_bus_h))]

        P_dso_w_up = []
        P_dso_w_down = []
        P_dso_g = []
        P_dso_h = []
        P_dso_h_up = []
        P_dso_h_down = []

        flag = 0
        k = 0
        iter = 0
        m3_h = []
        start = time()
        count = 5

        ro = {'ro': 0.0001}

        while flag == 0:
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            #    Run aggregator model
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            if b_prints:
                print("")
                print("#####################################################################################################")
                print("#     Iteration ", iter)
                print("#     Time ", t_main)
                print("#####################################################################################################")


                print("")
                print("______ Run Model Aggregator ______")

            m = ConcreteModel()
            m.c1 = ConstraintList()

            m = create_variables(m, number_buildings, load_in_bus_w, load_in_bus_g, load_in_bus_h)

            m = run_model_buildings(m, t_main, number_buildings, profile_solar, temperature_outside, resources_agr,
                                    load_in_bus_w, load_in_bus_g, load_in_bus_h, gen_dh, other_h, DA_bids)

            m = optimization_aggregator(m, t_main, prices, 0, iter, pi, ro, Pa, load_in_bus_w, load_in_bus_g, load_in_bus_h,
                                        other_g, other_h, b_prints)

            if b_prints: print_results_aggregator(m, t_main, load_in_bus_w, load_in_bus_g, load_in_bus_h)





            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            #    Run electricity DSO model
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            if b_prints:
                print("")
                print("______ Run Electricity DSO Flow Model ______")

            P_dso_w = []
            P_dso_old_w_up = deepcopy(P_dso_w_up)
            P_dso_w_up = []
            P_dso_old_w_down = deepcopy(P_dso_w_down)
            P_dso_w_down = []
            m1_h = []
            m1_h_up = []
            m1_h_down = []

            for s in range(1, 3):
                if b_prints:
                    print("")
                    if s == 0:
                        print("______ Scenario Energy ______")
                    elif s == 1:
                        print("______ Scenario Up ______")
                    elif s == 2:
                        print("______ Scenario Down ______")

                for t in range(0, h):
                    m1 = ConcreteModel()
                    m1.c1 = ConstraintList()
                    m1 = create_variables_power_flow(m1, h, branch_w, load_in_bus_w)

                    m1 = power_flow_elec(m1, s, branch_w, load_in_bus_w, other_w)


                    if s == 0:
                        m1 = optimization_dso(m1, m, t, pi, ro, load_in_bus_w, b_prints)
                        m1_h.append(m1)

                        P_dso_prov_w = []
                        for i in range(0, len(load_in_bus_w)):
                            P_dso_prov_w.append(m1.P_dso[k, i, 0].value)
                        P_dso_w.append(P_dso_prov_w)


                    elif s == 1:
                        m1 = optimization_dso_up(m1, m, t, pi, ro, load_in_bus_w, b_prints)
                        m1_h_up.append(deepcopy(m1))

                        P_dso_prov_w_up = []
                        for i in range(0, len(load_in_bus_w)):
                            P_dso_prov_w_up.append(m1.P_dso_up[k, i, 0].value)
                        P_dso_w_up.append(P_dso_prov_w_up)

                    elif s == 2:
                        m1 = optimization_dso_down(m1, m, t, pi, ro, load_in_bus_w, b_prints)
                        m1_h_down.append(deepcopy(m1))

                        P_dso_prov_w_down = []
                        for i in range(0, len(load_in_bus_w)):
                            P_dso_prov_w_down.append(deepcopy(m1.P_dso_down[k, i, 0].value))
                        P_dso_w_down.append(P_dso_prov_w_down)



            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            #    Run gas DSO model
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            if other_g['b_network']:
                if b_prints:
                    print("")
                    print("______ Run Gas DSO Flow Model ______")

                P_dso_old_g = deepcopy(P_dso_g)
                P_dso_g = []
                m2_h = []

                for s in range(0, 1):
                    if b_prints:
                        print("")
                        if s == 0:
                            print("______ Scenario Energy ______")
                        elif s == 1:
                            print("______ Scenario Up ______")
                        elif s == 2:
                            print("______ Scenario Down ______")

                    for t in range(0, h):
                        m2 = ConcreteModel()
                        m2.c1 = ConstraintList()

                        m2 = create_variables_power_flow_gas(m2, branch_g, load_in_bus_g)
                        m2 = power_flow_gas(m2, m, t, s, branch_g, load_in_bus_g, other_g)

                        if s == 0:
                            m2 = optimization_dso_gas(m2, m, t, pi, ro, load_in_bus_g, b_prints)
                            m2_h.append(m2)

                            P_dso_prov_g = []
                            for i in range(0, len(load_in_bus_g)):
                                P_dso_prov_g.append(m2.P_dso_gas[i, 0].value)
                            P_dso_g.append(P_dso_prov_g)

            else:
                P_dso_old_g = []
                m2_h = []

            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            #    Run heat DSO model
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            if other_h['b_network']:
                if b_prints:
                    print("")
                    print("______ Run Heat DSO Flow Model ______")

                P_dso_old_h = deepcopy(P_dso_h)
                P_dso_h = []
                P_dso_old_h_up = deepcopy(P_dso_h_up)
                P_dso_h_up = []
                P_dso_old_h_down = deepcopy(P_dso_h_down)
                P_dso_h_down = []
                m3_old = deepcopy(m3_h)
                m3_h = []
                m3_h_up = []
                m3_h_down = []

                for s in range(0, 3):
                    if b_prints:
                        print("")
                        if s == 0:
                            print("______ Scenario Energy ______")
                        elif s == 1:
                            print("______ Scenario Up ______")
                        elif s == 2:
                            print("______ Scenario Down ______")

                    for t in range(0, h):
                        flag_error = 1

                        while flag_error:
                            m3 = ConcreteModel()
                            m3.c1 = ConstraintList()

                            m3 = create_variables_power_flow_heat(m3, m3_old, 1, t, iter, branch_h, load_in_bus_h, number_buildings)
                            m3 = power_flow_heat(m3, m, t_main, s, branch_h, load_h, load_in_bus_h, resources_agr,  heat_network, other_h)

                            if s == 0:
                                m3, flag_error = optimization_dso_heat(m3, m, t, pi, ro, load_in_bus_h, b_prints)
                                if flag_error == 0:
                                    m3_h.append(m3)

                                    P_dso_prov_gen = []
                                    for i in range(0, len(load_in_bus_h)):
                                        P_dso_prov_gen.append(m3.P_dso_heat[i, 0].value)
                                    P_dso_h.append(P_dso_prov_gen)

                            elif s == 1:
                                m3, flag_error = optimization_dso_heat_up(m3, m, t, pi, ro, load_in_bus_h, b_prints)
                                if flag_error == 0:
                                    m3_h_up.append(m3)

                                    P_dso_prov_gen_up = []
                                    for i in range(0, len(load_in_bus_h)):
                                        P_dso_prov_gen_up.append(m3.P_dso_heat_up[i, 0].value)
                                    P_dso_h_up.append(P_dso_prov_gen_up)

                            elif s == 2:
                                m3, flag_error = optimization_dso_heat_down(m3, m, t, pi, ro, load_in_bus_h, b_prints)
                                if flag_error == 0:
                                    m3_h_down.append(m3)

                                    P_dso_prov_gen_down = []
                                    for i in range(0, len(load_in_bus_h)):
                                        P_dso_prov_gen_down.append(m3.P_dso_heat_down[i, 0].value)
                                    P_dso_h_down.append(P_dso_prov_gen_down)
            else:
                m3_h = []
                m3_h_up = []
                m3_h_down = []
                P_dso_old_h = []
                P_dso_old_h_up = []
                P_dso_old_h_down = []


            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            #    Update pi
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

            pi = update_pi(m, m1_h_up, m2_h, m1_h_down, m3_h, m3_h_up, m3_h_down,
                           k, h, pi, ro, load_in_bus_w, load_in_bus_g, load_in_bus_h, other_g, other_h)



            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            #    Stop criteria
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            if b_prints:
                print("")
                print("______ Stop criteria calculation ______")

            criteria, criteria_dual = calculate_criteria(m, m1_h_up, m1_h_down, m2_h, m3_h, m3_h_up, m3_h_down, h, k, iter,
                                                         load_in_bus_w, load_in_bus_g, load_in_bus_h, ro,
                                                         P_dso_old_w_up, P_dso_old_w_down, P_dso_old_g,
                                                         P_dso_old_h, P_dso_old_h_up, P_dso_old_h_down,
                                                         other_g, other_h)

            if b_prints: print("Primal residual =", criteria, ", Dual residual =", criteria_dual)
            criteria_h.append(criteria)
            criteria_dual_h.append(criteria_dual)



            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            #    Save Results
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

            if iter > 0 and criteria <= criteria_final and criteria >= -criteria_final and criteria_dual >= -criteria_final \
                        and criteria_dual <= criteria_final:
                #if iter > 0 and criteria <= criteria_final and criteria >= -criteria_final and criteria_dual >= -criteria_final \
                #        and criteria_dual <= criteria_final:
                end = time()

                print("")
                print("...ADMM converged...")
                print("Time of optimization:", end - start, "s")
                print("")

                m_h.append(m)
                save_results_aggr(m_h, t_main)

                flag = 1



            else:
                iter = iter + 1

            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            #    Update ro
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

            if iter > 1 and count >= 5 and criteria_dual < 0.05 and ro['ro'] < 0.5:
                ro['ro'] = ro['ro'] * 2
                count = 0
            else:
                count = count + 1
                if count > 50:
                    ro['ro'] = ro['ro'] + 0.1


            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            #    Create new variables
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

            # ___________ Electricity ____________
            Pa_w_up = []
            for i in range(0, len(load_in_bus_w)):
                Pa_temp_w_up = []
                for t in range(0, h):
                    Pa_temp_w_up.append(m1_h_up[t].P_dso_up[k, i, 0].value)
                Pa_w_up.append(Pa_temp_w_up)
                del (Pa_temp_w_up)
            Pa['w_up'] = deepcopy(Pa_w_up)

            Pa_w_down = []
            for i in range(0, len(load_in_bus_w)):
                Pa_temp_w_down = []
                for t in range(0, h):
                    Pa_temp_w_down.append(m1_h_down[t].P_dso_down[k, i, 0].value)
                Pa_w_down.append(Pa_temp_w_down)
                del (Pa_temp_w_down)
            Pa['w_down'] = deepcopy(Pa_w_down)


            # ___________ Gas ____________
            if other_g['b_network']:
                Pa_g = []
                for i in range(0, len(load_in_bus_g)):
                    Pa_temp_g = []
                    for t in range(0, h):
                        Pa_temp_g.append(m2_h[t].P_dso_gas[i, 0].value)
                    Pa_g.append(Pa_temp_g)
                    del (Pa_temp_g)
                Pa['g'] = deepcopy(Pa_g)


            # ___________ Heat ____________
            if other_h['b_network']:
                Pa_h = []
                for i in range(0, len(load_in_bus_h)):
                    Pa_temp_h = []
                    for t in range(0, h):
                        Pa_temp_h.append(m3_h[t].P_dso_heat[i, 0].value)
                    Pa_h.append(Pa_temp_h)
                    del (Pa_temp_h)
                Pa['h'] = deepcopy(Pa_h)

                Pa_h_up = []
                for i in range(0, len(load_in_bus_h)):
                    Pa_temp_h_up = []
                    for t in range(0, h):
                        Pa_temp_h_up.append(m3_h_up[t].P_dso_heat_up[i, 0].value)
                    Pa_h_up.append(Pa_temp_h_up)
                    del (Pa_temp_h_up)
                Pa['h_up'] = deepcopy(Pa_h_up)

                Pa_h_down = []
                for i in range(0, len(load_in_bus_h)):
                    Pa_temp_h_down = []
                    for t in range(0, h):
                        Pa_temp_h_down.append(m3_h_down[t].P_dso_heat_down[i, 0].value)
                    Pa_h_down.append(Pa_temp_h_down)
                    del (Pa_temp_h_down)
                Pa['h_down'] = deepcopy(Pa_h_down)











        # ##################################################################################################################
        # ##################################################################################################################
        # ##################################################################################################################
        # ##################################################################################################################
        #    Controller level
        # ##################################################################################################################
        # ##################################################################################################################
        # ##################################################################################################################
        # ##################################################################################################################

        if b_prints:
            print("")
            print("######################################################################################################")
            print("Controller level")
            print("######################################################################################################")
            print("")

        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        # Calculation of power of AGC considering DA bids
        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

        P_AGC = []
        for t in range(360 * t_main, 360 * t_main + 360):
            if AGC[t] > 0:
                P_AGC.append(m.E_RT[t_main].value + AGC[t] * DA_bids['DA_w_down'][t_main])
            elif AGC[t] < 0:
                P_AGC.append(m.E_RT[t_main].value + AGC[t] * DA_bids['DA_w_up'][t_main])
            else:
                P_AGC.append(0)

        P_AGC_control = []
        aux = []
        for t in range(0, 360):
            if m.U_RT[t_main].value + m.D_RT[t_main].value > 0:
                if P_AGC[t] >= m.E_RT[t_main].value:
                    P_AGC_control.append(min(P_AGC[t] - m.E_RT[t_main].value, m.D_RT[t_main].value))
                    aux.append(m.E_RT[t_main].value + min(P_AGC[t] - m.E_RT[t_main].value, m.D_RT[t_main].value))

                if P_AGC[t] < m.E_RT[t_main].value:
                    P_AGC_control.append(min(m.E_RT[t_main].value - P_AGC[t], m.U_RT[t_main].value))
                    aux.append(m.E_RT[t_main].value - min(m.E_RT[t_main].value - P_AGC[t], m.U_RT[t_main].value))
            else:
                P_AGC_control.append(0)


        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

        P_control_hour, P_soc_buildings, resources_agr = run_controller_hour(t_main, m, m3_h, resources_agr, number_buildings,
                                                    temperature_outside, P_AGC, P_AGC_control, load_in_bus_w, load_in_bus_h, gen_dh,
                                                    heat_network, other_h, branch_h, load_h, b_prints, P_soc_buildings)


        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

        P_control_day.append(P_control_hour)


        for j in range(0, number_buildings):
            resources_agr[j]['limits']['sto_soc_init'] = P_soc_buildings[j]

    # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

    output_path = os.path.join(config.output_dir, 'P_control_day.csv')
    pd.DataFrame(P_control_day).to_csv(output_path)


if __name__ == '__main__':
    main()
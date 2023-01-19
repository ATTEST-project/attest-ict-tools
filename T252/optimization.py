from xlrd import *
from numpy import *
from pyomo.environ import *
#from math import *
from time import *

import pandas as pd
import cloudpickle



def optimization_aggregator(m, t_main, prices, k, iter, pi0, ro0, Pa, load_in_bus_w, load_in_bus_g, load_in_bus_h,
                            other_g, other_h, b_prints):
    h = 1

    prices_w = prices['w']
    prices_w_up = prices['w_up']
    prices_w_down = prices['w_down']
    prices_w_imb_neg = prices['w_imb_neg']
    prices_w_imb_pos = prices['w_imb_pos']
    prices_w_imb_band = prices['w_imb_band']
    prices_g_imb = prices['g_imb']

    ratio_up = prices['ratio_up']
    ratio_down = prices['ratio_down']

    ro = ro0['ro']

    pi_w_up = pi0['w_up']
    pi_w_down = pi0['w_down']
    Pa0_w_up = Pa['w_up']
    Pa0_w_down = Pa['w_down']



    for t in range(0, h):
        for i in range(0, len(load_in_bus_w)):
            m.c1.add(m.P_dso[k, i, 0] == m.P_w[i, t_main])
            m.c1.add(m.P_dso_up[k, i, 0] == m.P_w_up[i, t_main])
            m.c1.add(m.P_dso_down[k, i, 0] == m.P_w_down[i, t_main])

    for t in range(0, h):
        for i in range(0, len(load_in_bus_g)):
            m.c1.add(m.P_dso_gas[k, i, 0] == m.P_g[i, t_main])

    for t in range(0, h):
        for i in range(0, len(load_in_bus_h)):
            m.c1.add(m.P_dso_heat[k, i, 0] == m.P_h[i, t_main])
            m.c1.add(m.P_dso_heat_up[k, i, 0] == m.P_h_up[i, t_main])
            m.c1.add(m.P_dso_heat_down[k, i, 0] == m.P_h_down[i, t_main])



    t = 0
    if iter == 0:
        m.value = Objective(expr= sum(
                                prices_w_imb_neg[t] * m.E_neg[t] + prices_w_imb_pos[t] * m.E_pos[t] +
                                (prices_w_down[t] * ratio_down[t] * m.D_RT[t] - prices_w_up[t] * ratio_up[t] * m.U_RT[t]) +
                                prices_w_imb_band[t] * (m.V_U[t] + m.V_D[t]) +
                                prices_g_imb[t] * m.G_neg[t] - prices_g_imb[t] * m.G_pos[t]
                                for t in range(t_main, 24))
                            , sense=minimize)

    else:
        aux_gas_network = 0
        aux_heat_network = 0
        if other_g['b_network']:
            pi_g = pi0['g']
            Pa0_g = Pa['g']
            aux_gas_network = sum(pi_g[i][0] * (m.P_dso_gas[k, i, 0] - Pa0_g[i][0]) for i in
                                         range(0, len(load_in_bus_g))) + \
                              ro / 2 * sum((m.P_dso_gas[k, i, 0] - Pa0_g[i][0]) ** 2
                                           for i in range(0, len(load_in_bus_g)))


        if other_h['b_network']:
            pi_h = pi0['h']
            pi_h_up = pi0['h_up']
            pi_h_down = pi0['h_down']
            Pa0_h = Pa['h']
            Pa0_h_up = Pa['h_up']
            Pa0_h_down = Pa['h_down']

            aux_heat_network =  sum(pi_h[i][0] * (m.P_dso_heat[k, i, 0] - Pa0_h[i][0]) for i in
                                         range(0, len(load_in_bus_h))) + \
                                ro / 2 * sum((m.P_dso_heat[k, i, 0] - Pa0_h[i][0]) ** 2 for i in
                                                  range(0, len(load_in_bus_h))) \
                                + \
                                sum(pi_h_up[i][0] * (m.P_dso_heat_up[k, i, 0] - Pa0_h_up[i][0]) for i in
                                         range(0, len(load_in_bus_h))) + \
                                ro / 2 * sum((m.P_dso_heat_up[k, i, 0] - Pa0_h_up[i][0]) ** 2 for i in
                                                  range(0, len(load_in_bus_h))) \
                                + \
                                sum(pi_h_down[i][0] * (m.P_dso_heat_down[k, i, 0] - Pa0_h_down[i][0]) for i in
                                         range(0, len(load_in_bus_h))) + \
                                ro / 2 * sum((m.P_dso_heat_down[k, i, 0] - Pa0_h_down[i][0]) ** 2 for i in
                                                  range(0, len(load_in_bus_h)))


        m.value = Objective(expr = sum(
                                prices_w_imb_neg[t] * m.E_neg[t] + prices_w_imb_pos[t] * m.E_pos[t] +
                                (prices_w_down[t] * ratio_down[t] * m.D_RT[t] - prices_w_up[t] * ratio_up[t] * m.U_RT[t]) +
                                prices_w_imb_band[t] * (m.V_U[t] + m.V_D[t]) +
                                prices_g_imb[t] * m.G_neg[t] - prices_g_imb[t] * m.G_pos[t]
                                for t in range(t_main, 24))


                                 +

                                 sum(pi_w_up[i][0] * (m.P_dso_up[k, i, 0] - Pa0_w_up[i][0]) for i in
                                         range(0, len(load_in_bus_w))) +
                                     ro / 2 * sum((m.P_dso_up[k, i, 0] ** 2 - 2 * m.P_dso_up[k, i, 0] * Pa0_w_up[i][0]
                                                   + Pa0_w_up[i][0] ** 2) for i in
                                                  range(0, len(load_in_bus_w)))


                                 +

                                 sum(pi_w_down[i][0] * (m.P_dso_down[k, i, 0] - Pa0_w_down[i][0]) for i in
                                         range(0, len(load_in_bus_w))) +
                                     ro / 2 * sum(
                                         (m.P_dso_down[k, i, 0] ** 2 - 2 * m.P_dso_down[k, i, 0] * Pa0_w_down[i][0]
                                          + Pa0_w_down[i][0] ** 2) for i in
                                         range(0, len(load_in_bus_w)))


                                + aux_gas_network

                                + aux_heat_network

                            , sense=minimize)


    solver = SolverFactory("cplex")

    results = solver.solve(m, tee=False)

    if (results.solver.status == SolverStatus.ok) and ( results.solver.termination_condition == TerminationCondition.optimal):
        if b_prints:
            print("Flow optimized")
    else:
        if b_prints:
            print("Did no converge")

    return m




def optimization_dso(m, m0, t, pi0, ro0, load_in_bus_w, b_prints):
    pi_w = pi0['w']
    ro = ro0['ro']
    k = 0



    m.value = Objective(expr=
                        sum(pi_w[i][t] * (m0.P_dso[k, i, t].value - m.P_dso[k, i, 0])
                            for i in range(0, len(load_in_bus_w))) +
                        ro / 2 * (sum(((m0.P_dso[k, i, t].value - m.P_dso[k, i, 0])) ** 2
                                            for i in range(0, len(load_in_bus_w))))
                        , sense=minimize)

    solver = SolverFactory("ipopt")
    solver.options['max_iter'] = 1000000

    results = solver.solve(m, tee=False)
    if (results.solver.status == SolverStatus.ok) and ( results.solver.termination_condition == TerminationCondition.optimal):
        if b_prints:
            print("Flow optimized - hour", t)
    else:
        if b_prints:
            print("Did not converge")


    return m



def optimization_dso_up(m, m0, t, pi0, ro0, load_in_bus_w, b_prints):
    pi_w_up = pi0['w_up']
    ro = ro0['ro']
    k = 0


    m.value = Objective(expr=
                        sum(pi_w_up[i][t] * (m0.P_dso_up[k, i, t].value - m.P_dso_up[k, i, 0])
                            for i in range(0, len(load_in_bus_w))) +
                        ro / 2 * (sum(((m0.P_dso_up[k, i, t].value - m.P_dso_up[k, i, 0])) ** 2
                                            for i in range(0, len(load_in_bus_w))))
                        , sense=minimize)

    solver = SolverFactory("ipopt")
    solver.options['max_iter'] = 1000000

    results = solver.solve(m, tee=False)
    if b_prints:
        if (results.solver.status == SolverStatus.ok) and ( results.solver.termination_condition == TerminationCondition.optimal):
            print("Flow optimized - hour", t)
        else:
            print("Did not converge")


    return m




def optimization_dso_down(m, m0, t, pi0, ro0, load_in_bus_w, b_prints):
    pi_w_down = pi0['w_down']
    ro = ro0['ro']
    k = 0

    m.value = Objective(expr=
                        sum(pi_w_down[i][t] * (m0.P_dso_down[k, i, t].value - m.P_dso_down[k, i, 0])
                            for i in range(0, len(load_in_bus_w))) +
                        ro / 2 * (sum(((m0.P_dso_down[k, i, t].value - m.P_dso_down[k, i, 0])) ** 2
                                            for i in range(0, len(load_in_bus_w))))
                        , sense=minimize)

    solver = SolverFactory("ipopt")
    solver.options['max_iter'] = 1000000

    results = solver.solve(m, tee=False)
    if b_prints:
        if (results.solver.status == SolverStatus.ok) and ( results.solver.termination_condition == TerminationCondition.optimal):
            print("Flow optimized - hour", t)
        else:
            print("Did not converge")


    return m




def optimization_dso_gas(m, m0, t, pi0, ro0, load_in_bus_g, b_prints):
    ro = ro0['ro']
    pi_g = pi0['g']
    k = 0

    m.value = Objective(expr=
                        sum(pi_g[i][t] * (m0.P_dso_gas[k, i, t].value - m.P_dso_gas[i, 0])
                            for i in range(0, len(load_in_bus_g))) +
                        ro / 2 * (sum((((m0.P_dso_gas[k, i, t].value) ** 2
                                              - 2 * (m0.P_dso_gas[k, i, t].value) * (m.P_dso_gas[i, 0]))
                                             + (m.P_dso_gas[i, 0])** 2)
                                            for i in range(0, len(load_in_bus_g))))
                        , sense=minimize)

    solver = SolverFactory("ipopt")
    solver.options['max_iter'] = 1000000

    results1 = solver.solve(m, tee=False, load_solutions=False)
    if (results1.solver.status == SolverStatus.ok) and (
            results1.solver.termination_condition == TerminationCondition.optimal):
        results = m.solutions.load_from(results1)

    if b_prints:
        if (results1.solver.status == SolverStatus.ok) and (
                results1.solver.termination_condition == TerminationCondition.optimal):
            print("Flow optimized - hour", t)
        else:
            print("Did not converge")

    return m






def optimization_dso_heat(m, m0, t, pi0, ro0, load_in_bus_h, b_prints):
    ro = ro0['ro']
    pi_h = pi0['h']
    k = 0

    m.value = Objective(expr=
                            sum(pi_h[i][t] * (m0.P_dso_heat[k, i, t].value - m.P_dso_heat[i, 0]) for i in range(0, len(load_in_bus_h))) +
                              ro/2 * (sum(((m0.P_dso_heat[k, i, t].value - m.P_dso_heat[i, 0])) ** 2 for i in range(0, len(load_in_bus_h))))
                        , sense=minimize)

    solver = SolverFactory("ipopt")
    solver.options['max_iter'] = 1000000

    results1 = solver.solve(m, tee=False, load_solutions=False)

    if (results1.solver.status == SolverStatus.ok) and \
            (results1.solver.termination_condition == TerminationCondition.optimal):
        results = m.solutions.load_from(results1)
        if b_prints: print("Flow optimized - hour", t)
        flag_error = 0
    else:
        if b_prints: print("Repeat solving...")
        flag_error = 1


    return m, flag_error


def optimization_dso_heat_up(m, m0, t, pi0, ro0, load_in_bus_h, b_prints):
    ro = ro0['ro']
    pi_h_up = pi0['h_up']
    k = 0

    m.value = Objective(expr=
                            sum(pi_h_up[i][t] * (m0.P_dso_heat_up[k, i, t].value - m.P_dso_heat_up[i, 0]) for i in range(0, len(load_in_bus_h))) +
                              ro/2 * (sum(((m0.P_dso_heat_up[k, i, t].value - m.P_dso_heat_up[i, 0])) ** 2 for i in range(0, len(load_in_bus_h))))
                        , sense=minimize)

    solver = SolverFactory("ipopt")
    solver.options['max_iter'] = 1000000

    results1 = solver.solve(m, tee=False, load_solutions=False)

    if (results1.solver.status == SolverStatus.ok) and \
            (results1.solver.termination_condition == TerminationCondition.optimal):
        results = m.solutions.load_from(results1)
        if b_prints: print("Flow optimized - hour", t)
        flag_error = 0
    else:
        if b_prints: print("Repeat solving...")
        flag_error = 1

    return m, flag_error


def optimization_dso_heat_down(m, m0, t, pi0, ro0, load_in_bus_h, b_prints):
    ro = ro0['ro']
    pi_h_down = pi0['h_down']
    k = 0

    m.value = Objective(expr=
                            sum(pi_h_down[i][t] * (m0.P_dso_heat_down[k, i, t].value - m.P_dso_heat_down[i, 0]) for i in range(0, len(load_in_bus_h))) +
                              ro/2 * (sum(((m0.P_dso_heat_down[k, i, t].value - m.P_dso_heat_down[i, 0])) ** 2 for i in range(0, len(load_in_bus_h))))
                        , sense=minimize)

    solver = SolverFactory("ipopt")
    solver.options['max_iter'] = 1000000

    results1 = solver.solve(m, tee=False, load_solutions=False)

    if (results1.solver.status == SolverStatus.ok) and \
            (results1.solver.termination_condition == TerminationCondition.optimal):
        results = m.solutions.load_from(results1)
        if b_prints: print("Flow optimized - hour", t)
        flag_error = 0
    else:
        if b_prints: print("Repeat solving...")
        flag_error = 1


    return m, flag_error




def optimization_dso_heat_update(m, m0, t_main, t, load_in_bus_h, b_prints, aux_P_bus_h_load, buses_with_gen_dh):

    aux = 0
    for i in range(0, len(load_in_bus_h)):
        if i not in buses_with_gen_dh:
            aux = aux + (m.P_dso_heat[i, 0] - aux_P_bus_h_load[i]) ** 2


    m.value = Objective(expr= aux, sense=minimize)

    solver = SolverFactory("ipopt")
    solver.options['max_iter'] = 1000000

    results1 = solver.solve(m, tee=False, load_solutions=False)

    if (results1.solver.status == SolverStatus.ok) and \
            (results1.solver.termination_condition == TerminationCondition.optimal):
        results = m.solutions.load_from(results1)
        if b_prints: print("Flow optimized - hour", t_main, t)
        flag_error = 0
    else:
        if b_prints: print("Repeat solving...")
        flag_error = 1


    return m, flag_error



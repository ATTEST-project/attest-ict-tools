from xlrd import *
from numpy import *
from pyomo.environ import *
#from math import *
from time import *

import pandas as pd
import cloudpickle



def optimization_aggregator(m, h, prices, k, iter, pi0, ro0, Pa, load_in_bus_w, load_in_bus_g, load_in_bus_h,
                            other_g, other_h, b_prints):

    prices_w = prices['w']
    prices_w_sec = prices['w_sec']
    prices_w_up = prices['w_up']
    prices_w_down = prices['w_down']
    prices_g = prices['g']
    ratio_up = prices['ratio_up']
    ratio_down = prices['ratio_down']
    ro = ro0['ro']
    price_admm = 1
    pi_w_up = pi0['w_up']
    pi_w_down = pi0['w_down']
    Pa0_w_up = Pa['w_up']
    Pa0_w_down = Pa['w_down']



    for t in range(0, h):
        for i in range(0, len(load_in_bus_w)):
            m.c1.add(m.P_dso[k, i, t] == m.P_w[i, t])
            m.c1.add(m.P_dso_up[k, i, t] == m.P_w_up[i, t])
            m.c1.add(m.P_dso_down[k, i, t] == m.P_w_down[i, t])

    for t in range(0, h):
        for i in range(0, len(load_in_bus_g)):
            m.c1.add(m.P_dso_gas[k, i, t] == m.P_g[i, t])

    for t in range(0, h):
        for i in range(0, len(load_in_bus_h)):
            m.c1.add(m.P_dso_heat[k, i, t] == m.P_h[i, t])
            m.c1.add(m.P_dso_heat_up[k, i, t] == m.P_h_up[i, t])
            m.c1.add(m.P_dso_heat_down[k, i, t] == m.P_h_down[i, t])



    if iter == 0:
        m.value = Objective(expr= (sum(m.P_aggr_w[t] * prices_w[t] + m.P_aggr_g[t] * prices_g[t] for t in range(0, h))
                                  -
                                  sum(sum(prices_w_sec[t] * (m.P_aggr_w_up[i, t] + m.P_aggr_w_down[i, t])
                                          for i in range(0, len(load_in_bus_w))) for t in range(0, h))
                                +
                                sum(sum(prices_w_down[t] * ratio_down[t] * m.P_aggr_w_down[i, t] -
                                        prices_w_up[t] * ratio_up[t] * m.P_aggr_w_up[i, t]
                                        for i in range(0, len(load_in_bus_w))) for t in range(0, h)))/price_admm
                            , sense=minimize)

    else:
        aux_gas_network = 0
        aux_heat_network = 0
        if other_g['b_network']:
            pi_g = pi0['g']
            Pa0_g = Pa['g']
            aux_gas_network = sum(sum(pi_g[i][t] * (m.P_dso_gas[k, i, t] - Pa0_g[i][t]) for i in
                                         range(0, len(load_in_bus_g))) +
                                     ro / 2 * sum((m.P_dso_gas[k, i, t] - Pa0_g[i][t]) ** 2 for i in
                                                  range(0, len(load_in_bus_g)))
                                     for t in range(0, h))

        if other_h['b_network']:
            pi_h = pi0['h']
            pi_h_up = pi0['h_up']
            pi_h_down = pi0['h_down']
            Pa0_h = Pa['h']
            Pa0_h_up = Pa['h_up']
            Pa0_h_down = Pa['h_down']
            price_admm = 1000

            aux_heat_network =  sum(sum(pi_h[i][t] * (m.P_dso_heat[k, i, t] - Pa0_h[i][t]) for i in
                                         range(0, len(load_in_bus_h))) +
                                     ro / 2 * sum((m.P_dso_heat[k, i, t] - Pa0_h[i][t]) ** 2 for i in
                                                  range(0, len(load_in_bus_h)))
                                     for t in range(0, h)) \
                                + \
                                sum(sum(pi_h_up[i][t] * (m.P_dso_heat_up[k, i, t] - Pa0_h_up[i][t]) for i in
                                         range(0, len(load_in_bus_h))) +
                                     ro / 2 * sum((m.P_dso_heat_up[k, i, t] - Pa0_h_up[i][t]) ** 2 for i in
                                                  range(0, len(load_in_bus_h)))
                                     for t in range(0, h)) \
                                + \
                                sum(sum(pi_h_down[i][t] * (m.P_dso_heat_down[k, i, t] - Pa0_h_down[i][t]) for i in
                                         range(0, len(load_in_bus_h))) +
                                     ro / 2 * sum((m.P_dso_heat_down[k, i, t] - Pa0_h_down[i][t]) ** 2 for i in
                                                  range(0, len(load_in_bus_h)))
                                     for t in range(0, h))

        m.value = Objective(expr = (sum(m.P_aggr_w[t] * prices_w[t] + m.P_aggr_g[t] * prices_g[t] for t in range(0, h))
                                 -
                                 sum(sum(prices_w_sec[t] * (m.P_aggr_w_up[i, t] + m.P_aggr_w_down[i, t])
                                         for i in range(0, len(load_in_bus_w))) for t in range(0, h))
                                 +
                                 sum(sum(prices_w_down[t] * ratio_down[t] * m.P_aggr_w_down[i, t] -
                                         prices_w_up[t] * ratio_up[t] * m.P_aggr_w_up[i, t]
                                         for i in range(0, len(load_in_bus_w))) for t in range(0, h)))/price_admm


                                 +

                                 sum(sum(pi_w_up[i][t] * (m.P_dso_up[k, i, t] - Pa0_w_up[i][t]) for i in
                                         range(0, len(load_in_bus_w))) +
                                     ro / 2 * sum((m.P_dso_up[k, i, t] ** 2 - 2 * m.P_dso_up[k, i, t] * Pa0_w_up[i][
                                         t] + Pa0_w_up[i][t] ** 2) for i in
                                                  range(0, len(load_in_bus_w)))
                                     for t in range(0, h))

                                 +

                                 sum(sum(pi_w_down[i][t] * (m.P_dso_down[k, i, t] - Pa0_w_down[i][t]) for i in
                                         range(0, len(load_in_bus_w))) +
                                     ro / 2 * sum(
                                         (m.P_dso_down[k, i, t] ** 2 - 2 * m.P_dso_down[k, i, t] * Pa0_w_down[i][
                                             t] + Pa0_w_down[i][t] ** 2) for i in
                                         range(0, len(load_in_bus_w)))
                                     for t in range(0, h))

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


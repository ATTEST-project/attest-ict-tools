from pulp import *
import numpy as np
import pandas as pd
import config

def market_data_generator(max_t, generators, loads_info, loads_val, gen_val, Pd, Ps):

    n_gen = len(generators.index)
    n_load = len(loads_info.index)
    prob = LpProblem("market_simple_orders_with_no_net", LpMaximize)

    Qd = LpVariable.dicts('Qd', range(0, n_load * max_t + 1), lowBound=0, cat='Continuous')
    Qs = LpVariable.dicts('Qs', range(0, n_gen * max_t + 1), lowBound=0, cat='Continuous')

    Qs_max = gen_val
    Qd_max = loads_val

    hour_objective = []

    for t in range(0, max_t):
            generation = pulp.lpSum(- Ps.loc["G" + str(ix), t + 1] * Qs[ix + n_gen * t] for ix in range(0, n_gen))
            load = pulp.lpSum(Pd.loc["L" + str(ix), t + 1] * Qd[ix + n_load * t] for ix in range(0, n_load))
            hour_objective.append(pulp.lpSum(load + generation))

    prob += pulp.lpSum(hour_objective), "obj"

    for t in range(0, max_t):
        for ix in range(0, n_gen):
            prob += Qs[ix + n_gen * t] <= Qs_max.loc["G" + str(ix), t+1], "max constraint " + str(Qs[ix + n_gen * t])
            prob += Qs[ix + n_gen * t] >= 0, "min constraint " + str(Qs[ix + n_gen * t])

        for ix in range(0, n_load):
            prob += Qd[ix + n_load * t] <= Qd_max.loc["L" + str(ix), t+1], "max constraint " + str(Qd[ix + n_load * t])
            prob += Qd[ix + n_load * t] >= 0, "min constraint " + str(Qd[ix + n_load * t])

    # prob += lpSum(Qs[ix] for ix in range(0, n_gen)) == lpSum(Qd[ix] for ix in range(1, n_load))
    for t in range(0, max_t):
        prob += lpSum(- Qs[ix + t * n_gen] for ix in range(0, n_gen)) + lpSum(Qd[ix + t * n_load] for ix in range(0, n_load)) == 0, "Load == Gen " + str(t + 1)

    prob.solve()

    gen_idx = pd.DataFrame(index=generators.index, columns=gen_val.columns)
    load_idx = pd.DataFrame(index=loads_info.index, columns=loads_val.columns)
    for t in range(0, max_t):
        for ix in range(0, n_gen):
            gen_idx.iloc[ix, t] = "Qs_" + str(ix + t * n_gen)
        for ix in range(0, n_load):
            load_idx.iloc[ix, t] = "Qd_" + str(ix + t * n_load)

    results_gen = pd.DataFrame(np.zeros((len(generators.index), max_t)), index=generators.index, columns=gen_val.columns)
    results_load = pd.DataFrame(np.zeros((len(loads_info.index), max_t)), index=loads_info.index, columns=loads_val.columns)

    for v in prob.variables():
        results_gen[gen_idx == v.name] = v.varValue
        results_load[load_idx == v.name] = v.varValue

    return results_gen, results_load


def market_solver(max_t, generators, loads_info, Qd_max, Qs_max, Pd, Ps, ram, zones, zones_ptdf):


    load_ix = []
    [load_ix.append(l.replace("L", "") + "_" + str(t)) for l in loads_info.index for t in range(1, max_t + 1)]
    gen_ix = []
    [gen_ix.append(g.replace("G", "") + "_" + str(t)) for g in generators.index for t in range(1, max_t + 1)]

    g_ix = list()
    for g in generators.index:
        g_ix.append(int(g.replace("G", "")))

    n_load = len(loads_info.index)
    prob = LpProblem("energy_market", LpMaximize)

    Qd = LpVariable.dicts('Qd', load_ix, lowBound=0, cat='Continuous')
    Qs = LpVariable.dicts('Qs', gen_ix, lowBound=0, cat='Continuous')

    hour_objective = []

    for t in range(1, max_t+1):
        generation = pulp.lpSum(- Ps.loc["G" + str(ix), t] * Qs[str(ix) + "_" + str(t)] for ix in g_ix)
        load = pulp.lpSum(Pd.loc["L" + str(ix), t] * Qd[str(ix) + "_" + str(t)] for ix in range(0, n_load))
        hour_objective.append(pulp.lpSum(load + generation))

    prob += pulp.lpSum(hour_objective), "obj"

    for t in range(1, max_t+1):
        for ix in g_ix:
            prob += Qs[str(ix) + "_" + str(t)] <= Qs_max.loc["G" + str(ix), t], "max constraint " + str(Qs[str(ix) + "_" + str(t)])
            prob += Qs[str(ix) + "_" + str(t)] >= 0, "min constraint " + str(Qs[str(ix) + "_" + str(t)])

        for ix in range(0, n_load):
            prob += Qd[str(ix) + "_" + str(t)] <= Qd_max.loc["L" + str(ix), t], "max constraint " + str(Qd[str(ix) + "_" + str(t)])
            prob += Qd[str(ix) + "_" + str(t)] >= 0, "min constraint " + str(Qd[str(ix) + "_" + str(t)])

    for t in range(1, max_t+1):
        prob += lpSum(- Qs[str(ix) + "_" + str(t)] for ix in g_ix) + lpSum(Qd[str(ix) + "_" + str(t)] for ix in range(0, n_load)) == 0, "Load == Gen " + str(t)

# todo: terminar complex orders
# LGC

    for t in range(1, max_t+1):
        for ix in g_ix:
            prob += Qs[str(ix) + "_" + str(t)] <= Qs_max.loc["G" + str(ix), t], "LGC up " + str(Qs[str(ix) + "_" + str(t)])

    # todo: energy equals sum of amount of energy a generator produces in an year


# todo: parte do FBMC
    for t in range(1, max_t+1):
        qz = []
        Fl = []

# todo: defining zones index

        iz_zones_load = []
        iz_zones_gen = []
        for iz, z_val in enumerate(zones):
            z_load = []
            z_gen = []
            for i in zones[z_val]:
                iz_load = loads_info.loc[loads_info.bus.astype(int) == i].index
                iz_gen = generators.loc[generators.bus.astype(int) == i].index
                for v in iz_load:
                    z_load.append(int(v.replace("L", "")))

                for v in iz_gen:
                    z_gen.append(int(v.replace("G", "")))
            iz_zones_load.append(z_load)
            iz_zones_gen.append(z_gen)

# todo: qz for FBMC

        for z, val in enumerate(zones):
            gen_qi = pulp.lpSum(Qs[str(iz) + "_" + str(t)] for iz in iz_zones_gen[z] if iz in g_ix)
            load_qi = pulp.lpSum(Qd[str(iz) + "_" + str(t)] for iz in iz_zones_load[z])
            qz.append(pulp.lpSum(load_qi - gen_qi))
            prob += pulp.lpSum(load_qi - gen_qi) == 0
# todo: RAM LIMIT
        for il, line in enumerate(zones_ptdf.index):
            Fl.append(pulp.lpSum(zones_ptdf.loc[line][ix] * (qz[ix]) for ix in range(len(zones))))
            prob += Fl[il] <= int(ram.loc[line, t])
            prob += -int(ram.loc[line, t]) <= Fl[il]

    prob.solve()

# todo: final

    results_gen = pd.DataFrame(np.zeros((len(generators.index), max_t)), index=generators.index, columns=Qs_max.columns)
    results_load = pd.DataFrame(np.zeros((len(loads_info.index), max_t)), index=loads_info.index, columns=Qd_max.columns)
    for v in prob.variables():
        v_name = v.name.split("_")
        if v_name[0] == "Qs":
            results_gen.loc["G" + v_name[1], int(v_name[2])] = v.varValue
        elif v_name[0] == "Qd":
            results_load.loc["L" + v_name[1], int(v_name[2])] = v.varValue

    return results_gen, results_load


def merit_order(gen, price, load, database):

    gen_list = []
    for v in gen.index.values:
        gen_list.append(int(v.replace("G", "")))

    prob = LpProblem("merit_order", LpMaximize)
    G = LpVariable.dicts('G', gen_list, lowBound=0, cat='Continuous')

    prob += pulp.lpSum(G[gen_list[ix]] * price.iloc[ix] for ix in range(0, len(gen_list))), "obj"
    prob += pulp.lpSum(G[gen_list[ix]] for ix in range(0, len(gen_list))) <= load

    for ix in gen_list:
        prob += G[ix] <= gen.loc["G" + str(ix)]

    prob.solve()

    for v in prob.variables():
        database.loc[v.name.replace("_", "")] = v.varValue

    return database


def secondary_market(gen_val, gen_zone, Ps, zones, datetime):

    # xx_amount = pd.read_csv(os.path.join("inputs", "secondary", "gen_bid_qnt.csv"), header=0, index_col=0)
    xx_amount = pd.read_csv(config.json_config['secondary']['gen_bid_qnt_path'], header=0, index_col=0)
    xx_amount.columns = xx_amount.columns.astype(int)
    # loads_sec = pd.read_csv(os.path.join("inputs", "secondary", "sec_req.csv"), header=0, index_col=0)
    loads_sec = pd.read_csv(config.json_config['secondary']['sec_req_path'], header=0, index_col=0)
    loads_sec.columns = loads_sec.columns.astype(int)
    res_secondary = pd.DataFrame(np.zeros(gen_val.shape), index=gen_val.index, columns=gen_val.columns)

    for t in range(1, datetime + 1):
        xx_amount_t = xx_amount.loc[xx_amount.loc[:, t] > 0, t]

        for z, val in enumerate(zones):
            zone_index = gen_zone[z][gen_zone[z].isin(xx_amount_t.index)]
            xx_amount_t_z = xx_amount_t.loc[zone_index]

            if xx_amount_t_z.empty:
                pass
            else:
                res_secondary.loc[:, t] = merit_order(xx_amount_t_z, Ps.loc[xx_amount_t_z.index, t], loads_sec.loc[z+1, t], res_secondary.loc[:, t])
    return res_secondary


def tertiary_market(gen_val, gen_zone, Ps, zones, datetime):

    # off_gen = pd.read_csv(os.path.join("inputs", "tertiary", "gen_bid_qnt.csv"), header=0, index_col=0)
    off_gen = pd.read_csv(config.json_config['tertiary']['gen_bid_qnt_path'], header=0, index_col=0)
    # off_gen = pd.read_csv(os.path.join("inputs", "tertiary", "energy_gen.csv"), header=0, index_col=0)
    off_gen.columns = off_gen.columns.astype(int)
    # loads_ter = pd.read_csv(os.path.join("inputs", "tertiary", "ter_req.csv"), header=0, index_col=0)
    loads_ter = pd.read_csv(config.json_config['tertiary']['ter_req_path'], header=0, index_col=0)
    loads_ter.columns = loads_ter.columns.astype(int)
    res_tertiary = pd.DataFrame(np.zeros(gen_val.shape), index=gen_val.index, columns=gen_val.columns)

    for t in range(1, datetime + 1):
        off_gen_t = off_gen.loc[off_gen.loc[:, t] > 0, t]

        for z, val in enumerate(zones):
            zone_index = gen_zone[z][gen_zone[z].isin(off_gen_t.index)]
            off_gen_t_z = off_gen_t.loc[zone_index]

            if off_gen_t_z.empty:
                pass
            else:
                res_tertiary.loc[:, t] = merit_order(off_gen_t_z, Ps.loc[off_gen_t.index, t], loads_ter.loc[z+1, t], res_tertiary.loc[:, t])

    return res_tertiary

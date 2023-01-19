import numpy as np
import pandas as pd
import os
import config

def import_data():

    # branches = pd.read_csv(os.path.join("inputs", "network", "branches.csv"), header=0, index_col=0)
    branches = pd.read_csv(config.json_config['network']['branches_path'], header=0, index_col=0)
    # buses = pd.read_csv(os.path.join("inputs", "network", "buses.csv"), header=0, index_col=0)
    buses = pd.read_csv(config.json_config['network']['buses_path'], header=0, index_col=0)
    # generators = pd.read_csv(os.path.join("inputs", "network", "generators.csv"), header=0, index_col=0)
    generators = pd.read_csv(config.json_config['network']['generators_path'], header=0, index_col=0)
    # loads_info = pd.read_csv(os.path.join("inputs", "network", "loads_info.csv"), header=0, index_col=0)
    loads_info = pd.read_csv(config.json_config['network']['loads_info_path'], header=0, index_col=0)
    return branches, buses, generators, loads_info


def import_energy_info():

    # Ps = pd.read_csv(os.path.join("inputs", "energy", "gen_bid_prices.csv"), header=0, index_col=0)
    Ps = pd.read_csv(config.json_config['energy']['gen_bid_prices_path'], header=0, index_col=0)
    Ps.columns = Ps.columns.astype(int)
    # Pd = pd.read_csv(os.path.join("inputs", "energy", "load_bid_prices.csv"), header=0, index_col=0)
    Pd = pd.read_csv(config.json_config['energy']['load_bid_prices_path'], header=0, index_col=0)
    Pd.columns = Pd.columns.astype(int)
    # loads_val = pd.read_csv(os.path.join("inputs", "energy", "loads_bid_qnt.csv"), header=0, index_col=0)
    loads_val = pd.read_csv(config.json_config['energy']['loads_bid_qnt_path'], header=0, index_col=0)
    loads_val.columns = loads_val.columns.astype(int)
    # gen_val = pd.read_csv(os.path.join("inputs", "energy", "gen_bid_qnt.csv"), header=0, index_col=0)
    gen_val = pd.read_csv(config.json_config['energy']['gen_bid_qnt_path'], header=0, index_col=0)
    gen_val.columns = gen_val.columns.astype(int)
    datetime = len(Ps.columns)
    return Ps, Pd, loads_val, gen_val, datetime


def import_reserve_info(reserve):

    if reserve == 2:
        res = "secondary"
    elif reserve == 3:
        res = "tertiary"

    # Ps = pd.read_csv(os.path.join("inputs", res, "gen_bid_prices.csv"), header=0, index_col=0)
    Ps = pd.read_csv(config.json_config[res]['gen_bid_prices_path'], header=0, index_col=0)
    Ps.columns = Ps.columns.astype(int)
    # gen_val = pd.read_csv(os.path.join("inputs", res, "gen_bid_qnt.csv"), header=0, index_col=0)
    gen_val = pd.read_csv(config.json_config[res]['gen_bid_qnt_path'], header=0, index_col=0)
    gen_val.columns = gen_val.columns.astype(int)
    datetime = len(Ps.columns)

    return Ps, gen_val, datetime


def set_zones(bus):
    d = dict()

    for a in range(1, max(bus.zone) + 1):
        d.update({"zone " + str(a): bus.loc[bus.zone == a].index.values})
    return d


def sensitivity_matrix(branches, buses):

    ref = int(buses.loc[buses.slack == 1].index[0])

    # B Matrix
    B = np.zeros((max(buses.index.astype(int)), max(buses.index.astype(int))))
    B[branches.bus0.astype(int) - 1, branches.bus1.astype(int) - 1] = - 1 / branches.x
    B[branches.bus1.astype(int) - 1, branches.bus0.astype(int) - 1] = - 1 / branches.x
    print()
    B[ref, :] = 0
    B[:, ref] = 0

    A = np.zeros((len(branches["bus0"].index), (max(buses.index.astype(int)))))

    for bus in buses.index:
        B[int(bus) - 1, int(bus) - 1] = 1 / (sum(branches[branches.bus0 == bus].x) + sum(branches[branches.bus1 == bus].x))
        A[:, int(bus) - 1] = (B[branches.bus0.astype(int) - 1, int(bus) - 1] - B[branches.bus1.astype(int) - 1, int(bus) - 1]) / branches.x
    A[:, ref] = 0
    PTDF = pd.DataFrame(A, index=branches.index, columns=buses.index.astype(int))

    return PTDF, A


def zonal_ptdf(nodal_ptdf, zones):
    # flat partitioning gsk - doi: 10.1109/EEM.2017.7981901
    #  creating zonal ptdf function
    gsk = []

    # creating zonal ptdf function
    zones_ptdf = pd.DataFrame(columns=["zone " + str((col + 1)) for col in range(len(zones))], index=nodal_ptdf.index)
    for ix, val in enumerate(zones):
        gsk.append(1 / len(zones[val]))
        zones_ptdf.loc[:, val] = nodal_ptdf.loc[:, [i for i in zones[val]]].sum(axis=1) * gsk[ix]
    return zones_ptdf, gsk


def net_balance(loads_info, generators, buses, z, gen, load, t):

    nb_node = pd.DataFrame(np.zeros((buses.shape[0], t)), columns=list(range(1, t+1)), index=buses.index)
    nb_node.loc[generators.bus, :] = nb_node.loc[generators.bus, :] + gen.values
    nb_node.loc[loads_info.bus, :] = nb_node.loc[loads_info.bus, :] - load.values

    zonal_nb = pd.DataFrame(np.zeros((len(z.keys()), t)), index=z.keys(), columns=list(range(1, t+1)))
    for ic in zonal_nb.columns:
        for ix, val in enumerate(z):
            zonal_nb.iloc[ix, :] = sum(nb_node.iloc[[i - 1 for i in z[val]], ic - 1])
    return zonal_nb, nb_node


def ram_calc(branches, mat_a, net_bal, t):

    ram = pd.DataFrame(index=mat_a.index, columns=[list(range(1, t+1))])
    for ic in ram.columns:
        for line in mat_a.index:
            ram.loc[line, ic] = branches.loc[line, "s_nom"] + sum([mat_a.loc[line, zone] * net_bal.loc[zone, ic] for zone in mat_a.columns])

    return ram


def set_marginal_price(gen_val, Ps):
    mp_data = []
    for ic in gen_val.columns:
        mp_hour_data = []
        for ix in gen_val.index:
            if gen_val.loc[ix, ic] > 0:
                mp_hour_data.append(int(Ps.loc[ix, ic]))
        mp_data.append(max(mp_hour_data))
    return mp_data


def gen_zone_import(generators, zones):
    gen_zone = []
    for a in zones:
        z_gen = generators[generators.bus.isin(zones[a])].index
        gen_zone.append(z_gen)
    return gen_zone

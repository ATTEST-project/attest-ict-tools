from network_data import *
from market_solver import *


def model_selector(energy, secondary, tertiary):

    # todo: network input data
    branches, buses, generators, loads_info = import_data()

    # todo: set zones info
    zones = set_zones(buses)

    # todo: set sensitivity matrix
    A_dataframe, A = sensitivity_matrix(branches, buses)

    # todo: generate indexes for separating gens by zone
    gen_zone = gen_zone_import(generators, zones)

    if energy:

        Ps, Pd, loads_val, gen_val, datetime = import_energy_info()

        # todo: create initial values for marginal price calc
        result_gen, result_load_aux = market_data_generator(datetime, generators, loads_info, loads_val, gen_val, Pd, Ps)

        # todo: calculate marginal price and complex order entry
        mp = set_marginal_price(result_gen, Ps)

        # todo: gsk set to be equal to every generator
        zones_ptdf, gsk = zonal_ptdf(A_dataframe, zones)

        # todo: calc of zonal net balance
        nb_zones, nb_nodes = net_balance(loads_info, generators, buses, zones, result_gen, loads_val, datetime)

        # todo: determine initial ram
        init_ram = ram_calc(branches, zones_ptdf, nb_zones, datetime)

        MIC_flag = 1
        generators_aux = generators
        gen_val_aux = gen_val
        Ps_aux = Ps
        result_gen_aux = result_gen
        while MIC_flag:
            # todo: run solver
            result_gen_aux, result_load = market_solver(datetime, generators_aux, loads_info, loads_val, gen_val_aux, Pd, Ps_aux, init_ram, zones, zones_ptdf)

            # todo: check mic constraints
            R_min = generators_aux.fixed_cost + generators_aux.variable_cost * result_gen_aux.sum(axis=1)
            check = mp * result_gen_aux.sum(axis=0)
            MIC = pd.DataFrame(index=generators_aux.index, columns=range(1, datetime + 1))

            for t in range(1, datetime + 1):
                for g in generators_aux.index:
                    if check.values[t - 1] - R_min[g] >= 0 or generators_aux.MIC[g] == 0:
                        MIC.loc[g, t] = 0
                    else:
                        MIC.loc[g, t] = check.values[t - 1] - R_min[g]
            if MIC.sum(axis=1).sum(0) < 0:
                MIC.sum(axis=1).idxmin()
                generators_aux = generators_aux.drop(index=MIC.sum(axis=1).idxmin())
                gen_val_aux = gen_val_aux.drop(index=MIC.sum(axis=1).idxmin())
                Ps_aux = Ps_aux.drop(index=MIC.sum(axis=1).idxmin())
            else:
                MIC_flag = 0

        result_gen = pd.DataFrame(index=generators.index, columns=result_load.columns)
        result_gen.loc[result_gen_aux.index, :] = result_gen_aux
        result_gen = result_gen.fillna(0)
        # todo: export primary energy market to ouput folder
        # result_gen.to_csv(os.path.join("outputs", "energy", "results_gen.csv"))
        result_gen.to_csv(os.path.join(config.json_config['output_dir']['energy'], "results_gen.csv"))
        # result_load.to_csv(os.path.join("outputs", "energy", "results_load.csv"))
        result_load.to_csv(os.path.join(config.json_config['output_dir']['energy'], "results_load.csv"))

        if secondary:

            # todo: set inputs for secondary and tertiary market

            xx_amount = gen_val - result_gen
            xx_amount[xx_amount == gen_val] = 0

            # result_gen.to_csv(os.path.join("inputs", "secondary", "energy_gen.csv"))
            # Ps.to_csv(os.path.join("inputs", "secondary", "gen_bid_prices.csv"))
            Ps.to_csv(config.json_config['secondary']['gen_bid_prices_path'])
            # xx_amount.to_csv(os.path.join("inputs", "secondary", "gen_bid_qnt.csv"))
            xx_amount.to_csv(config.json_config['secondary']['gen_bid_qnt_path'])

        if tertiary:
            off_gen = gen_val[result_gen == 0].fillna(0)
            # result_gen.to_csv(os.path.join("inputs", "tertiary", "energy_gen.csv"))
            # Ps.to_csv(os.path.join("inputs", "tertiary", "gen_bid_prices.csv"))
            Ps.to_csv(config.json_config['tertiary']['gen_bid_prices_path'])
            # off_gen.to_csv(os.path.join("inputs", "tertiary", "gen_bid_qnt.csv"))
            off_gen.to_csv(config.json_config['tertiary']['gen_bid_qnt_path'])

    if secondary:
        # todo: secondary market
        Ps, gen_val, datetime = import_reserve_info(2)
        res_secondary = secondary_market(gen_val, gen_zone, Ps, zones, datetime)
        # res_secondary.to_csv(os.path.join("outputs", "secondary", "results_secondary_ex1.csv"))
        res_secondary.to_csv(os.path.join(config.json_config['output_dir']['secondary'], "results_secondary_ex1.csv"))

    if tertiary:
        # todo: tertiary market
        Ps, gen_val, datetime = import_reserve_info(3)
        res_tertiary = tertiary_market(gen_val, gen_zone, Ps, zones, datetime)
        # res_tertiary.to_csv(os.path.join("outputs", "tertiary", "results_tertiary_1.csv"))
        res_tertiary.to_csv(os.path.join(config.json_config['output_dir']['tertiary'], "results_tertiary_1.csv"))


from xlrd import *
from numpy import *
from pyomo.environ import *
from math import *
import pandas as pd
import csv
from time import *
from copy import *
import config



def initialization():
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    # Networks
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################



    # name_folder = os.getcwd()

    # book_networks = name_folder + "\\Input Data - Networks.xlsx"
    # book_resources = name_folder + "\\Input Data - Resources.xlsx"
    # book_other = name_folder + "\\Input Data - Other.xlsx"
    # book_DA_bids = name_folder + "\\Input Data - DA bids.xlsx"
    # book_agc_signal = name_folder + "\\Input Data - AGC.xlsx"
    book_networks = config.input_network_path
    book_resources = config.input_resources_path
    book_other = config.input_other_path
    book_DA_bids = config.input_da_bids
    book_agc_signal = config.input_agc_signal
    wb_networks = open_workbook(book_networks)
    wb_resources = open_workbook(book_resources)
    wb_other = open_workbook(book_other)
    wb_DA_bids = open_workbook(book_DA_bids)
    wb_agc_signal = open_workbook(book_agc_signal)


    xl_sheet = wb_networks.sheet_by_index(0)
    b_network_g = xl_sheet.cell(3, 2).value
    b_network_h = xl_sheet.cell(4, 2).value

    ####################################################################################################################
    # Electricity network
    ####################################################################################################################
    # _________________ Branches__________________________________________________________________________________
    # Array with vectors identifying the starting bus, end bus, R (p.u.) and X (p.u.)
    xl_sheet = wb_networks.sheet_by_index(1)
    branch_w = []
    for i in range(0, xl_sheet.nrows - 2):
        prov = []
        for j in range(0, 4):
            prov.append(float(xl_sheet.cell(2 + i, 1 + j).value))
        branch_w.append(prov)
    branch_w = array(branch_w)




    # _________________ Building number in each bus __________________________________________________________________
    # Vector with the buildings identified in each node
    # Example, a network with 23 buses and several buildings in each bus

    xl_sheet = wb_networks.sheet_by_index(2)
    load_in_bus_w = []
    for i in range(0, xl_sheet.nrows - 2):
        prov = []
        for j in range(0, xl_sheet.ncols - 2):
            if xl_sheet.cell(2 + i, 2 + j).value == '':
                break
            else:
                prov.append(int(xl_sheet.cell(2 + i, 2 + j).value))
        load_in_bus_w.append(prov)


    # _________________ Other parameters _______________________________________________________________________________
    # ref_bus - bus with reference generator
    # MVA_base - MVA system base
    # v_min - minimum voltage limit (p.u.)
    # v_max - maximum voltage limit (p.u.)
    # v_ref - voltage of reference bus (p.u.)
    # I_max - maximum current limit (A)


    xl_sheet = wb_networks.sheet_by_index(3)
    ref_bus = xl_sheet.cell(1, 2).value
    v_ref = xl_sheet.cell(2, 2).value
    MVA_base = xl_sheet.cell(3, 2).value
    v_max = xl_sheet.cell(4, 2).value
    v_min = xl_sheet.cell(5, 2).value
    I_max = xl_sheet.cell(6, 2).value

    other_w = {'ref_bus': ref_bus, 'MVA_base': MVA_base, 'v_min': v_min, 'v_max': v_max, 'v_ref': v_ref, 'I_max': I_max}

    # __________________________________________________________________________________________________________________
    electrical_network = {'branch_w': branch_w, 'load_in_bus_w': load_in_bus_w, 'other_w': other_w}





    ####################################################################################################################
    # Gas network
    ####################################################################################################################
    if b_network_g:
        # _________________ Pipelines __________________________________________________________________________________
        # From, To, R, X

        xl_sheet = wb_networks.sheet_by_index(4)
        branch_g = []
        for i in range(0, xl_sheet.nrows - 2):
            prov = []
            for j in range(0, 4):
                prov.append(float(xl_sheet.cell(2 + i, 1 + j).value))
            branch_g.append(prov)
        branch_g = array(branch_g)


        # _________________ Building number in each bus __________________________________________________________________
        # Vector with the buildings identified in each node

        xl_sheet = wb_networks.sheet_by_index(5)
        load_in_bus_g = []
        for i in range(0, xl_sheet.nrows - 2):
            prov = []
            for j in range(0, xl_sheet.ncols - 2):
                if xl_sheet.cell(2 + i, 2 + j).value == '':
                    break
                else:
                    prov.append(int(xl_sheet.cell(2 + i, 2 + j).value))
            load_in_bus_g.append(prov)


        # _________________ Other parameters __________________________________________________________________________________
        # p_max - maximum pressure (bar)
        # ref_gas - reference bus

        xl_sheet = wb_networks.sheet_by_index(6)
        ref_gas = xl_sheet.cell(1, 2).value
        p_max = xl_sheet.cell(2, 2).value

        other_g = {'p_max': p_max * p_max, 'ref_gas': ref_gas, 'b_network': b_network_g}

        # __________________________________________________________________________________________________________________
        gas_network = {'branch_g': branch_g, 'load_in_bus_g': load_in_bus_g, 'other_g': other_g}
    else:
        other_g = {'b_network': b_network_g}
        gas_network = {'other_g': other_g}


    ####################################################################################################################
    # Heat network
    ####################################################################################################################
    if b_network_h:
        # _________________ Pipelines __________________________________________________________________________________
        # From, To, Length (m), Diameter (mm), Heat transfer coefficient (W/C)

        xl_sheet = wb_networks.sheet_by_index(7)
        branch_h = []
        for i in range(0, xl_sheet.nrows - 2):
            prov = []
            for j in range(0, 5):
                prov.append(float(xl_sheet.cell(2 + i, 1 + j).value))
            branch_h.append(prov)
        branch_h = array(branch_h)


        # _________________ Building number in each bus __________________________________________________________________
        # Vector with the buildings identified in each node

        xl_sheet = wb_networks.sheet_by_index(8)
        load_in_bus_h = []
        for i in range(0, xl_sheet.nrows - 2):
            prov = []
            for j in range(0, xl_sheet.ncols - 2):
                if xl_sheet.cell(2 + i, 2 + j).value == '':
                    break
                else:
                    prov.append(int(xl_sheet.cell(2 + i, 2 + j).value))
            load_in_bus_h.append(prov)


        # _________________ Building number in each bus __________________________________________________________________
        # Vector with information of heat generators connected to the district heating

        xl_sheet = wb_networks.sheet_by_index(9)
        gen_dh = []
        for i in range(0, xl_sheet.ncols - 2):
            type = xl_sheet.cell(1, 2 + i).value
            bus_elec = xl_sheet.cell(2, 2 + i).value
            bus_gas = xl_sheet.cell(3, 2 + i).value
            bus_dh = xl_sheet.cell(4, 2 + i).value
            P_max = xl_sheet.cell(5, 2 + i).value
            rend = xl_sheet.cell(6, 2 + i).value
            prov = {'type': type, 'bus_elec': bus_elec, 'bus_gas': bus_gas, 'bus_dh': bus_dh, 'P_max': P_max, 'rend': rend},
            gen_dh.append({'type': type, 'bus_elec': bus_elec, 'bus_gas': bus_gas, 'bus_dh': bus_dh, 'P_max': P_max, 'rend': rend})

        buses_generator = []
        for i in range(0, xl_sheet.ncols - 2):
            buses_generator.append(int(xl_sheet.cell(4, 2 + i).value))

        # _________________ Other parameters __________________________________________________________________________________
        # Cp - Specific heat of water (J/(kg.C))
        # Ta - Ambience temperature (C)
        # m_min - minimum mass flow rate (kg/s)
        # m_max - maximum mass flow rate (kg/s)
        # Ts_min, Ts_max - minimum and maximum supply nodal and pipeline temperature (C)
        # Tr_min, Tr_max - minimum and maximum return nodal and pipeline temperature (C)
        # friction - pipeline friction
        # p_min, p_max - minimum and maximum pipeline pressure (Pa)
        # T_load, T_gen - temperature of supply nodes with loads and generators (C)

        xl_sheet = wb_networks.sheet_by_index(10)
        Cp = xl_sheet.cell(1, 2).value
        Ta = xl_sheet.cell(2, 2).value
        m_max = xl_sheet.cell(3, 2).value
        m_min = xl_sheet.cell(4, 2).value
        Ts_min = xl_sheet.cell(5, 2).value
        Ts_max = xl_sheet.cell(6, 2).value
        Tr_min = xl_sheet.cell(7, 2).value
        Tr_max = xl_sheet.cell(8, 2).value
        friction = xl_sheet.cell(9, 2).value
        p_min = xl_sheet.cell(10, 2).value
        p_max = xl_sheet.cell(11, 2).value
        T_load = xl_sheet.cell(12, 2).value
        T_gen = xl_sheet.cell(13, 2).value

        other_h = {'Cp': Cp, 'Ta': Ta, 'm_max': m_max, 'm_min': m_min, 'Ts_min': Ts_min, 'Ts_max': Ts_max, 'Tr_min': Tr_min, 'Tr_max': Tr_max,
                   'friction': friction, 'p_min': p_min, 'p_max': p_max, 'T_load': T_load, 'T_gen': T_gen, 'b_network': b_network_h}

        # __________________________________________________________________________________________________________________
        heat_network = {'branch_h': branch_h, 'load_in_bus_h': load_in_bus_h, 'buses_gen': buses_generator, 'gen_dh': gen_dh,
                        'other_h': other_h}
    else:
        other_h = {'b_network': b_network_h}
        heat_network = {'other_h': other_h}








    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    # Buildings / Consumers / Resources
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    page = 0

    # _________________ Electrical load __________________________________________________________________________________

    # Vector with electrical load consumption of each building in MW for 24h
    # Buildings numbers should correspond to this vector position, i.e., building ID 1 should be in position 0,
    # building ID 2 should be in position 1, and so on

    # Example of loads for each building for 24h
    # load_w = [[load_building_1], [load_building_2], ..., [load_building_x]]
    #

    xl_sheet = wb_resources.sheet_by_index(page)
    load_w = []
    for i in range(0, xl_sheet.nrows - 2):
        prov = []
        for t in range(0, 24):
            prov.append(xl_sheet.cell(2 + i, 2 + t).value)
        load_w.append(prov)


    # _________________ Gas load __________________________________________________________________________________

    # Vector with gas load consumption of each building in MW for 24h
    # Buildings numbers should correspond to this vector position, i.e., building ID 1 should be in position 0,
    # building ID 2 should be in position 1, and so on

    # Example of loads for each building for 24h
    # load_g = [[load_building_1], [load_building_2], ..., [load_building_x]]
    page = page + 1
    xl_sheet = wb_resources.sheet_by_index(page)
    load_g = []
    for i in range(0, xl_sheet.nrows - 2):
        prov = []
        for t in range(0, 24):
            prov.append(xl_sheet.cell(2 + i, 2 + t).value)
        load_g.append(prov)


    # _________________ Heat load __________________________________________________________________________________

    # Vector with heat load consumption of each building in MW for 24h
    # Buildings numbers should correspond to this vector position, i.e., building ID 1 should be in position 0,
    # building ID 2 should be in position 1, and so on

    # Example of loads for each building for 24h
    # load_h = [[load_building_1], [load_building_2], ..., [load_building_x]]
    page = page + 1
    xl_sheet = wb_resources.sheet_by_index(page)
    load_h = []
    for i in range(0, xl_sheet.nrows - 2):
        prov = []
        for t in range(0, 24):
            prov.append(xl_sheet.cell(2 + i, 2 + t).value)
        load_h.append(prov)

    # _________________ Cooling load __________________________________________________________________________________

    # Vector with cooling load consumption of each building in MW for 24h
    # Buildings numbers should correspond to this vector position, i.e., building ID 1 should be in position 0,
    # building ID 2 should be in position 1, and so on

    # Example of loads for each building for 24h
    # load_h = [[load_building_1], [load_building_2], ..., [load_building_x]]
    page = page + 1
    xl_sheet = wb_resources.sheet_by_index(page)
    load_cool = []
    for i in range(0, xl_sheet.nrows - 2):
        prov = []
        for t in range(0, 24):
            prov.append(xl_sheet.cell(2 + i, 2 + t).value)
        load_cool.append(prov)


    # _________________ Building resources __________________________________________________________________________________
    # Vector with characteristics of each building, including resources installed (heat pump, gas boiler,
    # district heating, PV, storage, gas consumtion) and the respective limits

    # Example with two buildings

    # Buildings with hp/ without PV and storage/ without thermal modelling
    page = page + 1
    xl_sheet = wb_resources.sheet_by_index(page)
    page = page + 1
    xl_sheet2 = wb_resources.sheet_by_index(page)
    page = page + 1
    xl_sheet3 = wb_resources.sheet_by_index(page)
    resouces_aggregator = []
    for i in range(0, xl_sheet.ncols - 3):
        installed_hp = xl_sheet.cell(2, 3 + i).value
        max_power_hp = xl_sheet.cell(3, 3 + i).value
        effic_hp = xl_sheet.cell(4, 3 + i).value
        installed_gb = xl_sheet.cell(5, 3 + i).value
        max_power_gb = xl_sheet.cell(6, 3 + i).value
        effic_gb = xl_sheet.cell(7, 3 + i).value
        installed_pv = xl_sheet.cell(8, 3 + i).value
        max_power_pv = xl_sheet.cell(9, 3 + i).value
        installed_sto = xl_sheet.cell(10, 3 + i).value
        max_power_sto = xl_sheet.cell(11, 3 + i).value
        max_soc = xl_sheet.cell(12, 3 + i).value
        min_soc = xl_sheet.cell(13, 3 + i).value
        initial_soc = xl_sheet.cell(14, 3 + i).value
        effic_sto = xl_sheet.cell(15, 3 + i).value
        installed_dh = xl_sheet.cell(16, 3 + i).value
        max_power_dh = xl_sheet.cell(17, 3 + i).value
        installed_g_load = xl_sheet.cell(18, 3 + i).value
        building_R = xl_sheet.cell(19, 3 + i).value
        building_C = xl_sheet.cell(20, 3 + i).value
        building_init_temp = xl_sheet.cell(21, 3 + i).value
        installed_ac = xl_sheet.cell(22, 3 + i).value
        max_power_ac = xl_sheet.cell(23, 3 + i).value
        effic_ac = xl_sheet.cell(24, 3 + i).value


        prov_temp_max = []
        prov_temp_min = []
        for t in range(0, 24):
            prov_temp_max.append(xl_sheet2.cell(2 + t, 2 + i).value)
            prov_temp_min.append(xl_sheet3.cell(2 + t, 2 + i).value)

        resouces_aggregator.append({'installed': {'hp': installed_hp, 'gb': installed_gb, 'dh': installed_dh,
                                                  'PV': installed_pv, 'sto': installed_sto, 'g_out': installed_g_load,
                                                  'ac': installed_ac},
                         'limits':  {'hp': max_power_hp, 'gb': max_power_gb, 'PV': max_power_pv, 'sto_P': max_power_sto,
                                     'sto_soc_max': max_soc, 'sto_soc_min': min_soc, 'sto_soc_init': initial_soc,
                                     'dh': max_power_dh, 'ac': max_power_ac},
                         'rend': {'hp': effic_hp, 'gb': effic_gb, 'sto': effic_sto, 'ac': effic_ac},
                         'thermal': {'R': building_R, 'C': building_C, 'T_init': building_init_temp,
                                     'T_max': prov_temp_max,
                                     'T_min': prov_temp_min},
                       'consumption': {'elec': [], 'gas': [], 'heat': []}})


    resources = {'load_w': load_w, 'load_g': load_g, 'load_h': load_h, 'resouces_aggregator': resouces_aggregator}








    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    # Other
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################

    ####################################################################################################################
    # Weather data
    ####################################################################################################################

    xl_sheet = wb_other.sheet_by_index(0)
    # _________________ Solar profile __________________________________________________________________________________
    # Vector with solar profile (0-1)
    # _________________ Outside temperature ____________________________________________________________________________
    # Vector with outside temperature in Celsius degrees

    profile_solar = []
    temperature_outside = []
    for t in range(0, 24):
        profile_solar.append(xl_sheet.cell(2, 2 + t).value)
        temperature_outside.append(xl_sheet.cell(3, 2 + t).value)

    weather = {'profile_solar': profile_solar, 'temperature_outside': temperature_outside}



    ####################################################################################################################
    # Prices
    ####################################################################################################################

    xl_sheet = wb_other.sheet_by_index(1)
    prices_w = []
    prices_w_up = []
    prices_w_down = []
    prices_w_imb_neg = []
    prices_w_imb_pos = []
    prices_w_imb_band = []
    prices_g_imb = []
    ratio_up = []
    ratio_down = []
    for t in range(0, 24):
        prices_w.append(xl_sheet.cell(2, 2 + t).value)
        prices_w_up.append(xl_sheet.cell(3, 2 + t).value)
        prices_w_down.append(xl_sheet.cell(4, 2 + t).value)
        prices_w_imb_neg.append(xl_sheet.cell(5, 2 + t).value)
        prices_w_imb_pos.append(xl_sheet.cell(6, 2 + t).value)
        prices_w_imb_band.append(xl_sheet.cell(7, 2 + t).value)
        prices_g_imb.append(xl_sheet.cell(8, 2 + t).value)
        ratio_up.append(xl_sheet.cell(9, 2 + t).value)
        ratio_down.append(xl_sheet.cell(10, 2 + t).value)

    prices = {"w": prices_w,
             "w_up": prices_w_up,
             "w_down": prices_w_down,
            "w_imb_neg": prices_w_imb_neg,
            "w_imb_pos": prices_w_imb_pos,
            "w_imb_band": prices_w_imb_band,
            "g_imb": prices_g_imb,
            "ratio_up": ratio_up,
            "ratio_down": ratio_down}



    ####################################################################################################################
    # ADMM
    ####################################################################################################################

    xl_sheet = wb_other.sheet_by_index(2)
    ro = xl_sheet.cell(1, 2).value
    criteria_final = xl_sheet.cell(2, 2).value
    admm = {'ro': ro, 'criteria_final': criteria_final}


    ####################################################################################################################
    # DA bids
    ####################################################################################################################

    xl_sheet = wb_DA_bids.sheet_by_index(0)
    DA_elec_energy = []
    DA_elec_up = []
    DA_elec_down = []
    DA_gas = []
    for t in range(0, 24):
        DA_elec_energy.append(xl_sheet.cell(2, 2 + t).value)
        DA_elec_up.append(xl_sheet.cell(3, 2 + t).value)
        DA_elec_down.append(xl_sheet.cell(4, 2 + t).value)
        DA_gas.append(xl_sheet.cell(5, 2 + t).value)

    DA_bids = {"DA_w": DA_elec_energy,
             "DA_w_up": DA_elec_up,
             "DA_w_down": DA_elec_down,
             "DA_gas": DA_gas}

    ####################################################################################################################
    # AGC signal
    ####################################################################################################################

    xl_sheet = wb_agc_signal.sheet_by_index(0)
    DA_agc_signal = []
    for t in range(0, 6 * 60 * 24):
        DA_agc_signal.append(xl_sheet.cell(2 + t, 2).value)

    AGC = DA_agc_signal

    return electrical_network, gas_network, heat_network, resources, weather, prices, admm, DA_bids, AGC



if __name__ == '__main__':
    main()
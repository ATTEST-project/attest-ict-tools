using PowerModels, OdsIO
# file_name ="case5_modified.m"
# file_name ="Transmission_Network_UK_2020.m"
file_name = "HR\\HR_Tx_01_2020_new_Koprivnica\\Location1.m"
name="HR_Tx_01_2020_new_Koprivnica"
# file_name = "Location_1.m"
# file_name = "case30.m"
data=parse_file(file_name)

standardize_cost_terms!(data, order=2)

calc_thermal_limits!(data)

# ref =build_ref(data)[:nw][0]

buses=[data["bus"][i]["bus_i"] for i in keys(data["bus"])]
type=[data["bus"][i]["bus_type"] for i in keys(data["bus"])]
area=[data["bus"][i]["zone"] for i in keys(data["bus"])]
v_nom=[data["bus"][i]["base_kv"] for i in keys(data["bus"])]
v_max=[data["bus"][i]["vmax"] for i in keys(data["bus"])]
v_min=[data["bus"][i]["vmin"] for i in keys(data["bus"])]
va=[data["bus"][i]["va"] for i in keys(data["bus"])]
vm=[data["bus"][i]["vm"] for i in keys(data["bus"])]
v_real=vm.*cos.(va)
v_imag=vm.*sin.(va)

fr_branch=[]
to_branch=[]
g_branch=[]
b_branch=[]
g_sh_branch=[]
b_sh_branch=[]
rate_a_branch=[]
br_stat=[]

fr_branch_tr=[]
to_branch_tr=[]
g_tr=[]
b_tr=[]
# g_sh_tr=[]
b_sh_tr=[]
ratio_tr=[]
shift_angle=[]
rmin_tr=[]
rmax_tr=[]
rate_a_tr=[]
br_stat_tr=[]

for i in keys(data["branch"])
    # if data["branch"][i]["br_status"]==1
    if !data["branch"][i]["transformer"]
        from_br=data["branch"][i]["f_bus"]
        to_br= data["branch"][i]["t_bus"]
        r=         data["branch"][i]["br_r"]
        x=         data["branch"][i]["br_x"]
        g=r./(r.^2+x.^2)
        b=-x./(r.^2+x.^2)
        g_sh=       2*data["branch"][i]["g_fr"]
        b_sh=       2*data["branch"][i]["b_fr"]
        rate_a=     data["branch"][i]["rate_a"]
        br_status=  data["branch"][i]["br_status"]
        push!(fr_branch,from_br)
        push!(to_branch,to_br)
        push!(g_branch,g)
        push!(b_branch,b)
        push!(g_sh_branch,g_sh)
        push!(b_sh_branch,b_sh)
        push!(rate_a_branch,rate_a)
        push!(br_stat,br_status)
    else
        from_br=data["branch"][i]["f_bus"]
        to_br= data["branch"][i]["t_bus"]
        r=         data["branch"][i]["br_r"]
        x=         data["branch"][i]["br_x"]
        g=r./(r.^2+x.^2)
        b=-x./(r.^2+x.^2)
        # g_sh=       2*data["branch"][i]["g_fr"]
        b_sh=       2*data["branch"][i]["b_fr"]
        ratio=data["branch"][i]["tap"]
        shift=data["branch"][i]["shift"]
        rmin=1
        rmax=1

        rate_a=     data["branch"][i]["rate_a"]
        br_status_tr=  data["branch"][i]["br_status"]

        push!(g_tr,g)
        push!(b_tr,b)
        # push!(g_sh_tr,g_sh)
        push!(b_sh_tr,b_sh)
        push!(ratio_tr,ratio)
        push!(shift_angle,shift)
        push!(rmin_tr,rmin)
        push!(rmax_tr,rmax)
        push!(rate_a_tr,rate_a)
        push!(br_stat_tr,br_status_tr)
        push!(fr_branch_tr,from_br)
        push!(to_branch_tr,to_br)
    end
# end
end
# tr=[fr_branch_tr to_branch_tr]
#
# tr_new=[]
# for i in 1:size(tr[:,1],1)
#     for j in 1:size(tr[:,1],1)
#         if tr[i,:]==tr[j,:] && i!=j
#             tr[j,:]=[0 0]
#         end
#
#     end
#     push!(tr_new,tr)
# end
# tr_final=[setdiff(tr_new[1][:,1], 0) setdiff(tr_new[1][:,2], 0)]
# fr_tr=tr_final[:,1]
# to_tr=tr_final[:,2]

load_bus_map=[data["load"][i]["load_bus"] for i in keys(data["load"])]
pd_load=     [data["load"][i]["pd"] for i in keys(data["load"])]
qd_load=     [data["load"][i]["qd"] for i in keys(data["load"])]
columns=[]
for i in keys(data["load"])
    push!(columns,1)
end

# gen_bus_map=[data["gen"][i]["gen_bus"] for i in keys(data["gen"]) if data["gen"][i]["gen_status"]==1]
# pg_gen=[data["gen"][i]["pg"] for i in keys(data["gen"]) if data["gen"][i]["gen_status"]==1]
# qg_gen=[data["gen"][i]["qg"] for i in keys(data["gen"]) if data["gen"][i]["gen_status"]==1]
# gen_stat=[data["gen"][i]["gen_status"] for i in keys(data["gen"]) if data["gen"][i]["gen_status"]==1]
# pmin_gen=[data["gen"][i]["pmin"] for i in keys(data["gen"]) if data["gen"][i]["gen_status"]==1]
# pmax_gen=[data["gen"][i]["pmax"] for i in keys(data["gen"]) if data["gen"][i]["gen_status"]==1]
# qmin_gen=[data["gen"][i]["qmin"] for i in keys(data["gen"]) if data["gen"][i]["gen_status"]==1]
# qmax_gen=[data["gen"][i]["qmax"] for i in keys(data["gen"]) if data["gen"][i]["gen_status"]==1]
# vg_gen  =[data["gen"][i]["vg"] for i in keys(data["gen"]) if data["gen"][i]["gen_status"]==1]


gen_bus_map=[data["gen"][i]["gen_bus"] for i in keys(data["gen"]) ]
pg_gen=[data["gen"][i]["pg"] for i in keys(data["gen"]) ]
qg_gen=[data["gen"][i]["qg"] for i in keys(data["gen"]) ]
gen_stat=[data["gen"][i]["gen_status"] for i in keys(data["gen"]) ]
pmin_gen=[data["gen"][i]["pmin"] for i in keys(data["gen"]) ]
pmax_gen=[data["gen"][i]["pmax"] for i in keys(data["gen"]) ]
qmin_gen=[data["gen"][i]["qmin"] for i in keys(data["gen"]) ]
qmax_gen=[data["gen"][i]["qmax"] for i in keys(data["gen"]) ]
vg_gen  =[data["gen"][i]["vg"] for i in keys(data["gen"]) ]
# %  CWS (Connection with Spain),
# %  FOG (Fossil Gas),
# %  FHC (Fossil Hard Coal),
# %  HWR (Hydro Water Reservoir),
# %  HPS (Hydro Pumped Storage),
# %  HRP (Hydro Run-of-river and poundage),
# %  SH1 (Small Hydro - P ≤ 10 MW),
# %  SH3 (Small Hydro - 10 MW < P ≤ 30 MW),
# %  PVP (Photovoltaic power plant),
# %  WON (Wind onshore),
# %  WOF (Wind offshore),
# %  MAR (Marine),
# %  OTH (Other thermal, such as geothermal, biomass, biogas, Municipal solid waste and CHP renewable and non-renewable)
cost_b=[]
for i in keys(data["gen"])
    # if data["gen"][i]["gen_status"]==1
    if data["gen"][i]["col_1"]=="CWS"
        cost=1
        push!(cost_b,cost)
    elseif data["gen"][i]["col_1"]=="FOG"
        cost=2
        push!(cost_b,cost)
    elseif data["gen"][i]["col_1"]=="FHC"
        cost=3
        push!(cost_b,cost)
    elseif data["gen"][i]["col_1"]=="HWR"
        cost=4
        push!(cost_b,cost)
    elseif data["gen"][i]["col_1"]=="HPS"
        cost=5
        push!(cost_b,cost)
    elseif data["gen"][i]["col_1"]=="HRP"
        cost=6
        push!(cost_b,cost)
    elseif data["gen"][i]["col_1"]=="SH1"
        cost=7
        push!(cost_b,cost)
    elseif data["gen"][i]["col_1"]=="SH3"
        cost=8
        push!(cost_b,cost)
    elseif data["gen"][i]["col_1"]=="PVP"
        cost=9
        push!(cost_b,cost)
    elseif data["gen"][i]["col_1"]=="WON"
        cost=10
        push!(cost_b,cost)
    elseif data["gen"][i]["col_1"]=="WOF"
        cost=11
        push!(cost_b,cost)
    elseif data["gen"][i]["col_1"]=="MAR"
        cost=12
        push!(cost_b,cost)
    elseif data["gen"][i]["col_1"]=="OTH"
        cost=13
        push!(cost_b,cost)
    end
# end
end





# cost_a=[ data["gen"][i]["cost"][1]/(data["baseMVA"]^2) for i in keys(data["gen"])]
# cost_b=[ data["gen"][i]["cost"][2]/(data["baseMVA"]) for i in keys(data["gen"])]
# cost_c=[ data["gen"][i]["cost"][3] for i in keys(data["gen"])]

ods_write("data_conversion\\$(name).ods",Dict(("Buses",1,1)=>
["Bus_N" "Bus_Type"	"Area" "V_Nom (kV)"  "V_max (pu)" "V_min (pu)" "V_init_re (pu)" "V_init_im (pu)"]))

ods_write("data_conversion\\$(name).ods",Dict(("Lines",1,1)=>
["From" "To" "g (pu)" "b (pu)"  "g_sh (pu)" "b_sh (pu)" "RATE_A" "br_status"]))

ods_write("data_conversion\\$(name).ods",Dict(("Gens",1,1)=>
["Bus" "Pg (pu)" "Qg (pu)" "Q_max (pu)"  "Q_min (pu)" "V_set (pu)" "P_max (pu)" "P_min (pu)" "cost_a"   "cost_b"  "cost_c"
 ]))


ods_write("data_conversion\\$(name).ods",Dict(("Loads",1,1)=>
["Bus_N" "Pd (pu)" "Qd (pu)" "ShFr"  "ShFrMin" "ShFrMax" "ShFrOK" "ShCost" ]))


ods_write("data_conversion\\$(name).ods",Dict(("Transformers",1,1)=>
["From" "To" "g" "b"  "bsh" "ratio" "rmin" "rmax"  "Snom" "BStatus0" ]))

ods_write("data_conversion\\$(name).ods",Dict(("P_Profiles_Load",1,1)=>
# ["Bus"	"t1"	"t2"	"t3"	"t4"	"t5"	"t6"	"t7"	"t8"	"t9"	"t10"	"t11"	"t12"	"t13"	"t14"	"t15"	"t16"	"t17"	"t18"	"t19"	"t20"	"t21"	"t22"	"t23"	"t24"]))
["Bus"	"t1"	]))

ods_write("data_conversion\\$(name).ods",Dict(("Q_Profiles_Load",1,1)=>
# ["Bus"	"t1"	"t2"	"t3"	"t4"	"t5"	"t6"	"t7"	"t8"	"t9"	"t10"	"t11"	"t12"	"t13"	"t14"	"t15"	"t16"	"t17"	"t18"	"t19"	"t20"	"t21"	"t22"	"t23"	"t24"]))
["Bus"	"t1"	]))

ods_write("data_conversion\\$(name).ods",Dict(("Base_MVA",1,1)=>["base_MVA" 0]))

ods_write("data_conversion\\$(name).ods",Dict(("shunts",1,1)=>["Bus"	"bsh0"	"bshmin"	"bshmax"]))

ods_write("data_conversion\\$(name).ods",Dict(("contingencies",1,1)=>["cont"	"From"	"To"]))

ods_write("data_conversion\\$(name).ods",Dict(("Storage",1,1)=>["Bus"	"Ps"	"Qs"	"Energy (MWh)"	"E_rating (MWh)"	"Charge_rating (MW)"	"Discharge_rating (MW)"	"Charge_efficiency"	"Discharge_efficiency"	"Thermal_rating (MVA)"	"Qmin (MVAr)"	"Qmax (MVAr)"	"R"	"X"	"P_loss"	"Q_loss"	"Status"	"soc_initial"	"soc_min"	"soc_max"	"E_rating_min (MWh)"	"E_initial (MWh)"	"cost_a"	"cost_b"	"cost_c"
]))

ods_write("data_conversion\\$(name).ods",Dict(("Buses",2,1)=>[buses zeros(size(buses,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Buses",2,2)=>[type zeros(size(type,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Buses",2,3)=>[area zeros(size(area,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Buses",2,4)=>[v_nom zeros(size(v_nom,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Buses",2,5)=>[v_max zeros(size(v_max,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Buses",2,6)=>[v_min zeros(size(v_min,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Buses",2,7)=>[v_real zeros(size(v_real,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Buses",2,8)=>[v_imag zeros(size(v_imag,1))]))

ods_write("data_conversion\\$(name).ods",Dict(("Lines",2,1)=>[fr_branch zeros(size(fr_branch,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Lines",2,2)=>[to_branch zeros(size(to_branch,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Lines",2,3)=>[g_branch zeros(size(g_branch,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Lines",2,4)=>[b_branch zeros(size(b_branch,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Lines",2,5)=>[g_sh_branch zeros(size(g_sh_branch,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Lines",2,6)=>[b_sh_branch zeros(size(b_sh_branch,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Lines",2,7)=>[rate_a_branch zeros(size(rate_a_branch,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Lines",2,8)=>[br_stat zeros(size(br_stat,1))]))

# ods_write("data_conversion\\$(name).ods",Dict(("Transformers",2,1)=>)
ods_write("data_conversion\\$(name).ods",Dict(("Transformers",2,1)=>[fr_branch_tr zeros(size(fr_branch_tr,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Transformers",2,2)=>[to_branch_tr zeros(size(to_branch_tr,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Transformers",2,3)=>[g_tr zeros(size(g_tr,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Transformers",2,4)=>[b_tr zeros(size(b_tr,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Transformers",2,5)=>[b_sh_tr zeros(size(b_sh_tr,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Transformers",2,6)=>[ratio_tr zeros(size(ratio_tr,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Transformers",2,7)=>[rmin_tr zeros(size(rmin_tr,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Transformers",2,8)=>[rmax_tr zeros(size(rmax_tr,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Transformers",2,9)=>[rate_a_tr zeros(size(rate_a_tr,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Transformers",2,10)=>[br_stat_tr zeros(size(br_stat_tr,1))]))
# ods_write("data_conversion\\$(name).ods",Dict(("Transformers",2,11)=>[shift_angle zeros(size(shift_angle,1))]))

ods_write("data_conversion\\$(name).ods",Dict(("Loads",2,1)=>[load_bus_map zeros(size(load_bus_map,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Loads",2,2)=>[pd_load  zeros(size(pd_load,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Loads",2,3)=>[qd_load  zeros(size(qd_load,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Loads",2,4)=>[columns  zeros(size(columns,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Loads",2,5)=>[columns  zeros(size(columns,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Loads",2,6)=>[columns  zeros(size(columns,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Loads",2,7)=>[columns  zeros(size(columns,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Loads",2,8)=>[columns  zeros(size(columns,1))]))

ods_write("data_conversion\\$(name).ods",Dict(("P_Profiles_Load",2,1)=>[load_bus_map zeros(size(load_bus_map,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("P_Profiles_Load",2,2)=>[pd_load  zeros(size(pd_load,1))]))

ods_write("data_conversion\\$(name).ods",Dict(("Q_Profiles_Load",2,1)=>[load_bus_map zeros(size(load_bus_map,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Q_Profiles_Load",2,2)=>[qd_load  zeros(size(qd_load,1))]))


ods_write("data_conversion\\$(name).ods",Dict(("Gens",2,1)=>[gen_bus_map  zeros(size(gen_bus_map,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Gens",2,2)=>[pg_gen  zeros(size(pg_gen,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Gens",2,3)=>[qg_gen  zeros(size(qg_gen,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Gens",2,4)=>[qmax_gen  zeros(size(qmax_gen,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Gens",2,5)=>[qmin_gen  zeros(size(qmin_gen,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Gens",2,6)=>[vg_gen  zeros(size(vg_gen,1))]))
# ods_write("data_conversion\\$(name).ods",Dict(("Gens",2,7)=>[gen_stat  zeros(size(gen_stat,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Gens",2,7)=>[pmax_gen  zeros(size(pmax_gen,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Gens",2,8)=>[pmin_gen  zeros(size(pmin_gen,1))]))
# ods_write("data_conversion\\$(name).ods",Dict(("Gens",2,9)=>[cost_a  zeros(size(cost_a,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Gens",2,10)=>[cost_b  zeros(size(cost_b,1))]))
# ods_write("data_conversion\\$(name).ods",Dict(("Gens",2,11)=>[cost_c  zeros(size(cost_c,1))]))
ods_write("data_conversion\\$(name).ods",Dict(("Base_MVA",2,1)=>[data["baseMVA"]  zeros(size(data["baseMVA"],1))]))

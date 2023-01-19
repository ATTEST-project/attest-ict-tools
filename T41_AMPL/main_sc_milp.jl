################################################################################
# This following code corresponds to the Ancillary Services Procurement Tool in
# the Day-Ahead Operation Planning of Active Distribution System. Please cite the
# following work if you use this algorithm in your work. Thanks!

# Usman, M., & Capitanescu, F. (2022). A Novel Tractable Methodology to Stochastic Multi-Period AC OPF in Active Distribution Systems Using Sequential Linearization Algorithm. IEEE Transactions on Power Systems.

# @article{usman2022novel,
#       title={A Novel Tractable Methodology to Stochastic Multi-Period AC OPF in Active Distribution Systems Using Sequential Linearization Algorithm},
#       author={Usman, Muhammad and Capitanescu, Florin},
#       journal={IEEE Transactions on Power Systems},
#       year={2022},
#       publisher={IEEE}
# }
################################################################################
using JuMP,Ipopt,OdsIO,MathOptInterface,Juniper,Plots, LinearAlgebra, Dates,
AmplNLWriter, Cbc, XLSX, DataFrames

#-------------------Accessing current folder directory--------------------------
println(pwd());
cd(dirname(@__FILE__))
println(pwd());
################################################################################
#### -----------  Compilation of User-Defined Functions -------------------#####
################################################################################
include("ac_power_flow_func_check.jl")
include("ac_power_flow_model_check.jl")

include("ac_power_flow_model_opf_int.jl")
include("ac_power_flow_opf_functions_int.jl")

include("ac_power_flow_model_opf.jl")
include("ac_power_flow_opf_functions.jl")

include("data_nw_functions.jl")                                                  # Transformer data file is independant of multi-period and scenarios
include("power_flow_funcitons_milp.jl")
include("loop_finding.jl")

include("opf_functions.jl")
include("sql_loop.jl")
include("sql_opf_model.jl")
include("opf_model_sub_functions.jl")
include("model_sol_recovery.jl")

include("data_nw_functions_pf.jl")                                               # Transformer data file is indepdendant of multi-period and scenarios
include("non_linear_power_equations.jl")

include("data_types.jl")                                                         # Reading the structure of network related fields
include("data_reader.jl")                                                        # Function setting the data corresponding to each network quantity

################################################################################
######################  Select the Input file ##################################
################################################################################
#### --------------------- UK Network Files ------------------------------- ####
# filename_mat =  "input_data/uk_dx_01_2020.ods"
# filename_addt = "input_data/uk_dx_01_2020_flex.ods"
#### ---------------- Portuguese Network Files ---------------------------- ####
# filename_mat =  "input_data/pt_dx_01_2020.ods"
# filename_addt = "input_data/pt_dx_01_2020_flex.ods"
#### ---------------- Spanish Network Files ---------------------------- ####
# filename_mat =  "input_data/es_dx_01_2020.ods"
# filename_addt = "input_data/es_dx_01_2020_flex.ods"
#### -------------------- Croatia Network Files --------------------------- ####
################### ------------ WP4 -------------------------- ################
# filename_mat =  "input_data/hr_dx_01_green_2020.ods"
# filename_addt = "input_data/hr_dx_01_2020_green_flex.ods"
#
# filename_mat =  "input_data/hr_dx_01_red_2020.ods"
# filename_addt = "input_data/hr_dx_01_2020_red_flex.ods"
#
# filename_mat =  "input_data/hr_dx_01_brown_2020.ods"
# filename_addt = "input_data/hr_dx_01_2020_brown_flex.ods"

filename_mat = get(parameters, "network_file", "")
filename_addt = get(parameters, "auxiliary_file", "")
println("£ filename_mat: $filename_mat");
println("£ filename_addt: $filename_addt");

##### ----------------- WP4 -> WP5 Interaction ----------------------------#####
# filename_mat =  "input_data/WP5/hr_kpc_10_black.ods"
# filename_addt = "input_data/WP5/hr_kpc_10_black_flex.ods"

# filename_mat =  "input_data/WP5/hr_kpc_10_red.ods"
# filename_addt = "input_data/WP5/hr_kpc_10_red_flex.ods"

# filename_mat =  "input_data/WP5/hr_kpc_10_blue.ods"
# filename_addt = "input_data/WP5/hr_kpc_10_blue_flex.ods"

# filename_mat =  "input_data/WP5/hr_kpc_10_green.ods"
# filename_addt =  "input_data/WP5/hr_kpc_10_green_flex.ods"
################################################################################
######################  Select the Output file ##################################
################################################################################
#### --------------------- UK Network Files ------------------------------- ####
# file_op = "output_data/uk_output.xlsx"
#### ---------------- Portuguese Network Files ---------------------------- ####
# file_op = "output_data/pt_output.xlsx"
#### -------------------- Croatia Network Files --------------------------- ####
# file_op = "output_data/hr_green_output.xlsx"
# file_op = "output_data/hr_red_output.xlsx"
# file_op = "output_data/hr_brown_output.xlsx"
#### ---------------------- Spain Network Files --------------------------- ####
# file_op = "output_data/es_output.xlsx"

file_op = get(parameters, "output_file", "")
println("£ file_op: $file_op");

################################################################################
### -------------------- Reading Input Data Files -------------------------- ###
################################################################################
include("interface_excel.jl")                                                    # Reading Input Network data and additional flexibility data corresponding to the network

#filename = "input_data/scenario_gen.ods"                                         # Reading Scenario files generated by Scenario Generation Tool Box
filename = get(parameters, "scenario_file", "")
println("£ filename: $filename");

include("interface_scenarios.jl")

################################################################################
### ---------------------- Constants Declaration -------------------------- ####
################################################################################
include("constants.jl")
include("constants_pf_opf.jl")

## ------------------------------- Network Data ---------------------------#####
(idx_from_line, idx_to_line, yij_line,yij_line_sh,tap_ratio,tap_ratio_min,tap_ratio_max,nTrsf,dLines) = data_lines(array_lines,nw_lines,nLines)
idx_tap  = data_trsf(dLines)
dLines   = [dLines idx_tap]

node_data  = data_nodes(nBus,nw_buses,idx_from_line,idx_to_line,yij_line,yij_line_sh,tap_ratio,tap_ratio_min,tap_ratio_max,idx_tap,node)
(tdata,itap_tr,itap_0) = data_trsf_tap(node_data)
itap_r  = data_trsf_tap_index(tdata,itap_tr,itap_0)

itap    = union(itap_tr,setdiff(itap_0,itap_r))
tdata   = tdata[itap,:]

(trsf_fict_nodes,tap_ratio_range,tratio_init,n_tap) = fictitious_trsf_node_new(tap_ratio,rdata_buses,tdata,nw_trsf,rdata_trsf)

(cfl_inc,cfl_dec,cost_load_inc,cost_load_dec,bus_data_lsheet,idx_Gs_lsheet,idx_Bs_lsheet,idx_St_lsheet,nFl,iFl,nd_fl) = data_load(nw_loads,rheader_loads,rdata_loads,nLoads,nTP,nSc,sbase)
(bus_data_gsheet,i_ncurt_gens,i_curt_gens,nNcurt_gen,nCurt_gen,nd_ncurt_gen,nd_curt_gen,Pg_max,Pg_min,Qg_max,Qg_min,cA_gen,cB_gen,cC_gen) = data_gen(nw_gens,nw_gcost,rheader_gens,rdata_gens,nGens,nTP)

(bus_data_Ssheet,bus_data_Strcost,idx_St_Strsheet,iStr_active,nStr_active,nd_Str_active,cA_str,cB_str,cC_str,cost_a_str,cost_b_str,cost_c_str) = data_storage(rheader_storage,rdata_storage,nw_storage,nw_Strcost,nTP,nSc,sbase)

(p_load,q_load,pg_max,pg_min,qg_max,qg_min,cost_a_gen,cost_b_gen,cost_c_gen) = data_load_gen(nLoads,nGens,nTP,nSc,bus_data_lsheet,bus_data_gsheet,Pg_max,Pg_min,Qg_max,Qg_min,nw_pPrf_data_load,nw_qPrf_data_load,nw_pPrf_data_gen_max,nw_pPrf_data_gen_min,nw_qPrf_data_gen_max,nw_qPrf_data_gen_min,nw_loads,sbase,scenario,scenario_data_p_max,scenario_data_p_min,scenario_data_q_max,scenario_data_q_min,cA_gen,cB_gen,cC_gen)

graph = rdata_lines[:,1:2]
graph = convert.(Int64,graph)
cycleList = cycles_finding(graph,numCycles,cycles)                               # Loop finding Code
oltc_ratio  = zeros(Float64,(nSc,nTP,nTrsf))

## -------------------------- AC Power Flow ---------------------------------###
# vol_nodes_mag_pf   = zeros(nSc_pf,nTP_pf,size(nw_buses,1))
# vol_nodes_theta_pf = zeros(nSc_pf,nTP_pf,size(nw_buses,1))
##-----------------Scheme to run different types of AC-Power Flow ----------####
# 1. Deterministic SP: scenario = 0, nSc_pf = 1, nTP_pf = 1
# 2. Deterministic MP: scenario = 0, nSc_pf = 1, nTP_pf = 24
# 3. Stochastic MP (Avg): scenario = 1, nSc_pf = 1, nTP_pf = 24
# 4. Stochastic MP (Full): scenario = 1, nSc_pf = 10, nTP_pf = 24
# 5. Stochastic SP is not programmed
##------------------------------------------------------------------------------
idx_curt_dg = zeros(size(i_curt_gens,1))
for i in 1:size(i_curt_gens,1)
idx_curt_dg[i,1] = i_curt_gens[i][1]
end
idx_curt_dg = convert.(Int64,idx_curt_dg)

p_curt_pf = zeros(nSc_pf,nTP_pf,nCurt_gen)./sbase
p_dis_pf  = zeros(nSc_pf,nTP_pf,nStr_active)./sbase
p_ch_pf   = zeros(nSc_pf,nTP_pf,nStr_active)./sbase
p_od_pf   = zeros(nSc_pf,nTP_pf,nFl)./sbase
p_ud_pf   = zeros(nSc_pf,nTP_pf,nFl)./sbase
q_dg_pf   = tan(acos(dg_ac_pf)).*(pg_max[:,:,idx_curt_dg]-p_curt_pf)
oltc_tap_init = tratio_init                         # Unless the profile of tap ratio is given, it is fixed to the same value in all time-periods and all scenarios
p_strg_pf = p_dis_pf-p_ch_pf

pg_max_pf = pg_max[pf_scenario,:,:]
pg_min_pf = pg_min[pf_scenario,:,:]
qg_max_pf = qg_max[pf_scenario,:,:]
qg_min_pf = pg_min[pf_scenario,:,:]

pg_max_pf = reshape(pg_max_pf,(nSc_pf_new,nTP_pf_new,nGens))
pg_min_pf = reshape(pg_min_pf,(nSc_pf_new,nTP_pf_new,nGens))
qg_max_pf = reshape(qg_max_pf,(nSc_pf_new,nTP_pf_new,nGens))
qg_min_pf = reshape(qg_min_pf,(nSc_pf_new,nTP_pf_new,nGens))
prob_scs_pf = prob_scs[pf_scenario,1]


q_dg_pf   = tan(acos(dg_ac_pf)).*(pg_max[:,:,idx_curt_dg]-p_curt_pf)
oltc_tap_init = tratio_init                         # Unless the profile of tap ratio is given, it is fixed to the same value in all time-periods and all scenarios

idx_status_oltc = findall(x->x==1,rdata_trsf[:,end])
idx_slack_bus_pf = findall(x->x==slack_bus_type,rdata_buses[:,2])
if !isempty(idx_status_oltc)
    for s in 1:nSc_pf
        for i in 1:size(idx_status_oltc,1)
            oltc_tap_init[s,:,idx_status_oltc[i,1]] = rdata_oltcProfile[idx_status_oltc[i,1],2:nTP+1]
        end
    end
end
vm_ac     = zeros(nBus,nTP,nSc)
va_ac     = zeros(nBus,nTP,nSc)

display("Initial AC-Power Flow before MILP Model")

(vol_nodes_mag_pf,vol_nodes_theta_pf,vol_rect_pf) = ac_power_flow_opf_int(nBus,nLines,nNcurt_gen,rdata_buses,nSc_pf,nTP_pf,prob_scs_pf,time_step,stoch_model,p_curt_pf,
p_od_pf,p_ud_pf,p_strg_pf,q_dg_pf,nw_buses,nw_lines,rdata_loads,bus_data_lsheet,bus_data_Ssheet,node_data,nd_fl,nd_curt_gen,nd_ncurt_gen,p_load,q_load,idx_Gs_lsheet,idx_Bs_lsheet,yii_sh,i_curt_gens,sbase,flex_oltc,vbase,Ibase,
pg_min_pf,pg_max_pf,qg_min_pf,qg_max_pf,yij_line,dLines,i_ncurt_gens,error_msg,pgen_tol,qgen_tol,oltc_tap_init,vol_cstr_tol)

(br_crnt_pu_pf_int,br_crnt_si_pf_int,br_pwr_pu_pf_int,br_pwr_si_pf_int) = recovery_branch_current_pf(nSc,nTP,nLines,nw_lines_pf,vol_rect_pf,yij_line,Ibase,sbase,ybase,vbase,oltc_tap_init,dLines)

(vol_viol_int,crnt_viol_int,max_vol_viol_int,max_crnt_viol_int,viol_nodes_int,nVol_viol_int,avg_vol_viol_int,above_avg_vol_viol_int,below_avg_vol_viol_int,
nCrnt_viol_int,avg_crnt_viol_int,above_avg_crnt_viol_int,below_avg_crnt_viol_int,vol_viol_cn_lin_int) =
constraint_violation_pf(nBus,nw_buses,nLines,nw_lines,nTP,nSc,vol_nodes_mag_pf,br_crnt_si_pf_int,I_rat,1)

if !isempty(max_vol_viol_int)
    vol_viol_max_int  = maximum(max_vol_viol_int)
    vol_viol_less_tol = size(findall(x->x<=1,max_vol_viol_int),1)
else
    vol_viol_max_int = 0.001
    vol_viol_less_tol = 0.0
end

if !isempty(max_crnt_viol_int)
    crnt_viol_max_int      = maximum(max_crnt_viol_int)
    crnt_viol_less_tol = size(findall(x->x<=1,max_crnt_viol_int),1)
else
    crnt_viol_max_int = 0.001
    crnt_viol_less_tol = 0.0
end
# Number Max Avg Above_Avg Below_Avg Less than 1%
vol_viol_nw_int  = [nVol_viol_int  vol_viol_max_int  avg_vol_viol_int  above_avg_vol_viol_int  below_avg_vol_viol_int vol_viol_less_tol]
crnt_viol_nw_int = [nCrnt_viol_int crnt_viol_max_int avg_crnt_viol_int above_avg_crnt_viol_int below_avg_crnt_viol_int crnt_viol_less_tol]

slack_nd = convert.(Int64,rdata_buses[idx_slack_bus_pf,1])
slack_nd = slack_nd[1,1]

idx_slack_from = findall(x->x==slack_nd,rdata_lines[:,1])
idx_slack_to   = findall(x->x==slack_nd,rdata_lines[:,2])

num_slack_cnctd_nodes = size(idx_slack_from,1)+size(idx_slack_to,1)              # Number of nodes connecred to the slack = Number of times slack appear in the From and To columns
to_nodes   = convert.(Int64,rdata_lines[idx_slack_from,2])
from_nodes = convert.(Int64,rdata_lines[idx_slack_to,1])
slack_cnctd_nodes    = vcat(to_nodes,from_nodes)
slack_cnctd_nodes    = vcat(slack_nd,slack_cnctd_nodes)
br_crnt_si_pf_cnv    = zeros(nSc,nTP,nLines)
br_pwr_si_pf_cnv     = zeros(nSc,nTP,nLines)

v_mag_pf_int = deepcopy(vol_nodes_mag_pf)
v_ang_pf_int = deepcopy(vol_nodes_theta_pf)

(vol_viol_nw,vol_viol_nw_max,crnt_viol_nw,crnt_viol_nw_max,vol_nodes_pf_cnv,vol_nodes_ang_pf_cnv,br_crnt_si_pf_cnv,sql_obj,sql_time,rel_max_error,rel_avg_error,norm_s_err_max_power,norm_s_err_avg,
p_curt_gen,q_curt_gen,total_p_curt,str_dis,str_ch,viol_nodes_new,p_curt_lin,min_vol_limit,max_vol_limit,oltc_ratio,p_err_max_power,q_err_max_power,vm_ac,va_ac,vol_viol_cn_milp,model_infs,br_crnt_opf_app,br_crnt_opf_ex,
p_res_curt_op,q_res_op,fl_inc_op,fl_dec_op,p_ch_op,p_dis_op,p_strg_op,p_slack_pf_ip,q_slack_pf_ip,br_pwr_si_pf_cnv,v_rect_euler,v_rect_cmplx) = sql_loop(vol_viol_max,vol_viol_tol,crnt_viol_max,crnt_viol_tol,lin_itr,lin_itr_max,vol_nodes_mag_pf,vol_nodes_theta_pf,nSc,nTP,nBus,nNcurt_gen,nCurt_gen,nTrsf,nStr_active,nFl,nd_fl,flex_apc,flex_oltc,
flex_adpf,flex_str,flex_fl,str_bin,fl_bin,rdata_buses,nLines,trsf_fict_nodes,tap_ratio_range,oltc_bin,prob_scs,time_step,tdata,bus_data_Ssheet,bus_data_lsheet,cost_a_str,cost_b_str,cost_c_str,cost_load_inc,
cost_load_dec,nw_buses,rdata_loads,node_data,nd_curt_gen,nd_ncurt_gen,p_load,q_load,idx_Gs_lsheet,idx_Bs_lsheet,pg_max,yii_sh,i_curt_gens,sbase,dg_pf,iStr_active,yij_line,dLines,i_ncurt_gens,nw_lines,bus_data_gsheet,
pg_min,qg_min,qg_max,pgen_tol,qgen_tol,p_tol,q_tol,rcvr_branch,rcvr_inj,rcvr_tso_dso,Ibase,idx_slack_bus_pf,solver_ipopt,solver_cbc,solver_bonmin,sql_itr,sql_itr_max,s_inj_error_rel,s_error_tol,angle_lb,angle_ub,
cycleList,idx_slack_from,idx_slack_to,num_slack_cnctd_nodes,slack_cnctd_nodes,slack_nd,stoch_model,tratio_init,rdata_storage,load_theta,nd_Str_active,slack_bus_type,vol_ctrl_bus_type,load_bus_type,
rdata_gens,nw_pPrf_data_load,nw_qPrf_data_load,nw_pPrf_data_gen_max,nw_qPrf_data_gen_max,scenario_data_p_min,scenario_data_p_max,scenario_data_q_min,scenario_data_q_max,nw_buses_pf,nw_lines_pf,nw_loads_pf,nw_gens_pf,
nw_gcost_pf,nw_sbase_pf,v_initial_pf,v_mag_pf,v_angle_pf,max_mismatch_pf,epsilon,iteration,itr_max,ordata_buses_pf,ybase,vbase,I_rat,vol_viol_nw,vol_viol_nw_max,crnt_viol_nw,crnt_viol_nw_max,min_vol_limit,max_vol_limit,max_crnt_limit,term_status,vol_cstr_tol,br_crnt_si_pf_cnv,solver_cplex,int_tol,opt_tol,num_thread,rdata_trsf,nTrsf_s1,nw_trsf,n_tap,br_pwr_si_pf_cnv)

################################################################################
###################### Output Data to Comillas Tools ###########################
################################################################################

# severity = br_crnt_si_pf_cnv./max_crnt_limit_si
# severity = maximum(permutedims(reshape(severity,nTP,nLines)),dims=2)
#
# br_pwr = permutedims(reshape(br_pwr_si_pf_cnv,nTP,nLines))
# p_pwr = real(br_pwr)
# q_pwr = imag(br_pwr)

################################################################################
######################### Output Data to ICENT Tools ###########################
################################################################################

### ---- Curtailed Active Power and Output Reactive Power from RES Data -----###
nodes_curt_gen = Int64.(rdata_gens[idx_curt_dg,1])
avg_p_gen_curt = reshape(sum(prob_scs.*p_res_curt_op,dims=1),(nTP,nCurt_gen))
avg_q_gen_curt = reshape(sum(prob_scs.*q_res_op,dims=1),(nTP,nCurt_gen))

avg_p_gen_curt = permutedims(avg_p_gen_curt)
avg_q_gen_curt = permutedims(avg_q_gen_curt)

avg_p_gen_curt = hcat(nodes_curt_gen,avg_p_gen_curt)
avg_q_gen_curt = hcat(nodes_curt_gen,avg_q_gen_curt)

# ################################################################################
# ##### ----------------- Flexible Load Data --------------------------------#####
# ################################################################################
nodes_fl = Int64.(rdata_loads[iFl,1])
avg_fl_inc   = prob_scs.*fl_inc_op
avg_fl_dec   = prob_scs.*fl_dec_op

avg_fl_inc_op  = permutedims(avg_fl_inc[sc_max_prob,:,:])
avg_fl_dec_op  = permutedims(avg_fl_dec[sc_max_prob,:,:])

avg_fl_inc_op = hcat(nodes_fl,avg_fl_inc_op)
avg_fl_dec_op = hcat(nodes_fl,avg_fl_dec_op)

# ################################################################################
# ##### ----------------- Energy Storage Data --------------------------------####
# ################################################################################
nodes_str = Int64.(rdata_storage[iStr_active,1])
avg_p_ch_nd  = prob_scs.*p_ch_op
avg_p_dch_nd = prob_scs.*p_dis_op

avg_p_ch_op    = permutedims(avg_p_ch_nd[sc_max_prob,:,:])
avg_p_dch_op   = permutedims(avg_p_dch_nd[sc_max_prob,:,:])

avg_p_ch_op  = hcat(nodes_str,avg_p_ch_op)
avg_p_dch_op = hcat(nodes_str,avg_p_dch_op)
# ###############################################################################
#
header_op = ["nodes","t1","t2","t3","t4","t5","t6","t7","t8","t9","t10","t11",
"t12","t13","t14","t15","t16","t17","t18","t19","t20","t21","t22","t23","t24"]

df_p_curt = DataFrame(avg_p_gen_curt,header_op)
df_q_res  = DataFrame(avg_q_gen_curt,header_op)

df_fl_inc = DataFrame(avg_fl_inc_op,header_op)
df_fl_dec = DataFrame(avg_fl_dec_op,header_op)

df_str_ch  = DataFrame(avg_p_ch_op,header_op)
df_str_dch = DataFrame(avg_p_dch_op,header_op)
#
# ################################################################################
# ################## Cost of Procurement of Flexibility ##########################
# ################################################################################
header_cost = ["cost_flex"]
data_obj = reshape(sql_obj,(sql_itr_max*lin_itr_max))
idx_0 = findall(x->x!=0,data_obj)
cost_flex_proc = [data_obj[idx_0[end]]]
df_cost_pr = DataFrame(cost = cost_flex_proc)
#
# ################################################################################
# ####------------- Writing Output Data to Excel File ---------------------- #####
# ################################################################################
XLSX.writetable(file_op,APC_MW=(collect(DataFrames.eachcol(df_p_curt)),DataFrames.names(df_p_curt)),
EES_CH_MW=(collect(DataFrames.eachcol(df_str_ch)),names(df_str_ch)),
EES_DCH_MW=(collect(DataFrames.eachcol(df_str_dch)),names(df_str_dch)),
FL_OD_MW=(collect(DataFrames.eachcol(df_fl_inc)),names(df_fl_inc)),
FL_UD_MW=(collect(DataFrames.eachcol(df_fl_dec)),names(df_fl_dec)),
COST=(collect(DataFrames.eachcol(df_cost_pr)),names(df_cost_pr)),
;overwrite=true)
# ################################################################################

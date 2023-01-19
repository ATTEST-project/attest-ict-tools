using Ipopt

# filename="input_data\\SA_results_$nBus.ods"
# converged_PF=ods_readall(filename;sheetsNames=["PF"],innerType="Matrix") #p g v θ
# for i in 1:nGens
#       nw_gens[i].gen_Pg_avl=converged_PF["PF"][:,1][i]
#       nw_gens[i].gen_V_set=converged_PF["PF"][:,3][i]
# end
# nSc=1
# nTP=1

AC_SCOPF = Model(Ipopt.Optimizer)

model_name=AC_SCOPF
# set_optimizer_attributes(model_name,"mu_strategy"=>"adaptive")
set_optimizer_attributes(model_name,"tol"=>1e-05)
# set_optimizer_attributes(acopf,"mumps_mem_percent"=>100)
# set_optimizer_attributes(acopf,"barrier_tol_factor"=>1e-6)

(e, f, Pg, Qg, pen_ws, pen_lsh, p_fl_inc, p_fl_dec, p_ch, p_dis, soc)                      =variables_n(model_name)
# (e_c, f_c, Pg_c, Qg_c)=variables_c(model_name)
(vol_const_nr)=voltage_cons_n(model_name,"range")
# (vol_const_cn)=voltage_cons_c(model_name,"range")
if nFl!=0
FL_cons_normal(model_name)
end
if nStr_active!=0
storage_cons_normal(model_name)
end 
gen_limits_n(model_name,"range")
# gen_limits_c(model_name,"range")
(pinj_dict,qinj_dict)        =line_expression_n(model_name)
# (pinj_dict_c,qinj_dict_c,pinj_dict_c_sr,qinj_dict_c_sr)=line_expression_c(model_name)

(active_power_balance_normal)=active_power_bal_n(model_name,pinj_dict)
# (active_power_balance_contin)=active_power_bal_c(model_name,pinj_dict_c)
(reactive_power_balance_normal)=reactive_power_bal_n(model_name,qinj_dict)
# (reactive_power_balance_contin)=reactive_power_bal_c(model_name,qinj_dict_c)

(line_flow_normal_s,line_flow_normal_r)=line_flow_n(model_name,pinj_dict,qinj_dict,0 )
# (line_flow_contin_s,line_flow_contin_r)=line_flow_c(model_name,pinj_dict_c_sr,qinj_dict_c_sr,0 )

# coupling_constraint(model_name)

(total_cost,cost_gen,cost_pen_lsh,cost_fl,cost_str, cost_pen_ws)=objective_OPF(model_name)


optimize!(model_name)
println("Objective value", JuMP.objective_value(model_name))
println("Solver Time ", JuMP.solve_time(model_name))


# #
# (v_sq,voltage_gen,volt_ang,v_sq_c,voltage_gen_c,volt_ang_c)=rect_to_polar("normal")
# # # #
# v_gen=[voltage_gen[i] for i in 1:nBus if ~isempty(findall(x->x==i, bus_data_gsheet))]
# v_ang=[volt_ang[i] for i in 1:nBus if ~isempty(findall(x->x==i, bus_data_gsheet))]

# ods_write("input_data\\SA_results_$nBus.ods",Dict(("PF",1,1)=>[value.(Pg[1,:]) value.(Qg[1,:]) v_gen v_ang]) )

# (input_normal,input_contin,power_flow_normal_result2,power_flow_contin_result2)=power_flow("normal","non_initial", "out_of_OPF","v_sqr","v_sqr","contin")
# power_flow("normal/contin/all","initial/non_initial", "out_of_PF/out_of_OPF",0 if out of Pf and v_sqr/v_pol if out of opf,0 if out of SA and v_sqr/v_pol if out of contin, "contin/SA")

# #
# (nw_lines_pf,nw_loads_pf,nw_gens_pf,nw_sbase_pf,v_initial_pf,epsilon,epsilon_suf,iteration,itr_max,maxiter,load_bus_type,vol_ctrl_bus_type,slack_bus_type,
# v_sp_pf,node_vol_pf,v_angle_pf)=power_flow_initialization(array_bus,array_lines,array_loads,array_gens,array_sbase,rdata_buses)
#
#
# (p_scheduled_normal,q_scheduled_normal,v_mag_total,nd_shunt,nd_ren_curt,nd_load_curt,p_fl_inc,p_fl_dec,p_ch,p_dis)=PF_input_normal("out_of_OPF","v_pol")
# (p_scheduled_contin,q_scheduled_contin,nd_shunt_c,nd_ren_curt_c,nd_load_curt_c,v_mag_total_c,p_fl_inc_c,p_fl_dec_c,p_ch_c,p_dis_c)=PF_input_contin("contin","v_pol")
# (pf_result_perscen_normal,branch_flow_check,voltage_viol_number,volt_viol_normal)=run_PF_normal("non_initial")
# (pf_per_dimension,branch_flow_check_c,voltage_viol_contin_number,volt_viol_contin)=run_PF_contin("contin")
# total_result("all")

# (nTP,nSc,prof_PRES,RES_bus,nRES)=f_prof_PRES()

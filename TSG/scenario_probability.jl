function scenario_prob(scenarios,base_case)
#------------- Determining the probabilities of each wind scenario -------------
prob_scenario = Model()

set_optimizer(prob_scenario,Ipopt.Optimizer)                                     # Here the solver is being set
set_optimizer_attributes(prob_scenario,"tol"=>1e-6)

@variables(prob_scenario,begin
    prob[1:size(scenarios,2)]
end)

#--------Objective (Minimizing the difference from the historical data) --------
scenario_new = scenarios
base_case_new = base_case
prb_time_tmp = []
for t in 1:size(scenario_new,1)  # 1st dimension is Time 
    prb_sc_tmp = []
    for s in 1:size(scenario_new,2) # 2nd dimesnion is Scenario
        prb_sc = prob[s,1]*scenario_new[t,s]
        # prb_sc = (prob[s,1]*scenario_new[t,s]-base_case_new[t,1])^2
        push!(prb_sc_tmp,prb_sc)
    end
    push!(prb_time_tmp,(sum(prb_sc_tmp[j,1] for j in 1:size(prb_sc_tmp,1))-base_case_new[t,1])^2)
    # push!(prb_time_tmp,(sum(prb_sc_tmp[j,1] for j in 1:size(prb_sc_tmp,1))))

end
sc_prb = sum(prb_time_tmp[j,1] for j in 1:size(prb_time_tmp,1))
@objective(prob_scenario,Min,sc_prb)

#------------------------- Constraints ----------------------------------------
@constraint(prob_scenario,sum(prob[j,1] for j in 1:size(prob,1))==1)

for i in 1:size(prob,1)
    @constraint(prob_scenario,prob[i,1]>=0.0)
end
#-------------------------- Solving the Model ----------------------------------
print(prob_scenario)
status = optimize!(prob_scenario)
println("Objective value", JuMP.objective_value(prob_scenario))

#--------------------- Probability of scenarios---------------------------------
return prb_sc  = JuMP.value.(prob[:,1])
end

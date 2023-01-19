##---- Common file for generating the Wind and Soalr Power scenarios------------
using Distributions, StatsBase, DataFrames, CSV, HypothesisTests, LinearAlgebra, OdsIO
using Plots, StatsPlots, PyCall, BoxCoxTrans, JuMP, Ipopt, Random, Roots, ARFIMA

println(pwd());
cd(dirname(@__FILE__))
println(pwd());

include("adf_test_results.jl")
include("acf_pacf_plots.jl")
include("weibull_estimator.jl")
include("windpower_cube.jl")
include("windpower_weibull.jl")
include("data_type_scenario.jl")
include("scenario_probability.jl")

##---------------------- Constants and Variable Definitions -------------------
Random.seed!(2345);
model_hr    = []
ar_params   = []
ma_params   = []
hr_nf       = []    # hour for which there is not fitting of the model!
nScenarios  = 10
v_cut_in    = 1.5   # (m/s)
v_cut_out   = 22    # (m/s)
v_rat       = 10    # (m/s)
p_rat       = 1.0   # (kW)
day_time    = collect(6:16)     # Number of hours for which the data has to be taken!
summer_time = collect(150:300)  # Days for which solar data is used to determine the best ARMA model
hrs         = 24
arima_order = 4
def_limit   = 10^9
p_rat_pv    = 1000 #(1kw)
##---------------------- Importing functions from Python .----------------------
adf         = pyimport("statsmodels.tsa.stattools")                                    # Handler for ADF test in Python
kps         = pyimport("statsmodels.tsa.stattools")                                    # Handler for KPSS test in Python
arima       = pyimport("statsmodels.tsa.arima_model")                                  # Handler for ARIMA Model in Python
arima       = pyimport("statsmodels.tsa.arima.model")
arima_results = pyimport("statsmodels.tsa.arima.model")

plot_acf_py  = pyimport("statsmodels.graphics.tsaplots")
plot_pacf_py = pyimport("statsmodels.graphics.tsaplots")
plt          = pyimport("matplotlib.pyplot")
weibull_py   = pyimport("scipy.stats")
warn_py      = pyimport("warnings")
warn_py      = warn_py.filterwarnings("error")
arma_prcs    = pyimport("statsmodels.tsa.arima_process")

## --------------------------- Improting Data ----------------------------------
println("Loading the dataset")
filename = get(parameters, "input_file", "")

##------------------------------ Solar_data ------------------------------------
sheetname  = "solar_data";
fields  = ["Time (hr)","P (W)"]; # Fields that have to be read from the file
raw_data = ods_readall(filename;sheetsNames=[sheetname],innerType="Matrix")
raw_data = raw_data[sheetname]   # Conversion from Dict to Array
header_solar    = raw_data[1,:]
data_solar      = raw_data[2:end,1:size(header_solar,1)]

days_solar      = convert(Int64,size(data_solar,1)/hrs)
time_solar      = data_solar[:,1]
idx_data        = zeros(days_solar,size(day_time,1))
for i in 1:size(day_time,1)
    idx_time = findall(x->x==day_time[i,1],time_solar)
    idx_time = reshape(idx_time,size(idx_time,1),size(idx_time,2))
    idx_data[:,i] = idx_time
end
idx_data     = convert.(Int64,idx_data)
solar_power  = convert.(Float64,data_solar[:,2])
solar_data   = solar_power[idx_data,1]
solar_summer = solar_data[summer_time,:]

##----------------------------- Wind Data --------------------------------------
sheetname   = "wind_data";
fields      = ["Time (min)","speed (m/s)"]; # Fields that have to be read from the file
raw_data    = ods_readall(filename;sheetsNames=[sheetname],innerType="Matrix")
raw_data    = raw_data[sheetname]   # Conversion from Dict to Array
header_wind = raw_data[1,:]
data_wind   = raw_data[2:end,1:size(header_wind,1)]
speed       = convert.(Float64,data_wind[:,2])
s_train     = speed

## ------------- Determining the shape and scale parameters of------------------
# ------------ Weibull Distribution from historical wind speed data! -----------
par_est_jl = params(fit_mle(Weibull,speed))            # using Julia function provided in weibull_estimator.jl file
par_est_py = weibull_py.exponweib.fit(speed, floc=0, f0=1)   # using Python function to estimate the parameters of weibull distribution

alpha_jl = par_est_jl[1]
theta_jl = par_est_jl[2]

alpha_py = par_est_py[2]
theta_py = par_est_py[4]

rel_diff_alpha = abs((alpha_py-alpha_jl)/(alpha_py))
rel_diff_theta = abs((theta_py-theta_jl)/(theta_py))

if rel_diff_alpha <=1e-2
    alpha = alpha_jl
else
    alpha = alpha_py
end
if rel_diff_theta <=1e-2
    theta = theta_jl
else
    theta = theta_py
end

## -------------------Augmented Dickey Fuller Test-------------------------------
##--------- This is used to check the stationarity of the test-series ----------
critical_values_adf = ("5%","1%","10%")
critical_values_kpss = ("5%","1%","10%","2.5%")
stats_orig = Array{series_stat}(undef,1,1)

# adfuller (array, max_lag,regression = {c,ct,ctt,nc},autolag = {AIC,BIC,t-stat},store,regresults)
aug_df_py  = adf.adfuller(s_train,regression="c",autolag="AIC")                                               # ADF test from Python
data_tmp   = []
adf_data   = adf_test(aug_df_py,data_tmp,critical_values_adf)                        # Retrieving the values of ADF test
stats_orig = series_stat(adf_data...)                                            # Storing the values of ADF test in a structure
print(aug_df_py)

#--------- Determining the auto-regressive and moving average parameters--------
##---------------------Plot ACF and PACF plots ---------------------------------
p,d,q = 1,0,0
model = arima.ARIMA(Transpose(s_train),order=(p,d,q))                            # ARIMA model
model_fit = model.fit()                                                          # Fitted ARIMA model
print(model_fit.summary())
## ----------- Residual plot (Should be of white noise and Gaussian)------------
residuals_wind = model_fit.resid
# plot(residuals, reuse = false, title = "Residuals")
# density(residuals)
##-------------------- AR and MA parameters for the selected model -------------
if p!=0
    ar_params = model_fit.arparams
end
if q!=0
    ma_params = model_fit.maparams
end
## -------- White Noise Scenario Generation based on ARMA function -------------
stoch_fc = zeros(size(s_train,1),nScenarios)                                     # Stochastic forecast--(length of series, number of scenarios)
err      = zeros(size(s_train,1),nScenarios)
ar_fc    = zeros(size(s_train,1)+p,1)
ma_fc    = zeros(size(s_train,1)+q,1)

dist_fit          = fit(Normal,s_train)
mean_dist_fit     = mean(dist_fit)
std_dist_fit      = std(dist_fit)
error_initial     = 0.01

stoch_fc_initial  = mean_dist_fit                                                # Mean value of first-order-differenced series
ar_fc[1:p,1]      .= stoch_fc_initial
ma_fc[1:q,1]      .= error_initial
#------------------ Wind series data obtained -----------------
p_coeff = ar_params
q_coeff = ma_params
ar_terms = []
ma_terms = []

white_noise = Normal(0,sqrt(var(residuals_wind)))                                # Normal dist (mean, std)
for s in 1:nScenarios
       for t in 1:size(s_train,1)
        error_white_noise = rand(white_noise,1)
        error_white_noise = error_white_noise[1]
            if !isempty(ar_params)
                ar_terms = ar_params.*ar_fc[t:(t+p)-1,1]
                ar_terms_sum = sum(ar_terms[j,1] for j in 1:size(ar_terms,1))
            else
                ar_terms = []
                ar_terms_sum = 0.0
            end
            if !isempty(ma_params)
                ma_terms = ma_params.*ma_fc[t:(t+q)-1,1]
                ma_terms_sum = sum(ma_terms[j,1] for j in 1:size(ma_terms,1))
            else
                ma_terms = []
                ma_terms_sum = 0.0

            end
            y_arma = ar_terms_sum - ma_terms_sum + error_white_noise

            ar_fc[(t+p),1] = y_arma
            ma_fc[(t+q),1] = error_white_noise
            stoch_fc[t,s] = y_arma
    end
end
## --------- Distribution transformation from time-series based on--------------
##------ white noise to the time-series based on the requried transformation ---
wind_speed      = zeros(size(stoch_fc,1),size(stoch_fc,2))   # Scenarios for wind speed!
inverse_weibull = Weibull(alpha,theta)
for i in 1:size(wind_speed,2)
    gen_scenario  = stoch_fc[:,i]                                                # Scenario i from the generated time series
    scenario_dist = fit(Normal,gen_scenario)                                     # Why normal dist? Because error term in ARMA model is generated from white noise which follows normal distribution
    scenario_dist_mean = mean(scenario_dist)
    scenario_dist_var  = var(scenario_dist)
    scenario_dist_est  = Normal(scenario_dist_mean,sqrt(scenario_dist_var))      # A dist is defined based on the parameters of generated scenario distribution in order to apply the Distribution Transformation Process
    cum_prob = cdf.(scenario_dist_est,gen_scenario)                              # Cumulative Probability i.e., CDF
    wind_speed[:,i] = quantile.(inverse_weibull,cum_prob)                        # Inverse CDF i.e., Quantile of a distribution
end
#-------------------------------------------------------------------------------
##-------------- Conversion from wind speed to wind power ----------------------
wind_power_gen = zeros(size(wind_speed,1),size(wind_speed,2))
wind_power_org = zeros(size(s_train,1),size(s_train,2))
pwr_trsf  = "weibull"
##--------Cubic formula for determining the power output of wind turbine--------
a = p_rat/(v_rat^3-v_cut_in^3)
b = v_cut_in^3/(v_rat^3-v_cut_in^3)
if pwr_trsf == "cube"
    wind_power_gen = wind_power_cube(wind_power_gen,wind_speed,v_cut_in,v_cut_out,v_rat,p_rat,a,b)  # wind_speed = wind speed scenarios
    wind_power_org = wind_power_cube(wind_power_org,s_train,v_cut_in,v_cut_out,v_rat,p_rat,a,b)     #  s_train = historical wind speed
##----- Weibull formula for determining the power output of wind turbine--------
elseif pwr_trsf == "weibull"
    wind_power_gen = wind_power_weibull(wind_power_gen,wind_speed,v_cut_in,v_cut_out,v_rat,p_rat)
    wind_power_org = wind_power_weibull(wind_power_org,s_train,v_cut_in,v_cut_out,v_rat,p_rat)
end

## ----------------- Probabilities of Scenarios --------------------------------
rp = 3600:3744       # The probabilities are determined for this particular day
wind_power_gen_new   = wind_power_gen[rp,:]
wind_power_org_new   = wind_power_org[rp,1]
prb_wind = scenario_prob(wind_power_gen,wind_power_org)

##------- Rearranging the scenarios with respect to the probabilities ----------
wind_sc   = wind_power_gen
wind_prob = prb_wind
idx_prob = sortperm(wind_prob)

wind_sc_sort = transpose(wind_sc)
wind_sc_sort = wind_sc_sort[idx_prob,:]
wind_sc_sort = transpose(wind_sc_sort)
wind_prob_sort = wind_prob[idx_prob]
bar(wind_prob_sort)

################################################################################
################################################################################

##-------------------- Scenario generation for PV ------------------------------
##-------------- Fit the Distribution to the historical data -------------------
par_fit = zeros(size(day_time,1),2)
for i in 1:size(day_time,1)
    par_est_jl   = params(fit_mle(Weibull,solar_summer[:,i]))
    alpha_fit    = par_est_jl[1]
    theta_fit    = par_est_jl[2]
    par_fit[i,1] = alpha_fit
    par_fit[i,2] = theta_fit
end
#-------------------- Choose best ARMA model ----------------------------------]
ar_params  = []
ma_params  = []
pq         = zeros(hrs,2)
log_lf     = zeros(arima_order,arima_order)
aic_mdl    = zeros(arima_order,arima_order)
bic_mdl    = zeros(arima_order,arima_order)
for t in 1:hrs
    if in(t,day_time)
        for p in 1:arima_order
            for q in 1:arima_order
                try
                    # model = arima.ARIMA(Transpose(solar_data[1:days,(t-day_time[1])+1]),order=(p,0,q))
                    model = arima.ARIMA(Transpose(solar_summer[:,(t-day_time[1])+1]),order=(p,0,q))      # ARIMA model
                    model_fit    = model.fit()
                    log_lf[p,q]  = model_fit.llf      # Log- Likelihood value
                    aic_mdl[p,q] = model_fit.aic      # AIC Information
                    bic_mdl[p,q] = model_fit.bic      # BIC Information
                catch   # Catch the polynomial which is not solved successfully and then discard those values of p and q
                    log_lf[p,q]  = def_limit
                    aic_mdl[p,q] = def_limit
                    bic_mdl[p,q] = def_limit
                end
            end
        end
        aic_result = findmin(aic_mdl)
        bic_result = findmin(bic_mdl)

        if aic_result[1]!=def_limit
            aic_min   = aic_result[1]
            aic_idx_p = aic_result[2][1]
            aic_idx_q = aic_result[2][2]

            bic_min   = bic_result[1]
            bic_idx_p = aic_result[2][1]
            bic_idx_p = aic_result[2][2]

            p = aic_idx_p
            q = aic_idx_q
            pq[t,1] = p
            pq[t,2] = q
            # model = arima.ARIMA(Transpose(solar_data[1:days,(t-day_time[1])+1]),order=(p,0,q))
            model = arima.ARIMA(Transpose(solar_summer[:,(t-day_time[1])+1]),order=(p,0,q))
            model_fit    = model.fit()
            p_params = model_fit.arparams
            q_params = model_fit.maparams

            push!(model_hr,model_fit)
            push!(ar_params,p_params)
            push!(ma_params,q_params)
        else                            # time for which model has not been fit!
            push!(hr_nf,t)
        end
    end
end
## ------------------------ Scenario Generation ---------------------------------
##-------------------- Generate samples from ARMA process ---------------------
# arma_sample = zeros(nScenarios,size(model_hr,1))
# for i in 1:size(model_hr,1)
#     ar = vcat([1],-ar_params[i,1])
#     ma = vcat([1],ma_params[i,1])
#     arma_sample[:,i] = arma_prcs.arma_generate_sample(ar,ma,nsample)
# end
##------------------------ Scenario Generation ---------------------------------
##---------------- Generate samples using ARFIMA process -----------------------
arfima_sample = zeros(nScenarios,size(model_hr,1))
d = nothing
for i in 1:size(model_hr,1)
    model_fit = model_hr[i]
    residual  = model_fit.resid
    std_white = std(residual)
    ar = ar_params[i,1]
    ma = ma_params[i,1]
    ar_svec = SVector{size(ar,1),Float64}(ar)
    ma_svec = SVector{size(ma,1),Float64}(ma)
    arfima_sample[:,i] = arfima(nScenarios,std_white,d,ar_svec,ma_svec)
end
arma_sample = arfima_sample
## ---------------- Distribiution transformation to obtain ---------------------
##--------------------- the Weibull-based PV scenarios -------------------------
pv_scenario = zeros(size(arma_sample,1),size(arma_sample,2))
idx_par     = setdiff(day_time,hr_nf)
idx_par_new = (idx_par.-day_time[1,1]).+1

for i in 1:size(arma_sample,2)
    alpha = par_fit[idx_par_new[i,1],1]
    theta = par_fit[idx_par_new[i,1],2]
    inverse_weibull = Weibull(alpha,theta)

    gen_scenario  = arma_sample[:,i]                                             # Scenario i from the generated time series
    scenario_dist = fit(Normal,gen_scenario)                                     # Why normal dist? Because error term in ARMA model is generated from white noise which follows normal distribution
    scenario_dist_mean = mean(scenario_dist)
    scenario_dist_var  = var(scenario_dist)
    scenario_dist_est  = Normal(scenario_dist_mean,sqrt(scenario_dist_var))      # A dist is defined based on the parameters of generated scenario distribution in order to apply the Distribution Transformation Process
    cum_prob = cdf.(scenario_dist_est,gen_scenario)                              # Cumulative Probability i.e., CDF
    # pv_scenario is in scenario x time format (each row represents 1 scenario)
    pv_scenario[:,i] = quantile.(inverse_weibull,cum_prob)                       # Inverse CDF i.e., Quantile of a distribution
end
#------------- Determining the probabilities of each pv scenario -------------
# Format of data is very important:
# 1. pv_scneario == Scenario x Time format (each row represents 1 scenario)
# 2. pv_sc_fit == Time x Sceanrios format (each column represents 1 scneario)

pv_hist        = zeros(hrs,1)
pv_mean        = transpose(mean(solar_data[summer_time,:],dims=1))
pv_hist[day_time,1] = pv_mean

pv_sc_fit  = zeros(hrs,nScenarios)                                               # values are calculated for the hours which are not fitted!
idx_fit    = setdiff(day_time,hr_nf)
pv_sc_fit[idx_fit,:]  = transpose(pv_scenario)   # format: time x scenario (each column now represents 1 scenario)!
if !isempty(hr_nf)
    for i in 1:size(hr_nf,1)
        nhr = hr_nf[i,1]   # number of hour for which the data is not fitted
        for k in 1:size(pv_sc_fit,2)
            if nhr<= mean(day_time)
                    if nhr==day_time[1] || nhr==day_time[2]
                        sc_value = (pv_sc_fit[nhr+2,k]-pv_sc_fit[nhr+1,k])/2
                    else
                        sc_value = (pv_sc_fit[nhr-2,k]+pv_sc_fit[nhr-1,k])/2             # Scenario value
                    end
            elseif nhr > mean(day_time)
                    idx_mean_day_time = findall(x->x==convert(Int64,mean(day_time)), day_time)
                    if nhr == day_time[idx_mean_day_time[1,1]]+1
                        sc_value = (pv_sc_fit[nhr+1,k]+pv_sc_fit[nhr+2,k])/2
                    else
                        sc_value = (pv_sc_fit[nhr-2,k]-pv_sc_fit[nhr-1,k])/2
                    end
            end
            pv_sc_fit[nhr,k] = sc_value
        end
    end
end
# Probaility function takes the inout format as Times x Scenario format
prb_pv   = scenario_prob(pv_sc_fit[day_time,:],pv_hist[day_time,:])
## ------ Rearranging the scenarios with respect to the probabilities ----------
pv_sc    = pv_sc_fit
pv_prob  = prb_pv
idx_prob = sortperm(pv_prob)

pv_sc_sort = pv_sc[:,idx_prob]
pv_prob_sort = pv_prob[idx_prob]
bar(pv_prob_sort)
## ---------------- Calculation of combined probabilities ----------------------
# A simple normalization procedure is adopted for this purpose
cmb_prob = wind_prob_sort.*pv_prob_sort
cmb_prob_sum = sum(cmb_prob)
cmb_prob_norm = cmb_prob./cmb_prob_sum

scen_array = []
for i in 1:nScenarios
    push!(scen_array,"s$i")
end
## ------------ Writing Scenarios and Probabilities in the ods file ------------
aux_wind_scenarios = wind_sc_sort[rp,:]
aux_wind_scenarios = aux_wind_scenarios[1:end-1,:]

wind_scs = zeros(hrs,nScenarios)
wind_res = convert(Int64,size(aux_wind_scenarios,1)/hrs)
for i in 1:hrs
    wind_scs[i,:] = mean(aux_wind_scenarios[((i-1)*wind_res)+1:i*wind_res,:],dims=1)
end
wind_scs = wind_scs./p_rat
pv_scs = pv_sc_sort./p_rat_pv

output_file = get(parameters, "output_file", "")
##--------------------- Writing wind data --------------------------------------
data_wind = hcat(scen_array,transpose(wind_scs))
data      = convert(DataFrame,data_wind)
ods_write(output_file,Dict(("wind_scenarios",1,1)=>data))

##-----------------------Writing PV data ---------------------------------------
data_pv   = hcat(scen_array,transpose(pv_scs))
data      = convert(DataFrame,data_pv)
ods_write(output_file,Dict(("pv_scenarios",1,1)=>data))

##------------------------ Writing probabilities -------------------------------
data_prob = hcat(scen_array,cmb_prob_norm)
data      = convert(DataFrame,data_prob)
ods_write(output_file,Dict(("probabilities",1,1)=>data))

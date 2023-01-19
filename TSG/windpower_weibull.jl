function wind_power_weibull(wind_power,wind_speed,v_cut_in,v_cut_out,v_rat,p_rat)
    for i in 1:size(wind_power,2)
        par_est_jl = params(fit_mle(Weibull,wind_speed[:,i]))            # using Julia function provided in weibull_estimator.jl file
        shape = par_est_jl[1]
        a = p_rat/(v_rat^shape-v_cut_in^shape)
        for k in 1:size(wind_power,1)
            v = wind_speed[k,i]
                if 0<=v<= v_cut_in
                    wind_power[k,i] = 0.0
                elseif v>= v_cut_out
                    wind_power[k,i] = 0.0
                elseif v_rat<=v<=v_cut_out
                    wind_power[k,i] = p_rat
                else
                    wind_power[k,i] = a*(v^shape-v_cut_in^shape)
                end
        end
    end
    return wind_power
end

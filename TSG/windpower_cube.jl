function wind_power_cube(wind_power,wind_speed,v_cut_in,v_cut_out,v_rat,p_rat,a,b)
    for i in 1:size(wind_power,2)
        for k in 1:size(wind_power,1)
            v = wind_speed[k,i]
                if 0<=v<= v_cut_in
                    wind_power[k,i] = 0.0
                elseif v>= v_cut_out
                    wind_power[k,i] = 0.0
                elseif v_rat<=v<=v_cut_out
                    wind_power[k,i] = p_rat
                else
                    wind_power[k,i] = a*v^3-b*p_rat
                end
        end
    end
    return wind_power
end

function adf_test(stat_test,data_tmp,critical_values)
    for i in 1:length(stat_test)
        data = stat_test[i]
        if !(data isa Dict)   # data is not a dictionary
            push!(data_tmp,stat_test[i])
        else
            for k in 1:length(data)
                push!(data_tmp,stat_test[i][critical_values[k]])
            end
        end
    end
    return data_tmp
end

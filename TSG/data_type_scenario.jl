mutable struct series_stat
    ADF_statistics::Float64
    p_value::Float64
    lags::Int64
    nObs::Int64
    critical_value_1::Float64
    critical_value_5::Float64
    critical_value_10::Float64
    icbest::Float64
end

mutable struct series_stat_kpss
    kpss_statistics::Float64
    p_value::Float64
    lags::Int64
    critical_value_1::Float64
    critical_value_5::Float64
    critical_value_10::Float64
    critical_value_2_5::Float64
end

function correlation_plot(data)
    total_lags = min(size(data,1)-1,10*log10(size(data,1)))
    # total_lags = 100
    speed_acf  = autocor(data,collect(1:convert(Int64,round(total_lags))),demean=true)
    speed_pacf = pacf(data,collect(1:convert(Int64,round(total_lags))),method=:regression)

    p1 = bar(collect(1:convert(Int64,round(total_lags))),speed_acf,xlabel="lags",ylabel="ACF",title="Auto-Correlations")
    p2 = bar(collect(1:convert(Int64,round(total_lags))),speed_pacf,xlabel="lags",ylabel="PACF",title="Partial Auto-Correlations")

return p1,p2
end

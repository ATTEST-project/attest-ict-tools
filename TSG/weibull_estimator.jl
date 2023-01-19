function implicit_k_estimator(x, k::Number)
    xᵏ = x.^k
    lnx = log.(x)
    sum(xᵏ .* lnx) / sum(xᵏ) - inv(k) - sum(lnx) / length(x)
end

explicit_λ_estimator(k::Number, x) = (sum(x.^k) / length(x))^(1/k)

function Distributions.fit_mle(::Type{Weibull}, x::AbstractArray)
    f = k -> implicit_k_estimator(x, k)
    k = find_zero(f, oneunit(eltype(x)), Order2())
    λ = explicit_λ_estimator(k, x)
    Weibull(k, λ)
end

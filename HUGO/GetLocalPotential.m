function Vc = GetLocalPotential(c_res, s_res, params)

    c_w = (params.sigma + sqrt(sum(c_res.^2))).^(-params.gamma);
    s_w = (params.sigma + sqrt(sum(s_res.^2))).^(-params.gamma);
    Vc = (c_w + s_w);
end


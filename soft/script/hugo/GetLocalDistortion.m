function D = GetLocalDistortion(C_resVect, S_resVect, params)

    D = 0;
    % C_resVect and S_resVect must have size of 6x1   
    D = D + GetLocalPotential(C_resVect(1:3), S_resVect(1:3), params);
    D = D + GetLocalPotential(C_resVect(2:4), S_resVect(2:4), params);
    D = D + GetLocalPotential(C_resVect(3:5), S_resVect(3:5), params);
    D = D + GetLocalPotential(C_resVect(4:6), S_resVect(4:6), params);

end


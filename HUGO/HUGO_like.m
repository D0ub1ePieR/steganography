function [stego, distortion] = HUGO_like(cover, payload, params)

cover = double(cover);
disp(size(cover))
wetCost = 10^8;
responseP1 = [0; 0; -1; +1; 0; 0];

% create mirror padded cover image
padSize = 3;
coverPadded = padarray(cover, [padSize padSize], 'symmetric');

% create residuals
C_Rez_H = coverPadded(:, 1:end-1) - coverPadded(:, 2:end);
C_Rez_V = coverPadded(1:end-1, :) - coverPadded(2:end, :);
C_Rez_Diag = coverPadded(1:end-1, 1:end-1) - coverPadded(2:end, 2:end);
C_Rez_MDiag = coverPadded(1:end-1, 2:end) - coverPadded(2:end, 1:end-1);

stego = cover;                                  % initialize stego image
stegoPadded = coverPadded;
        
% create residuals
S_Rez_H = stegoPadded(:, 1:end-1) - stegoPadded(:, 2:end);
S_Rez_V = stegoPadded(1:end-1, :) - stegoPadded(2:end, :);
S_Rez_Diag = stegoPadded(1:end-1, 1:end-1) - stegoPadded(2:end, 2:end);
S_Rez_MDiag = stegoPadded(1:end-1, 2:end) - stegoPadded(2:end, 1:end-1);
        
rhoM1 = zeros(size(cover));                    % declare cost of -1 change           
rhoP1 = zeros(size(cover));                    % declare cost of +1 change        
        
%% Iterate over elements in the sublattice
for row=1:size(cover, 1)
    for col=1:size(cover, 2)    
        D_P1 = 0;
        D_M1 = 0;
            
        % Horizontal
        cover_sub = C_Rez_H(row+3, col:col+5)';
        stego_sub = S_Rez_H(row+3, col:col+5)';
            
        stego_sub_P1 = stego_sub + responseP1;
        stego_sub_M1 = stego_sub - responseP1;

        D_M1 = D_M1 + GetLocalDistortion(cover_sub, stego_sub_M1, params);
        D_P1 = D_P1 + GetLocalDistortion(cover_sub, stego_sub_P1, params);
            
        % Vertical
        cover_sub = C_Rez_V(row:row+5, col+3);
        stego_sub = S_Rez_V(row:row+5, col+3);
           
        stego_sub_P1 = stego_sub + responseP1;
        stego_sub_M1 = stego_sub - responseP1;

        D_M1 = D_M1 + GetLocalDistortion(cover_sub, stego_sub_M1, params);
        D_P1 = D_P1 + GetLocalDistortion(cover_sub, stego_sub_P1, params);            

        % Diagonal
        cover_sub = [C_Rez_Diag(row, col); C_Rez_Diag(row+1, col+1); C_Rez_Diag(row+2, col+2); C_Rez_Diag(row+3, col+3); C_Rez_Diag(row+4, col+4); C_Rez_Diag(row+5, col+5)];
        stego_sub = [S_Rez_Diag(row, col); S_Rez_Diag(row+1, col+1); S_Rez_Diag(row+2, col+2); S_Rez_Diag(row+3, col+3); S_Rez_Diag(row+4, col+4); S_Rez_Diag(row+5, col+5)];
            
        stego_sub_P1 = stego_sub + responseP1;
        stego_sub_M1 = stego_sub - responseP1;

        D_M1 = D_M1 + GetLocalDistortion(cover_sub, stego_sub_M1, params);
        D_P1 = D_P1 + GetLocalDistortion(cover_sub, stego_sub_P1, params);
            
        % Minor Diagonal
        cover_sub = [C_Rez_MDiag(row, col+5); C_Rez_MDiag(row+1, col+4); C_Rez_MDiag(row+2, col+3); C_Rez_MDiag(row+3, col+2); C_Rez_MDiag(row+4, col+1); C_Rez_MDiag(row+5, col)];
        stego_sub = [S_Rez_MDiag(row, col+5); S_Rez_MDiag(row+1, col+4); S_Rez_MDiag(row+2, col+3); S_Rez_MDiag(row+3, col+2); S_Rez_MDiag(row+4, col+1); S_Rez_MDiag(row+5, col)];

        stego_sub_P1 = stego_sub + responseP1;
        stego_sub_M1 = stego_sub - responseP1;

        D_M1 = D_M1 + GetLocalDistortion(cover_sub, stego_sub_M1, params);
        D_P1 = D_P1 + GetLocalDistortion(cover_sub, stego_sub_P1, params);
            
        rhoM1(row, col) = D_M1;
        rhoP1(row, col) = D_P1;            
    end
end      
        
% truncation of the costs
rhoM1(rhoM1>wetCost) = wetCost;
rhoP1(rhoP1>wetCost) = wetCost;
        
rhoP1(cover == 255) = wetCost;
rhoM1(cover == 0) = wetCost;
               
%% Embedding   
% embedding simulator - params.qarity \in {2,3}
stego = EmbeddingSimulator(cover, rhoP1, rhoM1, round(numel(cover)*payload), false);

% compute distortion
distM1 = rhoM1(stego-cover==-1);
distP1 = rhoP1(stego-cover==1);
distortion = sum(distM1) + sum(distP1);

end

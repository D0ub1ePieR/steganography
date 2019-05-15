function EmbeddingSimulator(x, rhoP1, rhoM1, m, filename)

%     mat = [];
%     fid = fopen(fullfile(filename(1:length(filename)-4),'.txt'));
%     while ~feof(fid)
%         line = fgetl(fid);
%         tmp = [];
%         for i = 1:length(line)
%             tmp = [tmp,eval(line(i))];
%         end
%         mat = [mat;tmp];
%     end
%     fclose(fid);
% 
%     if flag==0
%         n = numel(x)-nnz(mat); 
%     else
%         n = nnz(mat);
%     end
    n = numel(x);
    lambda = calc_lambda(rhoP1, rhoM1, m, n);
    pChangeP1 = (exp(-lambda .* rhoP1))./(1 + exp(-lambda .* rhoP1) + exp(-lambda .* rhoM1));
    pChangeM1 = (exp(-lambda .* rhoM1))./(1 + exp(-lambda .* rhoP1) + exp(-lambda .* rhoM1));
    
%     randChange = rand(size(x));
%     randChange(find(mat==0))=pChangeP1(find(mat==0))+pChangeM1(find(mat==0));
%    pChangeP1(pChangeP1<0.0005) = 1;
%    pChangeP1(pChangeP1~=0) = 0;

    y = x;
    y(pChangeP1<0.000001) = 0;
    y(y~=0) = 1;
    disp(numel(find(y==1)))
    fid = fopen(fullfile('./',strcat(filename(1:length(filename)-4),'.txt')),'w');
    sizep = size(y);
    for i = 1:sizep(1)
        for j = 1:sizep(2)
            fprintf(fid,'%d',y(i,j));
        end
        fprintf(fid,'\n');
    end
    fclose(fid);
%     y = x;
%     y(randChange < pChangeP1) = y(randChange < pChangeP1) + 1;
%     y(randChange >= pChangeP1 & randChange < pChangeP1+pChangeM1) = y(randChange >= pChangeP1 & randChange < pChangeP1+pChangeM1) - 1;

    function lambda = calc_lambda(rhoP1, rhoM1, message_length, n)

        l3 = 1e+3;
        m3 = double(message_length + 1);
        iterations = 0;
        while m3 > message_length
            l3 = l3 * 2;
            pP1 = (exp(-l3 .* rhoP1))./(1 + exp(-l3 .* rhoP1) + exp(-l3 .* rhoM1));
            pM1 = (exp(-l3 .* rhoM1))./(1 + exp(-l3 .* rhoP1) + exp(-l3 .* rhoM1));
            m3 = ternary_entropyf(pP1, pM1);
            iterations = iterations + 1;
            if (iterations > 100)
                lambda = l3;
                return;
            end
        end        

        l1 = 0; 
        m1 = double(n);        
        lambda = 0;

        alpha = double(message_length)/n;
        % limit search to 100 iterations
        % and require that relative payload embedded is roughly within 1/1000 of the required relative payload        
        while  (double(m1-m3)/n > alpha/1000.0 ) && (iterations<100)
            lambda = l1+(l3-l1)/2; 
            pP1 = (exp(-lambda .* rhoP1))./(1 + exp(-lambda .* rhoP1) + exp(-lambda .* rhoM1));
            pM1 = (exp(-lambda .* rhoM1))./(1 + exp(-lambda .* rhoP1) + exp(-lambda .* rhoM1));
            m2 = ternary_entropyf(pP1, pM1);
            if m2 < message_length
                l3 = lambda;
                m3 = m2;
            else
                l1 = lambda;
                m1 = m2;
        end
            iterations = iterations + 1;
        end
    end

    function Ht = ternary_entropyf(pP1, pM1)
        p0 = 1-pP1-pM1;
        P = [p0(:); pP1(:); pM1(:)];
        H = -((P).*log2(P));
        H((P<eps) | (P > 1-eps)) = 0;
        Ht = sum(H);
    end
end
% 优化（Optimization Toolbox）— 读 optimize_input.json，写 optimize_output.json
% 输入 JSON：{"fun":"...","x0":[...],"lb":[...],"ub":[...],"method":"fmincon"}
% method ∈ fmincon（梯度）/ ga（遗传）/ particleswarm / patternsearch
inp = jsondecode(fileread('optimize_input.json'));
fun = str2func(['@(x)' inp.fun]);
opts = optimoptions(inp.method, 'Display', 'iter');
switch inp.method
    case 'fmincon'
        [x, fval, flag, out] = fmincon(fun, inp.x0, [], [], [], [], inp.lb, inp.ub, [], opts);
    case 'ga'
        [x, fval, flag, out] = ga(fun, numel(inp.x0), [], [], [], [], inp.lb, inp.ub, [], opts);
    case 'particleswarm'
        [x, fval, flag, out] = particleswarm(fun, numel(inp.x0), inp.lb, inp.ub, opts);
    case 'patternsearch'
        [x, fval, flag, out] = patternsearch(fun, inp.x0, [], [], [], [], inp.lb, inp.ub, [], opts);
end
fprintf('optimal f=%.6g  flag=%d  nfeval=%d\n', fval, flag, out.funcCount);
res = struct('x', x, 'fval', fval, 'flag', flag, 'funcCount', out.funcCount);
fid = fopen('optimize_output.json','w'); fwrite(fid, jsonencode(res)); fclose(fid);
disp('OPTIMIZE_DONE');

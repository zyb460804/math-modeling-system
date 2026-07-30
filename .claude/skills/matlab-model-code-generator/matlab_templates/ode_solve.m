% ODE 求解（ode45/ode15s 自适应）— 读 ode_input.json，写 ode_output.json + 图
% 输入 JSON：{"rhs":"-0.5*x(1)","tspan":[0,5],"x0":[1],"stiff":false}
inp = jsondecode(fileread('ode_input.json'));
rhs = str2func(['@(t,x)' inp.rhs]);
solver = ternary(inp.stiff, @ode15s, @ode45);
[t, X] = solver(rhs, inp.tspan, inp.x0);
fprintf('ODE solved: t_end=%.3f  x_end=[%s]\n', t(end), num2str(X(end,:)));
fig = figure('Visible','off'); plot(t, X, 'LineWidth', 2); title('ODE'); xlabel('t');
exportgraphics(fig, 'ode_fig.png');
res = struct('t_end', t(end), 'x_end', X(end,:));
fid = fopen('ode_output.json','w'); fwrite(fid, jsonencode(res)); fclose(fid);
disp('ODE_DONE');

function r = ternary(cond, a, b)
    if cond, r = a; else, r = b; end
end

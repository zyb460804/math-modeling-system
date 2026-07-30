% 曲线拟合（Curve Fitting Toolbox）— 读 curve_fit_input.json，写 curve_fit_output.json + 图
% 输入 JSON：{"x":[...],"y":[...],"model":"exp2"}  model ∈ exp1/exp2/poly2/poly3/fourier2/gauss2
inp = jsondecode(fileread('curve_fit_input.json'));
x = inp.x; y = inp.y;
ft = fittype(inp.model);
f = fit(x', y', ft);
fprintf('SSE=%.6g  R2=%.4f  RMSE=%.6g\n', f.sse, f.rsquare, f.rmse);
fig = figure('Visible','off'); plot(f, x, y); title(inp.model);
exportgraphics(fig, 'curve_fit_fig.png');
out = struct('coefficients', num2cell(coefficients(f)), ...
    'sse', f.sse, 'rsquare', f.rsquare, 'rmse', f.rmse);
fid = fopen('curve_fit_output.json','w'); fwrite(fid, jsonencode(out)); fclose(fid);
disp('CURVE_FIT_DONE');

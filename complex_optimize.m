clear all;
randn('seed', 6); % 8
rand('seed', 7);
J = 256;
K = 100;
JJ = 1:J;
JJ = JJ';
KK = ones(1,K);
JK = JJ * KK;
Y = randn(J,K) + i * randn(J,K);
Z = randn(J,K) + i * randn(J,K);
%options = optimoptions('fsolve','Display','none','PlotFcn',@optimplotfirstorderopt);
stt = -pi;
step = 0.001;
endn = pi;
z = stt:step:endn;
loss = zeros(length(z),1);
f = @(x) sum(sum((abs(Y - exp(-1 * i * JK * x).* Z)).^2)); 
minimum = inf;
for j=1:length(z)
    loss(j) = f(z(j));
    if loss(j) < minimum
        minimum = loss(j);
        minimum_x = z(j);
    end
end

options=optimset('MaxIter',1e9,'TolFun',1e-15);
x0 = minimum_x; %% init
x_opt = fsolve(f,x0,options);  
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% this is the result

%%%following is test
f(x_opt) < f(minimum_x)
step2 = abs(x_opt - minimum_x) / 1000;
if x_opt < minimum_x
    left_x = x_opt * 2 - minimum_x;
    right_x = minimum_x;
else
    left_x = minimum_x;
    right_x = x_opt * 2 - minimum_x;
end
xx = left_x:step2:right_x;
yy = zeros(length(xx),1);
for j = 1:length(xx)
   yy(j) = f(xx(j)); 
end

plot(xx,yy,'g');
hold on;
plot(minimum_x,f(minimum_x),'bo','LineWidth',30);
hold on;
plot(x_opt,f(x_opt),'r*','LineWidth',30);
hold on;
legend('loss function', 'before fsolve', 'after fsolve');
%%% test



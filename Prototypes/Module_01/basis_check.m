Gi_n = sqrt(sum(Gi.*Gi,2));
Gi = Gi./repmat(Gi_n,[1 3]);
%%
[a b c] = sphere(128);
h = surf(a, b, c);
set(h, 'FaceAlpha', 0.5); shading interp; hold on;
Gi=gradients; % Gi = NGi;
scatter3(Gi(:,1), Gi(:,2), Gi(:,3), 40, 'b', 'filled'); hold on
for n=1:length(Gi)
    plot3([0 Gi(n,1)], [0 Gi(n,2)], [0, Gi(n,3)], 'Color', [0.2 0.6 1.0]); hold on
end
colormap([1.0, 1.0, 0.7]); hold on
grid off
% axis off
% Ng_n = sqrt(sum(Gi.*Gi,2));

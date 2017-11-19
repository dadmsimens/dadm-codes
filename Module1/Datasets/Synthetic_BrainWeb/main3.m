%% Loading 3D volumes
clear all; close all;

% main source to read
source_path = './DATA/';


% T1, 1mm, INU=0%
[dataset_T1] = openBrainWebData([source_path 'T1/t1_icbm_normal_1mm_pn0_rf0.rawb'], 181, 217, 181, 1);

% T2, 1mm, INU=0%
[dataset_T2] = openBrainWebData([source_path 'T2/t2_icbm_normal_1mm_pn0_rf0.rawb'], 181, 217, 181, 1);

% PD, 1mm, INU=0%
[dataset_PD] = openBrainWebData([source_path 'PD/pd_icbm_normal_1mm_pn0_rf0.rawb'], 181, 217, 181, 1);


% T1, 1mm, INU=20%
[dataset_T1_INU_20] = openBrainWebData([source_path 'T1/t1_icbm_normal_1mm_pn0_rf20.rawb'], 181, 217, 181, 1);

% T2, 1mm, INU=20%
[dataset_T2_INU_20] = openBrainWebData([source_path 'T2/t2_icbm_normal_1mm_pn0_rf20.rawb'], 181, 217, 181, 1);

% PD, 1mm, INU=20%
[dataset_PD_INU_20] = openBrainWebData([source_path 'PD/pd_icbm_normal_1mm_pn0_rf20.rawb'], 181, 217, 181, 1);


%plot2svg('data_t1_t2_pd.svg', 1);


%% Show more slices from one single 3D volume

slices_matrix_size = 5;
start_at = 40;
step = 10;

data_slices = [];
horizontal_slices = [];

for i=1:slices_matrix_size
    for j=1:slices_matrix_size
        horizontal_slices = horzcat(horizontal_slices, dataset_T1(:, :, start_at + (i-1)*slices_matrix_size + j*step));
    end
    
    data_slices = vertcat(data_slices, horizontal_slices);    
    horizontal_slices = [];
end

imshow(data_slices, []);





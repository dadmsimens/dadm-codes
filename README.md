# dadm-codes
<draft file>
The aim of this project is to create the system for MRI data pre-processing and post-processing using Python, scipy, cython and Qt5. The project is divided into 11 modules:
  
  
1. MRI reconstruction<br />
2. Intensity inhomogeneity correction<br />
3. Non-stationary noise estimation<br />
4. Non-stationary noise filtering #1<br />
5. Non-stationary noise filtering #2<br />
6. Diffusion tensor imaging<br />
<7th module excluded> <br />
8. Skull stripping<br />
9. Segmentation<br />
10. Upsampling<br />
11. Brain 3D<br />
12. Oblique imaging
# Prerequisites
Please add libraries you are using in your module
# Installing
Follow the steps below to establish enviroment for running this application
## Install Anaconda
Please follow the instructions from [official conda documentation](https://conda.io/docs/user-guide/install/index.html). I recommend you to let the installer change your path file (IDK: what's the risk of interference with other python packages?).
## Create Anaconda env
Once you have installed Anaconda, run in terminal:
```sh
conda create -n DADM python=3.5 pyqt=5 vtk cython -c menpo
```
Alternatively, you can navigate to this repo folder in terminal and run:
```sh
conda env create -f DADM_env.yml
```
The enviroment can be used in terminal by typing
```sh
source activate DADM
```
Run the python scripts from terminal window with activated source.

# Contributing
Every member of Developers and Organizational teams has the rights to push and pull - please be careful! <br />
Please add your code as "modulethe number of the module.py" (e.g. module1.py). If you have more than one file create your own folder (e.g. Module1). If you want to add your files to github in progress (not only final version), please create new branch for changes. 
  

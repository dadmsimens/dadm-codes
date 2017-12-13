import scipy.io
import vtk
from vtk.util import numpy_support
mat = scipy.io.loadmat('brain_scan.mat')
data = mat['t2_volume']

vtk_data = numpy_support.numpy_to_vtk(num_array=data.transpose(2, 1, 0).ravel(),deep=True,array_type=vtk.VTK_FLOAT)

#table to vtk class object
img_vtk = vtk.vtkImageData()
img_vtk.SetDimensions(data.shape)
img_vtk.SetSpacing(1,1,1)
img_vtk.GetPointData().SetScalars(vtk_data)

# renderer and interactor
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

#marching cubes
brainExtractor = vtk.vtkMarchingCubes()
brainExtractor.SetInputData(img_vtk)
brainExtractor.SetValue(0,2500)

#preparin visualization
brainMapper = vtk.vtkPolyDataMapper()
brainMapper.SetInputConnection(brainExtractor.GetOutputPort())
brainMapper.ScalarVisibilityOff()
brain = vtk.vtkActor()
brain.SetMapper(brainMapper)
c = brain.GetCenter()
ren.AddViewProp(brain)
camera = ren.GetActiveCamera()
camera.SetFocalPoint(c[0],c[1],c[2])
camera.SetPosition(500,- 100,- 100)
camera.SetViewUp(0,0,-1)
renWin.Render()
iren.Start()

import vtk

polyData = vtk.vtkPolyData()

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


#marching cubes
brainExtractor = vtk.vtkMarchingCubes()
brainExtractor.SetInputData(img_vtk)
brainExtractor.SetValue(0,2500)


plane = vtk.vtkPlane()
plane.SetOrigin(0,0,0);
plane.SetNormal(1.0, -1.0, -1.0)

clipper = vtk.vtkClipPolyData()
clipper.SetInputConnection(brainExtractor.GetOutputPort())
clipper.SetClipFunction(plane)
clipper.SetValue(0)
clipper.Update()

polyData = clipper.GetOutput()

clipMapper = vtk.vtkDataSetMapper()
clipMapper.SetInputData(polyData)

clipActor = vtk.vtkActor()
clipActor.SetMapper(clipMapper)
clipActor.GetProperty().SetColor(1.0000,0.3882,0.2784)
clipActor.GetProperty().SetInterpolationToFlat()


boundaryEdges = vtk.vtkFeatureEdges()
boundaryEdges.SetInputData(polyData)
boundaryEdges.BoundaryEdgesOn()
boundaryEdges.FeatureEdgesOff()
boundaryEdges.NonManifoldEdgesOff()
boundaryEdges.ManifoldEdgesOff()

boundaryStrips = vtk.vtkStripper()
boundaryStrips.SetInputConnection(boundaryEdges.GetOutputPort())
boundaryStrips.Update()

boundaryPoly = vtk.vtkPolyData()
boundaryPoly.SetPoints(boundaryStrips.GetOutput().GetPoints())
boundaryPoly.SetPolys(boundaryStrips.GetOutput().GetLines())

boundaryMapper = vtk.vtkPolyDataMapper()
boundaryMapper.SetInputData(boundaryPoly)

boundaryActor = vtk.vtkActor()
boundaryActor.SetMapper(boundaryMapper)
boundaryActor.GetProperty().SetColor(0.8900,0.8100,0.3400)





ren1 = vtk.vtkRenderer()
ren1.SetBackground(.1,.2,.3)

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.SetSize(512,512)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
ren1.AddActor(clipActor)
ren1.AddActor(boundaryActor)
iren.Initialize()
iren.Start()

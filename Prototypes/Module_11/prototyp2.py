import scipy.io
import vtk
from vtk.util import numpy_support

mat = scipy.io.loadmat('brain_scan.mat')
data = mat['t2_volume']
vtk_data = numpy_support.numpy_to_vtk(num_array=data.transpose(2, 1, 0).ravel(), deep=True, array_type=vtk.VTK_FLOAT)

#table to vtk class object
img_vtk = vtk.vtkImageData()
img_vtk.SetDimensions(data.shape)
img_vtk.SetSpacing(1,1,1)
img_vtk.GetPointData().SetScalars(vtk_data)

#choose plane
(xMin, xMax, yMin, yMax, zMin, zMax) = img_vtk.GetExtent()
(xSpacing, ySpacing, zSpacing) = img_vtk.GetSpacing()
(x0, y0, z0) = img_vtk.GetOrigin()

center = [x0 + xSpacing * 0.5 * (xMin + xMax),
          y0 + ySpacing * 0.5 * (yMin + yMax),
          z0 + zSpacing * 0.5 * (zMin + zMax)]


axial = vtk.vtkMatrix4x4()
axial.DeepCopy((1, 0, 0, center[0],
                0, 1, 0, center[1],
                0, 0, 1, center[2],
                0, 0, 0, 1))

coronal = vtk.vtkMatrix4x4()
coronal.DeepCopy((1, 0, 0, center[0],
                  0, 0, 1, center[1],
                  0,1, 0, center[2],
                  0, 0, 0, 1))

sagittal = vtk.vtkMatrix4x4()
sagittal.DeepCopy((0, 0,-1, center[0],
                   1, 0, 0, center[1],
                   0,-1, 0, center[2],
                   0, 0, 0, 1))


orientation = sagittal #change here if you want another plane!!

# Extract a slice in chosen orientation
reslice = vtk.vtkImageReslice()
reslice.SetInputData(img_vtk)
reslice.SetOutputDimensionality(2)
reslice.SetResliceAxes(orientation)
reslice.SetInterpolationModeToLinear()

#prepare visualization
table = vtk.vtkLookupTable()
table.SetRange(0, 2000)
table.SetValueRange(0.0, 1.0)
table.SetSaturationRange(0.0, 0.0)
table.SetRampToLinear()
table.Build()


color = vtk.vtkImageMapToColors()
color.SetLookupTable(table)
color.SetInputConnection(reslice.GetOutputPort())

actor = vtk.vtkImageActor()
actor.GetMapper().SetInputConnection(color.GetOutputPort())

renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
window = vtk.vtkRenderWindow()
window.AddRenderer(renderer)

# Set up the interaction to choose cross-section
interactorStyle = vtk.vtkInteractorStyleImage()
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetInteractorStyle(interactorStyle)
window.SetInteractor(interactor)
window.Render()
actions = {}
actions["Slicing"] = 0

def ButtonCallback(obj, event):
    if event == "LeftButtonPressEvent":
        actions["Slicing"] = 1
    else:
        actions["Slicing"] = 0

def MouseMoveCallback(obj, event):
    (lastX, lastY) = interactor.GetLastEventPosition()
    (mouseX, mouseY) = interactor.GetEventPosition()
    if actions["Slicing"] == 1:
        deltaY = mouseY - lastY
        reslice.Update()
        sliceSpacing = reslice.GetOutput().GetSpacing()[2]
        matrix = reslice.GetResliceAxes()
        center = matrix.MultiplyPoint((0, 0, sliceSpacing*deltaY, 1))
        matrix.SetElement(0, 3, center[0])
        matrix.SetElement(1, 3, center[1])
        matrix.SetElement(2, 3, center[2])
        window.Render()
    else:
        interactorStyle.OnMouseMove()


interactorStyle.AddObserver("MouseMoveEvent", MouseMoveCallback)
interactorStyle.AddObserver("LeftButtonPressEvent", ButtonCallback)
interactorStyle.AddObserver("LeftButtonReleaseEvent", ButtonCallback)

interactor.Start()

import vtk
from vtk.util import numpy_support
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class model3D():
    def __init__(self, mri_data = None, frame = None, layout = None):
        self.mri_data = mri_data
        self.frame = frame
        self.layout = layout
        self.clipped_model = None
        self.image, self.model = self.generate_model3D()
        self.setup_render_window()



    def generate_model3D(self):
        vtk_array = numpy_support.numpy_to_vtk(num_array=self.mri_data.transpose(2, 1, 0).ravel(),deep=True,array_type=vtk.VTK_FLOAT)
        image = vtk.vtkImageData()
        image.SetDimensions(self.mri_data.shape)
        image.SetSpacing(1,1,1)
        image.GetPointData().SetScalars(vtk_array)
        #marching cubes
        model = vtk.vtkMarchingCubes()
        model.SetInputData(image)
        model.SetValue(0,1)
        return image, model

    def setup_render_window(self):
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.layout.addWidget(self.vtkWidget)
        self.frame.setLayout(self.layout)
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(0.2, 0.2,0.2)
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.preview_model()


    def preview_model(self):

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(self.model.GetOutputPort())
        mapper.ScalarVisibilityOff()
        self.actor_clipped = vtk.vtkActor()
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(mapper)
        self.renderer.AddActor(self.actor)
        self.renderer.ResetCamera()
        cam1 = self.renderer.GetActiveCamera()
        cam1.Elevation(110)
        cam1.SetViewUp(0, 0, 1)
        cam1.Azimuth(45)
        self.renderer.ResetCameraClippingRange()
        self.iren.Initialize()

    def change_mode(self, mode):
        if mode == 0:
            self.renderer.RemoveActor(self.actor_clipped)
            self.preview_model()
        else:
            self.renderer.RemoveActor(self.actor)
            self.renderer.RemoveActor(self.actor_clipped)

    def cut_model(self):
        #self.renderer.AddActor(self.actor)
        self.actor.VisibilityOn()

        self.plane = vtk.vtkPlane()
        clipper = vtk.vtkClipPolyData()
        clipper.SetInputConnection(self.model.GetOutputPort())
        clipper.SetClipFunction(self.plane)
        clipper.InsideOutOn()
        clipMapper = vtk.vtkPolyDataMapper()
        clipMapper.SetInputConnection(clipper.GetOutputPort())
        clipMapper.ScalarVisibilityOff()

        self.clipActor = vtk.vtkActor()
        self.clipActor.SetMapper(clipMapper)
        self.clipActor.VisibilityOff()

        self.clipActor.SetScale(1.01, 1.01, 1.01)

        # The callback function
        def myCallback(obj, event):
            self.plane.SetNormal(obj.GetNormal())
            self.plane.SetOrigin(obj.GetCenter())
            self.actor.VisibilityOff()
            self.clipActor.VisibilityOn()
            
        planeWidget = vtk.vtkImagePlaneWidget()
        planeWidget.SetInteractor(self.iren)
        planeWidget.SetPlaceFactor(1.25)
        planeWidget.SetInputData(self.image)
        planeWidget.PlaceWidget()
        planeWidget.On()
        planeWidget.SetPlaneOrientationToZAxes()
        
        
        planeWidget.AddObserver("InteractionEvent", myCallback)
        planeWidget.TextureVisibilityOff()
        
        self.renderer.AddActor(self.actor)
        self.renderer.AddActor(self.clipActor)
        
        
        self.iren.Initialize()
        self.vtkWidget.GetRenderWindow().Render()
        self.iren.Start()


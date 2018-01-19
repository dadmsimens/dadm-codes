import vtk
from vtk.util import numpy_support
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class model3D():
    def __init__(self, mri_data = None, frame = None, layout = None):
        self.image, self.model = self.generate_model3D(mri_data)
        self.iren, self.renderer = self.setup_render_window(frame, layout)
        self.clipped_model = None

    def generate_model3D(self, mri_data):
        vtk_array = numpy_support.numpy_to_vtk(num_array=mri_data.transpose(2, 1, 0).ravel(),deep=True,array_type=vtk.VTK_FLOAT)
        image = vtk.vtkImageData()
        image.SetDimensions(mri_data.shape)
        image.SetSpacing(1,1,1)
        image.GetPointData().SetScalars(vtk_array)
        #marching cubes
        model = vtk.vtkMarchingCubes()
        model.SetInputData(image)
        model.SetValue(0,1)
        return image, model

    def setup_render_window(self, frame, layout):
        vtkWidget = QVTKRenderWindowInteractor(frame)
        layout.addWidget(vtkWidget)
        renderer = vtk.vtkRenderer()
        renderer.SetBackground(0.2, 0.2,0.2)
        vtkWidget.GetRenderWindow().AddRenderer(renderer)
        iren = vtkWidget.GetRenderWindow().GetInteractor()
        style = vtk.vtkInteractorStyleTrackballCamera()
        iren.SetInteractorStyle(style)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(self.model.GetOutputPort())
        mapper.ScalarVisibilityOff()
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(mapper)
        renderer.AddActor(self.actor)

        renderer.ResetCamera()
        cam1 = renderer.GetActiveCamera()
        cam1.Elevation(110)
        cam1.SetViewUp(0, 0, 1)
        cam1.Azimuth(45)
        renderer.ResetCameraClippingRange()
        iren.Initialize()
        return iren, renderer

    def preview_model(self):
        self.actor.VisibilityOn()
        self.renderer.RemoveAllViewProps()
        self.renderer.AddActor(self.actor)
        self.iren.Initialize()



    def cut_model(self, plane_mode=False):
        self.preview_model()

        plane_widget = vtk.vtkImagePlaneWidget()
        plane_widget.SetInteractor(self.iren)
        #plane_widget.SetPlaceFactor(1.25)
        plane_widget.SetInputData(self.image)
        plane_widget.PlaceWidget()
        plane_widget.SetPlaneOrientationToZAxes()

        plane = vtk.vtkPlane()
        clipper = vtk.vtkClipPolyData()
        clipper.SetInputConnection(self.model.GetOutputPort())
        clipper.SetClipFunction(plane)
        clipper.InsideOutOn()
        clip_mapper = vtk.vtkPolyDataMapper()
        clip_mapper.SetInputConnection(clipper.GetOutputPort())
        clip_mapper.ScalarVisibilityOff()
        clip_actor = vtk.vtkActor()
        clip_actor.SetMapper(clip_mapper)

        if plane_mode:
            plane_widget.TextureVisibilityOn()
            clip_actor.GetProperty().SetOpacity(0.1)
        else:
            plane_widget.TextureVisibilityOff()
        plane_widget.On()


        # The callback function
        def myCallback(obj, event):
            plane.SetNormal(obj.GetNormal())
            plane.SetOrigin(obj.GetCenter())
            self.actor.VisibilityOff()

        plane_widget.AddObserver("InteractionEvent", myCallback)

        self.renderer.AddActor(clip_actor)
        self.iren.Initialize()
        #self.iren.Start()


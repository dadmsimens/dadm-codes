import vtk
from vtk.util import numpy_support
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class Model3D():
    def __init__(self, mri_data = None):
        self.image, self.model = self.generate_model3D(mri_data)
        self.iren = None
        self.renderer = None

    def generate_model3D(self, mri_data):
        '''Reconstrucion image to 3d model via marching cubes alghoritm'''
        vtk_array = numpy_support.numpy_to_vtk(num_array=mri_data.transpose(2, 1, 0).ravel(),deep=True,array_type=vtk.VTK_FLOAT)
        image = vtk.vtkImageData()
        image.SetDimensions(mri_data.shape)
        image.SetSpacing(1,1,1)
        image.GetPointData().SetScalars(vtk_array)

        model = vtk.vtkMarchingCubes()
        model.SetInputData(image)
        model.SetValue(0,1)

        return image, model

    def setup_render_window(self, frame, layout):
        '''Initial setting VTK window'''
        vtkWidget = QVTKRenderWindowInteractor(frame)
        layout.addWidget(vtkWidget)
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(0.2, 0.2,0.2)
        vtkWidget.GetRenderWindow().AddRenderer(self.renderer)
        self.iren = vtkWidget.GetRenderWindow().GetInteractor()
        style = vtk.vtkInteractorStyleTrackballCamera()
        self.iren.SetInteractorStyle(style)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(self.model.GetOutputPort())
        mapper.ScalarVisibilityOff()
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

        self.plane_widget = vtk.vtkImagePlaneWidget()
        self.plane_widget.SetInteractor(self.iren)
        self.plane_widget.SetInputData(self.image)
        self.plane_widget.PlaceWidget()
        self.plane_widget.SetPlaneOrientationToZAxes()
        self.plane_widget.SetSliceIndex(180)

    def preview_model(self):
        '''Return to view of 3d model'''
        self.renderer.AddActor(self.actor)
        self.iren.Initialize()

    def reset_window(self):
        '''Clear window '''
        self.plane_widget.Off()
        self.renderer.RemoveAllViewProps()
        self.iren.Initialize()

    def cut_model(self, plane_mode=False):
        '''Cut model with intersection plane defining by user'''
        plane = vtk.vtkPlane()
        plane.SetNormal(self.plane_widget.GetNormal())
        plane.SetOrigin(self.plane_widget.GetCenter())
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
            self.plane_widget.TextureVisibilityOn()
            clip_actor.GetProperty().SetOpacity(0.1)
        else:
            self.plane_widget.TextureVisibilityOff()
        self.renderer.AddActor(clip_actor)
        self.plane_widget.On()
        textActor = vtk.vtkTextActor()
        textActor.GetTextProperty().SetFontSize (20)
        textActor.GetTextProperty().SetColor( 1, 1, 1)
        text = self.getPlaneInfo(self.plane_widget)
        textActor.SetInput(text)
        self.renderer.AddActor2D(textActor)

        def detect_plane_intersection(obj, event):
            plane.SetNormal(obj.GetNormal())
            plane.SetOrigin(obj.GetCenter())
            text = self.getPlaneInfo(obj)
            textActor.SetInput(text)

        self.plane_widget.AddObserver("InteractionEvent", detect_plane_intersection)
        

        self.iren.Initialize()
        
    def getPlaneInfo(self, plane):
        normal_vector = str(plane.GetNormal())
        normal_vector = normal_vector[1:-1].split(',')
        normal_vector = [round(float(x),2) for x in normal_vector]
        center_vector = str(plane.GetCenter())
        center_vector = center_vector[1:-1].split(',')
        center_vector = [round(float(x),2) for x in center_vector]
        text = 'Intersection plane\'s normal vector ' + str(normal_vector) +'\nIntersection plane\'s center ' + str(center_vector)
        return text


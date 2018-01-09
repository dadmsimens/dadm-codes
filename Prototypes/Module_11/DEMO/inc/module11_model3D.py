import vtk
from vtk.util import numpy_support
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class model3D():
    def __init__(self, mri_data = None, frame = None, layout = None):
        self.mri_data = mri_data
        self.frame = frame
        self.layout = layout
        self.mode = 0 # mode 0 - model view, mode 1 - cross section view
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
        model.SetValue(0,3)
        return image, model

    def setup_render_window(self):
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.layout.addWidget(self.vtkWidget)
        self.frame.setLayout(self.layout)
        self.renderer = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.preview_model()


    def preview_model(self):
        if self.mode == 0:
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(self.model.GetOutputPort())
            self.actor = vtk.vtkActor()
            self.actor.SetMapper(mapper)
            self.renderer.AddActor(self.actor)
        else:
            mapper = vtk.vtkDataSetMapper()
            mapper.SetInputData(self.clipped_model)
            plane_mapper = vtk.vtkPolyDataMapper()
            plane_mapper.SetInputData(self.plane_model)
            self.actor_clipped = vtk.vtkActor()
            self.actor_plane = vtk.vtkActor()

            self.actor_clipped.SetMapper(mapper)
            self.actor_plane.SetMapper(plane_mapper)
            self.actor_clipped.GetProperty().SetColor(1.0000,0.3882,0.2784)
            self.actor_clipped.GetProperty().SetInterpolationToFlat()
            self.actor_plane.GetProperty().SetColor(0.8900,0.8100,0.3400)
            self.actor_plane.GetProperty().SetOpacity(0.5)
            self.renderer.AddActor(self.actor_clipped)
            self.renderer.AddActor(self.actor_plane)


        self.renderer.ResetCamera()
        self.iren.Initialize()

    def change_mode(self):
        if self.mode == 0:
            self.mode = 1
            #self.renderer.RemoveActor(self.actor)
            #self.clipped_model = self.model

        else:
            self.mode = 0
            self.renderer.AddActor(self.actor)

        #self.preview_model()

    def cut_model(self):
        outline = vtk.vtkOutlineFilter()
        outline.SetInputConnection(self.model.GetOutputPort())

        outlineMapper = vtk.vtkPolyDataMapper()
        outlineMapper.SetInputConnection(outline.GetOutputPort())

        outlineActor = vtk.vtkActor()
        outlineActor.SetMapper(outlineMapper)
        planeWidgetX = vtk.vtkImagePlaneWidget()
        planeWidgetX.SetInputData(self.image)
        planeWidgetX.TextureVisibilityOff()
        planeWidgetX.SetPlaneOrientationToZAxes()
        prop1 = planeWidgetX.GetPlaneProperty()
        prop1.SetColor(1, 0, 0)
        
        self.renderer.AddActor(outlineActor)
        style=vtk.vtkInteractorStyleTrackballCamera()
        self.iren.SetInteractorStyle(style)
        planeWidgetX.SetInteractor(self.iren)
        planeWidgetX.On()
        self.renderer.ResetCamera();
        cam1 = self.renderer.GetActiveCamera()
        cam1.Elevation(110)
        cam1.SetViewUp(0, 0, -1)
        #cam1.Azimuth(45)
        self.renderer.ResetCameraClippingRange()
        
        
        def MouseMoveCallback(obj, event):
            plane = vtk.vtkPlane()
            plane.SetNormal(planeWidgetX.GetNormal())
            plane.SetOrigin(planeWidgetX.GetCenter())
            clipper = vtk.vtkClipPolyData()
            clipper.SetInputConnection(self.model.GetOutputPort())
            clipper.SetClipFunction(plane)
            clipper.SetValue(0)
            clipper.Update()
            mapper = vtk.vtkDataSetMapper()
            mapper.SetInputData(clipper.GetOutput())
            actor_clipped = vtk.vtkActor()
            actor_clipped.SetMapper(mapper)
            actor_clipped.GetProperty().SetColor(1.0000,0.3882,0.2784)
            actor_clipped.GetProperty().SetInterpolationToFlat()
            self.renderer.RemoveActor(outlineActor)
            self.renderer.RemoveActor(self.actor)
            self.renderer.AddActor(actor_clipped)
            #brainExtractor = clipper.GetOutput()
            planeWidgetX.Off()


        self.iren.Initialize()
        self.vtkWidget.GetRenderWindow().Render()
        style.AddObserver("RightButtonPressEvent", MouseMoveCallback)
        self.iren.Start()

        
        
        
        #if self.clipped_model:
            #self.renderer.RemoveActor(self.actor_clipped)
            #self.renderer.RemoveActor(self.actor_plane)
        
        #plane = vtk.vtkPlane()
        ##plane.SetOrigin(0,0,0)
        #plane.SetOrigin(self.actor.GetOrigin())#Sagital
        #print(self.actor.GetOrigin())
        ##plane.SetNormal(1,-1, -1)
        #plane.SetNormal(val1,val2,val3)#Sagital
        #print(self.actor.GetCenter())
        ##print(self.clipped_model.GetOrigin())
        #clipper = vtk.vtkClipPolyData()
        #clipper.SetInputConnection(self.model.GetOutputPort())
        #clipper.SetClipFunction(plane)
        #clipper.SetValue(0)
        #clipper.Update()

        #self.clipped_model = clipper.GetOutput()

        #boundaryEdges = vtk.vtkFeatureEdges()
        #boundaryEdges.SetInputData(self.clipped_model)
        #boundaryEdges.BoundaryEdgesOn()
        #boundaryEdges.FeatureEdgesOff()
        #boundaryEdges.NonManifoldEdgesOff()
        #boundaryEdges.ManifoldEdgesOff()

        #boundaryStrips = vtk.vtkStripper()
        #boundaryStrips.SetInputConnection(boundaryEdges.GetOutputPort())
        #boundaryStrips.Update()

        #self.plane_model = vtk.vtkPolyData()
        #self.plane_model.SetPoints(boundaryStrips.GetOutput().GetPoints())
        #self.plane_model.SetPolys(boundaryStrips.GetOutput().GetLines())
        #self.preview_model()
        
        
        #self.renderer.RemoveActor(self.actor_clipped)
        #self.renderer.RemoveActor(self.actor_plane)


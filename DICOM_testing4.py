import vtk
import pydicom
import os
import numpy as np

def load_dicom_series(directory):
    reader = vtk.vtkDICOMImageReader()
    reader.SetDirectoryName(directory)
    reader.Update()
    return reader.GetOutput()

def main():
    # Provide the path to the directory containing DICOM files
    dicom_directory = "DICOM_files"

    # Load the DICOM series
    volume = load_dicom_series(dicom_directory)

    # Create a 3D rendering window
    ren = vtk.vtkRenderer()
    ren.SetBackground(1.0, 1.0, 1.0) 
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetSize(800, 800)

    # Create a volume mapper
    volumeMapper = vtk.vtkSmartVolumeMapper()
    volumeMapper.SetBlendModeToComposite()
    volumeMapper.SetInputData(volume)

    # Create a volume property
    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.ShadeOff()
    volumeProperty.SetInterpolationTypeToLinear()
    volumeProperty.SetScalarOpacityUnitDistance(0.8919)

    # Create a volume actor
    volumeActor = vtk.vtkVolume()
    volumeActor.SetMapper(volumeMapper)
    volumeActor.SetProperty(volumeProperty)

    # Add the volume actor to the renderer
    ren.AddActor(volumeActor)

    # Create a rendering window interactor
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # Start the rendering loop
    renWin.Render()
    iren.Start()

if __name__ == "__main__":
    main()

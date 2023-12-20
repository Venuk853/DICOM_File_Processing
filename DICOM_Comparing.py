import tkinter as tk
import pydicom
import numpy as np
from PIL import Image, ImageTk
from tkinter import filedialog
from RangeSlider.RangeSlider import RangeSliderH 

class DICOMViewerApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("DICOM Viewer")
        self.window.configure(bg='white')

        # Initialize the DICOM file paths and pixel arrays for two boxes
        self.file_path1 = None
        self.pixel_array1 = None
        self.file_path2 = None
        self.pixel_array2 = None

        # Create variables to store the slider values (min and max) for two boxes
        self.min_slider_value1_left = tk.DoubleVar(value = 25)
        self.min_slider_value1_left.trace("w", self.update_image1)
        self.max_slider_value1_right = tk.DoubleVar(value = 225)
        self.max_slider_value1_right.trace("w", self.update_image1)
        self.min_slider_value2_left = tk.DoubleVar(value = 25)
        self.min_slider_value2_left.trace("w", self.update_image2)
        self.max_slider_value2_right = tk.DoubleVar(value = 225)
        self.max_slider_value2_right.trace("w", self.update_image2)

        # Create the main frame
        main_frame = tk.Frame(self.window, bg='white')
        main_frame.pack(padx=10, pady=10)

        # Create two boxes (Frames) side by side
        box1 = tk.Frame(main_frame, bg='white', bd=2, relief=tk.SOLID, highlightbackground='blue', highlightthickness=1)
        box1.pack(side=tk.LEFT, padx=10)

        box2 = tk.Frame(main_frame, bg='white', bd=2, relief=tk.SOLID, highlightbackground='blue', highlightthickness=1)
        box2.pack(side=tk.LEFT, padx=10)

        # Create buttons to open DICOM files for each box
        button1 = tk.Button(box1, text="Open DICOM File 1", bg='blue', fg='white', command=self.browse_file1)
        button1.pack(padx=20, pady=20)
        button2 = tk.Button(box2, text="Open DICOM File 2", bg='blue', fg='white', command=self.browse_file2)
        button2.pack(padx=20, pady=20)

        self.hSlider1 = RangeSliderH( box1 , [self.min_slider_value1_left, self.max_slider_value1_right] , padX = 20, min_val=0, max_val=255)
        self.hSlider1.pack()

        self.hSlider2 = RangeSliderH( box2 , [self.min_slider_value2_left, self.max_slider_value2_right] , padX = 20, min_val=0, max_val=255)
        self.hSlider2.pack()


        self.image_label1 = tk.Label(box1, bg='white')
        self.image_label1.pack(padx=10, pady=10)
        self.image_label2 = tk.Label(box2, bg='white')
        self.image_label2.pack(padx=10, pady=10)

    def browse_file1(self):
    # Open file dialog to select the DICOM file for box 1
        file_path = filedialog.askopenfilename(filetypes=[("DICOM Files", "*.dcm")])

        if file_path:
            self.file_path1 = file_path  # Update the DICOM file path
            
            # Read the DICOM file
            ds = pydicom.dcmread(self.file_path1)

            # Get the pixel data as an array
            self.pixel_array1 = ds.pixel_array

            # Update the slider values for the RangeSliderH
            self.min_slider_value1_left.set(np.min(self.pixel_array1))
            self.max_slider_value1_right.set(np.max(self.pixel_array1))

            # Process and display the initial image for box 1
            self.update_image1()

    def browse_file2(self):
    # Open file dialog to select the DICOM file for box 2
        file_path = filedialog.askopenfilename(filetypes=[("DICOM Files", "*.dcm")])

        if file_path:
            self.file_path2 = file_path  # Update the DICOM file path
            
            # Read the DICOM file
            ds = pydicom.dcmread(self.file_path2)

            # Get the pixel data as an array
            self.pixel_array2 = ds.pixel_array

            # Update the slider values for the RangeSliderH
            self.min_slider_value2_left.set(np.min(self.pixel_array2))
            self.max_slider_value2_right.set(np.max(self.pixel_array2))

            # Process and display the initial image for box 2
            self.update_image2()


    def update_image1(self, *args):
        # This function gets called whenever the slider values change for box 1
        if self.pixel_array1 is not None:
            # Get the selected grayscale value range from the sliders
            min_value = int(self.min_slider_value1_left.get())
            max_value = int(self.max_slider_value1_right.get())

            # Process the pixel array based on the selected grayscale value range
            processed_array = ((self.pixel_array1 >= min_value) & (self.pixel_array1 <= max_value)) * 255

            # Convert the processed array to an image
            processed_image = Image.fromarray(processed_array.astype(np.uint8))
            photo = ImageTk.PhotoImage(processed_image)

            # Display the processed image for box 1
            self.image_label1.configure(image=photo)
            self.image_label1.image = photo

    def update_image2(self, *args):
        # This function gets called whenever the slider values change for box 2
        if self.pixel_array2 is not None:
            # Get the selected grayscale value range from the sliders
            min_value = int(self.min_slider_value2_left.get())
            max_value = int(self.max_slider_value2_right.get())

            # Process the pixel array based on the selected grayscale value range
            processed_array = ((self.pixel_array2 >= min_value) & (self.pixel_array2 <= max_value)) * 255

            # Convert the processed array to an image
            processed_image = Image.fromarray(processed_array.astype(np.uint8))
            photo = ImageTk.PhotoImage(processed_image)

            # Display the processed image for box 2
            self.image_label2.configure(image=photo)
            self.image_label2.image = photo

    def run(self):
        # Start the Tkinter event loop
        self.window.mainloop()

# Create an instance of the DICOMViewerApp
app = DICOMViewerApp()

# Run the application
app.run()

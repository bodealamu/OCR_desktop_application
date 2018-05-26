import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter
import tkinter.messagebox
import pytesseract
import cv2
import numpy as np


def extract_text(Image_path):
    # converts the image to text by taking the image path as an input
    output_text = pytesseract.image_to_string(Image_path)
    return output_text


class Parent(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack()
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {}

        # allows the different screens to be raised to the front

        for F in (First_page,Image_view):
            frame = F(container, self)
            self.frames[F]= frame
            frame.grid(row=0,column=0,sticky = 'nsew')
        self.show_screen(First_page)

    def show_screen(self, screenpage):
        # selects the appropriate screen to be pushed to the front of the application
        frame = self.frames[screenpage]
        frame.tkraise()

class First_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Front page label
        Front_page_label = tk.Label(self,text = 'Please select the image file.')
        Front_page_label.pack(side='left',fill = 'x',expand =1)
        # Button used to select an image from the file system
        BrowseButton1 = tk.Button(self,text='Broswe for image.', command= self.browse_images)
        BrowseButton1.pack(side= 'left',fill = 'x',expand =1,padx = 20)

        # Button used to view the selected image and to proceed to the next page in the app
        ViewButton1 = tk.Button(self,text='View uploaded image.', command= self.view)
        ViewButton1.pack(side= 'left',fill = 'y',expand =1,padx = 20)

    def view(self):
        try:
            image = Image.open(filename)
            photo = ImageTk.PhotoImage(image)
            global lx
            lx = tk.Label(image=photo)
            lx.image = photo
            lx.pack()
            self.controller.show_screen(Image_view)
        except:
            tkinter.messagebox.showinfo('Error', 'Select a Jpeg or Png image first')

    def browse_images(self):
        global filename
        filename =  filedialog.askopenfilename(initialdir = "/",title = "Select image file",filetypes = (("jpeg files","*.jpg"),("png files","*.png"),("all files","*.*")))
        if len(filename) == 0:
            tkinter.messagebox.showinfo('Error', 'Please select an actual file')
        else:
            tkinter.messagebox.showinfo('Success!', 'The image has been uploaded, click on View uploaded image.')

    def preprocess():
        image_file = cv2.imread(filename, cv2.IMREAD_GRAYSCALE) # read the image into opencv format
        kernel = np.ones((1,1),np.uint8) # kernel used for erosion and dilation
        image_file = cv2.dilate(image_file, kernel, iterations = 1)
        image_file = cv2.erode(image_file, kernel, iterations = 1)
        retval, threshold = cv2.threshold(image_file, 115,255, cv2.THRESH_BINARY) # different thresholding function may be used later
        cv2.imshow('Result of Image preprocessing.', threshold) # displays the preprocessed image
        text_released = extract_text(image_file)
        result_print = tk.StringVar()
        result_print.set(text_released)

        # A new window is created to display the extracted text
        top = tk.Toplevel()
        top.title('Extracted text.')
        top.geometry('800x450')
        t= tk.Label(top,text = '', textvariable =result_print)
        t.pack()
        if len(text_released) == 0:
            tkinter.messagebox.showinfo('', 'No text extracted from image.')


class Image_view(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        preprocessButton = tk.Button(self,text = 'Preprocess Image and Extract text.',command = First_page.preprocess)
        preprocessButton.pack(side = 'bottom')


App = Parent()
App.title('Optical Character Recognition App')
App.geometry('1600x900')
App.mainloop()

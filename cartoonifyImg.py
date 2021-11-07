
import cv2 #for image processing
import easygui #to open the fileopenbox
import numpy as np # to store image
import imageio # to read the image stored at particular path1

import sys
import matplotlib.pyplot as plt  #This library is used for visualization and plotting. Thus, it is imported to form the plot of images.
import os                      #For OS interaction. Here, to read the path and save images to that path
import tkinter as tk           #Tkinter is a Python binding to the Tk GUI toolkit.
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image  #Python Imaging Library is a free and open-source additional library for the Python programming language
                                 #that adds support for opening, manipulating, and saving many different image file formats.

top = tk.TK()
top = geomentry('400x400')
top.title('Cartoonify yout Image !')
top.configure(background = 'white')
label = Label(top,background='#CDCDCD', font=('calibri',20,'bold'))
#################################################
#building the file box to choose the particular file
#main window of our application called as upload()
###################################################
''' fileopenbox opens the filebox and helps to choose the file and to store the file path as string'''

def upload():
    ImagePath = easygui.fileopenbox()
    cartoonify(ImagePath)

def cartoonify(ImagePath):
    #read the image in number that computer understand
    original_image = cv2.imread(ImagePath)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    #print(image) #image is stored in form of numbers

    #confirm that image is chosen.......
    if original_image is None:
        print("cannot finf any image. Choose appropriate file!")
        sys.exit()

#.................begin the image transformation................
    ReSized1 = cv2.resize(original_image, (960,540))
    #plt.imshow(ReSized1, cmap='gray')

#...............transforming the image to grayScaleImage................
#converting the image to grayScaleImage......
    grayScaleImage = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    ReSized2 = cv2.resize(grayScaleImage, (960,540))
    #plt.imshow(ReSized2, cmap = 'gray')

#......smoothening the gray scale image...........................
##applying median blur to smoothen an image......
    smoothGrayScale = cv2.medianBlur(grayScaleImage,5)
    ReSized3 = cv2.resize(smoothGrayScale, (960,540))
    #plt.imshow(ReSized3 , cmap = 'gray')

#..........Retrieving the edges of the image.........................
#retrieving the edges for cartoon effect
#by using thresholding technique
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255,
                cv2.ADAPTIVE_THRESH_MEAN_C,
                cv2.THRESH-BINARY, 9, 9)
    ReSized4 = cv2.resize(getEdge, (960,540))
    #plt.imshow(ReSized4, cmap ='gray')

#..............preparing the mask Image...............................
    #applying bacterial filter to remove noise
    #and keep edge sharp as required
    colorImage = cv2.bilateralFilter(original_image, 9, 300, 300)
    ReSized5 = cv2.resize(colorImage, (960,540))
    #plt.imshow(ReSized5, cmap = 'gray')

#..............giving a cartoon effect.................................
    #masking edged image with our "BEAUTIFY" images
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
    ReSized6 = cv2.resize(cartoonImage, (960,540))

    #plt.imshow(ReSized6, cmap ='gray')

#..............polloting all the transitions together....................
    #plotting the whole transiton
    images = [ReSized1, ReSized2 , ReSized3, ReSized4, ReSized5, ReSized6]

    fig, axes = plt.subplot(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace =0.1, wspace = 0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i],camp='gray')

    save1 = Button(top,text ="save cartoon image",command = lambda: save(ReSized6, ImagePath),padx = 30,pady=5)
    save1.configure(background='#364156', foreground = 'white', font=('calibri',10,'bold'))
    save1.pack(side=TOP,pady = 50)

    plt.show()

def save(ReSized6, ImagePath):
    #daving an image using imwrite()
    newName ="cartoonified_Image"
    path1 = os.path.dirname(ImagePath)
    extension = os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path,cv2.cvtColor(ReSized6,cv2.COLOR_RGB2BGR))
    i = "image saved by name" + newName + "at" + path
    tk.messagebox.showinfo(title = None, message = I)

upload = Button(top,text = "Cartoonify an Image", command = upload, padx=10, pady=5)
upload.configure(background='#364156', foreground="white",front=('calibri',10,'bold'))
upload.pack(side= Top, pady=50)

top.mainloop()

#from __future__ import print_function
from tkinter import *
import os
from threading import Thread
from time import *
import tkinter as tk
from PIL import Image, ImageTk
import cv2
from matplotlib import pyplot as plt
import numpy as np
from matplotlib import *
import matplotlib.figure
import matplotlib.patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
class MainWindow():
    def __init__(self):
        self.i = 0
        self.j = 0
        self.main = Tk()
        self.cap = cv2.VideoCapture(0)
        self.main.title("Waleed Al-Akwa")
        self.main['bg']='brown'
        self.main_width = 1500
        self.main_height = 750

        self.main_x = int((self.main.winfo_screenwidth() / 2) - (self.main_width / 2))  
        self.main_y = int((self.main.winfo_screenheight() / 2) - (self.main_height / 2))
        self.main_geometry = str(self.main_width) + 'x' + str(self.main_height) + '+' + str(self.main_x) + '+' + str(self.main_y)
        self.main.geometry(self.main_geometry)


        self.title_frame = Frame(self.main,width=1180,height=100)
        self.title_frame.place(anchor="nw",x=250,y=20)
        self.title_label = Label(self.title_frame,width=1180,height=100,text="Object Detection")
        self.title_label.config(font=("Courier", 20))
        self.title_label.place(anchor="c",relx=0.5,rely=0.5)


        self.videoboxframe = Frame(self.main,width=350,height=300)
        self.videoboxframe.place(anchor="nw",x=200,y=200)
        self.videoboxbuttonframe = Frame(self.main,width=350,height=30)
        self.videoboxbuttonframe.place(anchor="nw",x=200,y=520)
        self.videoboxbutton = Button(self.videoboxbuttonframe,text="video capturing",width=250,height=30,command=self.video_captured,bg="white",fg="black")
        self.videoboxbutton.place(anchor="c",relx=0.5,rely=0.5)


        self.pictureboxframe = Frame(self.main,width=350,height=300)
        self.pictureboxframe.place(anchor="nw",x=660,y=200)
        self.pictureboxbuttonframe = Frame(self.main,width=350,height=30)
        self.pictureboxbuttonframe.place(anchor="nw",x=660,y=520)
        self.pictureboxbutton = Button(self.pictureboxbuttonframe,text="photo capturing",width=250,height=30,command=self.photo_captured,bg="white",fg="black")
        self.pictureboxbutton.place(anchor="c",relx=0.5,rely=0.5)



        self.pictureanalyzboxframe = Frame(self.main,width=350,height=300)
        self.pictureanalyzboxframe.place(anchor="nw",x=1120,y=200)
        self.pictureanalyzboxlabel = Label(self.pictureanalyzboxframe,width=350,height=300)
        self.pictureanalyzboxlabel.place(anchor="c",relx=0.5,rely=0.5)
        self.pictureanalyzboxbuttonframe = Frame(self.main,width=350,height=30)
        self.pictureanalyzboxbuttonframe.place(anchor="nw",x=1120,y=520)
        self.pictureanalyzboxbutton = Button(self.pictureanalyzboxbuttonframe,text="photo analyzing",width=250,height=30,command=self.cracks_detection,bg="white",fg="black")
        self.pictureanalyzboxbutton.place(anchor="c",relx=0.5,rely=0.5)


        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.interval = 100 # Interval in ms to get the latest frame
        # Create canvas for image
        self.canvas = tk.Canvas(self.videoboxframe, width=self.width, height=self.height)
        # Update image on canvas
        self.update_image()
        self.main.mainloop()
    def update_image(self):
        # Get the latest frame and convert image format
        self.image = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_BGR2RGB) # to RGB
        self.image = Image.fromarray(self.image) # to PIL format
        self.image = ImageTk.PhotoImage(self.image) # to ImageTk format
        # Update image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
        # Repeat every 'interval' ms
        self.main.after(self.interval, self.update_image)


    def photo_captured(self):
    	self.return_value, self.image1 = self.cap.read()
    	#cv2.imshow("Test Picture", image) 
    	cv2.imwrite('opencv'+str(self.i)+'.png', self.image1)
    	self.photos1 = PhotoImage(file = r"\home\pi\waleedalakwa\screenshot"+str(self.i)+".png")
    	self.photo_lable = Label(self.pictureboxframe,width=350,height=300,image=self.photos1)
    	self.photo_lable.place(anchor="c",relx=0.5,rely=0.5)
    	self.i = self.i+1

    def video_captured(self):
    	self.canvas.place(anchor="c",relx=0.5,rely=0.5)


    def cracks_detection(self):
    	self.img = cv2.imread(r'/home/pi/waleedalakwa/screenshot'+str(self.i-1)+'.png')
    	#print("opencv"+str(self.i))
    	self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
    	self.blur = cv2.blur(self.gray,(3,3))
    	self.img_log = (np.log(self.blur+1)/(np.log(1+np.max(self.blur))))*255
    	self.img_log = np.array(self.img_log,dtype=np.uint8)
    	self.bilateral = cv2.bilateralFilter(self.img_log, 5, 75, 75)
    	self.edges = cv2.Canny(self.bilateral,100,200)
    	self.kernel = np.ones((5,5),np.uint8)
    	self.closing = cv2.morphologyEx(self.edges, cv2.MORPH_CLOSE, self.kernel)
    	self.orb = cv2.ORB_create(nfeatures=1500)
    	self.keypoints, self.descriptors = self.orb.detectAndCompute(self.closing, None)
    	self.featuredImg = cv2.drawKeypoints(self.closing, self.keypoints, None)
    	#print(type(self.featuredImg))
    	self.converted_image = ImageTk.PhotoImage(Image.fromarray(self.featuredImg))
    	cv2.imwrite(r'/home/pi/waleedalakwa/screenshot'+str(self.i-1)+'.png', self.featuredImg)
    	#self.photos2 = PhotoImage(file = r'C:/Users/output/opencv'+str(self.i-1)+'.png')
    	#print(type(self.converted_image))
    	self.converted_image = Image.open(r'/home/pi/waleedalakwa/screenshot'+str(self.i-1)+'.png')
    	self.converted_image = self.converted_image.resize((350, 300), Image.ANTIALIAS)
    	self.my_img = ImageTk.PhotoImage(self.converted_image)
    	self.pictureanalyzboxlabel.configure(image=self.my_img)
    	self.pictureanalyzboxlabel.pack()
        




#del(camera)
object = MainWindow()

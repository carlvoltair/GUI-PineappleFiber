import cv2
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from ultralytics import YOLO
import numpy as np

# YOLOv8 model path
model = YOLO("YOLOv8_best.pt")  

# Main window
window = Tk()
window.title("Pineapple Grade Detection")
window.configure(bg='black')

# Set up camera
cap = cv2.VideoCapture(0)

# Video frame
def update_frame():
    global current_frame
    ret, frame = cap.read()
    if ret:
        current_frame = frame.copy()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
    video_label.after(10, update_frame)

# Detect button
def detect():
    if current_frame is not None:
        results = model(current_frame)[0]  
        annotated_frame = results.plot()  

        # Display in the GUI
        frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

# Quit the program
def quit_app():
    cap.release()
    window.destroy()

# GUI Layout
video_label = Label(window)
video_label.grid(row=0, column=0, padx=10, pady=10)

button_frame = Frame(window, bg='black')
button_frame.grid(row=0, column=1, padx=10, pady=10)

detect_btn = Button(button_frame, text="DETECT", bg='green', fg='white', width=15, height=3, command=detect)
detect_btn.pack(pady=10)

quit_btn = Button(button_frame, text="EXIT", bg='red', fg='white', width=15, height=3, command=quit_app)
quit_btn.pack(pady=10)


current_frame = None

# Video
update_frame()
window.mainloop()

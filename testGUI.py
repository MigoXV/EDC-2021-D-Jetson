import cv2
import _thread
from read import Read
from uartGUI import JetsonGUI
import matplotlib.pyplot as plt
import numpy as np

ip_A = "127.0.0.1"
ip_B = "127.0.0.1"

image_from_A = None
# image_from_B = None

def read_image_A_thread(thread_name, reader):
    global image_from_A, time_from_A, t
    while True:
        temp_t = cv2.getTickCount()
        image1, time_from_A = reader.receive_image()
        image_from_A = image1.copy()
        t = 1.0 / ((cv2.getTickCount() - temp_t) / cv2.getTickFrequency())
        # print("A", int(t))


# def read_image_B_thread(thread_name, reader):
#     global image_from_B, time_from_B, t
#     while True:
#         temp_t = cv2.getTickCount()
#         image1, time_from_B = reader.receive_image()
#         image_from_B = image1.copy()
#         t = 1.0 / ((cv2.getTickCount() - temp_t) / cv2.getTickFrequency())
#         # print("B", int(t))


def start_thread():
    reader_A = Read()
    reader_A.set_read_config(ip_A, 8001)
    _thread.start_new_thread(read_image_A_thread, ("1", reader_A))
    print("connect node A success")
    # reader_B = Read()
    # reader_B.set_read_config(ip_B, 8001)
    # _thread.start_new_thread(read_image_B_thread, ("1", reader_B))
    # print("connect node B success")
    # image_from_B=image_from_A
    
# if __name__ == '__main__':
#     start_thread()
#     while True:
#         # print(type(image_from_A))
#         # print(type(image_from_A)=="<class 'numpy.ndarray'>")
#         if image_from_A is None:
#             print('image_from_A is None')  
#         elif isinstance(image_from_A, np.ndarray):
#             print('image_from_A is ndarray')  # x is ndarray
#             plt.imshow(image_from_A[:,:,::-1])
#             plt.show()
            
#     # MyGUI=JetsonGUI()
    
from tkinter import *
import threading

image_array = np.zeros((480, 640, 3), dtype=np.uint8)

start_thread()
        
root = Tk()
canvas = Canvas(root, width=640, height=480)
canvas.pack()

# photo_image = PhotoImage(width=640, height=480)
# image_array = photo_image
canvas.create_image(0, 0, image=image_from_A, anchor='nw')

def update():
    global image_from_A
    image_from_A.put()
#     photo_image.put(image_array.tobytes())
#     root.after(50, update)



# update()
root.mainloop() 
from read import Read
import cv2
import threading
import numpy as np
import some_image
from some_image import *
# from search import *
import search
from algorithm import *
from tkGUI import JetsonGUI as tkGUI
from PIL import Image, ImageTk
import random
import tkinter as tk

image_from_A = None
image_from_B = None
image_use_A = None
image_use_B = None

check_flag = False
is_complete_flag = True
is_cal_flag = True
task_id = None
is_first = True
to_zero_flag = False

time_from_A = 0
time_from_B = 0

L = 0
theta = 0
t = 0

# ip_A = "192.168.43.120"
# ip_B = "192.168.43.92"

ip_A = "192.168.43.33"
ip_B = "127.0.0.1"

def calc_thread():
    global image_from_A,image_from_B
    cv2.namedWindow("MainWindow", cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow("MainWindow", 0, 0)
    cv2.setWindowProperty("MainWindow", cv2.WND_PROP_TOPMOST, 1)
    image2 = some_image.get_button_image()
    image3 = some_image.get_ellipse()
    record_image_A = None
    record_image_B = None
    search_A = search.Search("1")
    search_B = search.Search("2")
    show_T = 0
    show_deltaA = 0
    show_deltaB = 0    
    
    while True:
        try:
            if image_from_A is not None and image_from_B is not None:
                image_from_A=cv2.resize(image_from_A,(640,480))
                image_from_B=cv2.resize(image_from_B,(640,480))
                if image_from_A is not record_image_A:
                    record_image_A = image_from_A
                    time_A = time_from_A
                    image_use_A = image_from_A.copy()
                    search_A.search_black(image_use_A, time_A)
                if image_from_B is not record_image_B:
                    record_image_B = image_from_B
                    time_B = time_from_B
                    image_use_B = image_from_B.copy()
                    search_B.search_black(image_use_B, time_B)
                A_T, A_deltaX = search_A.get_T_and_deltaX()
                B_T, B_deltaX = search_B.get_T_and_deltaX()
                if (A_T is not None or A_deltaX is not None or B_T is not None or B_deltaX is not None) and \
                        not is_complete_flag:
                    is_complete_flag = True
                    task_id = 0
                if A_T is not None and A_deltaX is not None and B_T is not None and B_deltaX is not None and \
                        not is_cal_flag:
                    is_complete_flag = True
                    is_cal_flag = True
                    task_id = 0
                    print("T:", (A_T + B_T) / 2)
                    print("A_deltaX:", A_deltaX)
                    print("B_deltaX:", B_deltaX)
                    print("k:", A_deltaX / B_deltaX)
                    theta, flag = cal_theta(A_deltaX, B_deltaX, to_zero_flag)
                    to_zero_flag = False
                    L, T = cal_l(A_T, B_T, theta, flag)
                    show_T = T
                    show_deltaA = A_deltaX
                    show_deltaB = B_deltaX
                    # usart.complete_write()
                    print("L:", L)
                    print("theta:", theta)
                else:
                    pass
                
                image = np.hstack((image_use_A, image_use_B))
                image = np.vstack((image, image2))
                image = np.vstack((image, image3))  
                text = "fps: " + str(int(t))
                cv2.putText(image, text, (0, 670 + 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
                text = "A"
                cv2.putText(image, text, (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
                text = "B"
                cv2.putText(image, text, (640, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
                if not check_flag:
                    text = "Checking!!!"
                    cv2.putText(image, text, (400, 600), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 1)
                elif is_complete_flag and (task_id is None or is_first):
                    text = "Waiting for command"
                    cv2.putText(image, text, (150, 600), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 1)
                elif not is_cal_flag and task_id is not None and not is_first:
                    text = "Measuring"
                    cv2.putText(image, text, (400, 540), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 1)
                    text = "A epoch: " + str(min(10, search_A.count))
                    cv2.putText(image, text, (400, 610), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 1)
                    text = "B epoch: " + str(min(10, search_B.count))
                    cv2.putText(image, text, (400, 670), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 1)
                elif is_complete_flag and task_id is not None and not is_first and is_cal_flag:
                    text = "L: " + str(L)
                    cv2.putText(image, text, (250, 550), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 1)
                    text = "Theta: " + str(theta)
                    cv2.putText(image, text, (250, 650), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 1)
                    text = "T: " + str(show_T)
                    cv2.putText(image, text, (1070, 670 + 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
                    text = "deltaX_B: " + str(show_deltaB)
                    cv2.putText(image, text, (1070, 640 + 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
                    text = "deltaX_A: " + str(show_deltaA)
                    cv2.putText(image, text, (1070, 610 + 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
                
                # image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                # pil_image = Image.fromarray(image_rgb)
                # tk_image = ImageTk.PhotoImage(pil_image)
                # imageSize=(image.size[0]/2,image.size[1]/2)
                image=cv2.resize(image,(960,900))
                cv2.imshow("MainWindow", image)
                cv2.waitKey(1)
                

                # tk.canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
                # usart.canvas.image = tk_image
                
        except Exception as e:
            print(e)
            is_complete_flag = True
            is_cal_flag = True
            task_id = 0
            search_A.reset()
            search_B.reset()


def read_image_A_thread(thread_name, reader):
    global image_from_A, time_from_A, t
    while True:
        temp_t = cv2.getTickCount()
        image1, time_from_A = reader.receive_image()
        image_from_A = image1.copy()
        t = 1.0 / ((cv2.getTickCount() - temp_t) / cv2.getTickFrequency())
        # if image_from_A is not None:
        #     print("received a image")

def read_image_B_thread(thread_name, reader):
    global image_from_B, time_from_B, t
    while True:
        temp_t = cv2.getTickCount()
        image1, time_from_B = reader.receive_image()
        image_from_B = image1.copy()
        t = 1.0 / ((cv2.getTickCount() - temp_t) / cv2.getTickFrequency())
        # if image_from_B is not None:
        #     print("received B image")

# def GUI_thread(GUIobj):
#     GUIobj.window.mainloop()

def start_thread():
    reader_A = Read()
    reader_A.set_read_config(ip_A, 8001)
    threadA=threading.Thread(target=read_image_A_thread,args=("1", reader_A,))
    threadA.start()
    print("connect node A success")
    
    reader_B = Read()
    reader_B.set_read_config(ip_B, 8001)
    threadB=threading.Thread(target=read_image_B_thread,args=("1", reader_B,))
    threadB.start()
    print("connect node B success")
    
    # global image_from_B, time_from_B
    # image_from_B, time_from_B=image_from_A, time_from_A
    
    threadCalc=threading.Thread(target=calc_thread)
    threadCalc.start()
    
    # threadGUI=threading.Thread(target=GUI_thread,args=(usart,))
    # threadGUI.start()

if __name__ == '__main__':
    # 启动A、B线程
    start_thread()
    # tkinter必须放在主线程里
    usart=tkGUI()
    usart.window.mainloop()
    # GUI_thread(usart)

    # # cv2.namedWindow("MainWindow", cv2.WINDOW_AUTOSIZE)
    # # cv2.moveWindow("MainWindow", 0, 0)
    # # cv2.setWindowProperty("MainWindow", cv2.WND_PROP_TOPMOST, 1)
    # image2 = get_button_image()
    # image3 = get_ellipse()
    # record_image_A = None
    # record_image_B = None
    # search_A = Search("1")
    # search_B = Search("2")
    # show_T = 0
    # show_deltaA = 0
    # show_deltaB = 0
    # while True:
    #     try:
    #         if image_from_A is not None and image_from_B is not None:
    #             if image_from_A is not record_image_A:
    #                 record_image_A = image_from_A
    #                 time_A = time_from_A
    #                 image_use_A = image_from_A.copy()
    #                 search_A.search_black(image_use_A, time_A)
    #             if image_from_B is not record_image_B:
    #                 record_image_B = image_from_B
    #                 time_B = time_from_B
    #                 image_use_B = image_from_B.copy()
    #                 search_B.search_black(image_use_B, time_B)
    #             A_T, A_deltaX = search_A.get_T_and_deltaX()
    #             B_T, B_deltaX = search_B.get_T_and_deltaX()
    #             if (A_T is not None or A_deltaX is not None or B_T is not None or B_deltaX is not None) and \
    #                     not is_complete_flag:
    #                 is_complete_flag = True
    #                 task_id = 0
    #             if A_T is not None and A_deltaX is not None and B_T is not None and B_deltaX is not None and \
    #                     not is_cal_flag:
    #                 is_complete_flag = True
    #                 is_cal_flag = True
    #                 task_id = 0
    #                 print("T:", (A_T + B_T) / 2)
    #                 print("A_deltaX:", A_deltaX)
    #                 print("B_deltaX:", B_deltaX)
    #                 print("k:", A_deltaX / B_deltaX)
    #                 theta, flag = cal_theta(A_deltaX, B_deltaX, to_zero_flag)
    #                 to_zero_flag = False
    #                 L, T = cal_l(A_T, B_T, theta, flag)
    #                 show_T = T
    #                 show_deltaA = A_deltaX
    #                 show_deltaB = B_deltaX
    #                 usart.complete_write()
    #                 print("L:", L)
    #                 print("theta:", theta)
    #             else:
    #                 pass
    #             image = np.hstack((image_use_A, image_use_B))
    #             image = np.vstack((image, image2))
    #             image = np.vstack((image, image3))
    #             text = "fps: " + str(int(t))
    #             cv2.putText(image, text, (0, 670 + 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
    #             text = "A"
    #             cv2.putText(image, text, (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
    #             text = "B"
    #             cv2.putText(image, text, (640, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
    #             if not check_flag:
    #                 text = "Checking!!!"
    #                 cv2.putText(image, text, (400, 600), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 1)
    #             elif is_complete_flag and (task_id is None or is_first):
    #                 text = "Waiting for command"
    #                 cv2.putText(image, text, (150, 600), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 1)
    #             elif not is_cal_flag and task_id is not None and not is_first:
    #                 text = "Measuring"
    #                 cv2.putText(image, text, (400, 540), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 1)
    #                 text = "A epoch: " + str(min(10, search_A.count))
    #                 cv2.putText(image, text, (400, 610), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 1)
    #                 text = "B epoch: " + str(min(10, search_B.count))
    #                 cv2.putText(image, text, (400, 670), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 1)
    #             elif is_complete_flag and task_id is not None and not is_first and is_cal_flag:
    #                 text = "L: " + str(L)
    #                 cv2.putText(image, text, (250, 550), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 1)
    #                 text = "Theta: " + str(theta)
    #                 cv2.putText(image, text, (250, 650), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 1)
    #                 text = "T: " + str(show_T)
    #                 cv2.putText(image, text, (1070, 670 + 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
    #                 text = "deltaX_B: " + str(show_deltaB)
    #                 cv2.putText(image, text, (1070, 640 + 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
    #                 text = "deltaX_A: " + str(show_deltaA)
    #                 cv2.putText(image, text, (1070, 610 + 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
                
    #             image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #             pil_image = Image.fromarray(image_rgb)
    #             tk_image = ImageTk.PhotoImage(pil_image)
    #             # cv2.imshow("MainWindow", image)
    #             # cv2.waitKey(1)
                

    #             tk.canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
    #             usart.canvas.image = tk_image
                
    #     except Exception as e:
    #         print(e)
    #         is_complete_flag = True
    #         is_cal_flag = True
    #         task_id = 0
    #         search_A.reset()
    #         search_B.reset()

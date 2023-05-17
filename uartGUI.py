
# 这个程序设计了一个GUI
# 这个GUI完成如下功能：
#   1. 显示GUI，其中共有5个按钮，分别显示check,task1,task4
#   2. 点击check按钮，文本框输出check OK字符
#   3. 点击task1按钮，返回数字1
#   4. 点击task4按钮，返回数字4
#   5. 其他程序调用complete_write函数后，屏幕上显示complete

from tkinter import * 
from PIL import Image, ImageTk
import cv2




class JetsonGUI:
    def __init__(self):
        
        self.data2send = 0
        self.checkState = 'Checking'
        # 创建GUI窗口
        self.window = Tk()
        self.window.title("JetsonGUI")

        self.frame1 = Frame(self.window)
        self.frame1.pack()

        self.checkLabel = Label(self.frame1, text=self.checkState)
        btCheckSend = Button(self.frame1, text='check',command=self.check_write)
        btTask1 = Button(self.frame1, text='task1', command=lambda:self.setData(1))
        btTask4 = Button(self.frame1, text='task4', command=lambda:self.setData(4))
        self.completeLabel = Label(self.frame1, text='waiting')
        canvas = Canvas(self.frame1, width=400, height=300)
        
        self.checkLabel.pack()
        btCheckSend.pack()
        btTask1.pack()
        btTask4.pack()
        self.completeLabel.pack()
        canvas.pack()
        
        # 窗口创建完毕，准备开始主循环
        self.window.mainloop()

    def check_write(self):
        # self.checkState='check OK'
        self.checkLabel['text'] = 'check OK'

    def check_read(self):
        self.checkLabel['text'] = self.checkState
    
    def setData(self, ButtonNum):
        self.data2send = ButtonNum
        self.complete_write()
        # print(ButtonNum)
        
    def get_result(self):
        return self.data2send

    def complete_write(self):
        self.completeLabel["text"] = 'complete'


if __name__ == '__main__':
    MyGUI=JetsonGUI()


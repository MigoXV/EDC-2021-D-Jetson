
# 这个程序设计了一个GUI
# 这个GUI完成如下功能：
#   1. 显示GUI，其中共有5个按钮，分别显示check,task1,task4
#   2. 点击check按钮，文本框输出check OK字符
#   3. 点击task1按钮，返回数字1
#   4. 点击task4按钮，返回数字4
#   5. 其他程序调用complete_write函数后，屏幕上显示complete

from tkinter import * 

class JetsonGUI:
    def __init__(self):
        self.data2send = 0
        self.checkState = 'Checking'
        window = Tk()
        window.title("JetsonGUI")

        frame1 = Frame(window)
        frame1.pack()

        self.checkLabel = Label(frame1, text=self.checkState)
        btCheckSend = Button(frame1, text='check',command=self.check_write)
        btTask1 = Button(frame1, text='task1', command=lambda:self.setData(1))
        btTask4 = Button(frame1, text='task4', command=lambda:self.setData(4))
        self.completeLabel = Label(frame1, text='waiting')
        
        self.checkLabel.pack()
        btCheckSend.pack()
        btTask1.pack()
        btTask4.pack()
        self.completeLabel.pack()
        
        window.mainloop()

    def check_write(self):
        self.checkState='checking'
        # self.checkLabel['text'] = 'check OK'

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
    JetsonGUI()

# class Usart:
#     def __init__(self):
#         self.usart = serial.Serial("COM5", 115200, timeout=0)

#     def write(self, command):
#         self.usart.write(bytearray(command))

#     def read(self):
#         res2 = self.usart.read(5)
#         return res2

#     @staticmethod
#     def compare(command1, command2):
#         if len(command1) < 5:
#             return False
#         if command1[0] == command2[0] and command1[1] == command2[1] and \
#                 command1[2] == command2[2] and command1[3] == command2[3] and \
#                 command1[4] == command2[4]:
#             return True
#         else:
#             return False

#     def check_write(self):
#         self.write(check_send)

#     def check_read(self):
#         res = self.read()
#         if len(res) < 5:
#             return False
#         return self.compare(res, check_read)

#     def complete_write(self):
#         self.write(complete)

#     def get_result(self):
#         res1 = self.read()
#         if res1 is None:
#             return 0
#         if len(res1) < 5:
#             return 0
#         print(res1)
#         if self.compare(res1, task1):
#             return 1
#         elif self.compare(res1, task2):
#             return 2
#         elif self.compare(res1, task3):
#             return 3
#         elif self.compare(res1, task4):
#             return 4
#         return 0

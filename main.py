# import tkinter as tk
from app import App
# from login import Login
#
# from config import CONFIGURATION


if __name__ == '__main__':
    # user = [""]
    # login = [False]
    # login_app = Login(CONFIGURATION, user, login)
    # login_app.mainloop()
    # if login[0]:
    app = App()
    app.mainloop()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from utility import *



# class Stats():
#     def __init__(self,ui):
#         self.ui=ui
#         self.ui.P3B1.clicked.connect(self.f_but1)#Page3的Import Files按键
#         self.ui.P4B1.clicked.connect(self.f_but2)#Page4的Align按键
#         self.ui.P5B1.clicked.connect(self.f_but3)#Page5的Remove Color按键
#         self.ui.P5B2.clicked.connect(self.f_but4)#Page5的Grayscale按键
#         self.ui.P6B1.clicked.connect(self.f_but5)#Page6的Luminasity to 45%按键
#         self.ui.P7B1.clicked.connect(self.f_but6)#Page7的Compress按键
#
#     def f_but1(self):
#         try:
#             scale_input = self.ui.P3Text1.toPlainText()
#             scale_output = self.ui.P3Text2.toPlainText()
#             size_input = str(self.ui.P3Box1.currentText())
#             size_output = str(self.ui.P3Box2.currentText())
#         except:
#             print('f_but1 error')
#
#
#
#
#     def f_but2(self):
#         try:
#             print('f_but2 test')
#         except:
#             print('f_but2 error')
#
#     def f_but3(self):
#         try:
#             print('f_but3 test')
#         except:
#             print('f_but3 error')
#
#     def f_but4(self):
#         try:
#             print('f_but4 test')
#         except:
#             print('f_but4 error')
#
#     def f_but5(self):
#         try:
#             print('f_but5 test')
#         except:
#             print('f_but5 error')
#
#     def f_but6(self):
#         try:
#             print('f_but6 test')
#         except:
#             print('f_but6 error')
#
# app = QApplication([])
# app.setWindowIcon(QIcon('logo.png'))#左上角的图标
# ui=uic.loadUi("test.ui")#加载ui文件名称
# stats = Stats(ui)
# stats.ui.show()
# app.exec_()
# -*- coding: utf-8 -*-
"""
@Project Name  pyqt5_learning
@File Name:    main
@Software:     PyCharm
@Time:         2021/12/10 17:26
@Author:       9527
@contact:      langangpaibian@sina.com
@version:      1.0
@Description:　
"""
import os
import sys

from pathlib import Path
import traceback
import time
import shutil
from threading import Thread
import multiprocessing

import numpy as np
from PIL import Image
import cv2
import qimage2ndarray

# import qdarkstyle
# import qtstylish

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QIcon, QPalette, QBrush, QCursor
from PyQt5.QtCore import pyqtSignal, Qt, QDir, pyqtSlot
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMessageBox, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import QTimer

from double_image_viewer import Ui_MainWindow

from colorama import init, Fore, Back, Style, Cursor

if "PYCHARM_HOSTED" in os.environ:
    convert = False
    strip = False
else:
    convert = None
    strip = None

init(convert=convert, strip=strip)

class PushButton(QtWidgets.QPushButton):

    def __init__(self, text, parent):
        super(PushButton, self).__init__(text, parent)
        # QtWidgets.QMenuBar.__init__(self)

        self.m_flag = False

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.parent().parent().parent().pos()  # 获取鼠标相对窗口的位置
            # event.accept()
            # self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

        # event.ignore()

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.m_flag:
            self.parent().parent().parent().move(event.globalPos() - self.m_Position)  # 更改窗口位置
            # event.accept()

        # event.ignore()

    def mouseReleaseEvent(self, event):
        self.m_flag = False
        # self.setCursor(QCursor(Qt.ArrowCursor))

        # event.ignore()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        ## 基本设置 ##
        # self.loadQss()
        self.setWindowIcon(QIcon("images\logo\logo.ico"))
        self.setWindowTitle('DoubleImageViewer')

        # 最大化 #
        # screen = QtWidgets.QDesktopWidget().screenGeometry()
        # self.resize(screen.width(), screen.height())
        # self.move(0, 0)

        self.setWindowFlags(Qt.CustomizeWindowHint)          # 有边框但无标题栏和按钮，不能移动和拖动
        # self.setWindowFlags(Qt.FramelessWindowHint)        # 窗体无边框
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)       # 窗体始终处于顶层位置

        # self.setAttribute(Qt.WA_TranslucentBackground)    # 设置背景透明

        ## 软件窗口操作 ##
        self.btn_close = QtWidgets.QPushButton("", self.menubar)
        self.btn_close.setObjectName("btn_close")
        self.btn_close.setStyleSheet("#btn_close{background:transparent}")
        self.btn_close.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.btn_close.setIcon(QIcon(QPixmap("./images/logo/close.png")))
        self.btn_close.clicked.connect(self.window_close)

        self.btn_max_rec = QtWidgets.QPushButton("", self.menubar)
        self.btn_max_rec.setObjectName("btn_max_rec")
        self.btn_max_rec.setStyleSheet("#btn_max_rec{background:transparent}")
        self.btn_max_rec.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.btn_max_rec.setIcon(QIcon(QPixmap("./images/logo/max_forward.png")))
        self.btn_max_rec.clicked.connect(self.window_max_or_recv)

        self.btn_min = QtWidgets.QPushButton("", self.menubar)
        self.btn_min.setObjectName("btn_min")
        self.btn_min.setStyleSheet("#btn_min{background:transparent}")
        self.btn_min.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.btn_min.setIcon(QIcon(QPixmap("./images/logo/min.png")))
        self.btn_min.clicked.connect(self.window_min)

        # self.btn_move = QtWidgets.QPushButton("", self.menubar)
        self.btn_move =PushButton("", self.menubar)
        self.btn_move.setObjectName("btn_move")
        self.btn_move.setStyleSheet("#btn_move{background:transparent;width:%d}" % (600))
        self.btn_move.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        self.groupBox_opera = QtWidgets.QGroupBox()
        self.groupBox_opera.setObjectName("groupBox_opera")
        self.groupBox_opera.setStyleSheet("#groupBox_opera{border:none}")

        self.h_layout = QtWidgets.QHBoxLayout()
        self.h_layout.addWidget(self.btn_move)
        self.h_layout.addWidget(self.btn_min)
        self.h_layout.addWidget(self.btn_max_rec)
        self.h_layout.addWidget(self.btn_close)  # 将控件添加到垂直布局中，最先添加的出现在最上方

        self.h_layout.setContentsMargins(0, 0, 0, 0)  # 设置外边距--(左边距离, 上边距离, 右边距离, 下边距离)
        self.h_layout.setSpacing(0)  # 设置内边距---各控件之间的距离

        self.groupBox_opera.setLayout(self.h_layout)
        self.menubar.setCornerWidget(self.groupBox_opera, Qt.TopRightCorner)

        ## 手动初始化 ##
        # self.label_left.setScaledContents(True)
        # self.label_right.setScaledContents(True)

        self.action_before.setEnabled(False)
        self.action_next.setEnabled(False)

        ## 信号与槽 ##
        # 切换图像
        self.action_before.triggered.connect(self.before_image)
        self.action_next.triggered.connect(self.next_image)

        # 打开图像文件夹
        self.action_left_from_folder.triggered.connect(self.open_folder_left)
        self.action_right_from_folder.triggered.connect(self.open_folder_right)

        # 打开图像文件
        self.action_left_from_file.triggered.connect(self.open_file_left)
        self.action_right_from_file.triggered.connect(self.open_file_right)

        # 打开图像csv
        self.action_left_from_csv.triggered.connect(self.open_csv_left)
        self.action_right_from_csv.triggered.connect(self.open_csv_right)

        # clicked listView
        self.listWidget_left.clicked.connect(self.list_view_left_click)
        self.listWidget_right.clicked.connect(self.list_view_right_click)

        # show/hide listView
        self.action_show_list.triggered.connect(self.show_list_view)
        self.action_hide_list.triggered.connect(self.hide_list_view)

        ## 其他成员变量 ##
        # 附加成员
        self.img_path_list_left = []
        self.img_path_list_right = []
        self.cur_index_left = 0
        self.cur_index_right = 0

    def loadQss(self):
        """加载QSS """
        file = r'qss/Combinear.qss'
        with open(file, 'rt', encoding='utf8') as f:
            styleSheet = f.read()
        self.setStyleSheet(styleSheet)
        f.close()

    ####################################################################################################################################
    def window_close(self):
        """
        关闭窗口
        :return:
        """
        self.close()

    def window_max_or_recv(self):
        """
        窗口最大化与恢复
        :return:
        """
        if self.isMaximized():
            self.showNormal()

            self.btn_max_rec.setStyleSheet("#btn_max_rec{background:transparent}")
            self.btn_max_rec.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
            self.btn_max_rec.setIcon(QIcon(QPixmap("./images/logo/max_forward.png")))

        else:
            self.showMaximized()
            self.setContentsMargins(0, 0, 0, 0)

            self.btn_max_rec.setStyleSheet("#btn_max_rec{background:transparent}")
            self.btn_max_rec.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
            self.btn_max_rec.setIcon(QIcon(QPixmap("./images/logo/max_back.png")))

    def window_min(self):
        """
        最小化窗口
        :return:
        """
        self.showMinimized()

    ####################################################################################################################################
    def open_file_left(self):

        file_path, _ = QFileDialog.getOpenFileName(self, 'Open file', './', 'Image files (*.jpg *.gif *.png *.jpeg *.mrxs *.bmp *.tif)')
        if file_path == '':
            self.action_before.setEnabled(False)
            self.action_next.setEnabled(False)

            self.img_path_list_left = []
            self.cur_index_left = 0
        else:
            self.img_path_list_left = [file_path]
            self.cur_index_left = 0

            ## 显示方法：Image ##
            # img_pil_left = Image.open(self.img_path_list_left[self.cur_index_left]).convert("RGB")
            # self.pixmap_left = img_pil_left.toqpixmap()
            # self.pixmap_left = self.pixmap_left.scaled(self.label_left.width(), self.label_left.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            # self.label_left.setPixmap(self.pixmap_left)

            ## 显示方法：Numpy ##
            # img_cv = cv2.imread(self.img_path_list_left[self.cur_index_left], cv2.IMREAD_COLOR)
            img_cv = cv2.imdecode(np.fromfile(self.img_path_list_left[self.cur_index_left], dtype=np.uint8), cv2.IMREAD_COLOR)
            self.qimage_left = qimage2ndarray.array2qimage(img_cv[:, :, ::-1])
            self.pixmap_left = QPixmap.fromImage(self.qimage_left)
            self.pixmap_left = self.pixmap_left.scaled(self.label_left.width(), self.label_left.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label_left.setPixmap(self.pixmap_left)

            ## 显示方法：路径 ##
            # self.label_left.setPixmap(QPixmap(self.img_path_list_left[self.cur_index_left]).scaled(self.label_left.width(), self.label_left.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

            ## 添加到liveView ##
            self.listWidget_left.clear()
            self.listWidget_left.addItems(self.img_path_list_left)

    def open_file_right(self):

        file_path, _ = QFileDialog.getOpenFileName(self, 'Open file', './', 'Image files (*.jpg *.gif *.png *.jpeg *.mrxs *.bmp *.tif)')
        if file_path == '':
            self.action_before.setEnabled(False)
            self.action_next.setEnabled(False)

            self.img_path_list_right = []
            self.cur_index_right = 0
        else:
            self.img_path_list_right = [file_path]
            self.cur_index_right = 0

            ## 显示方法：Image ##
            # img_pil_right = Image.open(self.img_path_list_right[self.cur_index_right]).convert("RGB")
            # self.pixmap_right = img_pil_right.toqpixmap()
            # self.pixmap_right = self.pixmap_right.scaled(self.label_right.width(), self.label_right.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            # self.label_right.setPixmap(self.pixmap_right)

            ## 显示方法：Numpy ##
            # img_cv = cv2.imread(self.img_path_list_right[self.cur_index_right], cv2.IMREAD_COLOR)
            img_cv = cv2.imdecode(np.fromfile(self.img_path_list_right[self.cur_index_right], dtype=np.uint8), cv2.IMREAD_COLOR)
            self.qimage_right = qimage2ndarray.array2qimage(img_cv[:, :, ::-1])
            self.pixmap_right = QPixmap.fromImage(self.qimage_right)
            self.pixmap_right = self.pixmap_right.scaled(self.label_right.width(), self.label_right.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label_right.setPixmap(self.pixmap_right)

            ## 显示方法：路径 ##
            # self.label_right.setPixmap(QPixmap(self.img_path_list_right[self.cur_index_right]).scaled(self.label_right.width(), self.label_right.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

            ## 添加到liveView ##
            self.listWidget_right.clear()
            self.listWidget_right.addItems(self.img_path_list_right)

    def open_folder_left(self):

        folder_dir = QFileDialog.getExistingDirectory(self, "load image set", "./")
        if folder_dir == '':
            self.action_before.setEnabled(False)
            self.action_next.setEnabled(False)

            self.img_path_list_left = []
            self.cur_index_left = 0
        else:

            self.img_path_list_left = [p.as_posix() for p in Path(folder_dir).iterdir() if p.suffix.lower() in [".jpg", ".gif", ".png", ".jpeg", ".mrxs", ".bmp", ".tif"]]
            print(Fore.BLUE + f"img_path_list_left: {self.img_path_list_left}" + Style.RESET_ALL)
            self.cur_index_left = 0

            ## 显示方法：Numpy ##
            # img_cv = cv2.imread(self.img_path_list_left[self.cur_index_left], cv2.IMREAD_COLOR)
            img_cv = cv2.imdecode(np.fromfile(self.img_path_list_left[self.cur_index_left], dtype=np.uint8), cv2.IMREAD_COLOR)
            self.qimage_left = qimage2ndarray.array2qimage(img_cv[:, :, ::-1])
            self.pixmap_left = QPixmap.fromImage(self.qimage_left)
            self.pixmap_left = self.pixmap_left.scaled(self.label_left.width(), self.label_left.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label_left.setPixmap(self.pixmap_left)

            ## 显示方法：路径 ##
            # self.label_left.setPixmap(QPixmap(self.img_path_list_left[self.cur_index_left]).scaled(self.label_left.width(), self.label_left.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

            ## 添加到liveView ##
            self.listWidget_left.clear()
            self.listWidget_left.addItems(self.img_path_list_left)

            ## 设置按钮状态 ##
            if len(self.img_path_list_left) != 0 and len(self.img_path_list_right) != 0:
                self.action_before.setEnabled(True)
                self.action_next.setEnabled(True)


    def open_folder_right(self):

        folder_dir = QFileDialog.getExistingDirectory(self, "load image set", "./")
        if folder_dir == '':
            self.action_before.setEnabled(False)
            self.action_next.setEnabled(False)

            self.img_path_list_right = []
            self.cur_index_right = 0
        else:

            self.img_path_list_right = [p.as_posix() for p in Path(folder_dir).iterdir() if p.suffix.lower() in [".jpg", ".gif", ".png", ".jpeg", ".mrxs", ".bmp", ".tif"]]
            print(Fore.BLUE + f"img_path_list_right: {self.img_path_list_right}" + Style.RESET_ALL)
            self.cur_index_right = 0

            ## 显示方法：Numpy ##
            # img_cv = cv2.imread(self.img_path_list_right[self.cur_index_right], cv2.IMREAD_COLOR)
            img_cv = cv2.imdecode(np.fromfile(self.img_path_list_right[self.cur_index_right], dtype=np.uint8), cv2.IMREAD_COLOR)
            self.qimage_right = qimage2ndarray.array2qimage(img_cv[:, :, ::-1])
            self.pixmap_rigth = QPixmap.fromImage(self.qimage_right)
            self.pixmap_right = self.pixmap_rigth.scaled(self.label_right.width(), self.label_right.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label_right.setPixmap(self.pixmap_right)

            ## 显示方法：路径 ##
            # self.label_right.setPixmap(QPixmap(self.img_path_list_right[self.cur_index_right]).scaled(self.label_right.width(), self.label_right.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

            ## 添加到liveView ##
            self.listWidget_right.clear()
            self.listWidget_right.addItems(self.img_path_list_right)

            ## 设置按钮状态 ##
            if len(self.img_path_list_left) != 0 and len(self.img_path_list_right) != 0:
                self.action_before.setEnabled(True)
                self.action_next.setEnabled(True)

    def open_csv_left(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open file', './', 'Image files (*.csv *.txt)')
        if file_path == '':
            self.action_before.setEnabled(False)
            self.action_next.setEnabled(False)

            self.img_path_list_left = []
            self.cur_index_left = 0
        else:
            with open(file_path, 'r') as file:
                self.img_path_list_left = [img_path.strip() for img_path in file.readlines()]
            self.cur_index_left = 0

            ## 显示方法：Image ##
            # img_pil_left = Image.open(self.img_path_list_left[self.cur_index_left]).convert("RGB")
            # self.pixmap_left = img_pil_left.toqpixmap()
            # self.pixmap_left = self.pixmap_left.scaled(self.label_left.width(), self.label_left.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            # self.label_left.setPixmap(self.pixmap_left)

            ## 显示方法：Numpy ##
            # img_cv = cv2.imread(self.img_path_list_left[self.cur_index_left], cv2.IMREAD_COLOR)
            img_cv = cv2.imdecode(np.fromfile(self.img_path_list_left[self.cur_index_left], dtype=np.uint8), cv2.IMREAD_COLOR)
            self.qimage_left = qimage2ndarray.array2qimage(img_cv[:, :, ::-1])
            self.pixmap_left = QPixmap.fromImage(self.qimage_left)
            self.pixmap_left = self.pixmap_left.scaled(self.label_left.width(), self.label_left.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label_left.setPixmap(self.pixmap_left)

            ## 显示方法：路径 ##
            # self.label_left.setPixmap(QPixmap(self.img_path_list_left[self.cur_index_left]).scaled(self.label_left.width(), self.label_left.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

            ## 添加到liveView ##
            self.listWidget_left.clear()
            self.listWidget_left.addItems(self.img_path_list_left)

            ## 设置按钮状态 ##
            if len(self.img_path_list_left) != 0 and len(self.img_path_list_right) != 0:
                self.action_before.setEnabled(True)
                self.action_next.setEnabled(True)


    def open_csv_right(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open file', './', 'Image files (*.csv *.txt)')
        if file_path == '':
            self.action_before.setEnabled(False)
            self.action_next.setEnabled(False)

            self.img_path_list_right = []
            self.cur_index_right = 0
        else:
            with open(file_path, 'r') as file:
                self.img_path_list_right = [img_path.strip() for img_path in file.readlines()]
            self.cur_index_right = 0

            ## 显示方法：Image ##
            # img_pil_right = Image.open(self.img_path_list_right[self.cur_index_right]).convert("RGB")
            # self.pixmap_right = img_pil_right.toqpixmap()
            # self.pixmap_right = self.pixmap_right.scaled(self.label_right.width(), self.label_right.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            # self.label_right.setPixmap(self.pixmap_right)

            ## 显示方法：Numpy ##
            # img_cv = cv2.imread(self.img_path_list_right[self.cur_index_right], cv2.IMREAD_COLOR)
            img_cv = cv2.imdecode(np.fromfile(self.img_path_list_right[self.cur_index_right], dtype=np.uint8), cv2.IMREAD_COLOR)
            self.qimage_right = qimage2ndarray.array2qimage(img_cv[:, :, ::-1])
            self.pixmap_right = QPixmap.fromImage(self.qimage_right)
            self.pixmap_right = self.pixmap_right.scaled(self.label_right.width(), self.label_right.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label_right.setPixmap(self.pixmap_right)

            ## 显示方法：路径 ##
            # self.label_right.setPixmap(QPixmap(self.img_path_list_right[self.cur_index_right]).scaled(self.label_right.width(), self.label_right.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

            ## 添加到liveView ##
            self.listWidget_right.clear()
            self.listWidget_right.addItems(self.img_path_list_right)

            ## 设置按钮状态 ##
            if len(self.img_path_list_left) != 0 and len(self.img_path_list_right) != 0:
                self.action_before.setEnabled(True)
                self.action_next.setEnabled(True)


    #######################################################################################################################
    def before_image(self):
        self.action_next.setEnabled(True)
        if self.cur_index_left == 0 or self.cur_index_right == 0:
            self.action_before.setEnabled(False)
            self.action_next.setEnabled(True)
        else:

            ##############################################################################################################################################
            ### 更新左边图像 ###
            self.cur_index_left = self.cur_index_left - 1
            print(Fore.CYAN + f"left: {self.img_path_list_left[self.cur_index_left]}" + Style.RESET_ALL)
            ## 显示方法：Numpy ##
            # img_cv = cv2.imread(self.img_path_list_left[self.cur_index_left], cv2.IMREAD_COLOR)
            img_cv = cv2.imdecode(np.fromfile(self.img_path_list_left[self.cur_index_left], dtype=np.uint8), cv2.IMREAD_COLOR)
            self.qimage_left = qimage2ndarray.array2qimage(img_cv[:, :, ::-1])
            self.pixmap_left = QPixmap.fromImage(self.qimage_left)
            self.pixmap_left = self.pixmap_left.scaled(self.label_left.width(), self.label_left.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label_left.setPixmap(self.pixmap_left)

            ## 显示方法：路径 ##
            # self.label_left.setPixmap(QPixmap(self.img_path_list_left[self.cur_index_left]).scaled(self.label_left.width(), self.label_left.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

            ## 高亮选择 ##
            item_cur = self.listWidget_left.item(self.cur_index_left)
            item_cur.setSelected(True)

            ##############################################################################################################################################
            ### 更新右边图像 ###
            self.cur_index_right = self.cur_index_right - 1
            print(Fore.CYAN + f"right: {self.img_path_list_right[self.cur_index_right]}" + Style.RESET_ALL)
            ## 显示方法：Numpy ##
            # img_cv = cv2.imread(self.img_path_list_right[self.cur_index_right], cv2.IMREAD_COLOR)
            img_cv = cv2.imdecode(np.fromfile(self.img_path_list_right[self.cur_index_right], dtype=np.uint8), cv2.IMREAD_COLOR)
            self.qimage_right = qimage2ndarray.array2qimage(img_cv[:, :, ::-1])
            self.pixmap_rigth = QPixmap.fromImage(self.qimage_right)
            self.pixmap_right = self.pixmap_rigth.scaled(self.label_right.width(), self.label_right.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label_right.setPixmap(self.pixmap_right)

            ## 显示方法：路径 ##
            # self.label_right.setPixmap(QPixmap(self.img_path_list_right[self.cur_index_right]).scaled(self.label_right.width(), self.label_right.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

            ## 高亮选择 ##
            item_cur = self.listWidget_right.item(self.cur_index_right)
            item_cur.setSelected(True)

    def next_image(self):
        self.action_before.setEnabled(True)
        if self.cur_index_left >= (len(self.img_path_list_left) - 1) or self.cur_index_right >= (len(self.img_path_list_right) - 1):
            self.action_before.setEnabled(True)
            self.action_next.setEnabled(False)
        else:

            ##############################################################################################################################################
            ### 更新左边图像 ###
            self.cur_index_left = self.cur_index_left + 1
            print(Fore.CYAN + f"left: {self.img_path_list_left[self.cur_index_left]}" + Style.RESET_ALL)
            ## 显示方法：Numpy ##
            # img_cv = cv2.imread(self.img_path_list_left[self.cur_index_left], cv2.IMREAD_COLOR)
            img_cv = cv2.imdecode(np.fromfile(self.img_path_list_left[self.cur_index_left], dtype=np.uint8), cv2.IMREAD_COLOR)
            self.qimage_left = qimage2ndarray.array2qimage(img_cv[:, :, ::-1])
            self.pixmap_left = QPixmap.fromImage(self.qimage_left)
            self.pixmap_left = self.pixmap_left.scaled(self.label_left.width(), self.label_left.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label_left.setPixmap(self.pixmap_left)

            ## 显示方法：路径 ##
            # self.label_left.setPixmap(QPixmap(self.img_path_list_left[self.cur_index_left]).scaled(self.label_left.width(), self.label_left.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

            ## 高亮选择 ##
            item_cur = self.listWidget_left.item(self.cur_index_left)
            item_cur.setSelected(True)

            ##############################################################################################################################################
            ### 更新右边图像 ###
            self.cur_index_right = self.cur_index_right + 1
            print(Fore.CYAN + f"right: {self.img_path_list_right[self.cur_index_right]}" + Style.RESET_ALL)
            ## 显示方法：Numpy ##
            # img_cv = cv2.imread(self.img_path_list_right[self.cur_index_right], cv2.IMREAD_COLOR)
            img_cv = cv2.imdecode(np.fromfile(self.img_path_list_right[self.cur_index_right], dtype=np.uint8), cv2.IMREAD_COLOR)
            self.qimage_right = qimage2ndarray.array2qimage(img_cv[:, :, ::-1])
            self.pixmap_rigth = QPixmap.fromImage(self.qimage_right)
            self.pixmap_right = self.pixmap_rigth.scaled(self.label_right.width(), self.label_right.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label_right.setPixmap(self.pixmap_right)

            ## 显示方法：路径 ##
            # self.label_right.setPixmap(QPixmap(self.img_path_list_right[self.cur_index_right]).scaled(self.label_right.width(), self.label_right.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

            ## 高亮选择 ##
            item_cur = self.listWidget_right.item(self.cur_index_right)
            item_cur.setSelected(True)

    #######################################################################################################################
    def list_view_left_click(self):
        """
        改变对应索引
        :return:
        """
        items = self.listWidget_left.selectedItems()
        item = items[0]
        item_text = item.text()

        self.cur_index_left = self.img_path_list_left.index(item_text)

        ## 显示方法：Numpy ##
        # img_cv = cv2.imread(self.img_path_list_left[self.cur_index_left], cv2.IMREAD_COLOR)
        img_cv = cv2.imdecode(np.fromfile(self.img_path_list_left[self.cur_index_left], dtype=np.uint8), cv2.IMREAD_COLOR)
        self.qimage_left = qimage2ndarray.array2qimage(img_cv[:, :, ::-1])
        self.pixmap_left = QPixmap.fromImage(self.qimage_left)
        self.pixmap_left = self.pixmap_left.scaled(self.label_left.width(), self.label_left.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label_left.setPixmap(self.pixmap_left)

        ## 显示方法：路径 ##
        # self.label_left.setPixmap(QPixmap(self.img_path_list_left[self.cur_index_left]).scaled(self.label_left.width(), self.label_left.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def list_view_right_click(self):
        """
        改变对应索引
        :return:
        """
        items = self.listWidget_right.selectedItems()
        item = items[0]
        item_text = item.text()

        self.cur_index_right = self.img_path_list_right.index(item_text)

        ## 显示方法：Numpy ##
        # img_cv = cv2.imread(self.img_path_list_right[self.cur_index_right], cv2.IMREAD_COLOR)
        img_cv = cv2.imdecode(np.fromfile(self.img_path_list_right[self.cur_index_right], dtype=np.uint8), cv2.IMREAD_COLOR)
        self.qimage_right = qimage2ndarray.array2qimage(img_cv[:, :, ::-1])
        self.pixmap_rigth = QPixmap.fromImage(self.qimage_right)
        self.pixmap_right = self.pixmap_rigth.scaled(self.label_right.width(), self.label_right.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label_right.setPixmap(self.pixmap_right)

        ## 显示方法：路径 ##
        # self.label_right.setPixmap(QPixmap(self.img_path_list_right[self.cur_index_right]).scaled(self.label_right.width(), self.label_right.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    #######################################################################################################################
    def show_list_view(self):
        # set stretch for main layout
        if self.horizontalLayout.__len__() == 4:
            self.horizontalLayout.setStretch(0, 1)
            self.horizontalLayout.setStretch(1, 2)
            self.horizontalLayout.setStretch(2, 2)
            self.horizontalLayout.setStretch(3, 1)
        elif self.horizontalLayout.__len__() == 2:
            self.horizontalLayout.setStretch(0, 2)
            self.horizontalLayout.setStretch(1, 2)

        width = self.width()
        height = self.height()

        ## show ##
        self.LeftImageList.show()
        self.RightImageList.show()

        ## 保证大小不变 ##
        self.resize(width, height)


    def hide_list_view(self):

        # set stretch for main layout
        if self.horizontalLayout.__len__() == 4:
            self.horizontalLayout.setStretch(0, 1)
            self.horizontalLayout.setStretch(1, 2)
            self.horizontalLayout.setStretch(2, 2)
            self.horizontalLayout.setStretch(3, 1)
        elif self.horizontalLayout.__len__() == 2:
            self.horizontalLayout.setStretch(0, 2)
            self.horizontalLayout.setStretch(1, 2)

        ## hide ##
        self.LeftImageList.hide()
        self.RightImageList.hide()

    #######################################################################################################################
    def tips(self):
        QMessageBox.information(self, "tips", self.tr("1)：load image\n2)：run\nor\n1): open folder that has some picture\n2): select picture\n3): run"))

    def about(self):
        QMessageBox.information(self, "help", self.tr("Copyright All Rights Reserved"))

    #######################################################################################################################
    @staticmethod
    def ndarray2qpixmap(img_c3_np, height, width):

        # if Image.isImageType(img_c3_np):
        #     img_c3_np = np.array(img_c3_np.convert("RGB"))

        ## 显示方法：Image ##
        # img_pil = Image.fromarray(img_c3_np)
        # qpixmap = img_pil.toqpixmap()
        # qpixmap_scaled = qpixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # return qpixmap_scaled

        ## 显示方法：Numpy ##
        qimage = qimage2ndarray.array2qimage(img_c3_np)
        qpixmap = QPixmap.fromImage(qimage)
        qpixmap_scaled = qpixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return qpixmap_scaled

    @staticmethod
    def resize_with_ratio_to_bounding_cv(img_cv, size=(512, 512)):
        """
        将原图bounding式缩放到指定尺寸；
        即给定bounding box大小，将图像等比例缩放后嵌入到bounding box中
        :param img_cv:
        :param size: size为tuple，可以长宽不同
        :return:
        """
        [h, w] = size
        hh, ww = img_cv.shape[0], img_cv.shape[1]
        scale = min(h / hh, w / ww)  # 指定高宽相同时，是按原图大的边进行缩放
        im_cv_new = cv2.resize(img_cv, (int(ww * scale), int(hh * scale)))
        return im_cv_new


# class MyQApplication(QApplication):
#     def __init__(self, param):
#         super(MyQApplication, self).__init__(param)
#
#     def notify(self, object, event):
#         if event.type() == QEvent.MouseButtonPress:
#             print('MyQApplication.notify')
#         return QApplication.notify(self, object, event)
#
#     def eventFilter(self, object, event):
#
#         if object == self.menubar:
#             print('MyQApplication.eventFilter')
#             if event.type() == QEvent.MouseButtonPress:
#                 if event.button() == Qt.LeftButton:
#                     self.m_flag = True
#                     self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
#                     event.accept()
#                     self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标
#             elif event.type() == QEvent.MouseMove:
#                 if event.button() == Qt.LeftButton:
#                     self.m_flag = True
#                     self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
#                     event.accept()
#                     self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标
#             elif event.type() == QEvent.MouseButtonRelease:
#                 self.m_flag = False
#                 self.setCursor(QCursor(Qt.ArrowCursor))
#
#         return QApplication.eventFilter(self, object, event)


if __name__ == '__main__':
    # multiprocessing.freeze_support()

    try:
        # app = MyQApplication(sys.argv)
        # app.installEventFilter(app)
        app = QtWidgets.QApplication(sys.argv)

        app.setWindowIcon(QIcon("images\logo\logo.ico"))

        window = MainWindow()
        # 设置样式表
        # app.setStyleSheet(qdarkstyle.load_stylesheet())
        # app.setStyleSheet(qtstylish.light())

        window.show()

        sys.exit(app.exec_())
    except Exception:
        print(traceback.print_exc())

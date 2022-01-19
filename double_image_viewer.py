# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'double_image_viewer.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(830, 604)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.LeftImageList = QtWidgets.QGroupBox(self.centralwidget)
        self.LeftImageList.setObjectName("LeftImageList")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.LeftImageList)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.listWidget_left = QtWidgets.QListWidget(self.LeftImageList)
        self.listWidget_left.setObjectName("listWidget_left")
        self.gridLayout_2.addWidget(self.listWidget_left, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.LeftImageList)
        self.label_left = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_left.sizePolicy().hasHeightForWidth())
        self.label_left.setSizePolicy(sizePolicy)
        self.label_left.setText("")
        self.label_left.setPixmap(QtGui.QPixmap(":/centerwidget/images/logo/logo_left.jpg"))
        self.label_left.setAlignment(QtCore.Qt.AlignCenter)
        self.label_left.setObjectName("label_left")
        self.horizontalLayout.addWidget(self.label_left)
        self.label_right = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_right.sizePolicy().hasHeightForWidth())
        self.label_right.setSizePolicy(sizePolicy)
        self.label_right.setText("")
        self.label_right.setPixmap(QtGui.QPixmap(":/centerwidget/images/logo/logo_right.jpg"))
        self.label_right.setAlignment(QtCore.Qt.AlignCenter)
        self.label_right.setObjectName("label_right")
        self.horizontalLayout.addWidget(self.label_right)
        self.RightImageList = QtWidgets.QGroupBox(self.centralwidget)
        self.RightImageList.setObjectName("RightImageList")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.RightImageList)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.listWidget_right = QtWidgets.QListWidget(self.RightImageList)
        self.listWidget_right.setObjectName("listWidget_right")
        self.gridLayout_3.addWidget(self.listWidget_right, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.RightImageList)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 2)
        self.horizontalLayout.setStretch(3, 1)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 830, 23))
        self.menubar.setObjectName("menubar")
        self.menuloadImage = QtWidgets.QMenu(self.menubar)
        self.menuloadImage.setObjectName("menuloadImage")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuabout = QtWidgets.QMenu(self.menubar)
        self.menuabout.setObjectName("menuabout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action_show_list = QtWidgets.QAction(MainWindow)
        self.action_show_list.setObjectName("action_show_list")
        self.action_hide_list = QtWidgets.QAction(MainWindow)
        self.action_hide_list.setObjectName("action_hide_list")
        self.action_left_from_folder = QtWidgets.QAction(MainWindow)
        self.action_left_from_folder.setObjectName("action_left_from_folder")
        self.action_right_from_folder = QtWidgets.QAction(MainWindow)
        self.action_right_from_folder.setObjectName("action_right_from_folder")
        self.action_before = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/toolbar/images/logo/before_image.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_before.setIcon(icon)
        self.action_before.setObjectName("action_before")
        self.action_next = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/toolbar/images/logo/next_image.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_next.setIcon(icon1)
        self.action_next.setObjectName("action_next")
        self.action_about = QtWidgets.QAction(MainWindow)
        self.action_about.setObjectName("action_about")
        self.action_tips = QtWidgets.QAction(MainWindow)
        self.action_tips.setObjectName("action_tips")
        self.action_left_from_file = QtWidgets.QAction(MainWindow)
        self.action_left_from_file.setObjectName("action_left_from_file")
        self.action_right_from_file = QtWidgets.QAction(MainWindow)
        self.action_right_from_file.setObjectName("action_right_from_file")
        self.action_left_from_csv = QtWidgets.QAction(MainWindow)
        self.action_left_from_csv.setObjectName("action_left_from_csv")
        self.action_right_from_csv = QtWidgets.QAction(MainWindow)
        self.action_right_from_csv.setObjectName("action_right_from_csv")
        self.menuloadImage.addAction(self.action_left_from_file)
        self.menuloadImage.addAction(self.action_right_from_file)
        self.menuloadImage.addSeparator()
        self.menuloadImage.addAction(self.action_left_from_folder)
        self.menuloadImage.addAction(self.action_right_from_folder)
        self.menuloadImage.addSeparator()
        self.menuloadImage.addAction(self.action_left_from_csv)
        self.menuloadImage.addAction(self.action_right_from_csv)
        self.menuView.addAction(self.action_show_list)
        self.menuView.addAction(self.action_hide_list)
        self.menuView.addSeparator()
        self.menuabout.addAction(self.action_tips)
        self.menuabout.addAction(self.action_about)
        self.menubar.addAction(self.menuloadImage.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuabout.menuAction())
        self.toolBar.addAction(self.action_before)
        self.toolBar.addAction(self.action_next)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.LeftImageList.setTitle(_translate("MainWindow", "LeftImageList"))
        self.RightImageList.setTitle(_translate("MainWindow", "RightImageList"))
        self.menuloadImage.setTitle(_translate("MainWindow", "Load"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuabout.setTitle(_translate("MainWindow", "Help"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.action_show_list.setText(_translate("MainWindow", "show list"))
        self.action_hide_list.setText(_translate("MainWindow", "hide list"))
        self.action_left_from_folder.setText(_translate("MainWindow", "left from folder"))
        self.action_right_from_folder.setText(_translate("MainWindow", "right from folder"))
        self.action_before.setText(_translate("MainWindow", "before"))
        self.action_before.setShortcut(_translate("MainWindow", "Left"))
        self.action_next.setText(_translate("MainWindow", "next"))
        self.action_next.setShortcut(_translate("MainWindow", "Right"))
        self.action_about.setText(_translate("MainWindow", "about"))
        self.action_tips.setText(_translate("MainWindow", "tips"))
        self.action_left_from_file.setText(_translate("MainWindow", "left from file"))
        self.action_right_from_file.setText(_translate("MainWindow", "right from file"))
        self.action_left_from_csv.setText(_translate("MainWindow", "left from csv"))
        self.action_right_from_csv.setText(_translate("MainWindow", "right from csv"))
import double_image_viewer_rc
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QMainWindow, QLineEdit, QTextEdit, QLabel,
                             QAction, QFileDialog, QApplication, QPushButton, QInputDialog)
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui
import imageio
import os
from random import randint


class Editor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.statusBar()

        self.images = []
        self.path_to_add = '/home'
        self.path_to_save = '/home'
        addFile = QAction(QIcon('open.png'), 'Add', self)
        addFile.setShortcut('Ctrl+O')
        addFile.setStatusTip('Add frame')
        addFile.triggered.connect(self.add)
        self.btn = QPushButton('Save...', self)
        self.btn.resize(80, 25)
        self.btn.move(15, 460)
        self.btn.clicked.connect(self.save)

        self.btn_c = QPushButton('Clean', self)
        self.btn_c.resize(80, 25)
        self.btn_c.move(15, 420)
        self.btn_c.clicked.connect(self.clean)

        self.btn_c = QPushButton('Add...', self)
        self.btn_c.resize(80, 25)
        self.btn_c.move(15, 380)
        self.btn_c.clicked.connect(self.add)


        saveFile = QAction(QIcon('save.png'), 'Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save GIF')
        saveFile.triggered.connect(self.save)
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('&Add')
        fileMenu.addAction(addFile)
        fileMenu = menubar.addMenu('&Save')
        fileMenu.addAction(saveFile)

        self.t1 = QLabel(self)
        self.t1.setText("Duration time:")
        self.t1.move(15, 290)

        self.duration_input = QLineEdit(self)
        self.duration_input.move(15, 330)
        self.duration_input.setText('0.1')

        self.setGeometry(300, 300, 700, 500)
        self.setWindowTitle('GIF-editor')
        pal = self.palette()

        # установка цвета (3) для фона (2) состояний Normal и Inactive (1)
        pal.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Background, QtGui.QColor("#FFF8E7"))
        pal.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Background, QtGui.QColor("#FFEBCD"))
        self.setPalette(pal)
        self.show()

    def clean(self):
        self.images = []

    def add(self):
        name = False
        name = QFileDialog.getOpenFileName(self, 'Choose file', self.path_to_add)[0]
        if name:
            if name.endswith(('.jpeg', '.png', '.gif', '.jpg')):
                self.images.append(name)
                self.path_to_add = name
            print(self.images)

    def save(self):
        path = False
        path = QFileDialog.getExistingDirectory(self, 'Choose directory', self.path_to_save)
        if path:
            i, okBtnPressed = QInputDialog.getText(
                self, "Write name", "Save"
            )
            if okBtnPressed:
                if len(i) >= 4:
                    if i[-4:] == '.gif':
                        i = i[0:-4]
                if i == '':
                    i = 'image' + str(randint(10000000, 99999999))
                path += '/' + i + '.gif'
            print(path)
            self.work(path)

    def work(self, path):
        try:
            images = list(map(lambda filename: imageio.imread(filename), self.images))
            imageio.mimsave(path, images, duration=float(self.duration_input.text()))
        except Exception as er:
            print(er)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Editor()
    sys.exit(app.exec_())

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
    QAction, QFileDialog, QApplication, QPushButton, QInputDialog)
from PyQt5.QtGui import QIcon
import imageio
import os
from random import randint


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        self.statusBar()

        self.images = []
        addFile = QAction(QIcon('open.png'), 'Add', self)
        addFile.setShortcut('Ctrl+O')
        addFile.setStatusTip('Add frame')
        addFile.triggered.connect(self.add)
        self.btn = QPushButton('Save...', self)
        self.btn.resize(80, 35)
        self.btn.move(550, 450)

        self.btn.clicked.connect(self.save)

        saveFile = QAction(QIcon('save.png'), 'Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save GIF')
        saveFile.triggered.connect(self.save)
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('&Add')
        fileMenu.addAction(addFile)
        fileMenu = menubar.addMenu('&Save')
        fileMenu.addAction(saveFile)

        self.setGeometry(300, 300, 700, 500)
        self.setWindowTitle('GIF-editor')
        self.show()


    def add(self):
        name = False
        name = QFileDialog.getOpenFileName(self, 'Choose file', '/home')[0]
        if name:
            if name.endswith(('.jpeg', '.png', '.gif')):
                self.images.append(name)
            print(self.images)

    def save(self):
        path = False
        path = QFileDialog.getExistingDirectory(self, 'Choose directory', '/home')
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
            imageio.mimsave(path, images, duration=0.1)
        except Exception as er:
            print(er)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
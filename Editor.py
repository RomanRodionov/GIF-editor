#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QListWidget, QListWidgetItem, QComboBox, QMainWindow, QLineEdit,
                             QLabel, QAction, QFileDialog, QApplication, QPushButton, QInputDialog)
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QSize
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

        self.quality = 256
        self.gif_palette = QComboBox(self)
        self.gif_palette.addItems(["256", "128",
                                   "64", "32", "16"])

        self.gif_palette.move(15, 250)
        self.gif_palette.resize(80, 25)

        self.gif_palette.activated[str].connect(self.ch_pal)
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

        self.btn_a = QPushButton('Add...', self)
        self.btn_a.resize(80, 25)
        self.btn_a.move(15, 380)
        self.btn_a.clicked.connect(self.add)

        self.btn_r = QPushButton('Delete', self)
        self.btn_r.resize(80, 25)
        self.btn_r.move(15, 180)
        self.btn_r.clicked.connect(self.delete)

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

        self.t2 = QLabel(self)
        self.t2.setText("Pallet size:")
        self.t2.move(15, 210)

        self.duration_input = QLineEdit(self)
        self.duration_input.move(15, 330)
        self.duration_input.resize(80, 25)
        self.duration_input.setText('0.1')

        self.setGeometry(300, 300, 700, 500)
        self.setWindowTitle('GIF-editor')

        # работа со списком изображений
        self.lst = QListWidget(self)
        self.lst.move(150, 40)
        self.lst.resize(300, 450)
        self.lst.setIconSize(QSize(90, 90))

        pal = self.palette()

        pal.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Background, QtGui.QColor("#FFEBCD"))
        pal.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Background, QtGui.QColor("#FFF8E7"))
        self.setPalette(pal)
        self.show()

    def get_lst(self):
        items = []
        for index in range(self.lst.count()):
            items.append(self.lst.item(index).text())
        return items

    def ch_pal(self, text):
        self.quality = int(text)

    def clean(self):
        self.lst.clear()

    def delete(self):
        listItems = self.lst.selectedItems()
        if not listItems:
            return
        for item in listItems:
            self.lst.takeItem(self.lst.row(item))

    def add(self):
        name = False
        name = QFileDialog.getOpenFileName(self, 'Choose file', self.path_to_add)[0]
        if name:
            if name.endswith(('.jpeg', '.png', '.gif', '.jpg')):
                item = QListWidgetItem(name)
                item.setIcon(QIcon(name))
                self.lst.addItem(item)
                self.path_to_add = name

    def save(self):
        path = False
        path = QFileDialog.getExistingDirectory(self, 'Choose directory', self.path_to_save)
        if path:
            self.path_to_save = path
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
            images = list(map(lambda filename: imageio.imread(filename), self.get_lst()))
            imageio.mimsave(path, images, palettesize=self.quality, duration=float(self.duration_input.text()))
        except Exception as er:
            print(er)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Editor()
    sys.exit(app.exec_())

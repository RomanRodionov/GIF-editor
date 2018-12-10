#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QSlider, QWidget, QTabWidget, QListWidget, QListWidgetItem, QComboBox, QMainWindow,
                             QLineEdit, QLabel, QAction, QFileDialog, QApplication, QPushButton, QInputDialog,
                             QVBoxLayout, QSizePolicy)
from PyQt5.QtGui import QIcon, QMovie
from PyQt5.QtCore import QByteArray, Qt
from PyQt5.Qt import QSize
from PyQt5 import QtCore, QtGui
from PIL import Image
import imageio
from random import randint


#Код класс GifPlayer, который создает и проигрывает гиф-изображение
class GifPlayer(QWidget):
    def __init__(self, name, parent=None):
        QWidget.__init__(self, parent)

        self.movie = QMovie(name, QByteArray(), self)
        size = self.movie.scaledSize()
        print(size)
        self.setGeometry(0, 0, size.width(), size.height())
        self.im = Image.open(name).size
        self.movie_screen = QLabel()
        self.movie_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.movie_screen.setAlignment(Qt.AlignCenter)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.movie_screen)
        self.setLayout(main_layout)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie_screen.setMovie(self.movie)
        self.movie.start()
        self.movie.loopCount()

        self.btn_s = QPushButton('Scale', self)
        self.btn_s.resize(80, 25)
        self.btn_s.move(0, 460)
        self.btn_s.clicked.connect(self.resizeGIF)
        self.btn_s.setStyleSheet("""
    QPushButton:hover { background-color: red; color: white }
    QPushButton:!hover { background-color: rgb(105, 105, 105); color: white }
    QPushButton:pressed { background-color: rgb(205, 92, 92); color: white }
""")
    #Этот метод меняет разрешение гиф-анимации в окне result
    def resizeGIF(self):
        try:
            rect = self.geometry()
            w = rect.width()
            h = rect.height()
            w1, h1 = self.im
            print(w, h, w1, h1)
            if w > 20 and h > 20:
                w -= 20
                h -= 20
            k = h1 / h
            w = w1 / k
            size = QtCore.QSize(int(w), h)

            movie = self.movie_screen.movie()
            movie.setScaledSize(size)
        except Exception as er:
            print(er)

# Код класса оконного приложения
class Editor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.statusBar()

        self.quality = 256
        self.gif_palette = QComboBox(self)
        self.gif_palette.addItems(["256", "128",
                                   "64", "32", "16", "8", "4", "2"])

        self.gif_palette.move(15, 250)
        self.gif_palette.resize(80, 25)
        self.gif_palette.setStyleSheet("""
    QComboBox:hover { background-color: red; color: white }
    QComboBox:!hover { background-color: rgb(105, 105, 105); color: white }
    QComboBox:pressed { background-color: rgb(205, 92, 92); color: white }
""")

        self.gif_palette.activated[str].connect(self.ch_pal)
        self.path_to_add = '/home'
        self.path_to_save = '/home'

        addFile = QAction(QIcon('open.png'), 'Add', self)
        addFile.setShortcut('Ctrl+O')
        addFile.setStatusTip('Add frame')
        addFile.triggered.connect(self.add)

#Кнопки для работы с программой
        self.btn = QPushButton('Save...', self)
        self.btn.resize(80, 25)
        self.btn.move(15, 460)
        self.btn.clicked.connect(self.save)

        self.btn_cl = QPushButton('Clean', self)
        self.btn_cl.resize(80, 25)
        self.btn_cl.move(15, 420)
        self.btn_cl.clicked.connect(self.clean)

        self.btn_a = QPushButton('Add...', self)
        self.btn_a.resize(80, 25)
        self.btn_a.move(15, 380)
        self.btn_a.clicked.connect(self.add)

        self.btn_d = QPushButton('Delete', self)
        self.btn_d.resize(80, 25)
        self.btn_d.move(15, 60)
        self.btn_d.clicked.connect(self.delete)

        self.btn_r = QPushButton('Remove', self)
        self.btn_r.resize(80, 25)
        self.btn_r.move(15, 100)
        self.btn_r.clicked.connect(self.remove)

        self.btn_c = QPushButton('Copy', self)
        self.btn_c.resize(80, 25)
        self.btn_c.move(15, 140)
        self.btn_c.clicked.connect(self.copy)

        self.btn_p = QPushButton('Paste', self)
        self.btn_p.resize(80, 25)
        self.btn_p.move(15, 180)
        self.btn_p.clicked.connect(self.paste)

        for button in [self.btn, self.btn_a, self.btn_c, self.btn_cl, self.btn_d, self.btn_p, self.btn_r, self.btn]:
            button.setStyleSheet("""
    QPushButton:hover { background-color: red; color: white }
    QPushButton:!hover { background-color: rgb(105, 105, 105); color: white }
    QPushButton:pressed { background-color: rgb(205, 92, 92); color: white }
""")

        saveFile = QAction(QIcon('save.png'), 'Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save GIF')
        saveFile.triggered.connect(self.save)
        menubar = self.menuBar()
        self.setStyleSheet("""
                QMenuBar {
                    background-color: rgb(49,49,49);
                    color: rgb(255,255,255);
                    border: 1px solid #000;
                }

                QMenuBar::item {
                    background-color: rgb(49,49,49);
                    color: rgb(255,255,255);
                }

                QMenuBar::item::selected {
                    background-color: rgb(30,30,30);
                }

                QMenu {
                    background-color: rgb(49,49,49);
                    color: rgb(255,255,255);
                    border: 1px solid #000;           
                }

                QMenu::item::selected {
                    background-color: rgb(30,30,30);
                }
            """)

        fileMenu = menubar.addMenu('&Add')
        fileMenu.addAction(addFile)
        fileMenu = menubar.addMenu('&Save')
        fileMenu.addAction(saveFile)

        self.t1 = QLabel(self)
        self.t1.setText("Duration time:")
        self.t1.move(15, 290)
        self.t1.setStyleSheet("""
    QLabel { color: white }
""")

        self.t2 = QLabel(self)
        self.t2.setText("Pallet size:")
        self.t2.move(15, 210)
        self.t2.setStyleSheet("""
            QLabel { color: white }
        """)

        self.duration_input = QLineEdit(self)
        self.duration_input.move(15, 330)
        self.duration_input.resize(80, 25)
        self.duration_input.setText('0.1')
        self.duration_input.setStyleSheet("""
    QLineEdit:hover { background-color: red; color: white }
    QLineEdit:!hover { background-color: rgb(105, 105, 105); color: white }
""")

        self.setGeometry(300, 300, 810, 575)
        self.setWindowTitle('GIF-editor')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        pal = self.palette()
        pal.setBrush(QtGui.QPalette.Normal, QtGui.QPalette.Background,
                     QtGui.QBrush(QtGui.QPixmap("bg.png")))
        self.setPalette(pal)
        # Ссылка на изображение: https://wallscloud.net/wallpaper/textures/Siniy-Fon/qLj7

        # работа со списком изображений
        self.lst = QListWidget(self)
        self.lst.move(150, 40)
        self.lst.resize(400, 450)
        self.lst.setIconSize(QSize(90, 90))

        pal = self.palette()

        self.buffer = []

        #pal.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Background, QtGui.QColor("#778899"))
        #pal.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Background, QtGui.QColor("#778899"))
        #self.setPalette(pal)

        # tabwidget
        _translate = QtCore.QCoreApplication.translate
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(120, 25, 670, 510))
        self.tabWidget.setStyleSheet(" background-color: rgb(233, 233, 233) ")
        self.tabWidget.addTab(self.lst, "")

        self.res_display = GifPlayer('ex.gif')
        self.tabWidget.addTab(self.res_display, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.lst), _translate("Form", "Frames"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.res_display), _translate("Form", "Result"))

        # Масштабирование
        self.slider = QSlider(QtCore.Qt.Horizontal, self)
        self.slider.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setValue(20)
        self.slider.move(700, 540)
        self.slider.valueChanged.connect(self.change_slider)

        self.show()

    # Изменение размера иконок во вкладке Frames
    def change_slider(self):
        value = self.slider.value() * 6
        self.lst.setIconSize(QSize(value, value))

    # Функция сохранения фрэйма в буфер обмена
    def copy(self):
        listItems = self.lst.selectedItems()
        if not listItems:
            return
        self.buffer = []
        for item in listItems:
            self.buffer.append(self.lst.item(self.lst.row(item)).clone())

    # Функция вставки фрэйма из буфера обмена
    def paste(self):
        try:
            ch_item = self.lst.selectedItems()[0]
            if self.buffer:
                for item in self.buffer:
                    self.lst.insertItem(self.lst.row(ch_item), item.clone())
        except Exception as a:
            print(a)

    # Функция удаления фрэйма из вкладки Frames и сохранения его в буфер обмена
    def remove(self):
        self.copy()
        self.delete()

    # Получение списка адресов фрэймов из вкладки Frames
    def get_lst(self):
        items = []
        for index in range(self.lst.count()):
            items.append(self.lst.item(index).text())
        return items

    # Изменение количества цветов в палитре гиф-изображения
    def ch_pal(self, text):
        self.quality = int(text)

    # Функция удаления всех фреймов из вкладки Frames
    def clean(self):
        self.lst.clear()

    # Функция удаления фрэйма
    def delete(self):
        listItems = self.lst.selectedItems()
        if not listItems:
            return
        for item in listItems:
            self.lst.takeItem(self.lst.row(item))

    # Функция добавления фрэйма во вкладку Frames
    def add(self):
        name = False
        name = QFileDialog.getOpenFileName(self, 'Choose file', self.path_to_add)[0]
        if name:
            if name.endswith(('.jpeg', '.png', '.gif', '.jpg')):
                item = QListWidgetItem(name)
                item.setIcon(QIcon(name))
                self.lst.addItem(item)
                self.path_to_add = name

    # Функция создания гиф-файла и сохранения в директории
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

            _translate = QtCore.QCoreApplication.translate
            self.work(path)
            self.tabWidget.removeTab(1)
            self.res_display = GifPlayer(path)
            self.tabWidget.addTab(self.res_display, "")
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.lst), _translate("Form", "Frames"))
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.res_display), _translate("Form", "Result"))


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

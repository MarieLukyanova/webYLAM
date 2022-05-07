import os
import sys
import json


import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit


SCREEN_SIZE = [600, 610]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.x, self.y = 37.6200, 55.7536
        self.z = 10
        self.type = 'map'
        self.metka = ''
        self.getImage()
        self.initUI()

    def getImage(self):
        map_request =f"https://static-maps.yandex.ru/1.x/?ll={self.x},{self.y}{self.metka}&size=600,450&z={self.z}&l={self.type}"
        response = requests.get(map_request)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(600, 250, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.btn = QPushButton('Добавить координаты', self)
        self.btn.move(70, 500)
        self.btn.resize(140, 30)
        self.btn.clicked.connect(self.getcoord)
        self.btn_type = QPushButton('Схема', self)
        self.btn_type.move(70, 550)
        self.btn_type.clicked.connect(self.map_layer)
        self.edit_x = QLineEdit(self)
        self.edit_x.move(10, 470)
        self.edit_y = QLineEdit(self)
        self.edit_y.move(160, 470)
        self.edit_adress = QLineEdit(self)
        self.edit_adress.move(325, 470)
        self.edit_adress.resize(250, 24)
        self.btn_adress = QPushButton('Искать', self)
        self.btn_adress.move(400, 500)
        self.btn_adress.clicked.connect(self.search)
        self.btn_back = QPushButton('Сбросить', self)
        self.btn_back.move(400, 580)
        self.btn_back.clicked.connect(self.throw_off)
        self.adress = QLineEdit(self)
        self.adress.move(250, 547)
        self.adress.resize(345, 24)
        self.adress.setReadOnly(True)
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def getcoord(self):
        self.x, self.y = self.edit_x.text(), self.edit_y.text()
        self.edit_adress.clear()
        self.adress.clear()
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def map_layer(self):
        if self.type == 'map':
            self.type = 'sat'
            self.btn_type.setText('Спутник')
        elif self.type == 'sat':
            self.type = 'skl'
            self.btn_type.setText('Гибрид')
        else:
            self.type = 'map'
            self.btn_type.setText('Схема')
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def search(self):
        adress = '+'.join(self.edit_adress.text().split())
        response = requests.get(
            f'https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={adress}&format=json')
        if response:
            jj = json.loads(response.content.decode())
            self.x = jj['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()[0]
            self.y = jj['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()[1]
            adress = jj['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
            self.z = 13
            self.metka = '&pt=' + str(self.x) + ',' + str(self.y)
        else:
            print('Ошибка запроса: ')
            print(response)
            print('HHTP статус: ', response.status_code, "(", response.reason, ')')
            sys.exit(0)
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)
        self.adress.setText(adress)

    def throw_off(self):
        self.x, self.y = 37.6200, 55.7536
        self.metka = ''
        self.edit_adress.clear()
        self.adress.clear()
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        if event.key() == 16777235:
            if self.z != 17:
                self.z += 1
            self.getImage()
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)
        if event.key() == 16777237:
            if self.z != 0:
                self.z -= 1
            self.getImage()
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)
        if event.key() == Qt.Key_A:
            self.x += 0.01
            self.getImage()
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)
        if event.key() == Qt.Key_D:
            self.x -= 0.01
            self.getImage()
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)
        if event.key() == Qt.Key_W:
            self.y -= 0.01
            self.getImage()
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)
        if event.key() == Qt.Key_S:
            self.y += 0.01
            self.getImage()
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())

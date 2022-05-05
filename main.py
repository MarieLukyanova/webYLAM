import os
import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit


SCREEN_SIZE = [450, 600]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.x, self.y = 37.620070, 55.753630
        self.z = 13
        self.getImage()
        self.initUI()

    def getImage(self):
        map_request = f"https://static-maps.yandex.ru/1.x/?ll={self.x},{self.y}&size=450,450&z={self.z}&l=map"
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
        self.edit_x = QLineEdit(self)
        self.edit_x.move(10, 470)
        self.edit_y = QLineEdit(self)
        self.edit_y.move(160, 470)
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(450, 450)
        self.image.setPixmap(self.pixmap)

    def getcoord(self):
        self.x, self.y = self.edit_x.text(), self.edit_y.text()
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
        if event.key() == 16777234:
            self.x -= 0.01
            self.getImage()
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)
        if event.key() == 16777236:
            self.x += 0.01
            self.getImage()
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)
        if event.key() == Qt.Key_S:
            #Up - Ctrl
            self.y += 0.01
            self.getImage()
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)
        if event.key() == Qt.Key_D:
            #Down - Shift
            self.y -= 0.01
            self.getImage()
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
import sys
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QMainWindow

class SimMoveDemo(QMainWindow):

    def __init__(self, brojIgraca, lvlNumber):
        super().__init__()

        oImage = QImage("images\\background.png")
        sImage = oImage.scaled(QSize(1000, 562))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))  # 10 = Windowrole
        self.setPalette(palette)

        self.pix1 = QPixmap('images\\sml')
        self.pix11 = QPixmap('images\\smr')
        self.pix12 = QPixmap('images\\lml')
        self.pix112 = QPixmap('images\\lmr')
        self.pix2 = QPixmap('images\\p')

        self.pix4 = QPixmap('images\\Ladders.png')
        self.pix5 = QPixmap('images\\Ladders.png')
        self.pix6 = QPixmap('images\\Ladders.png')
        self.pix7 = QPixmap('images\\Ladders.png')
        self.pix3 = QPixmap('images\\gl')
        self.pixBottleR = QPixmap('images\\barrelR.png')
        self.pixBottleL = QPixmap('images\\barrel.png')
        self.pix32 = QPixmap('images\\gr')

        self.left = 400
        self.top = 200
        self.width = 1000
        self.height = 562

        self.__init_ui__()

    def __init_ui__(self):
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.show()

if __name__ == '__main__':
     app = QApplication(sys.argv)
     ex = SimMoveDemo(1, 1)
     sys.exit(app.exec_())
import sys
from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont, QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QPushButton


class GameOver(QMainWindow):

    def __init__(self, br, sc):
        super().__init__()

        oImage = QImage("images\\over.jpg")
        self.label = QLabel(self)
        self.rezz = QLabel(self)
        self.who_is_winner = QLabel(self)
        self.who_is_winner1 = QPixmap('images\\player1-wins.png')
        self.who_is_winner2 = QPixmap('images\\player2-wins.png')
        self.left = 400
        self.top = 200
        self.width = 450
        self.height = 470
        self.score = sc
        palette = QPalette()
        sImage = oImage.scaled(QSize(450, 470))
        palette.setBrush(10, QBrush(sImage))  # 10 = Windowrole
        self.setPalette(palette)

        self.__init_ui__(br)

    def __init_ui__(self, br):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QtGui.QIcon('images\\smr'))
        #self.setWindowState(Qt.WindowFullScreen)

        self.setWindowTitle("Game Over")
        """if(br == 0):
            palette = QPalette()
            oImage = QImage("images\\over.jpg")
            sImage = oImage.scaled(QSize(450, 470))
            palette.setBrush(10, QBrush(sImage))  # 10 = Windowrole
            self.setPalette(palette)
            self.rezz.setText('Score: ' + str(self.score))
            font = QtGui.QFont()
            font.setPointSize(20)
            #self.rezz.setFont(font)
            #self.rezz.setGeometry(250, 350, 300, 100)
            #self.show()"""
        if(br==1):
            self.who_is_winner.setPixmap(self.who_is_winner1)
            self.who_is_winner.setGeometry(35, 250, 395, 43)
        else:
            self.who_is_winner.setPixmap(self.who_is_winner2)
            self.who_is_winner.setGeometry(35, 250, 395, 43)

        button4 = QPushButton('QUIT', self)
        button4.resize(200, 30)
        button4.move(135, 316)

        button4.clicked.connect(self.quit_on_click)
        self.show()

    def quit_on_click(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameOver(1, 1)
    sys.exit(app.exec_())
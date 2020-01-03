import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QMainWindow
from GorilaMovement import GorilaMovement
from JasminMovement import JasminMovement
from pomocniFajl import isHit, generateBarrel, GorilaFreezeProcess
from multiprocessing import Queue, Process
from BarrelMovement import BarrelMovement
from random import randint
from key_notifier import KeyNotifier
from key_notifier2 import KeyNotifier2

brLevel = 0

class SimMoveDemo(QMainWindow):

    def __init__(self, brojIgraca, lvlNumber):
        super().__init__()

        oImage = QImage("images\\back")
        sImage = oImage.scaled(QSize(1000, 562))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))  # 10 = Windowrole
        self.setPalette(palette)

        self.pix1 = QPixmap('images\\sml')
        self.pix11 = QPixmap('images\\smr')
        self.pix12 = QPixmap('images\\lml')
        self.pix112 = QPixmap('images\\lmr')
        self.pix2 = QPixmap('images\\jasmin')
        self.pix22 = QPixmap('images\\pll')

        self.pix3 = QPixmap('images\\gl')

        self.pix32 = QPixmap('images\\gr')
        self.izadji = QPixmap('images\\quit')
        self.pix4 = QPixmap('images\\barell')

        self.hitSide = False

        self.label2 = QLabel(self)
        self.label4 = QLabel(self)
        self.label3 = QLabel(self)
        self.label30 = QLabel(self)

        self.labelLifes1 = QLabel(self)
        self.labelLifes2 = QLabel(self)
        self.life1ispis = QLabel(self)
        self.life2ispis = QLabel(self)
        self.label1 = QLabel(self)
        self.label11 = QLabel(self)
        self.one = None

        self.labelLevel = QLabel(self)
        self.ispisLabel1 = QLabel(self)
        self.playerRez1 = QLabel(self)
        self.playerRez11 = QLabel(self)
        self.playerRez2 = QLabel(self)
        self.playerRez22 = QLabel(self)
        self.gameoverLab = QLabel(self)
        self.izlazIzIgre = QLabel(self)

        self.barrelQueue = Queue()
        self.barrelProcess = Process(target=generateBarrel, args=[self.barrelQueue])
        self.barrels = []
        self.barrelProcess.start()
        self.gorilaStop = Queue()
        self.gorilaStart = Queue()
        self.gorilaBug = Process(target=GorilaFreezeProcess, args=[self.gorilaStart, self.gorilaStop])
        self.gorilaBug.start()

        self.zaustavio = False

        self.prvi = False
        self.drugi = False

        self.prviSprat = False

        self.poeniPL1 = 0
        self.poeniPL2 = 0
        self.trenutniNivo = lvlNumber

        self.ispisLabel1.setText('Level: ')
        self.ispisLabel1.setStyleSheet('color: blue')

        self.playerRez1.setText('P1: ')
        self.playerRez1.setStyleSheet('color: red')

        self.playerRez2.setText('P2: ')

        self.life1ispis.setText('P1 Life: ')
        self.life1ispis.setStyleSheet('color: red')

        self.life2ispis.setText('P2 Life: ')

        self.playerRez11.setText(str(self.poeniPL1))
        self.playerRez11.setStyleSheet('color: red')

        self.playerRez22.setText(str(self.poeniPL2))

        self.left = 400
        self.top = 200
        self.width = 1000
        self.height = 562

        self.key_notifier = KeyNotifier()

        if (brojIgraca == 1):
            self.key_notifier.key_signal.connect(self.__update_position__)  # -----------------
            self.brojIgracaJedan = True
        else:
            self.brojIgracaJedan = False
            self.key_notifier2 = KeyNotifier2()
            self.key_notifier.key_signal.connect(self.__update_position__)  # -----------------
            self.key_notifier2.key_signal2.connect(self.__update_position2__)  # -----------------
            self.key_notifier2.start()

        self.key_notifier.start()

        self.__init_ui__(brLevel, brojIgraca)

    def __init_ui__(self, brLevel, brojIgraca):
        self.setWindowTitle('Donkey Kong')

        self.setGeometry(self.left, self.top, self.width, self.height)

        self.label1.setPixmap(self.pix1)
        self.label1.setGeometry(280, 475, 57, 67)

        self.label2.setPixmap(self.pix2)
        self.label2.setGeometry(475, -15, 75, 100)
        self.promenioSliku = True

        self.label3.setPixmap(self.pix3)
        self.label3.setGeometry(455, 75, 75, 100)

        self.izlazIzIgre.setPixmap(self.izadji)
        self.izlazIzIgre.setGeometry(750, 50, 250, 47)
        self.izlazIzIgre.mousePressEvent = self.shutdown

        brLevel += 1
        font = QtGui.QFont()
        font.setPointSize(20)

        self.labelLevel.setText(str(self.trenutniNivo))
        self.labelLevel.setGeometry(110, 5, 50, 50)
        self.labelLevel.setFont(font)
        self.labelLevel.setStyleSheet('color: blue')

        self.ispisLabel1.setGeometry(2, -20, 100, 100)
        self.ispisLabel1.setFont(font)

        self.lives1 = 3
        self.lives2 = 3

        self.labelLifes1.setText(str(self.lives1))
        self.labelLifes1.setGeometry(110, 15, 100, 100)
        self.labelLifes1.setFont(font)
        self.labelLifes1.setStyleSheet('color: red')

        self.life1ispis.setGeometry(2, 40, 150, 50)
        self.life1ispis.setFont(font)

        self.playerRez1.setGeometry(2, 40, 120, 100)
        self.playerRez11.setGeometry(110, 40, 100, 100)
        self.playerRez1.setFont(font)
        self.playerRez1.setStyleSheet('color: red')
        self.playerRez11.setFont(font)

        if (brojIgraca == 2):
            self.brojIgracaJedan = False

            self.playerRez2.setGeometry(2, 110, 100, 100)
            self.playerRez22.setGeometry(110, 110, 100, 100)
            self.playerRez2.setFont(font)
            self.playerRez2.setStyleSheet('color: green')
            self.playerRez22.setFont(font)
            self.playerRez22.setStyleSheet('color: green')

            self.life2ispis.setGeometry(2, 85, 120, 100)
            self.labelLifes2.setGeometry(110, 85, 100, 100)
            self.life2ispis.setFont(font)
            self.life2ispis.setStyleSheet('color: green')
            self.labelLifes2.setText(str(self.lives2))
            self.labelLifes2.setStyleSheet('color: green')
            self.labelLifes2.setFont(font)

            self.label30.setPixmap(self.pix112)
            self.label30.setGeometry(660, 475, 57, 75)

        self.jasminMovement = JasminMovement()
        self.jasminMovement.jasminMovementSignal.connect(self.moveJasmin)
        self.jasminMovement.start()

        self.gorilaMovement = GorilaMovement()
        self.gorilaMovement.gorilaMovementSignal.connect(self.moveGorila)
        self.gorilaMovement.start()

        self.movingBarrels = BarrelMovement()
        self.movingBarrels.barrelMovementSignal.connect(self.moveBarrels)
        self.movingBarrels.start()

        self.show()

    def keyPressEvent(self, event):
        a = event.key()
        self.key_notifier.add_key(a)
        if (self.brojIgracaJedan == False):
            b = event.key()
            self.key_notifier2.add_key(b)

    def keyReleaseEvent(self, event):
        a = event.key()
        self.key_notifier.rem_key(a)
        if (self.brojIgracaJedan == False):
            b = event.key()
            self.key_notifier2.rem_key(b)

    def __update_position__(self, key):
        rec1 = self.label1.geometry()

        if key == Qt.Key_Right:
            self.label1.setPixmap(self.pix11)
        elif key == Qt.Key_Left:
            self.label1.setPixmap(self.pix1)

        if key == Qt.Key_Right and rec1.x() <= 660 and (rec1.y() == 475 or rec1.y() == 385 or rec1.y() == 295 or rec1.y() == 205 or rec1.y() == 115 or rec1.y() == -15):
            self.label1.setGeometry(rec1.x() + 10, rec1.y(), rec1.width(), rec1.height())
        elif key == Qt.Key_Left and rec1.x() >= 280 and (rec1.y() == 475 or rec1.y() == 385 or rec1.y() == 295 or rec1.y() == 205 or rec1.y() == 115 or rec1.y() == -15):
            self.label1.setGeometry(rec1.x() - 10, rec1.y(), rec1.width(), rec1.height())
        elif key == Qt.Key_Up:
            if (rec1.x() >= 445 and rec1.x() <= 465 and rec1.y() > 385 and rec1.y() <= 475):
                 self.label1.setGeometry(rec1.x(), rec1.y() - 10, rec1.width(), rec1.height())
                 if rec1.y() == 395:
                     self.poeniPL1 += 1
                     self.playerRez11.setText(str(self.poeniPL1))
            elif (rec1.x() >= 290  and rec1.x() <= 310 and rec1.y() > 295 and rec1.y() <= 385):
                self.label1.setGeometry(rec1.x(), rec1.y() - 10, rec1.width(), rec1.height())
                if rec1.y() == 305:
                    self.poeniPL1 += 1
                    self.playerRez11.setText(str(self.poeniPL1))
            elif (rec1.x() >= 620 and rec1.x() <= 640 and rec1.y() > 205 and rec1.y() <= 295):
                self.label1.setGeometry(rec1.x(), rec1.y() - 10, rec1.width(), rec1.height())
                if rec1.y() == 215:
                    self.poeniPL1 += 1
                    self.playerRez11.setText(str(self.poeniPL1))
            elif (rec1.x() >= 320 and rec1.x() <= 340 and rec1.y() > 115 and rec1.y() <= 205):
                self.label1.setGeometry(rec1.x(), rec1.y() - 10, rec1.width(), rec1.height())
                if rec1.y() == 125:
                    self.poeniPL1 += 1
                    self.playerRez11.setText(str(self.poeniPL1))
            elif (rec1.x() >= 400 and rec1.x() <= 420 and rec1.y() > -15 and rec1.y() <= 115):
                self.label1.setGeometry(rec1.x(), rec1.y() - 10, rec1.width(), rec1.height())
                if rec1.y() == -5:
                    self.poeniPL1 += 1
                    self.playerRez11.setText(str(self.poeniPL1))
        elif key == Qt.Key_Down:
            if (rec1.x() >= 445 and rec1.x() <= 465 and rec1.y() >= 385 and rec1.y() < 475):
                self.label1.setGeometry(rec1.x(), rec1.y() + 10, rec1.width(), rec1.height())
                if rec1.y() == 395:
                    self.poeniPL1 -= 1
                    self.playerRez11.setText(str(self.poeniPL1))
            elif (rec1.x() >= 290 and rec1.x() <= 310 and rec1.y() >= 295 and rec1.y() < 385):
                self.label1.setGeometry(rec1.x(), rec1.y() + 10, rec1.width(), rec1.height())
                if rec1.y() == 305:
                    self.poeniPL1 -= 1
                    self.playerRez11.setText(str(self.poeniPL1))
            elif (rec1.x() >= 620 and rec1.x() <= 640 and rec1.y() >= 205 and rec1.y() < 295):
                self.label1.setGeometry(rec1.x(), rec1.y() + 10, rec1.width(), rec1.height())
                if rec1.y() == 215:
                    self.poeniPL1 -= 1
                    self.playerRez11.setText(str(self.poeniPL1))
            elif (rec1.x() >= 320 and rec1.x() <= 340 and rec1.y() >= 115 and rec1.y() < 205):
                self.label1.setGeometry(rec1.x(), rec1.y() + 10, rec1.width(), rec1.height())
                if rec1.y() == 125:
                    self.poeniPL1 -= 1
                    self.playerRez11.setText(str(self.poeniPL1))
            elif (rec1.x() >= 400 and rec1.x() <= 420 and rec1.y() >= -15 and rec1.y() < 115):
                self.label1.setGeometry(rec1.x(), rec1.y() + 10, rec1.width(), rec1.height())
                if rec1.y() == -5:
                    self.poeniPL1 -= 1
                    self.playerRez11.setText(str(self.poeniPL1))




    def __update_position2__(self, key):
        rec2 = self.label30.geometry()

        if key == Qt.Key_D:
            self.label30.setPixmap(self.pix112)
        elif key == Qt.Key_A:
            self.label30.setPixmap(self.pix12)

        if key == Qt.Key_D and rec2.x() <= 660 and  (rec2.y() == 475 or rec2.y() == 385 or rec2.y() == 295 or rec2.y() == 205 or rec2.y() == 115 or rec2.y() == -15):
            self.label30.setGeometry(rec2.x() + 10, rec2.y(), rec2.width(), rec2.height())
        elif key == Qt.Key_A and rec2.x() >= 280 and (rec2.y() == 475 or rec2.y() == 385 or rec2.y() == 295 or rec2.y() == 205 or rec2.y() == 115 or rec2.y() == -15):
            self.label30.setGeometry(rec2.x() - 10, rec2.y(), rec2.width(), rec2.height())
        elif key == Qt.Key_W:
            if (rec2.x() >= 445 and rec2.x() <= 465 and rec2.y() > 385 and rec2.y() <= 475):
                self.label30.setGeometry(rec2.x(), rec2.y() - 10, rec2.width(), rec2.height())
                if rec2.y() == 395:
                    self.poeniPL2 += 1
                    self.playerRez22.setText(str(self.poeniPL2))
            elif (rec2.x() >= 290 and rec2.x() <= 310 and rec2.y() > 295 and rec2.y() <= 385):
                self.label30.setGeometry(rec2.x(), rec2.y() - 10, rec2.width(), rec2.height())
                if rec2.y() == 305:
                    self.poeniPL2 += 1
                    self.playerRez22.setText(str(self.poeniPL2))
            elif (rec2.x() >= 620 and rec2.x() <= 640 and rec2.y() > 205 and rec2.y() <= 295):
                self.label30.setGeometry(rec2.x(), rec2.y() - 10, rec2.width(), rec2.height())
                if rec2.y() == 215:
                    self.poeniPL2 += 1
                    self.playerRez22.setText(str(self.poeniPL2))
            elif (rec2.x() >= 320 and rec2.x() <= 340 and rec2.y() > 115 and rec2.y() <= 205):
                self.label30.setGeometry(rec2.x(), rec2.y() - 10, rec2.width(), rec2.height())
                if rec2.y() == 125:
                    self.poeniPL2 += 1
                    self.playerRez22.setText(str(self.poeniPL2))
            elif (rec2.x() >= 400 and rec2.x() <= 420 and rec2.y() > -15 and rec2.y() <= 115):
                self.label30.setGeometry(rec2.x(), rec2.y() - 10, rec2.width(), rec2.height())
                if rec2.y() == -5:
                    self.poeniPL2 += 1
                    self.playerRez22.setText(str(self.poeniPL2))
        elif key == Qt.Key_S:
            if (rec2.x() >= 445 and rec2.x() <= 465 and rec2.y() >= 385 and rec2.y() < 475):
                self.label30.setGeometry(rec2.x(), rec2.y() + 10, rec2.width(), rec2.height())
                if rec2.y() == 395:
                    self.poeniPL2 -= 1
                    self.playerRez22.setText(str(self.poeniPL2))
            elif (rec2.x() >= 290 and rec2.x() <= 310 and rec2.y() >= 295 and rec2.y() < 385):
                self.label30.setGeometry(rec2.x(), rec2.y() + 10, rec2.width(), rec2.height())
                if rec2.y() == 305:
                    self.poeniPL2 -= 1
                    self.playerRez22.setText(str(self.poeniPL2))
            elif (rec2.x() >= 620 and rec2.x() <= 640 and rec2.y() >= 205 and rec2.y() < 295):
                self.label30.setGeometry(rec2.x(), rec2.y() + 10, rec2.width(), rec2.height())
                if rec2.y() == 215:
                    self.poeniPL2 -= 1
                    self.playerRez22.setText(str(self.poeniPL2))
            elif (rec2.x() >= 320 and rec2.x() <= 340 and rec2.y() >= 115 and rec2.y() < 205):
                self.label30.setGeometry(rec2.x(), rec2.y() + 10, rec2.width(), rec2.height())
                if rec2.y() == 125:
                    self.poeniPL2 -= 1
                    self.playerRez22.setText(str(self.poeniPL2))
            elif (rec2.x() >= 400 and rec2.x() <= 420 and rec2.y() >= -15 and rec2.y() < 115):
                self.label30.setGeometry(rec2.x(), rec2.y() + 10, rec2.width(), rec2.height())
                if rec2.y() == -5:
                    self.poeniPL2 -= 1
                    self.playerRez22.setText(str(self.poeniPL2))

    def moveJasmin(self):
        self.timerP1 = QTimer(self)
        self.timerP1.start(2000)
        self.timerP1.timeout.connect(self.menjajSliku)

        if isHit(self.label2, self.label1) or isHit(self.label2, self.label30):
            if self.brojIgracaJedan:
                self.label1.setGeometry(280, 475, 75, 75)
                self.lives1 = 3
                self.trenutniNivo += 1
                self.labelLifes1.setText(str(self.lives1))
                self.labelLevel.setText(str(self.trenutniNivo))
            else:
                if self.prvi and self.drugi:
                    self.trenutniNivo += 1
                    self.labelLevel.setText(str(self.trenutniNivo))
                    self.label1.setGeometry(280, 475, 75, 75)
                    self.label30.setGeometry(660, 475, 75, 75)
                    self.label30.show()
                    self.label1.show()
                    self.drugi = False
                    self.prvi = False

                elif isHit(self.label2, self.label1):
                    self.label1.hide()
                    self.prvi = True
                    self.lives1 = 3
                    self.labelLifes1.setText(str(self.lives1))

                elif isHit(self.label2, self.label30):
                    self.label30.hide()
                    self.drugi = True
                    self.lives2 = 3
                    self.labelLifes2.setText(str(self.lives2))

        if self.lives1 == 0:
            self.label1.hide()
        elif self.lives2 == 0:
            self.label30.hide()

        if self.lives1 == 0 and self.drugi:
            self.drugi = False
            self.trenutniNivo += 1
            self.label30.setGeometry(660, 475, 75, 75)
            self.labelLevel.setText(str(self.trenutniNivo))
            self.label30.show()

        if self.lives2 == 0 and self.prvi:
            self.prvi = False
            self.label1.setGeometry(280, 475, 75, 75)
            self.trenutniNivo += 1
            self.labelLevel.setText(str(self.trenutniNivo))
            self.label1.show()

        if self.lives1 == 0 and self.lives2 == 0:
            self.close()

    def menjajSliku(self):
        if self.promenioSliku:
            self.label2.setPixmap(self.pix22)
            self.promenioSliku = False
        else:
            self.label2.setPixmap(self.pix2)
            self.promenioSliku = True

    def moveGorila(self):
        rec2 = self.label3.geometry()

        if (rec2.x() >= 580):
            self.hitSide = True
        elif (rec2.x() <= 320):
            self.hitSide = False

        a = randint(0, 100)
        if a % 15 == 0:
            self.hitSide = True

        b = randint(0, 100)
        if b % 13 == 0:
            self.hitSide = False

        if (self.hitSide):
            self.label3.setGeometry(rec2.x() - 10, rec2.y(), rec2.width(), rec2.height())
            self.label3.setPixmap(self.pix3)
        else:
            self.label3.setGeometry(rec2.x() + 10, rec2.y(), rec2.width(), rec2.height())
            self.label3.setPixmap(self.pix32)

        if isHit(self.label1, self.label3):
            if self.lives1 > 0:
                self.lives1 -= 1
                self.labelLifes1.setText(str(self.lives1))
                if self.lives1 == 0:
                    if self.brojIgracaJedan:
                        self.close()
                    else:
                        self.label1.hide()


        if isHit(self.label30, self.label3):
            if self.lives2 > 0:
                self.lives2 -= 1
                self.labelLifes2.setText(str(self.lives2))
                if self.lives2 == 0:
                    self.label30.hide()

        if not self.zaustavio:
            self.gorilaStop.put(1)
            self.zaustavio = True
            return
        else:
            if self.gorilaStart.empty():
                return
            else:
                a = self.gorilaStart.get()
            self.zaustavio = False

    def moveBarrels(self):
        rec = self.label3.geometry()

        a = randint(0, 100)
        if a % 12 == 0:
            barrel = QLabel(self)
            self.barrels.append(barrel)
            self.barrels[len(self.barrels) - 1].setPixmap(self.pix4)
            self.barrels[len(self.barrels) - 1].setGeometry(rec.x(), rec.y(), 40, 40)
            self.barrels[len(self.barrels) - 1].show()

        for barrel in self.barrels:
            recb = barrel.geometry()
            barrel.setGeometry(recb.x(), recb.y() + 10, recb.width(), recb.height())

            if recb.y() > 600:
                barrel.hide()
                self.barrels.remove(barrel)

            if isHit(barrel, self.label1):
                if self.lives1 > 0:
                    self.lives1 -= 1
                    self.labelLifes1.setText(str(self.lives1))
                    barrel.hide()
                    self.barrels.remove(barrel)

                    if self.lives1 == 0:
                        if self.brojIgracaJedan:
                            self.close()
                        else:
                            self.label1.hide()

            if isHit(barrel, self.label30):
                if self.lives2 > 0:
                    self.lives2 -= 1
                    self.labelLifes2.setText(str(self.lives2))
                    barrel.hide()
                    self.barrels.remove(barrel)

                    if self.lives2 == 0:
                        self.label30.hide()

    def closeEvent(self, event):
        self.jasminMovement.die()
        self.gorilaMovement.die()
        self.barrelProcess.terminate()
        self.movingBarrels.die()
        self.gorilaBug.terminate()
        self.key_notifier.die()
        self.key_notifier2.die()

    def shutdown(self, event):
        self.barrelProcess.terminate()
        self.gorilaBug.terminate()
        self.close()



        #self.close()
       # self.one = SimMoveDemo(x, self.trenutniNivo + 1)

if __name__ == '__main__':
     app = QApplication(sys.argv)
     ex = SimMoveDemo(1, 1)
     sys.exit(app.exec_())
import math
import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5 import QtWidgets, QtGui

from besel_curve import generate
import numpy as np
import time

pets = []
def addPets(n=1):
    for _ in range(n):
        pets.append(myPet())


def delOnePet():
    if len(pets) == 0:
        return
    del pets[len(pets) - 1]


class myPet(QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self)
        self.initUI()

    def initUI(self):
        self.dense = 100
        self.freq = 20

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.repaint()  # 可有可无
        self.img = QLabel(self)
        self.actionDatas = []
        self.initData()
        self.index = 0
        self.setPic("shime1.png")
        self.resize(128, 128)
        self.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.actionRun)
        self.timer.start(500)
        self.coord = self.randomPos()  # 初始化随机位置
        self.speed = self.get_random_direction()
        self.path_list = self.get_besels_list()

        self.move_timer = QTimer()  # 随机移动
        self.move_timer.timeout.connect(self.besel_move)
        self.move_timer.start(self.freq)
        self.move_event_pos_list = []

        self.runing = False
        self.is_move = True
        self.m_drag = False

    def besel_move(self):
        if not self.is_move:
            return
        if self.path_list:
            self.move(self.path_list.pop(0))
        else:
            self.path_list = self.get_besels_list()
            self.besel_move()

    def get_besels_list(self):
        if np.isnan(self.speed).any():
            self.speed = self.get_random_direction()
        x, y, speed, coord = generate(width=self.random_area[0],
                                      height=self.random_area[1],
                                      coord=self.qp2np(self.coord),
                                      speed=self.speed,
                                      dense=self.dense)
        self.speed = speed
        self.coord = self.np2qp(coord)
        list_to_return = []
        for i in zip(x, y):
            list_to_return.append(self.np2qp(i))
        return list_to_return

    @staticmethod
    def getImgs(pics):
        """将图片路径转化为QImage图片实例，服务于self.initData"""
        listPic = []
        for item in pics:
            img = QImage()
            img.load('img/' + item)
            listPic.append(img)
        return listPic

    @staticmethod
    def get_random_direction():
        theta = random.random()*math.pi*2
        return np.array([math.cos(theta), math.sin(theta)])

    @staticmethod
    def np2qp(array):
        return QPoint(int(array[0]), int(array[1]))

    @staticmethod
    def qp2np(qp):
        return np.array([qp.x(), qp.y()])

    def initData(self):
        """初始化self.actionDatas的内容"""
        imgs = self.getImgs(["shime1b.png", "shime2b.png", "shime1b.png", "shime3b"])
        self.actionDatas.append(imgs)
        imgs = self.getImgs(
            ["shime11.png", "shime15.png", "shime16.png", "shime17.png", "shime16.png", "shime17.png", "shime16.png",
             "shime17.png"])
        self.actionDatas.append(imgs)
        imgs = self.getImgs(
            ["shime54.png", "shime55.png", "shime26.png", "shime27.png", "shime28.png", "shime29.png", "shime26.png",
             "shime27.png", "shime28.png", "shime29.png", "shime26.png", "shime27.png", "shime28.png", "shime29.png"])
        self.actionDatas.append(imgs)
        imgs = self.getImgs(["shime31.png", "shime32.png", "shime31.png", "shime33.png"])
        self.actionDatas.append(imgs)
        imgs = self.getImgs(["shime18.png", "shime19.png"])
        self.actionDatas.append(imgs)
        imgs = self.getImgs(["shime34b.png", "shime35b.png", "shime34b.png", "shime36b.png"])
        self.actionDatas.append(imgs)
        imgs = self.getImgs(
            ["shime14.png", "shime14.png", "shime52.png", "shime13.png", "shime13.png", "shime13.png", "shime52.png",
             "shime14.png"])
        self.actionDatas.append(imgs)
        imgs = self.getImgs(["shime42.png", "shime43.png", "shime44.png", "shime45.png", "shime46.png"])
        self.actionDatas.append(imgs)
        imgs = self.getImgs(["shime1.png", "shime38.png", "shime39.png", "shime40.png", "shime41.png"])
        self.actionDatas.append(imgs)
        imgs = self.getImgs(
            ["shime25.png", "shime25.png", "shime53.png", "shime24.png", "shime24.png", "shime24.png", "shime53.png",
             "shime25.png"])
        self.actionDatas.append(imgs)
        imgs = self.getImgs(["shime20.png", "shime21.png", "shime20.png", "shime21.png", "shime20.png"])
        self.actionDatas.append(imgs)

        self.special_action = {
            key: val for key, val in zip(
                ('l1', 'l2', 'l3', 'r1', 'r2', 'r3', 'up', 'down'),
                self.getImgs(['shime{}.png'.format(i) for i in (6, 8, '9r', 5, 7, 9, 10, 4)])
            )
        }



    def actionRun(self):
        if self.m_drag:
            return
        if not self.runing:
            self.action = random.randint(0, len(self.actionDatas) - 1)
            self.index = 0
            self.runing = True
        self.runAnimation(self.actionDatas[self.action])

    def setPic(self, pic):
        """仅服务于init中的初始化第一张图片"""
        img = QImage()
        img.load('img/' + pic)
        self.setImg(img)
        
    
    def setImg(self, img):
        self.img.setPixmap(QPixmap.fromImage(img))

    def runAnimation(self, imgs):
        if self.index >= len(imgs):
            self.runing = False
            self.actionRun()
        self.img.setPixmap(QPixmap.fromImage(imgs[self.index]))
        self.index += 1

    def randomPos(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.random_area = (screen.width() - size.width(),
                            screen.height() - size.height())
        coord = (random.randint(0, self.random_area[0]),
                 random.randint(0, self.random_area[1]))
        self.move(*coord)
        return QPoint(*coord)

    def mousePressEvent(self, event):
        """左键按下时改变鼠标图标，设置一些移动时的参数"""
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.is_move = False
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
            self.setImg(self.special_action['up'])

    def mouseMoveEvent(self, QMouseEvent):
        if self.m_drag:
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            self.move_event_pos_list.append((self.pos(), time.time()))
            if len(self.move_event_pos_list) > 4:
                qp1, t1 = self.move_event_pos_list[-4]
                qp2, t2 = self.move_event_pos_list[-1]
                if t1 == t2:
                    self.setImg(self.special_action['up'])
                    return
                spd = self.qp2np((qp1 - qp2) / (t1 - t2))
                x, y = spd
                if abs(x)<abs(y):
                    if y > 0:
                        self.setImg(self.special_action['down'])
                    else:
                        self.setImg(self.special_action['up'])
                else:
                    if x > 0:
                        self.setImg(self.special_action[f'r{min(3, x//300+1)}'])
                    else:
                        self.setImg(self.special_action[f'l{min(3, -x//300+1)}'])

            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        def deal_pos():
            """处理self.move_event_pos_list得到末速度"""
            try:
                qp1, t1 = self.move_event_pos_list[-4]
                qp2, t2 = self.move_event_pos_list[-1]
            except:
                return self.get_random_direction()
            if t1 == t2:
                return self.get_random_direction()
            spd = self.qp2np((qp1 - qp2) / (t1 - t2))
            length = np.linalg.norm(spd)
            print(length)
            std_length = length/10000*3000 if length < 10000 else 2500+(length/10000-1)*1200
            print(std_length)
            self.move_event_pos_list = []
            return spd*std_length/length

        if QMouseEvent.button() == Qt.LeftButton:
            self.m_drag = False
            self.is_move = True
            self.coord = self.pos()
            # self.speed = self.get_random_direction()
            self.speed = deal_pos()
            self.path_list = self.get_besels_list()
            self.setCursor(QCursor(Qt.ArrowCursor))

    def contextMenuEvent(self, QContextMenuEvent):
        quit = QAction("退出", self, triggered=self.close)
        quit.setIcon(QIcon("img/icon.png"))
        addPet = QAction("添加一个Miku", self, triggered=addPets)
        addPet.setIcon(QIcon("img/icon.png"))
        addNPet = QAction("添加十个Miku", self, triggered=lambda: addPets(10))
        addNPet.setIcon(QIcon("img/icon.png"))
        removePet = QAction("移除一个Miku", self, triggered=delOnePet)
        removePet.setIcon(QIcon("img/icon.png"))
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(addPet)
        self.trayIconMenu.addAction(addNPet)
        self.trayIconMenu.addAction(removePet)
        self.trayIconMenu.addAction(quit)
        self.trayIconMenu.exec_(QContextMenuEvent.globalPos())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = myPet()
    sys.exit(app.exec_())

import sys
import keyboard

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



class Window(QMainWindow):
    MODULE = False

    def __init__(self, App: QApplication):
        super().__init__()
        self.App = App

        self.module = False
        
        scale = 200
        self.desktop = QDesktopWidget()
        self.WIDTH   = self.desktop.width() + scale
        self.HEIGHT  = self.desktop.height() + scale
        
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SplashScreen)
        self.setGeometry(-100, -100, self.WIDTH, self.HEIGHT)
        self.setWindowOpacity(0.001)
        self.setWindowIcon(QIcon(QPixmap('icon.png')))
        self.setWindowTitle('ScreenClipper Pro')

        self.sc           = self.App.primaryScreen()
        self.image        = self.sc.grabWindow(0)
        self.image        = self.image.scaled(self.WIDTH, self.HEIGHT)
        self.source_image = self.image

        self.image_label = QLabel(self)
        self.image_label.setGeometry(0, 0, self.WIDTH, self.HEIGHT)
        self.image_label.setPixmap(self.image)
        self.image_label.setAlignment(Qt.AlignCenter)
        # self.image_label.setScaledContents(True)
        self.setCentralWidget(self.image_label)

        self.blur = QGraphicsBlurEffect()
        self.blur.setBlurRadius(50)
        # self.blur.setBlurHints(QGraphicsBlurEffect.QualityHint)
        self.image_label.setGraphicsEffect(self.blur)

        self.front = QWidget(self)
        self.front.setStyleSheet('''
            background-color: rgba(10, 10, 10, 100); 
            color: white; 
            border-top: 1px solid qlineargradient(
                spread:pad, x1:0, y1:0, x2:1, y2:0, 
                stop:0 rgba(255, 0, 0, 255), 
                stop:0.166 rgba(255, 255, 0, 255), 
                stop:0.333 rgba(0, 255, 0, 255), 
                stop:0.5 rgba(0, 255, 255, 255), 
                stop:0.666 rgba(0, 0, 255, 255), 
                stop:0.833 rgba(255, 0, 255, 255), 
                stop:1 rgba(255, 0, 0, 255));
            border-bottom: 1px solid qlineargradient(
                spread:pad, x1:0, y1:0, x2:1, y2:0, 
                stop:0 rgba(255, 0, 0, 255), 
                stop:0.166 rgba(255, 255, 0, 255), 
                stop:0.333 rgba(0, 255, 0, 255), 
                stop:0.5 rgba(0, 255, 255, 255), 
                stop:0.666 rgba(0, 0, 255, 255), 
                stop:0.833 rgba(255, 0, 255, 255), 
                stop:1 rgba(255, 0, 0, 255));
            border-right: 1px solid qlineargradient(
                spread:pad, x1:0, y1:0, x2:0, y2:1, 
                stop:0 rgba(255, 0, 0, 255), 
                stop:0.166 rgba(255, 255, 0, 255), 
                stop:0.333 rgba(0, 255, 0, 255), 
                stop:0.5 rgba(0, 255, 255, 255), 
                stop:0.666 rgba(0, 0, 255, 255), 
                stop:0.833 rgba(255, 0, 255, 255), 
                stop:1 rgba(255, 0, 0, 255));
            border-left: 1px solid qlineargradient(
                spread:pad, x1:0, y1:0, x2:0, y2:1, 
                stop:0 rgba(255, 0, 0, 255), 
                stop:0.166 rgba(255, 255, 0, 255), 
                stop:0.333 rgba(0, 255, 0, 255), 
                stop:0.5 rgba(0, 255, 255, 255), 
                stop:0.666 rgba(0, 0, 255, 255), 
                stop:0.833 rgba(255, 0, 255, 255), 
                stop:1 rgba(255, 0, 0, 255));
        ''')
        self.front.setGeometry(scale // 2, scale // 2, self.WIDTH - scale, self.HEIGHT - scale)


        self.anim_opacity = QVariantAnimation()
        self.anim_opacity.setStartValue(0.001)
        self.anim_opacity.setEndValue(1.0)
        self.anim_opacity.setDuration(200)
        self.anim_opacity.valueChanged.connect(self.setWindowOpacity)
        
        
        self.front.setMouseTracking(True)
        self.front.mouseMoveEvent = self.mouseMove
        pass


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.hide()
        return super().keyPressEvent(event)

    def setWindowOpacity(self, level):
        if level == 0.001:
            self.close()
            self.App.quit()
        return super().setWindowOpacity(level)


    def show(self):
        self.anim_opacity.setDirection(QVariantAnimation.Forward)
        self.anim_opacity.start()
        super().show()

    def hide(self, module=False):
        self.MODULE = module
        self.anim_opacity.setDirection(QVariantAnimation.Backward)
        self.anim_opacity.start()

    def mouseMove(self, event: QMouseEvent):
        self.image = self.source_image.copy(QRect(
                self.image.rect().x() + int(event.x() * 0.03),
                self.image.rect().y() + int(event.y() * 0.03),
                self.image.width(),
                self.image.height()
            )
        )
        self.image_label.setPixmap(self.image)
        # print(self.image.size())
        # return super().mouseMoveEvent(event)

    
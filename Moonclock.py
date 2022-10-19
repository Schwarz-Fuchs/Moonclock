import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import datetime
import zhdate

def get_second():
    now_time = datetime.datetime.now()
    second=now_time.second
    return  second


class moonclock(QWidget):
    def __init__(self):
        #在这里设置窗口大小
        self.scale=200

        super().__init__()
        self.icon_quit()
        self.background()
        self.pos_first = self.pos()
        self.timer = QTimer()
        self.timer.start(1000)
        #随timer 更新
        self.timer.timeout.connect(self.update)


    def background(self):
        '''
        窗体与moon clock 外框设置
        '''
        #设置窗体
        self.x = self.scale
        self.y = self.scale
        self.setGeometry(self.x, self.y, self.scale, self.scale)
        self.setWindowTitle('MOON CLOCK')

        # 加载MOON clock外框
        self.lable = QLabel(self)
        self.background = "clock dial\outer dial small.png"
        self.qpixmap = QPixmap(self.background)
        self.qpixmap = self.qpixmap.scaled(self.scale,self.scale)
        self.lable.setPixmap(self.qpixmap)

        #窗体隐藏
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow) #隐藏程序框,始终置顶
        self.setAutoFillBackground(False) #不填充背景
        self.setAttribute(Qt.WA_TranslucentBackground, True) #程序设置透明


    def paintEvent(self, event):
        '''
        绘制背景与月亮动画
        '''

        mooncolor = QColor(230, 230, 250, 240) #月亮颜色 R,G,B,透明度
        nightcolor= QColor(10, 20, 30, 240) #背景填充色
        side = min(self.width(), self.height())

        #初始化painter,启用抗锯齿
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        #绘制背景，一个同窗口相同大小的圆
        painter.save()
        painter.setPen(Qt.NoPen)  # 无轮廓线
        painter.setBrush(nightcolor)  # 填充色
        painter.drawEllipse(0, 0, self.scale, self.scale)
        painter.restore()

        #获取农历时间 以确定月亮绘制位置
        time_now= QDateTime.currentDateTime()
        #sec=time_now.time().second()
        hour = int(time_now.time().hour())
        day=str(zhdate.ZhDate.today())
        time=datetime.datetime.strptime(day, '农历%Y年%m月%d日')  #将公历时间转为农历时间
        lunar_day=float(time.day)+hour/24-1 #使用小时将天数精确到小数点后一位

        #切换painter到坐标中心
        painter.translate(self.width() / 2, self.height() / 2) # painter坐标系原点移至widget中央
        painter.scale(side / self.scale, side / self.scale) # 缩放painterwidget坐标系，使绘制的时钟位于widge中央,即支持缩放

        #绘制月亮
        painter.save()
        painter.setPen(Qt.NoPen)  # 无轮廓线
        painter.setBrush(mooncolor)  # 填充色
        ''''
        这里注释的是秒表，可以让月亮转的飞快
        painter.rotate(-135)
        painter.rotate(6 * sec) #每秒旋转6°
        '''
        painter.rotate(45)  #归零
        painter.rotate(12.2 * lunar_day) #每天月亮转12.2度
        r_moon=int(self.scale/8*2.7) #月亮大小
        painter.drawEllipse(int(0.09*r_moon),int(0.09*r_moon),r_moon,r_moon) #绘制月亮，与坐标中心横纵均偏移0.09月亮半径
        painter.restore()


    def quit(self):
        '''
        程序退出
        '''
        self.close()
        sys.exit()

    def icon_quit(self):
        '''
        在工具栏生成退出按钮
        '''
        mini_icon = QSystemTrayIcon(self)
        mini_icon.setIcon(QIcon('clock dial\outer dial small.png'))
        quit_menu = QAction('Exit', self, triggered=self.quit)
        tpMenu = QMenu(self)
        tpMenu.addAction(quit_menu)
        mini_icon.setContextMenu(tpMenu)
        mini_icon.show()

    def mousePressEvent(self, QMouseEvent):
        '''
        鼠标点击事件，会变成小手
        '''
        if QMouseEvent.button() == Qt.LeftButton:
            self.pos_first = QMouseEvent.globalPos() - self.pos()
            QMouseEvent.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        '''
        鼠标移动事件，窗口可以拖动
        '''
        if Qt.LeftButton:
            self.move(QMouseEvent.globalPos() - self.pos_first)
            self.x, self.y = self.pos().x, self.pos().y
            QMouseEvent.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = moonclock()
    clock.show()
    sys.exit(app.exec_())
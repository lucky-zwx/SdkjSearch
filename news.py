# coding:utf-8
import sqlite3
import sys

import requests
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem, QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget

from search_face import searchface
from take_a_picture import get_img_from_camera_local
from upload_picture import get_token, imgdata


class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        self.status = 0
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(800, 600)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格

        self.right_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格

        self.main_layout.addWidget(self.left_widget, 0, 0, 12, 2)  # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget, 0, 2, 12, 10)  # 右侧部件在第0行第3列，占8行9列
        self.main_widget.setWindowIcon(QIcon('./ico/main.ico'))

        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        self.left_close = QtWidgets.QPushButton("")  # 关闭按钮
        self.left_visit = QtWidgets.QPushButton("")  # 空白按钮
        self.left_mini = QtWidgets.QPushButton("")  # 最小化按钮
        self.left_searchbyface = QtWidgets.QPushButton(QIcon('ico/相机.png'), "拍照识别")  # 面部识别搜索
        self.left_searchbyface.setObjectName('left_button')
        self.left_searchbyface_p = QtWidgets.QPushButton(QIcon('ico/添加.png'), "上传识别")  # 面部识别搜索通过照片
        self.left_searchbyface_p.setObjectName('left_button')
        self.left_searchbyname = QtWidgets.QPushButton(QIcon('ico/姓名.png'), "姓名搜索")  # 姓名搜索
        self.left_searchbyname.setObjectName('left_button')
        self.left_help = QtWidgets.QPushButton(QIcon('ico/帮助.png'), "帮助")
        self.left_help.setObjectName('left_button')
        self.left_request = QtWidgets.QPushButton(QIcon('ico/反馈.png'), "反馈")
        self.left_request.setObjectName('left_button')

        self.left_layout.addWidget(self.left_mini, 0, 0, 1, 1)
        self.left_layout.addWidget(self.left_close, 0, 2, 1, 1)
        self.left_layout.addWidget(self.left_visit, 0, 1, 1, 1)
        self.left_layout.addWidget(self.left_searchbyface, 1, 0, 1, 3)
        self.left_layout.addWidget(self.left_searchbyface_p, 2, 0, 1, 3)
        self.left_layout.addWidget(self.left_searchbyname, 3, 0, 1, 3)
        self.left_layout.addWidget(self.left_help, 4, 0, 1, 3)
        self.left_layout.addWidget(self.left_request, 5, 0, 1, 3)

        self.left_close.setFixedSize(15, 15)  # 设置关闭按钮的大小
        self.left_visit.setFixedSize(15, 15)  # 设置按钮大小
        self.left_mini.setFixedSize(15, 15)  # 设置最小化按钮大小

        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_visit.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')

        self.left_widget.setStyleSheet('''
            QPushButton{border:none;color:white;}
            QPushButton#left_label{
                border:none;
                border-bottom:1px solid white;
                font-size:18px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
            QWidget#left_widget{
            background:gray;
            border-top:1px solid white;
            border-bottom:1px solid white;
            border-left:1px solid white;
            border-top-left-radius:10px;
            border-bottom-left-radius:10px;}
        ''')

        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel#right_lable{
                border:none;
                font-size:16px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
        ''')

        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.main_layout.setSpacing(0)

    def take_picture(self):
        if self.status == 1:
            return
        if self.status != 1:
            from removewidget import RemoveWidget
            RemoveWidget.autoremove(self)
        self.status = 1
        self.right_tableView1 = QtWidgets.QTableView()
        self.model = QStandardItemModel(4, 4, self.right_tableView1)
        self.model.setHorizontalHeaderLabels(['姓名', '班级', '电话', '学号'])
        self.right_tableView1.setMaximumHeight(100)
        self.right_pushbutton = QtWidgets.QPushButton('点击拍照')
        self.right_pushbutton.setStyleSheet('''QPushButton{
        padding: 10px 20px;
        font-size: 15px;
        text-align: center;
        text-decoration: none;
        outline: none;
        color: #fff;
        background-color: #4CAF50;
        border: none;
        border-radius: 15px;}
        QPushButton:hover {background-color: #3e8e41}
        ''')
        self.right_lableme = QtWidgets.QLabel()
        self.right_lableme.setMinimumSize(200, 400)
        self.right_lableme.setText('拍照后，你的照片将在这里显示！')
        self.right_lableme.setStyleSheet(
            'QLabel{border: 1px solid #ccc!important;padding:14px;border-radius: 16px!important;margin-left:auto;margin-right:auto;}')
        self.right_lablese = QtWidgets.QLabel()
        self.right_lablese.setMinimumSize(200, 400)
        self.right_lablese.setText('人脸识别对比后的照片！')
        self.right_lablese.setStyleSheet(
            'QLabel{border: 1px solid #ccc!important;padding:14px;border-radius: 16px!important;margin-left:auto;margin-right:auto;}')
        self.right_layout.addWidget(self.right_tableView1, 0, 0, 1, 2)
        self.right_layout.addWidget(self.right_pushbutton, 2, 0, 1, 2)
        self.right_layout.addWidget(self.right_lableme, 1, 0, 1, 1)
        self.right_layout.addWidget(self.right_lablese, 1, 1, 1, 1)
        self.right_tableView1.setModel(self.model)
        self.right_pushbutton.clicked.connect(self.search_p)
        self.right_tableView1.clicked.connect(self.battle)

    def uploadpic(self):
        if self.status == 2:
            return
        if self.status != 2:
            from removewidget import RemoveWidget
            RemoveWidget.autoremove(self)
        self.status = 2
        self.right_tableView2 = QtWidgets.QTableView()
        self.model2 = QStandardItemModel(4, 4, self.right_tableView2)
        self.model2.setHorizontalHeaderLabels(['姓名', '班级', '电话', '学号'])
        self.right_tableView2.setMaximumHeight(100)
        self.right_pushbutton2 = QtWidgets.QPushButton('点击搜索')
        self.right_pushbutton2.setStyleSheet('''QPushButton{
        padding: 10px 20px;
        font-size: 15px;
        text-align: center;
        text-decoration: none;
        outline: none;
        color: #fff;
        background-color: #4CAF50;
        border: none;
        border-radius: 15px;}
        QPushButton:hover {background-color: #3e8e41}
        ''')
        self.right_lableme2 = QtWidgets.QLabel()
        self.right_lableme2.setMinimumSize(200, 400)
        self.right_lableme2.setText('这里将显示你查找的照片！')
        self.right_lableme2.setStyleSheet(
            'QLabel{border: 1px solid #ccc!important;padding:14px;border-radius: 16px!important;margin-left:auto;margin-right:auto;}')
        self.right_lablese2 = QtWidgets.QLabel()
        self.right_lablese2.setMinimumSize(200, 400)
        self.right_lablese2.setText('人脸识别对比后的照片！')
        self.right_lablese2.setStyleSheet(
            'QLabel{border: 1px solid #ccc!important;padding:14px;border-radius: 16px!important;margin-left:auto;margin-right:auto;}')
        self.right_layout.addWidget(self.right_tableView2, 0, 0, 1, 2)
        self.right_layout.addWidget(self.right_pushbutton2, 2, 0, 1, 2)
        self.right_layout.addWidget(self.right_lableme2, 1, 0, 1, 1)
        self.right_layout.addWidget(self.right_lablese2, 1, 1, 1, 1)
        self.right_tableView2.setModel(self.model2)
        self.right_pushbutton2.clicked.connect(self.search_f)
        self.right_tableView2.clicked.connect(self.battle2)

    def searchbyname(self):
        if self.status == 3:
            return
        if self.status != 3:
            from removewidget import RemoveWidget
            RemoveWidget.autoremove(self)
        self.status = 3
        self.right_tableView3 = QtWidgets.QTableView()
        self.model3 = QStandardItemModel(4, 4, self.right_tableView3)
        self.model3.setHorizontalHeaderLabels(['姓名', '班级', '电话', '学号'])
        self.right_tableView3.setMaximumHeight(100)
        self.right_pushbutton3 = QtWidgets.QPushButton('点击搜索')
        self.right_pushbutton3.setStyleSheet('''QPushButton{
        padding: 10px 20px;
        font-size: 15px;
        text-align: center;
        text-decoration: none;
        outline: none;
        color: #fff;
        background-color: #4CAF50;
        border: none;
        border-radius: 15px;}
        QPushButton:hover {background-color: #3e8e41}
        ''')
        self.right_lablese3 = QtWidgets.QLabel()
        self.right_lablese3.setMaximumSize(300, 400)
        self.right_lablese3.setText('查找后的照片！')
        self.right_lablese3.setStyleSheet(
            'QLabel{border: 1px solid #ccc!important;padding:14px;border-radius: 16px!important;margin-left:auto;margin-right:auto;}')
        self.right_lineedit = QtWidgets.QLineEdit()
        self.right_lineedit.setPlaceholderText('在这里输入你要搜索的名字：')
        self.right_layout.addWidget(self.right_tableView3, 0, 0, 1, 1)
        self.right_layout.addWidget(self.right_pushbutton3, 3, 0, 1, 1)
        self.right_layout.addWidget(self.right_lablese3, 1, 0, 1, 1)
        self.right_layout.addWidget(self.right_lineedit, 2, 0, 1, 1)
        self.right_tableView3.setModel(self.model3)
        self.right_pushbutton3.clicked.connect(self.search_n)
        self.right_tableView3.clicked.connect(self.battle3)

    def infomation(self):
        if self.status == 4:
            return
        if self.status != 4:
            from removewidget import RemoveWidget
            RemoveWidget.autoremove(self)
        self.status = 4
        self.right_help = QtWidgets.QLabel()
        self.right_help.setObjectName('lable')
        self.right_help.setText("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">本软件遵循GPL2.0协议开发</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">数据来源：宥马运动，山东科技职业学院JAVA教务平台</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">请务必联网使用</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">人脸搜索：百度API</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:600; color:#ff0000;\">由于此软件已经触碰到法律，请勿大面积传播！</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt;\"><br /></p></body></html>")
        self.right_help.setAlignment(QtCore.Qt.AlignCenter)
        # self.right_help.setMinimumHeight(30)
        self.right_help.setStyleSheet('''
        QLabel{
        border-style:none;
        border-radius:0px;
        padding:5px;
        color:#000000;
        background:qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 #E4E4E4,stop:1 #A2A2A2);
        }''')
        self.right_layout.addWidget(self.right_help, 0, 0, 4, 1)

    def getinfo(self):
        if self.status == 5:
            return
        if self.status != 5:
            from removewidget import RemoveWidget
            RemoveWidget.autoremove(self)
        self.status = 5
        self.right_rec = QtWidgets.QLabel()
        self.right_rec.setObjectName('lable')
        self.right_rec.setText("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:20pt;\">邮箱:</span><span style=\" font-family:\'lucida Grande,Verdana,Microsoft YaHei\'; font-size:20pt; color:#aaaaff; background-color:#ffffff;\">zhuwx1998@qq.com</span></p></body></html>")
        self.right_rec.setAlignment(QtCore.Qt.AlignCenter)
        self.right_rec.setStyleSheet('''
                QLabel{
                border-style:none;
                border-radius:0px;
                padding:5px;
                color:#000000;
                background:qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 #E4E4E4,stop:1 #A2A2A2);
                }''')
        self.right_layout.addWidget(self.right_rec, 0, 0, 4, 1)

    def search_p(self):
        try:
            conn = sqlite3.connect('test.db')
            c = conn.cursor()
            get_img_from_camera_local('./take/yourface.jpg')
            findmess = searchface(token=token, pic_data=imgdata('./take/yourface.jpg'))
            row = 0
            firstone = findmess[0]['user_info']
            # print(firstone)
            for mess in findmess:
                self.model.setItem(row, 0, QStandardItem(mess['user_info'][12:]))
                self.model.setItem(row, 3, QStandardItem(mess['user_info'][:12]))
                sqlmes = c.execute("SELECT majorName,phone from Message001 where studentNo like " + "\'" + str(
                    mess['user_info'][:12]) + "\'").fetchall()
                print(sqlmes)
                if len(sqlmes) > 0:
                    self.model.setItem(row, 1, QStandardItem(sqlmes[0][0]))
                    self.model.setItem(row, 2, QStandardItem(sqlmes[0][1]))
                row += 1
                r = requests.get('http://www.xiaoyuan666.com:8081/' + mess['user_info'][:] + '.png')
                file = open('./take/' + mess['user_info'][:] + '.jpg', 'wb')
                file.write(r.content)
                file.close()
            image = QImage('./take/yourface.jpg')
            newimg = image.scaled(230, 400)
            image2 = QImage('./take/' + firstone + '.jpg')
            newimg2 = image2.scaled(230, 400)
            self.right_lableme.setPixmap(QPixmap.fromImage(newimg))
            self.right_lablese.setPixmap(QPixmap.fromImage(newimg2))
            c.close()
            conn.close()
        except BaseException:
            return

    def battle(self, bala):
        if self.model.item(bala.row(), 0) is not None:
            filename = self.model.item(bala.row(), 3).text() + self.model.item(bala.row(), 0).text()
            image = QImage('./take/' + filename + '.jpg')
            newimg = image.scaled(230, 400)
            self.right_lablese.setPixmap(QPixmap.fromImage(newimg))

    def battle2(self, bala):
        if self.model2.item(bala.row(), 0) is not None:
            filename = self.model2.item(bala.row(), 3).text() + self.model2.item(bala.row(), 0).text()
            image = QImage('./take/' + filename + '.jpg')
            newimg = image.scaled(230, 400)
            self.right_lablese2.setPixmap(QPixmap.fromImage(newimg))

    def battle3(self, bala):
        if self.model3.item(bala.row(), 0) is not None:
            filename = self.model3.item(bala.row(), 3).text() + self.model3.item(bala.row(), 0).text()
            image = QImage('./take/' + filename + '.jpg')
            newimg = image.scaled(230, 400)
            self.right_lablese3.setPixmap(QPixmap.fromImage(newimg))

    def search_f(self):
        try:
            openfile_name = QFileDialog.getOpenFileName(QWidget(), '选择图片', './', 'Picture files(*.jpg , *.png, *jepg)')
            conn = sqlite3.connect('test.db')
            c = conn.cursor()
            findmess = searchface(token=token, pic_data=imgdata(openfile_name[0]))
            row = 0
            firstone = findmess[0]['user_info']
            # print(firstone)
            for mess in findmess:
                self.model2.setItem(row, 0, QStandardItem(mess['user_info'][12:]))
                self.model2.setItem(row, 3, QStandardItem(mess['user_info'][:12]))
                sqlmes = c.execute("SELECT majorName,phone from Message001 where studentNo like " + "\'" + str(
                    mess['user_info'][:12]) + "\'").fetchall()
                print(sqlmes)
                if len(sqlmes) > 0:
                    self.model2.setItem(row, 1, QStandardItem(sqlmes[0][0]))
                    self.model2.setItem(row, 2, QStandardItem(sqlmes[0][1]))
                row += 1
                r = requests.get('http://www.xiaoyuan666.com:8081/' + mess['user_info'][:] + '.png')
                file = open('./take/' + mess['user_info'][:] + '.jpg', 'wb')
                file.write(r.content)
                file.close()
            image = QImage(openfile_name[0])
            newimg = image.scaled(230, 400)
            image2 = QImage('./take/' + firstone + '.jpg')
            newimg2 = image2.scaled(230, 400)
            self.right_lableme2.setPixmap(QPixmap.fromImage(newimg))
            self.right_lablese2.setPixmap(QPixmap.fromImage(newimg2))
            c.close()
            conn.close()
        except BaseException:
            return

    def search_n(self):
        try:
            conn = sqlite3.connect('test.db')
            c = conn.cursor()
            row = 0
            sqlmes = c.execute(
                "SELECT realName,majorName,phone,studentNo from Message001 where realName like " + "\'" + str(
                    self.right_lineedit.text()) + "\'").fetchall()
            for mess in sqlmes:
                self.model3.setItem(row, 0, QStandardItem(mess[0]))
                self.model3.setItem(row, 1, QStandardItem(mess[1]))
                self.model3.setItem(row, 2, QStandardItem(mess[2]))
                self.model3.setItem(row, 3, QStandardItem(mess[3]))
                r = requests.get('http://www.xiaoyuan666.com:8081/' + mess[3] + mess[0] + '.png')
                file = open('./take/' + mess[3] + mess[0] + '.jpg', 'wb')
                file.write(r.content)
                file.close()
                row += 1
            image2 = QImage('./take/' + mess[3] + mess[0] + '.jpg')
            newimg2 = image2.scaled(230, 400)
            self.right_lablese3.setPixmap(QPixmap.fromImage(newimg2))
            c.close()
            conn.close()
        except BaseException:
            return


def closeWin():
    qApp = QApplication.instance()
    qApp.quit()


def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.left_close.clicked.connect(closeWin)
    gui.left_visit.clicked.connect(gui.showMinimized)
    gui.left_mini.clicked.connect(gui.showMinimized)
    gui.left_searchbyface.clicked.connect(gui.take_picture)
    gui.left_searchbyface_p.clicked.connect(gui.uploadpic)
    gui.left_searchbyname.clicked.connect(gui.searchbyname)
    gui.left_help.clicked.connect(gui.infomation)
    gui.left_request.clicked.connect(gui.getinfo)
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    try:
        token = get_token()
    except BaseException:
        bat = MainUi()
        bat.take_picture()
        bat.right_lablese.setText('请联网后重试！')
    main()

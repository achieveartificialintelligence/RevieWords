import sys  # main函数使用
from peewee import *  # 数据库引擎
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, QStringListModel
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListView, QMessageBox
from playsound import playsound


# 数据库连接
db = MySQLDatabase(
    host="",
    port=3306,
    user="",
    password="",
    database="")

# 数据库设计


class RiCheng(Model):
    cishu = IntegerField()  # 次数
    shijian = CharField()  # 事件名
    riqi = CharField()  # 日期

    class Meta:
        database = db

# QDate转str


def StrDate(date):
    DD = str(date.year())
    if date.month() < 10:
        DD += '0'
    DD += str(date.month())
    if date.day() < 10:
        DD += '0'
    DD += str(date.day())
    return DD

# 今天后的日期计算，


def AfterDays(date, num):
    date = date.addDays(num)
    return StrDate(date)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(864, 510)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(0, 0, 392, 251))
        self.calendarWidget.setObjectName("calendarWidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 300, 371, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 270, 241, 16))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 410, 181, 81))
        self.pushButton.setObjectName("pushButton")
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(400, 10, 451, 491))
        self.listView.setObjectName("listView")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(10, 370, 121, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 340, 121, 16))
        self.label_2.setObjectName("label_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(200, 410, 181, 81))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(200, 350, 181, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 仅保留关闭键
        MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

        # 禁用窗口拉伸
        MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())

        # 日历点击后的槽函数
        self.calendarWidget.clicked[QDate].connect(self.showDate)

        # 点击执行后的槽函数
        self.pushButton.clicked.connect(self.tijiao)

        # 点击删除后的槽函数
        self.pushButton_2.clicked.connect(self.shanchu)

        # 点击刷新的槽函数
        self.pushButton_3.clicked.connect(self.todaytxt)

        # 默认次数为1
        self.lineEdit_2.setText('0')

        # 单击事件
        self.listView.clicked.connect(self.danji)

        # 双击事件
        self.listView.doubleClicked.connect(self.shuangji)

        # 自动显示今天日程
        self.chaxun(self.calendarWidget.selectedDate())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "孙哥哥考研复习程序"))
        self.label.setText(_translate("MainWindow", "事项名称："))
        self.pushButton.setText(_translate("MainWindow", "增加事项"))
        self.label_2.setText(_translate("MainWindow", "起始次数："))
        self.pushButton_2.setText(_translate("MainWindow", "删除事项"))
        self.pushButton_3.setText(_translate("MainWindow", "刷新今天"))

    # 查询函数
    def chaxun(self, date):
        if db.is_closed():
            db.connect()
        # Listview 需要使用model
        slm = QStringListModel()  # 创建model
        self.qList = []  # 添加的数组数据

        # 将查询后的数据输入model
        for d in RiCheng.select().where(RiCheng.riqi == StrDate(date)):
            self.qList.append(str(RiCheng[d].cishu)+"\t"+RiCheng[d].shijian)

        self.qList.sort()  # 排序
        slm.setStringList(self.qList)  # 将数据设置到model
        self.listView.setModel(slm)  # 绑定 listView 和 model

        db.close()

    # 日历日期选择
    def showDate(self, date):
        TTT = "距离考研："
        TTT += str(self.calendarWidget.selectedDate().daysTo(QDate(2020, 12, 21)))+"天"
        MainWindow.setWindowTitle(TTT)
        self.chaxun(date)

    # 单击事件
    def danji(self, index):
        db.connect()
        s = self.qList[index.row()].split('\t')
        print(s)
        self.lineEdit.setText(s[1])
        self.lineEdit_2.setText(s[0])

        # 窗口显示共多少项
        TT = RiCheng.select().where(RiCheng.shijian == s[1]).count()
        MainWindow.setWindowTitle("共"+str(TT)+"项")

        db.close()

    # 删除
    def shanchu(self):
        db.connect()

        sj = self.lineEdit.text()
        if sj == db.database:
            RiCheng.drop_table()
            # 显示当前日期日程
            MainWindow.setWindowTitle("全部表删除完成")
            RiCheng.create_table()
            self.chaxun(self.calendarWidget.selectedDate())
        else:
            RiCheng.delete().where(RiCheng.shijian == sj).execute()

            # 显示当前日期日程
            self.chaxun(self.calendarWidget.selectedDate())
            MainWindow.setWindowTitle("删除完成")

        db.close()

    # 双击删除事项
    def shuangji(self, index):
        db.connect()

        playsound('nice.mp3')
        # 分割字符
        s = self.qList[index.row()].split('\t')
        print(s)

        RiCheng.delete().where((RiCheng.cishu == s[0]) & (
            RiCheng.shijian == s[1])).execute()
        self.lineEdit.setText(s[1])
        self.lineEdit_2.setText(s[0])

        # 显示当前日期日程
        self.chaxun(self.calendarWidget.selectedDate())

        # 窗口显示共多少项
        TT = RiCheng.select().where(RiCheng.shijian == s[1]).count()
        MainWindow.setWindowTitle("共"+str(TT)+"项")

        db.close()

    # 添加事件
    def tijiao(self):
        db.connect()

        DD = self.calendarWidget.selectedDate()
        sj = self.lineEdit.text()
        cs = int(self.lineEdit_2.text())

        # 判断第几次事件，【核心代码】
        if cs != 1:
            DD = self.calendarWidget.selectedDate().addDays(-2**(cs-1)+1)

        # 添加8次事件，【核心代码】
        # 间隔日期：1 , 2 , 3 , 4 , 5  ,  6  ,  7
        # 对应间隔：  1 , 2 , 4 , 8 ， 16 ,  32
        while(cs <= 7):
            rq = AfterDays(DD, 2**(cs-1)-1)
            RiCheng.insert(cishu=int(cs), shijian=sj, riqi=rq).execute()
            cs += 1
            print(rq)

        self.lineEdit_2.setText('1')

        self.chaxun(self.calendarWidget.selectedDate())
        MainWindow.setWindowTitle("增加完成")

        db.close()

    # 刷新今天
    def todaytxt(self):

        TTT = "刷新"
        TTT += str(QDate.currentDate().month())+"月"
        TTT += str(QDate.currentDate().day())+"日"
        self.pushButton_3.setText(TTT)
        # 选中今天

        self.calendarWidget.setSelectedDate(QDate.currentDate())
        self.lineEdit.setText("")
        self.lineEdit_2.setText('0')

        TTT = "距离考研：" + \
            str(self.calendarWidget.selectedDate().daysTo(QDate(2020, 12, 21)))+"天"
        MainWindow.setWindowTitle(TTT)
        # 显示当前日期日程
        self.chaxun(self.calendarWidget.selectedDate())

        print("刷新完成")


# 主程序设计
if __name__ == "__main__":
    # 判断表是否存在
    if not RiCheng.table_exists():
        RiCheng.create_table()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

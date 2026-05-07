# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_PM.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QPushButton, QRadioButton, QScrollArea, QSizePolicy,
    QStackedWidget, QStatusBar, QTabWidget, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)
class Ui_PM(object):
    def setupUi(self, PM):
        if not PM.objectName():
            PM.setObjectName(u"PM")
        PM.resize(1137, 684)
        font = QFont()
        font.setPointSize(9)
        PM.setFont(font)
        PM.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.centralwidget = QWidget(PM)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        font1 = QFont()
        font1.setFamilies([u"Tahoma"])
        font1.setPointSize(8)
        font1.setBold(False)
        self.widget.setFont(font1)
        self.widget.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget_4 = QWidget(self.widget)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setMinimumSize(QSize(613, 34))
        self.widget_4.setFont(font1)
        self.widget_4.setStyleSheet(u"background-color: rgb(200, 200, 200);\n"
"border-radius: 8px;")
        self.horizontalLayout = QHBoxLayout(self.widget_4)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.widget_4)
        self.label.setObjectName(u"label")
        font2 = QFont()
        font2.setFamilies([u"Tahoma"])
        font2.setPointSize(12)
        font2.setBold(True)
        self.label.setFont(font2)
        self.label.setStyleSheet(u"")
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label)


        self.verticalLayout_2.addWidget(self.widget_4, 0, Qt.AlignTop)

        self.widget_5 = QWidget(self.widget)
        self.widget_5.setObjectName(u"widget_5")
        self.widget_5.setFont(font1)
        self.horizontalLayout_2 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.widget_5)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 0))
        self.frame.setFont(font1)
        self.frame.setStyleSheet(u"")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font1)

        self.horizontalLayout_3.addWidget(self.label_2)

        self.lineEdit = QLineEdit(self.frame)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setFont(font1)

        self.horizontalLayout_3.addWidget(self.lineEdit)


        self.horizontalLayout_2.addWidget(self.frame, 0, Qt.AlignTop)

        self.frame_2 = QFrame(self.widget_5)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFont(font1)
        self.frame_2.setStyleSheet(u"")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(self.frame_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)

        self.horizontalLayout_4.addWidget(self.label_3)

        self.lineEdit_2 = QLineEdit(self.frame_2)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setFont(font1)

        self.horizontalLayout_4.addWidget(self.lineEdit_2)


        self.horizontalLayout_2.addWidget(self.frame_2, 0, Qt.AlignTop)

        self.widget_6 = QWidget(self.widget_5)
        self.widget_6.setObjectName(u"widget_6")
        self.widget_6.setFont(font1)
        self.widget_6.setStyleSheet(u"")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_5 = QLabel(self.widget_6)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font1)

        self.horizontalLayout_6.addWidget(self.label_5)

        self.efpc = QRadioButton(self.widget_6)
        self.efpc.setObjectName(u"efpc")
        self.efpc.setFont(font1)

        self.horizontalLayout_6.addWidget(self.efpc)

        self.smt = QRadioButton(self.widget_6)
        self.smt.setObjectName(u"smt")
        self.smt.setFont(font1)

        self.horizontalLayout_6.addWidget(self.smt)


        self.horizontalLayout_2.addWidget(self.widget_6)

        self.frame_3 = QFrame(self.widget_5)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFont(font1)
        self.frame_3.setStyleSheet(u"")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_4 = QLabel(self.frame_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font1)

        self.horizontalLayout_5.addWidget(self.label_4)

        self.lineEdit_3 = QLineEdit(self.frame_3)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setFont(font1)

        self.horizontalLayout_5.addWidget(self.lineEdit_3)

        self.label_6 = QLabel(self.frame_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font1)

        self.horizontalLayout_5.addWidget(self.label_6)


        self.horizontalLayout_2.addWidget(self.frame_3, 0, Qt.AlignTop)


        self.verticalLayout_2.addWidget(self.widget_5, 0, Qt.AlignTop)


        self.verticalLayout.addWidget(self.widget, 0, Qt.AlignTop)

        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setMinimumSize(QSize(300, 300))
        self.widget_2.setMaximumSize(QSize(16777215, 16777215))
        self.widget_2.setFont(font1)
        self.widget_2.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.verticalLayout_3 = QVBoxLayout(self.widget_2)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.widget_7 = QWidget(self.widget_2)
        self.widget_7.setObjectName(u"widget_7")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_7.sizePolicy().hasHeightForWidth())
        self.widget_7.setSizePolicy(sizePolicy1)
        self.widget_7.setFont(font1)
        self.horizontalLayout_7 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.widget_8 = QWidget(self.widget_7)
        self.widget_8.setObjectName(u"widget_8")
        self.widget_8.setMinimumSize(QSize(432, 430))
        self.widget_8.setFont(font1)
        self.horizontalLayout_10 = QHBoxLayout(self.widget_8)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.tableWidget = QTableWidget(self.widget_8)
        if (self.tableWidget.columnCount() < 10):
            self.tableWidget.setColumnCount(10)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        if (self.tableWidget.rowCount() < 30):
            self.tableWidget.setRowCount(30)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(7, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(8, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(9, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(10, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(11, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(12, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(13, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(14, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(15, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(16, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(17, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(18, __qtablewidgetitem28)
        __qtablewidgetitem29 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(19, __qtablewidgetitem29)
        __qtablewidgetitem30 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(20, __qtablewidgetitem30)
        __qtablewidgetitem31 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(21, __qtablewidgetitem31)
        __qtablewidgetitem32 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(22, __qtablewidgetitem32)
        __qtablewidgetitem33 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(23, __qtablewidgetitem33)
        __qtablewidgetitem34 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(24, __qtablewidgetitem34)
        __qtablewidgetitem35 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(25, __qtablewidgetitem35)
        __qtablewidgetitem36 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(26, __qtablewidgetitem36)
        __qtablewidgetitem37 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(27, __qtablewidgetitem37)
        __qtablewidgetitem38 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(28, __qtablewidgetitem38)
        __qtablewidgetitem39 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(29, __qtablewidgetitem39)
        font3 = QFont()
        font3.setPointSize(7)
        __qtablewidgetitem40 = QTableWidgetItem()
        __qtablewidgetitem40.setFont(font3);
        self.tableWidget.setItem(0, 0, __qtablewidgetitem40)
        __qtablewidgetitem41 = QTableWidgetItem()
        self.tableWidget.setItem(0, 1, __qtablewidgetitem41)
        __qtablewidgetitem42 = QTableWidgetItem()
        self.tableWidget.setItem(0, 2, __qtablewidgetitem42)
        __qtablewidgetitem43 = QTableWidgetItem()
        self.tableWidget.setItem(0, 3, __qtablewidgetitem43)
        __qtablewidgetitem44 = QTableWidgetItem()
        self.tableWidget.setItem(0, 4, __qtablewidgetitem44)
        __qtablewidgetitem45 = QTableWidgetItem()
        self.tableWidget.setItem(0, 5, __qtablewidgetitem45)
        __qtablewidgetitem46 = QTableWidgetItem()
        self.tableWidget.setItem(0, 6, __qtablewidgetitem46)
        __qtablewidgetitem47 = QTableWidgetItem()
        self.tableWidget.setItem(0, 7, __qtablewidgetitem47)
        __qtablewidgetitem48 = QTableWidgetItem()
        self.tableWidget.setItem(0, 8, __qtablewidgetitem48)
        __qtablewidgetitem49 = QTableWidgetItem()
        self.tableWidget.setItem(0, 9, __qtablewidgetitem49)
        __qtablewidgetitem50 = QTableWidgetItem()
        self.tableWidget.setItem(1, 0, __qtablewidgetitem50)
        __qtablewidgetitem51 = QTableWidgetItem()
        self.tableWidget.setItem(1, 1, __qtablewidgetitem51)
        __qtablewidgetitem52 = QTableWidgetItem()
        self.tableWidget.setItem(1, 2, __qtablewidgetitem52)
        __qtablewidgetitem53 = QTableWidgetItem()
        self.tableWidget.setItem(1, 3, __qtablewidgetitem53)
        __qtablewidgetitem54 = QTableWidgetItem()
        self.tableWidget.setItem(1, 4, __qtablewidgetitem54)
        __qtablewidgetitem55 = QTableWidgetItem()
        self.tableWidget.setItem(1, 5, __qtablewidgetitem55)
        __qtablewidgetitem56 = QTableWidgetItem()
        self.tableWidget.setItem(1, 6, __qtablewidgetitem56)
        __qtablewidgetitem57 = QTableWidgetItem()
        self.tableWidget.setItem(1, 7, __qtablewidgetitem57)
        __qtablewidgetitem58 = QTableWidgetItem()
        self.tableWidget.setItem(1, 8, __qtablewidgetitem58)
        __qtablewidgetitem59 = QTableWidgetItem()
        self.tableWidget.setItem(1, 9, __qtablewidgetitem59)
        __qtablewidgetitem60 = QTableWidgetItem()
        self.tableWidget.setItem(2, 0, __qtablewidgetitem60)
        __qtablewidgetitem61 = QTableWidgetItem()
        self.tableWidget.setItem(2, 1, __qtablewidgetitem61)
        __qtablewidgetitem62 = QTableWidgetItem()
        self.tableWidget.setItem(2, 2, __qtablewidgetitem62)
        __qtablewidgetitem63 = QTableWidgetItem()
        self.tableWidget.setItem(2, 3, __qtablewidgetitem63)
        __qtablewidgetitem64 = QTableWidgetItem()
        self.tableWidget.setItem(2, 4, __qtablewidgetitem64)
        __qtablewidgetitem65 = QTableWidgetItem()
        self.tableWidget.setItem(2, 5, __qtablewidgetitem65)
        __qtablewidgetitem66 = QTableWidgetItem()
        self.tableWidget.setItem(2, 6, __qtablewidgetitem66)
        __qtablewidgetitem67 = QTableWidgetItem()
        self.tableWidget.setItem(2, 7, __qtablewidgetitem67)
        __qtablewidgetitem68 = QTableWidgetItem()
        self.tableWidget.setItem(2, 8, __qtablewidgetitem68)
        __qtablewidgetitem69 = QTableWidgetItem()
        self.tableWidget.setItem(2, 9, __qtablewidgetitem69)
        __qtablewidgetitem70 = QTableWidgetItem()
        self.tableWidget.setItem(3, 0, __qtablewidgetitem70)
        __qtablewidgetitem71 = QTableWidgetItem()
        self.tableWidget.setItem(3, 1, __qtablewidgetitem71)
        __qtablewidgetitem72 = QTableWidgetItem()
        self.tableWidget.setItem(3, 2, __qtablewidgetitem72)
        __qtablewidgetitem73 = QTableWidgetItem()
        self.tableWidget.setItem(3, 3, __qtablewidgetitem73)
        __qtablewidgetitem74 = QTableWidgetItem()
        self.tableWidget.setItem(3, 4, __qtablewidgetitem74)
        __qtablewidgetitem75 = QTableWidgetItem()
        self.tableWidget.setItem(3, 5, __qtablewidgetitem75)
        __qtablewidgetitem76 = QTableWidgetItem()
        self.tableWidget.setItem(3, 6, __qtablewidgetitem76)
        __qtablewidgetitem77 = QTableWidgetItem()
        self.tableWidget.setItem(3, 7, __qtablewidgetitem77)
        __qtablewidgetitem78 = QTableWidgetItem()
        self.tableWidget.setItem(3, 8, __qtablewidgetitem78)
        __qtablewidgetitem79 = QTableWidgetItem()
        self.tableWidget.setItem(3, 9, __qtablewidgetitem79)
        __qtablewidgetitem80 = QTableWidgetItem()
        self.tableWidget.setItem(4, 0, __qtablewidgetitem80)
        __qtablewidgetitem81 = QTableWidgetItem()
        self.tableWidget.setItem(4, 1, __qtablewidgetitem81)
        __qtablewidgetitem82 = QTableWidgetItem()
        self.tableWidget.setItem(4, 2, __qtablewidgetitem82)
        __qtablewidgetitem83 = QTableWidgetItem()
        self.tableWidget.setItem(4, 3, __qtablewidgetitem83)
        __qtablewidgetitem84 = QTableWidgetItem()
        self.tableWidget.setItem(4, 4, __qtablewidgetitem84)
        __qtablewidgetitem85 = QTableWidgetItem()
        self.tableWidget.setItem(4, 5, __qtablewidgetitem85)
        __qtablewidgetitem86 = QTableWidgetItem()
        self.tableWidget.setItem(4, 6, __qtablewidgetitem86)
        __qtablewidgetitem87 = QTableWidgetItem()
        self.tableWidget.setItem(4, 7, __qtablewidgetitem87)
        __qtablewidgetitem88 = QTableWidgetItem()
        self.tableWidget.setItem(4, 8, __qtablewidgetitem88)
        __qtablewidgetitem89 = QTableWidgetItem()
        self.tableWidget.setItem(4, 9, __qtablewidgetitem89)
        __qtablewidgetitem90 = QTableWidgetItem()
        self.tableWidget.setItem(5, 0, __qtablewidgetitem90)
        __qtablewidgetitem91 = QTableWidgetItem()
        self.tableWidget.setItem(5, 1, __qtablewidgetitem91)
        __qtablewidgetitem92 = QTableWidgetItem()
        self.tableWidget.setItem(5, 2, __qtablewidgetitem92)
        __qtablewidgetitem93 = QTableWidgetItem()
        self.tableWidget.setItem(5, 3, __qtablewidgetitem93)
        __qtablewidgetitem94 = QTableWidgetItem()
        self.tableWidget.setItem(5, 4, __qtablewidgetitem94)
        __qtablewidgetitem95 = QTableWidgetItem()
        self.tableWidget.setItem(5, 5, __qtablewidgetitem95)
        __qtablewidgetitem96 = QTableWidgetItem()
        self.tableWidget.setItem(5, 6, __qtablewidgetitem96)
        __qtablewidgetitem97 = QTableWidgetItem()
        self.tableWidget.setItem(5, 7, __qtablewidgetitem97)
        __qtablewidgetitem98 = QTableWidgetItem()
        self.tableWidget.setItem(5, 8, __qtablewidgetitem98)
        __qtablewidgetitem99 = QTableWidgetItem()
        self.tableWidget.setItem(5, 9, __qtablewidgetitem99)
        __qtablewidgetitem100 = QTableWidgetItem()
        self.tableWidget.setItem(6, 0, __qtablewidgetitem100)
        __qtablewidgetitem101 = QTableWidgetItem()
        self.tableWidget.setItem(6, 1, __qtablewidgetitem101)
        __qtablewidgetitem102 = QTableWidgetItem()
        self.tableWidget.setItem(6, 2, __qtablewidgetitem102)
        __qtablewidgetitem103 = QTableWidgetItem()
        self.tableWidget.setItem(6, 3, __qtablewidgetitem103)
        __qtablewidgetitem104 = QTableWidgetItem()
        self.tableWidget.setItem(6, 4, __qtablewidgetitem104)
        __qtablewidgetitem105 = QTableWidgetItem()
        self.tableWidget.setItem(6, 5, __qtablewidgetitem105)
        __qtablewidgetitem106 = QTableWidgetItem()
        self.tableWidget.setItem(6, 6, __qtablewidgetitem106)
        __qtablewidgetitem107 = QTableWidgetItem()
        self.tableWidget.setItem(6, 7, __qtablewidgetitem107)
        __qtablewidgetitem108 = QTableWidgetItem()
        self.tableWidget.setItem(6, 8, __qtablewidgetitem108)
        __qtablewidgetitem109 = QTableWidgetItem()
        self.tableWidget.setItem(6, 9, __qtablewidgetitem109)
        __qtablewidgetitem110 = QTableWidgetItem()
        self.tableWidget.setItem(7, 0, __qtablewidgetitem110)
        __qtablewidgetitem111 = QTableWidgetItem()
        self.tableWidget.setItem(7, 1, __qtablewidgetitem111)
        __qtablewidgetitem112 = QTableWidgetItem()
        self.tableWidget.setItem(7, 2, __qtablewidgetitem112)
        __qtablewidgetitem113 = QTableWidgetItem()
        self.tableWidget.setItem(7, 3, __qtablewidgetitem113)
        __qtablewidgetitem114 = QTableWidgetItem()
        self.tableWidget.setItem(7, 4, __qtablewidgetitem114)
        __qtablewidgetitem115 = QTableWidgetItem()
        self.tableWidget.setItem(7, 5, __qtablewidgetitem115)
        __qtablewidgetitem116 = QTableWidgetItem()
        self.tableWidget.setItem(7, 6, __qtablewidgetitem116)
        __qtablewidgetitem117 = QTableWidgetItem()
        self.tableWidget.setItem(7, 7, __qtablewidgetitem117)
        __qtablewidgetitem118 = QTableWidgetItem()
        self.tableWidget.setItem(7, 8, __qtablewidgetitem118)
        __qtablewidgetitem119 = QTableWidgetItem()
        self.tableWidget.setItem(7, 9, __qtablewidgetitem119)
        __qtablewidgetitem120 = QTableWidgetItem()
        self.tableWidget.setItem(8, 0, __qtablewidgetitem120)
        __qtablewidgetitem121 = QTableWidgetItem()
        self.tableWidget.setItem(8, 1, __qtablewidgetitem121)
        __qtablewidgetitem122 = QTableWidgetItem()
        self.tableWidget.setItem(8, 2, __qtablewidgetitem122)
        __qtablewidgetitem123 = QTableWidgetItem()
        self.tableWidget.setItem(8, 3, __qtablewidgetitem123)
        __qtablewidgetitem124 = QTableWidgetItem()
        self.tableWidget.setItem(8, 4, __qtablewidgetitem124)
        __qtablewidgetitem125 = QTableWidgetItem()
        self.tableWidget.setItem(8, 5, __qtablewidgetitem125)
        __qtablewidgetitem126 = QTableWidgetItem()
        self.tableWidget.setItem(8, 6, __qtablewidgetitem126)
        __qtablewidgetitem127 = QTableWidgetItem()
        self.tableWidget.setItem(8, 7, __qtablewidgetitem127)
        __qtablewidgetitem128 = QTableWidgetItem()
        self.tableWidget.setItem(8, 8, __qtablewidgetitem128)
        __qtablewidgetitem129 = QTableWidgetItem()
        self.tableWidget.setItem(8, 9, __qtablewidgetitem129)
        __qtablewidgetitem130 = QTableWidgetItem()
        self.tableWidget.setItem(9, 0, __qtablewidgetitem130)
        __qtablewidgetitem131 = QTableWidgetItem()
        self.tableWidget.setItem(9, 1, __qtablewidgetitem131)
        __qtablewidgetitem132 = QTableWidgetItem()
        self.tableWidget.setItem(9, 2, __qtablewidgetitem132)
        __qtablewidgetitem133 = QTableWidgetItem()
        self.tableWidget.setItem(9, 3, __qtablewidgetitem133)
        __qtablewidgetitem134 = QTableWidgetItem()
        self.tableWidget.setItem(9, 4, __qtablewidgetitem134)
        __qtablewidgetitem135 = QTableWidgetItem()
        self.tableWidget.setItem(9, 5, __qtablewidgetitem135)
        __qtablewidgetitem136 = QTableWidgetItem()
        self.tableWidget.setItem(9, 6, __qtablewidgetitem136)
        __qtablewidgetitem137 = QTableWidgetItem()
        self.tableWidget.setItem(9, 7, __qtablewidgetitem137)
        __qtablewidgetitem138 = QTableWidgetItem()
        self.tableWidget.setItem(9, 8, __qtablewidgetitem138)
        __qtablewidgetitem139 = QTableWidgetItem()
        self.tableWidget.setItem(9, 9, __qtablewidgetitem139)
        __qtablewidgetitem140 = QTableWidgetItem()
        self.tableWidget.setItem(10, 0, __qtablewidgetitem140)
        __qtablewidgetitem141 = QTableWidgetItem()
        self.tableWidget.setItem(10, 1, __qtablewidgetitem141)
        __qtablewidgetitem142 = QTableWidgetItem()
        self.tableWidget.setItem(10, 2, __qtablewidgetitem142)
        __qtablewidgetitem143 = QTableWidgetItem()
        self.tableWidget.setItem(10, 3, __qtablewidgetitem143)
        __qtablewidgetitem144 = QTableWidgetItem()
        self.tableWidget.setItem(10, 4, __qtablewidgetitem144)
        __qtablewidgetitem145 = QTableWidgetItem()
        self.tableWidget.setItem(10, 5, __qtablewidgetitem145)
        __qtablewidgetitem146 = QTableWidgetItem()
        self.tableWidget.setItem(10, 6, __qtablewidgetitem146)
        __qtablewidgetitem147 = QTableWidgetItem()
        self.tableWidget.setItem(10, 7, __qtablewidgetitem147)
        __qtablewidgetitem148 = QTableWidgetItem()
        self.tableWidget.setItem(10, 8, __qtablewidgetitem148)
        __qtablewidgetitem149 = QTableWidgetItem()
        self.tableWidget.setItem(10, 9, __qtablewidgetitem149)
        __qtablewidgetitem150 = QTableWidgetItem()
        self.tableWidget.setItem(11, 0, __qtablewidgetitem150)
        __qtablewidgetitem151 = QTableWidgetItem()
        self.tableWidget.setItem(11, 1, __qtablewidgetitem151)
        __qtablewidgetitem152 = QTableWidgetItem()
        self.tableWidget.setItem(11, 2, __qtablewidgetitem152)
        __qtablewidgetitem153 = QTableWidgetItem()
        self.tableWidget.setItem(11, 3, __qtablewidgetitem153)
        __qtablewidgetitem154 = QTableWidgetItem()
        self.tableWidget.setItem(11, 4, __qtablewidgetitem154)
        __qtablewidgetitem155 = QTableWidgetItem()
        self.tableWidget.setItem(11, 5, __qtablewidgetitem155)
        __qtablewidgetitem156 = QTableWidgetItem()
        self.tableWidget.setItem(11, 6, __qtablewidgetitem156)
        __qtablewidgetitem157 = QTableWidgetItem()
        self.tableWidget.setItem(11, 7, __qtablewidgetitem157)
        __qtablewidgetitem158 = QTableWidgetItem()
        self.tableWidget.setItem(11, 8, __qtablewidgetitem158)
        __qtablewidgetitem159 = QTableWidgetItem()
        self.tableWidget.setItem(11, 9, __qtablewidgetitem159)
        __qtablewidgetitem160 = QTableWidgetItem()
        self.tableWidget.setItem(12, 0, __qtablewidgetitem160)
        __qtablewidgetitem161 = QTableWidgetItem()
        self.tableWidget.setItem(12, 1, __qtablewidgetitem161)
        __qtablewidgetitem162 = QTableWidgetItem()
        self.tableWidget.setItem(12, 2, __qtablewidgetitem162)
        __qtablewidgetitem163 = QTableWidgetItem()
        self.tableWidget.setItem(12, 3, __qtablewidgetitem163)
        __qtablewidgetitem164 = QTableWidgetItem()
        self.tableWidget.setItem(12, 4, __qtablewidgetitem164)
        __qtablewidgetitem165 = QTableWidgetItem()
        self.tableWidget.setItem(12, 5, __qtablewidgetitem165)
        __qtablewidgetitem166 = QTableWidgetItem()
        self.tableWidget.setItem(12, 6, __qtablewidgetitem166)
        __qtablewidgetitem167 = QTableWidgetItem()
        self.tableWidget.setItem(12, 7, __qtablewidgetitem167)
        __qtablewidgetitem168 = QTableWidgetItem()
        self.tableWidget.setItem(12, 8, __qtablewidgetitem168)
        __qtablewidgetitem169 = QTableWidgetItem()
        self.tableWidget.setItem(12, 9, __qtablewidgetitem169)
        __qtablewidgetitem170 = QTableWidgetItem()
        self.tableWidget.setItem(13, 0, __qtablewidgetitem170)
        __qtablewidgetitem171 = QTableWidgetItem()
        self.tableWidget.setItem(13, 1, __qtablewidgetitem171)
        __qtablewidgetitem172 = QTableWidgetItem()
        self.tableWidget.setItem(13, 2, __qtablewidgetitem172)
        __qtablewidgetitem173 = QTableWidgetItem()
        self.tableWidget.setItem(13, 3, __qtablewidgetitem173)
        __qtablewidgetitem174 = QTableWidgetItem()
        self.tableWidget.setItem(13, 4, __qtablewidgetitem174)
        __qtablewidgetitem175 = QTableWidgetItem()
        self.tableWidget.setItem(13, 5, __qtablewidgetitem175)
        __qtablewidgetitem176 = QTableWidgetItem()
        self.tableWidget.setItem(13, 6, __qtablewidgetitem176)
        __qtablewidgetitem177 = QTableWidgetItem()
        self.tableWidget.setItem(13, 7, __qtablewidgetitem177)
        __qtablewidgetitem178 = QTableWidgetItem()
        self.tableWidget.setItem(13, 8, __qtablewidgetitem178)
        __qtablewidgetitem179 = QTableWidgetItem()
        self.tableWidget.setItem(13, 9, __qtablewidgetitem179)
        __qtablewidgetitem180 = QTableWidgetItem()
        self.tableWidget.setItem(14, 0, __qtablewidgetitem180)
        __qtablewidgetitem181 = QTableWidgetItem()
        self.tableWidget.setItem(14, 1, __qtablewidgetitem181)
        __qtablewidgetitem182 = QTableWidgetItem()
        self.tableWidget.setItem(14, 2, __qtablewidgetitem182)
        __qtablewidgetitem183 = QTableWidgetItem()
        self.tableWidget.setItem(14, 3, __qtablewidgetitem183)
        __qtablewidgetitem184 = QTableWidgetItem()
        self.tableWidget.setItem(14, 4, __qtablewidgetitem184)
        __qtablewidgetitem185 = QTableWidgetItem()
        self.tableWidget.setItem(14, 5, __qtablewidgetitem185)
        __qtablewidgetitem186 = QTableWidgetItem()
        self.tableWidget.setItem(14, 6, __qtablewidgetitem186)
        __qtablewidgetitem187 = QTableWidgetItem()
        self.tableWidget.setItem(14, 7, __qtablewidgetitem187)
        __qtablewidgetitem188 = QTableWidgetItem()
        self.tableWidget.setItem(14, 8, __qtablewidgetitem188)
        __qtablewidgetitem189 = QTableWidgetItem()
        self.tableWidget.setItem(14, 9, __qtablewidgetitem189)
        __qtablewidgetitem190 = QTableWidgetItem()
        self.tableWidget.setItem(15, 0, __qtablewidgetitem190)
        __qtablewidgetitem191 = QTableWidgetItem()
        self.tableWidget.setItem(15, 1, __qtablewidgetitem191)
        __qtablewidgetitem192 = QTableWidgetItem()
        self.tableWidget.setItem(15, 2, __qtablewidgetitem192)
        __qtablewidgetitem193 = QTableWidgetItem()
        self.tableWidget.setItem(15, 3, __qtablewidgetitem193)
        __qtablewidgetitem194 = QTableWidgetItem()
        self.tableWidget.setItem(15, 4, __qtablewidgetitem194)
        __qtablewidgetitem195 = QTableWidgetItem()
        self.tableWidget.setItem(15, 5, __qtablewidgetitem195)
        __qtablewidgetitem196 = QTableWidgetItem()
        self.tableWidget.setItem(15, 6, __qtablewidgetitem196)
        __qtablewidgetitem197 = QTableWidgetItem()
        self.tableWidget.setItem(15, 7, __qtablewidgetitem197)
        __qtablewidgetitem198 = QTableWidgetItem()
        self.tableWidget.setItem(15, 8, __qtablewidgetitem198)
        __qtablewidgetitem199 = QTableWidgetItem()
        self.tableWidget.setItem(15, 9, __qtablewidgetitem199)
        __qtablewidgetitem200 = QTableWidgetItem()
        self.tableWidget.setItem(16, 0, __qtablewidgetitem200)
        __qtablewidgetitem201 = QTableWidgetItem()
        self.tableWidget.setItem(16, 1, __qtablewidgetitem201)
        __qtablewidgetitem202 = QTableWidgetItem()
        self.tableWidget.setItem(16, 2, __qtablewidgetitem202)
        __qtablewidgetitem203 = QTableWidgetItem()
        self.tableWidget.setItem(16, 3, __qtablewidgetitem203)
        __qtablewidgetitem204 = QTableWidgetItem()
        self.tableWidget.setItem(16, 4, __qtablewidgetitem204)
        __qtablewidgetitem205 = QTableWidgetItem()
        self.tableWidget.setItem(16, 5, __qtablewidgetitem205)
        __qtablewidgetitem206 = QTableWidgetItem()
        self.tableWidget.setItem(16, 6, __qtablewidgetitem206)
        __qtablewidgetitem207 = QTableWidgetItem()
        self.tableWidget.setItem(16, 7, __qtablewidgetitem207)
        __qtablewidgetitem208 = QTableWidgetItem()
        self.tableWidget.setItem(16, 8, __qtablewidgetitem208)
        __qtablewidgetitem209 = QTableWidgetItem()
        self.tableWidget.setItem(16, 9, __qtablewidgetitem209)
        __qtablewidgetitem210 = QTableWidgetItem()
        self.tableWidget.setItem(17, 0, __qtablewidgetitem210)
        __qtablewidgetitem211 = QTableWidgetItem()
        self.tableWidget.setItem(17, 1, __qtablewidgetitem211)
        __qtablewidgetitem212 = QTableWidgetItem()
        self.tableWidget.setItem(17, 2, __qtablewidgetitem212)
        __qtablewidgetitem213 = QTableWidgetItem()
        self.tableWidget.setItem(17, 3, __qtablewidgetitem213)
        __qtablewidgetitem214 = QTableWidgetItem()
        self.tableWidget.setItem(17, 4, __qtablewidgetitem214)
        __qtablewidgetitem215 = QTableWidgetItem()
        self.tableWidget.setItem(17, 5, __qtablewidgetitem215)
        __qtablewidgetitem216 = QTableWidgetItem()
        self.tableWidget.setItem(17, 6, __qtablewidgetitem216)
        __qtablewidgetitem217 = QTableWidgetItem()
        self.tableWidget.setItem(17, 7, __qtablewidgetitem217)
        __qtablewidgetitem218 = QTableWidgetItem()
        self.tableWidget.setItem(17, 8, __qtablewidgetitem218)
        __qtablewidgetitem219 = QTableWidgetItem()
        self.tableWidget.setItem(17, 9, __qtablewidgetitem219)
        __qtablewidgetitem220 = QTableWidgetItem()
        self.tableWidget.setItem(18, 0, __qtablewidgetitem220)
        __qtablewidgetitem221 = QTableWidgetItem()
        self.tableWidget.setItem(18, 1, __qtablewidgetitem221)
        __qtablewidgetitem222 = QTableWidgetItem()
        self.tableWidget.setItem(18, 2, __qtablewidgetitem222)
        __qtablewidgetitem223 = QTableWidgetItem()
        self.tableWidget.setItem(18, 3, __qtablewidgetitem223)
        __qtablewidgetitem224 = QTableWidgetItem()
        self.tableWidget.setItem(18, 4, __qtablewidgetitem224)
        __qtablewidgetitem225 = QTableWidgetItem()
        self.tableWidget.setItem(18, 5, __qtablewidgetitem225)
        __qtablewidgetitem226 = QTableWidgetItem()
        self.tableWidget.setItem(18, 6, __qtablewidgetitem226)
        __qtablewidgetitem227 = QTableWidgetItem()
        self.tableWidget.setItem(18, 7, __qtablewidgetitem227)
        __qtablewidgetitem228 = QTableWidgetItem()
        self.tableWidget.setItem(18, 8, __qtablewidgetitem228)
        __qtablewidgetitem229 = QTableWidgetItem()
        self.tableWidget.setItem(18, 9, __qtablewidgetitem229)
        __qtablewidgetitem230 = QTableWidgetItem()
        self.tableWidget.setItem(19, 0, __qtablewidgetitem230)
        __qtablewidgetitem231 = QTableWidgetItem()
        self.tableWidget.setItem(19, 1, __qtablewidgetitem231)
        __qtablewidgetitem232 = QTableWidgetItem()
        self.tableWidget.setItem(19, 2, __qtablewidgetitem232)
        __qtablewidgetitem233 = QTableWidgetItem()
        self.tableWidget.setItem(19, 3, __qtablewidgetitem233)
        __qtablewidgetitem234 = QTableWidgetItem()
        self.tableWidget.setItem(19, 4, __qtablewidgetitem234)
        __qtablewidgetitem235 = QTableWidgetItem()
        self.tableWidget.setItem(19, 5, __qtablewidgetitem235)
        __qtablewidgetitem236 = QTableWidgetItem()
        self.tableWidget.setItem(19, 6, __qtablewidgetitem236)
        __qtablewidgetitem237 = QTableWidgetItem()
        self.tableWidget.setItem(19, 7, __qtablewidgetitem237)
        __qtablewidgetitem238 = QTableWidgetItem()
        self.tableWidget.setItem(19, 8, __qtablewidgetitem238)
        __qtablewidgetitem239 = QTableWidgetItem()
        self.tableWidget.setItem(19, 9, __qtablewidgetitem239)
        __qtablewidgetitem240 = QTableWidgetItem()
        self.tableWidget.setItem(20, 0, __qtablewidgetitem240)
        __qtablewidgetitem241 = QTableWidgetItem()
        self.tableWidget.setItem(20, 1, __qtablewidgetitem241)
        __qtablewidgetitem242 = QTableWidgetItem()
        self.tableWidget.setItem(20, 2, __qtablewidgetitem242)
        __qtablewidgetitem243 = QTableWidgetItem()
        self.tableWidget.setItem(20, 3, __qtablewidgetitem243)
        __qtablewidgetitem244 = QTableWidgetItem()
        self.tableWidget.setItem(20, 4, __qtablewidgetitem244)
        __qtablewidgetitem245 = QTableWidgetItem()
        self.tableWidget.setItem(20, 5, __qtablewidgetitem245)
        __qtablewidgetitem246 = QTableWidgetItem()
        self.tableWidget.setItem(20, 6, __qtablewidgetitem246)
        __qtablewidgetitem247 = QTableWidgetItem()
        self.tableWidget.setItem(20, 7, __qtablewidgetitem247)
        __qtablewidgetitem248 = QTableWidgetItem()
        self.tableWidget.setItem(20, 8, __qtablewidgetitem248)
        __qtablewidgetitem249 = QTableWidgetItem()
        self.tableWidget.setItem(20, 9, __qtablewidgetitem249)
        __qtablewidgetitem250 = QTableWidgetItem()
        self.tableWidget.setItem(21, 0, __qtablewidgetitem250)
        __qtablewidgetitem251 = QTableWidgetItem()
        self.tableWidget.setItem(21, 1, __qtablewidgetitem251)
        __qtablewidgetitem252 = QTableWidgetItem()
        self.tableWidget.setItem(21, 2, __qtablewidgetitem252)
        __qtablewidgetitem253 = QTableWidgetItem()
        self.tableWidget.setItem(21, 3, __qtablewidgetitem253)
        __qtablewidgetitem254 = QTableWidgetItem()
        self.tableWidget.setItem(21, 4, __qtablewidgetitem254)
        __qtablewidgetitem255 = QTableWidgetItem()
        self.tableWidget.setItem(21, 5, __qtablewidgetitem255)
        __qtablewidgetitem256 = QTableWidgetItem()
        self.tableWidget.setItem(21, 6, __qtablewidgetitem256)
        __qtablewidgetitem257 = QTableWidgetItem()
        self.tableWidget.setItem(21, 7, __qtablewidgetitem257)
        __qtablewidgetitem258 = QTableWidgetItem()
        self.tableWidget.setItem(21, 8, __qtablewidgetitem258)
        __qtablewidgetitem259 = QTableWidgetItem()
        self.tableWidget.setItem(21, 9, __qtablewidgetitem259)
        __qtablewidgetitem260 = QTableWidgetItem()
        self.tableWidget.setItem(22, 0, __qtablewidgetitem260)
        __qtablewidgetitem261 = QTableWidgetItem()
        self.tableWidget.setItem(22, 1, __qtablewidgetitem261)
        __qtablewidgetitem262 = QTableWidgetItem()
        self.tableWidget.setItem(22, 2, __qtablewidgetitem262)
        __qtablewidgetitem263 = QTableWidgetItem()
        self.tableWidget.setItem(22, 3, __qtablewidgetitem263)
        __qtablewidgetitem264 = QTableWidgetItem()
        self.tableWidget.setItem(22, 4, __qtablewidgetitem264)
        __qtablewidgetitem265 = QTableWidgetItem()
        self.tableWidget.setItem(22, 5, __qtablewidgetitem265)
        __qtablewidgetitem266 = QTableWidgetItem()
        self.tableWidget.setItem(22, 6, __qtablewidgetitem266)
        __qtablewidgetitem267 = QTableWidgetItem()
        self.tableWidget.setItem(22, 7, __qtablewidgetitem267)
        __qtablewidgetitem268 = QTableWidgetItem()
        self.tableWidget.setItem(22, 8, __qtablewidgetitem268)
        __qtablewidgetitem269 = QTableWidgetItem()
        self.tableWidget.setItem(22, 9, __qtablewidgetitem269)
        __qtablewidgetitem270 = QTableWidgetItem()
        self.tableWidget.setItem(23, 0, __qtablewidgetitem270)
        __qtablewidgetitem271 = QTableWidgetItem()
        self.tableWidget.setItem(23, 1, __qtablewidgetitem271)
        __qtablewidgetitem272 = QTableWidgetItem()
        self.tableWidget.setItem(23, 2, __qtablewidgetitem272)
        __qtablewidgetitem273 = QTableWidgetItem()
        self.tableWidget.setItem(23, 3, __qtablewidgetitem273)
        __qtablewidgetitem274 = QTableWidgetItem()
        self.tableWidget.setItem(23, 4, __qtablewidgetitem274)
        __qtablewidgetitem275 = QTableWidgetItem()
        self.tableWidget.setItem(23, 5, __qtablewidgetitem275)
        __qtablewidgetitem276 = QTableWidgetItem()
        self.tableWidget.setItem(23, 6, __qtablewidgetitem276)
        __qtablewidgetitem277 = QTableWidgetItem()
        self.tableWidget.setItem(23, 7, __qtablewidgetitem277)
        __qtablewidgetitem278 = QTableWidgetItem()
        self.tableWidget.setItem(23, 8, __qtablewidgetitem278)
        __qtablewidgetitem279 = QTableWidgetItem()
        self.tableWidget.setItem(23, 9, __qtablewidgetitem279)
        __qtablewidgetitem280 = QTableWidgetItem()
        self.tableWidget.setItem(24, 0, __qtablewidgetitem280)
        __qtablewidgetitem281 = QTableWidgetItem()
        self.tableWidget.setItem(24, 1, __qtablewidgetitem281)
        __qtablewidgetitem282 = QTableWidgetItem()
        self.tableWidget.setItem(24, 2, __qtablewidgetitem282)
        __qtablewidgetitem283 = QTableWidgetItem()
        self.tableWidget.setItem(24, 3, __qtablewidgetitem283)
        __qtablewidgetitem284 = QTableWidgetItem()
        self.tableWidget.setItem(24, 4, __qtablewidgetitem284)
        __qtablewidgetitem285 = QTableWidgetItem()
        self.tableWidget.setItem(24, 5, __qtablewidgetitem285)
        __qtablewidgetitem286 = QTableWidgetItem()
        self.tableWidget.setItem(24, 6, __qtablewidgetitem286)
        __qtablewidgetitem287 = QTableWidgetItem()
        self.tableWidget.setItem(24, 7, __qtablewidgetitem287)
        __qtablewidgetitem288 = QTableWidgetItem()
        self.tableWidget.setItem(24, 8, __qtablewidgetitem288)
        __qtablewidgetitem289 = QTableWidgetItem()
        self.tableWidget.setItem(24, 9, __qtablewidgetitem289)
        __qtablewidgetitem290 = QTableWidgetItem()
        self.tableWidget.setItem(25, 0, __qtablewidgetitem290)
        __qtablewidgetitem291 = QTableWidgetItem()
        self.tableWidget.setItem(25, 1, __qtablewidgetitem291)
        __qtablewidgetitem292 = QTableWidgetItem()
        self.tableWidget.setItem(25, 2, __qtablewidgetitem292)
        __qtablewidgetitem293 = QTableWidgetItem()
        self.tableWidget.setItem(25, 3, __qtablewidgetitem293)
        __qtablewidgetitem294 = QTableWidgetItem()
        self.tableWidget.setItem(25, 4, __qtablewidgetitem294)
        __qtablewidgetitem295 = QTableWidgetItem()
        self.tableWidget.setItem(25, 5, __qtablewidgetitem295)
        __qtablewidgetitem296 = QTableWidgetItem()
        self.tableWidget.setItem(25, 6, __qtablewidgetitem296)
        __qtablewidgetitem297 = QTableWidgetItem()
        self.tableWidget.setItem(25, 7, __qtablewidgetitem297)
        __qtablewidgetitem298 = QTableWidgetItem()
        self.tableWidget.setItem(25, 8, __qtablewidgetitem298)
        __qtablewidgetitem299 = QTableWidgetItem()
        self.tableWidget.setItem(25, 9, __qtablewidgetitem299)
        __qtablewidgetitem300 = QTableWidgetItem()
        self.tableWidget.setItem(26, 0, __qtablewidgetitem300)
        __qtablewidgetitem301 = QTableWidgetItem()
        self.tableWidget.setItem(26, 1, __qtablewidgetitem301)
        __qtablewidgetitem302 = QTableWidgetItem()
        self.tableWidget.setItem(26, 2, __qtablewidgetitem302)
        __qtablewidgetitem303 = QTableWidgetItem()
        self.tableWidget.setItem(26, 3, __qtablewidgetitem303)
        __qtablewidgetitem304 = QTableWidgetItem()
        self.tableWidget.setItem(26, 4, __qtablewidgetitem304)
        __qtablewidgetitem305 = QTableWidgetItem()
        self.tableWidget.setItem(26, 5, __qtablewidgetitem305)
        __qtablewidgetitem306 = QTableWidgetItem()
        self.tableWidget.setItem(26, 6, __qtablewidgetitem306)
        __qtablewidgetitem307 = QTableWidgetItem()
        self.tableWidget.setItem(26, 7, __qtablewidgetitem307)
        __qtablewidgetitem308 = QTableWidgetItem()
        self.tableWidget.setItem(26, 8, __qtablewidgetitem308)
        __qtablewidgetitem309 = QTableWidgetItem()
        self.tableWidget.setItem(26, 9, __qtablewidgetitem309)
        __qtablewidgetitem310 = QTableWidgetItem()
        self.tableWidget.setItem(27, 0, __qtablewidgetitem310)
        __qtablewidgetitem311 = QTableWidgetItem()
        self.tableWidget.setItem(27, 1, __qtablewidgetitem311)
        __qtablewidgetitem312 = QTableWidgetItem()
        self.tableWidget.setItem(27, 2, __qtablewidgetitem312)
        __qtablewidgetitem313 = QTableWidgetItem()
        self.tableWidget.setItem(27, 3, __qtablewidgetitem313)
        __qtablewidgetitem314 = QTableWidgetItem()
        self.tableWidget.setItem(27, 4, __qtablewidgetitem314)
        __qtablewidgetitem315 = QTableWidgetItem()
        self.tableWidget.setItem(27, 5, __qtablewidgetitem315)
        __qtablewidgetitem316 = QTableWidgetItem()
        self.tableWidget.setItem(27, 6, __qtablewidgetitem316)
        __qtablewidgetitem317 = QTableWidgetItem()
        self.tableWidget.setItem(27, 7, __qtablewidgetitem317)
        __qtablewidgetitem318 = QTableWidgetItem()
        self.tableWidget.setItem(27, 8, __qtablewidgetitem318)
        __qtablewidgetitem319 = QTableWidgetItem()
        self.tableWidget.setItem(27, 9, __qtablewidgetitem319)
        __qtablewidgetitem320 = QTableWidgetItem()
        self.tableWidget.setItem(28, 0, __qtablewidgetitem320)
        __qtablewidgetitem321 = QTableWidgetItem()
        self.tableWidget.setItem(28, 1, __qtablewidgetitem321)
        __qtablewidgetitem322 = QTableWidgetItem()
        self.tableWidget.setItem(28, 2, __qtablewidgetitem322)
        __qtablewidgetitem323 = QTableWidgetItem()
        self.tableWidget.setItem(28, 3, __qtablewidgetitem323)
        __qtablewidgetitem324 = QTableWidgetItem()
        self.tableWidget.setItem(28, 4, __qtablewidgetitem324)
        __qtablewidgetitem325 = QTableWidgetItem()
        self.tableWidget.setItem(28, 5, __qtablewidgetitem325)
        __qtablewidgetitem326 = QTableWidgetItem()
        self.tableWidget.setItem(28, 6, __qtablewidgetitem326)
        __qtablewidgetitem327 = QTableWidgetItem()
        self.tableWidget.setItem(28, 7, __qtablewidgetitem327)
        __qtablewidgetitem328 = QTableWidgetItem()
        self.tableWidget.setItem(28, 8, __qtablewidgetitem328)
        __qtablewidgetitem329 = QTableWidgetItem()
        self.tableWidget.setItem(28, 9, __qtablewidgetitem329)
        __qtablewidgetitem330 = QTableWidgetItem()
        self.tableWidget.setItem(29, 0, __qtablewidgetitem330)
        __qtablewidgetitem331 = QTableWidgetItem()
        self.tableWidget.setItem(29, 1, __qtablewidgetitem331)
        __qtablewidgetitem332 = QTableWidgetItem()
        self.tableWidget.setItem(29, 2, __qtablewidgetitem332)
        __qtablewidgetitem333 = QTableWidgetItem()
        self.tableWidget.setItem(29, 3, __qtablewidgetitem333)
        __qtablewidgetitem334 = QTableWidgetItem()
        self.tableWidget.setItem(29, 4, __qtablewidgetitem334)
        __qtablewidgetitem335 = QTableWidgetItem()
        self.tableWidget.setItem(29, 5, __qtablewidgetitem335)
        __qtablewidgetitem336 = QTableWidgetItem()
        self.tableWidget.setItem(29, 6, __qtablewidgetitem336)
        __qtablewidgetitem337 = QTableWidgetItem()
        self.tableWidget.setItem(29, 7, __qtablewidgetitem337)
        __qtablewidgetitem338 = QTableWidgetItem()
        self.tableWidget.setItem(29, 8, __qtablewidgetitem338)
        __qtablewidgetitem339 = QTableWidgetItem()
        self.tableWidget.setItem(29, 9, __qtablewidgetitem339)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setMinimumSize(QSize(0, 0))
        self.tableWidget.setFont(font1)
        self.tableWidget.setStyleSheet(u"")
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.verticalHeader().setVisible(False)

        self.horizontalLayout_10.addWidget(self.tableWidget)


        self.horizontalLayout_7.addWidget(self.widget_8)

        self.widget_9 = QWidget(self.widget_7)
        self.widget_9.setObjectName(u"widget_9")
        self.widget_9.setMinimumSize(QSize(410, 264))
        self.widget_9.setFont(font1)
        self.widget_9.setStyleSheet(u"")
        self.verticalLayout_4 = QVBoxLayout(self.widget_9)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_2 = QScrollArea(self.widget_9)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setFont(font1)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 557, 520))
        self.verticalLayout_9 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.stackedWidget = QStackedWidget(self.scrollAreaWidgetContents_2)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setMinimumSize(QSize(473, 347))
        self.stackedWidget.setFont(font1)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_6 = QVBoxLayout(self.page)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.widget_11 = QWidget(self.page)
        self.widget_11.setObjectName(u"widget_11")
        self.widget_11.setFont(font1)
        self.horizontalLayout_11 = QHBoxLayout(self.widget_11)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.widget_11)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFont(font1)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 537, 364))
        self.horizontalLayout_12 = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.widget_13 = QWidget(self.scrollAreaWidgetContents)
        self.widget_13.setObjectName(u"widget_13")
        self.widget_13.setMinimumSize(QSize(471, 345))
        self.widget_13.setFont(font1)
        self.verticalLayout_10 = QVBoxLayout(self.widget_13)
        self.verticalLayout_10.setSpacing(5)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 5, 0, 0)
        self.label_16 = QLabel(self.widget_13)
        self.label_16.setObjectName(u"label_16")
        font4 = QFont()
        font4.setFamilies([u"Tahoma"])
        font4.setPointSize(9)
        font4.setBold(True)
        self.label_16.setFont(font4)

        self.verticalLayout_10.addWidget(self.label_16)

        self.tabWidget = QTabWidget(self.widget_13)
        self.tabWidget.setObjectName(u"tabWidget")
        font5 = QFont()
        font5.setFamilies([u"Tahoma"])
        self.tabWidget.setFont(font5)
        self.tabWidget.setStyleSheet(u"")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tab.setStyleSheet(u"")
        self.verticalLayout_8 = QVBoxLayout(self.tab)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.widget_12 = QWidget(self.tab)
        self.widget_12.setObjectName(u"widget_12")
        self.verticalLayout_11 = QVBoxLayout(self.widget_12)
        self.verticalLayout_11.setSpacing(10)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.label_13 = QLabel(self.widget_12)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font4)

        self.verticalLayout_11.addWidget(self.label_13, 0, Qt.AlignTop)

        self.frame_5 = QFrame(self.widget_12)
        self.frame_5.setObjectName(u"frame_5")
        sizePolicy.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy)
        font6 = QFont()
        font6.setFamilies([u"Tahoma"])
        font6.setPointSize(9)
        font6.setBold(False)
        self.frame_5.setFont(font6)
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_14.setSpacing(5)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(15, 5, 5, 5)
        self.label_17 = QLabel(self.frame_5)
        self.label_17.setObjectName(u"label_17")
        sizePolicy1.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy1)
        self.label_17.setFont(font6)

        self.horizontalLayout_14.addWidget(self.label_17, 0, Qt.AlignLeft)

        self.comboBox = QComboBox(self.frame_5)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setMinimumSize(QSize(84, 20))
        self.comboBox.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_14.addWidget(self.comboBox)

        self.lineEdit_4 = QLineEdit(self.frame_5)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        sizePolicy.setHeightForWidth(self.lineEdit_4.sizePolicy().hasHeightForWidth())
        self.lineEdit_4.setSizePolicy(sizePolicy)
        self.lineEdit_4.setMinimumSize(QSize(115, 20))
        font7 = QFont()
        font7.setFamilies([u"Tahoma"])
        font7.setPointSize(8)
        self.lineEdit_4.setFont(font7)
        self.lineEdit_4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_14.addWidget(self.lineEdit_4)


        self.verticalLayout_11.addWidget(self.frame_5)

        self.frame_6 = QFrame(self.widget_12)
        self.frame_6.setObjectName(u"frame_6")
        sizePolicy.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy)
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_15.setSpacing(5)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(15, 5, 5, 5)
        self.label_18 = QLabel(self.frame_6)
        self.label_18.setObjectName(u"label_18")
        sizePolicy1.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy1)
        self.label_18.setFont(font6)

        self.horizontalLayout_15.addWidget(self.label_18, 0, Qt.AlignLeft)

        self.comboBox_2 = QComboBox(self.frame_6)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")
        sizePolicy.setHeightForWidth(self.comboBox_2.sizePolicy().hasHeightForWidth())
        self.comboBox_2.setSizePolicy(sizePolicy)
        self.comboBox_2.setMinimumSize(QSize(84, 20))
        self.comboBox_2.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_15.addWidget(self.comboBox_2)

        self.lineEdit_5 = QLineEdit(self.frame_6)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        sizePolicy.setHeightForWidth(self.lineEdit_5.sizePolicy().hasHeightForWidth())
        self.lineEdit_5.setSizePolicy(sizePolicy)
        self.lineEdit_5.setMinimumSize(QSize(115, 20))
        self.lineEdit_5.setFont(font1)
        self.lineEdit_5.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_15.addWidget(self.lineEdit_5)


        self.verticalLayout_11.addWidget(self.frame_6)


        self.verticalLayout_8.addWidget(self.widget_12, 0, Qt.AlignTop)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.horizontalLayout_16 = QHBoxLayout(self.tab_2)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.widget_14 = QWidget(self.tab_2)
        self.widget_14.setObjectName(u"widget_14")
        sizePolicy1.setHeightForWidth(self.widget_14.sizePolicy().hasHeightForWidth())
        self.widget_14.setSizePolicy(sizePolicy1)
        self.verticalLayout_12 = QVBoxLayout(self.widget_14)
        self.verticalLayout_12.setSpacing(10)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.label_19 = QLabel(self.widget_14)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFont(font4)

        self.verticalLayout_12.addWidget(self.label_19)

        self.frame_7 = QFrame(self.widget_14)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_17.setSpacing(5)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(15, 5, 5, 5)
        self.label_15 = QLabel(self.frame_7)
        self.label_15.setObjectName(u"label_15")
        sizePolicy1.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy1)
        self.label_15.setFont(font6)

        self.horizontalLayout_17.addWidget(self.label_15, 0, Qt.AlignLeft)

        self.comboBox_3 = QComboBox(self.frame_7)
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")
        sizePolicy.setHeightForWidth(self.comboBox_3.sizePolicy().hasHeightForWidth())
        self.comboBox_3.setSizePolicy(sizePolicy)
        self.comboBox_3.setMinimumSize(QSize(84, 20))

        self.horizontalLayout_17.addWidget(self.comboBox_3)

        self.lineEdit_6 = QLineEdit(self.frame_7)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        sizePolicy.setHeightForWidth(self.lineEdit_6.sizePolicy().hasHeightForWidth())
        self.lineEdit_6.setSizePolicy(sizePolicy)
        self.lineEdit_6.setMinimumSize(QSize(115, 20))
        self.lineEdit_6.setFont(font6)
        self.lineEdit_6.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_17.addWidget(self.lineEdit_6)


        self.verticalLayout_12.addWidget(self.frame_7)


        self.horizontalLayout_16.addWidget(self.widget_14, 0, Qt.AlignTop)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.verticalLayout_13 = QVBoxLayout(self.tab_4)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.widget_15 = QWidget(self.tab_4)
        self.widget_15.setObjectName(u"widget_15")
        self.verticalLayout_14 = QVBoxLayout(self.widget_15)
        self.verticalLayout_14.setSpacing(10)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.label_20 = QLabel(self.widget_15)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font4)

        self.verticalLayout_14.addWidget(self.label_20)

        self.frame_4 = QFrame(self.widget_15)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_21 = QLabel(self.frame_4)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setFont(font6)

        self.horizontalLayout_8.addWidget(self.label_21, 0, Qt.AlignLeft)

        self.comboBox_4 = QComboBox(self.frame_4)
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.setObjectName(u"comboBox_4")
        sizePolicy.setHeightForWidth(self.comboBox_4.sizePolicy().hasHeightForWidth())
        self.comboBox_4.setSizePolicy(sizePolicy)
        self.comboBox_4.setMinimumSize(QSize(84, 20))

        self.horizontalLayout_8.addWidget(self.comboBox_4)

        self.lineEdit_9 = QLineEdit(self.frame_4)
        self.lineEdit_9.setObjectName(u"lineEdit_9")
        sizePolicy.setHeightForWidth(self.lineEdit_9.sizePolicy().hasHeightForWidth())
        self.lineEdit_9.setSizePolicy(sizePolicy)
        self.lineEdit_9.setMinimumSize(QSize(115, 19))
        self.lineEdit_9.setFont(font1)
        self.lineEdit_9.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_8.addWidget(self.lineEdit_9)


        self.verticalLayout_14.addWidget(self.frame_4)

        self.frame_8 = QFrame(self.widget_15)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_22 = QLabel(self.frame_8)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setFont(font6)

        self.horizontalLayout_18.addWidget(self.label_22, 0, Qt.AlignLeft)

        self.comboBox_5 = QComboBox(self.frame_8)
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.setObjectName(u"comboBox_5")
        sizePolicy.setHeightForWidth(self.comboBox_5.sizePolicy().hasHeightForWidth())
        self.comboBox_5.setSizePolicy(sizePolicy)
        self.comboBox_5.setMinimumSize(QSize(84, 20))

        self.horizontalLayout_18.addWidget(self.comboBox_5)

        self.lineEdit_8 = QLineEdit(self.frame_8)
        self.lineEdit_8.setObjectName(u"lineEdit_8")
        sizePolicy.setHeightForWidth(self.lineEdit_8.sizePolicy().hasHeightForWidth())
        self.lineEdit_8.setSizePolicy(sizePolicy)
        self.lineEdit_8.setMinimumSize(QSize(115, 19))
        self.lineEdit_8.setFont(font1)
        self.lineEdit_8.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_18.addWidget(self.lineEdit_8)


        self.verticalLayout_14.addWidget(self.frame_8)

        self.frame_9 = QFrame(self.widget_15)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.frame_9)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 9, 9, 9)
        self.label_23 = QLabel(self.frame_9)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setFont(font6)

        self.verticalLayout_15.addWidget(self.label_23)

        self.label_24 = QLabel(self.frame_9)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setFont(font6)

        self.verticalLayout_15.addWidget(self.label_24)

        self.frame_10 = QFrame(self.frame_9)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setMinimumSize(QSize(343, 39))
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_19 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.comboBox_6 = QComboBox(self.frame_10)
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.setObjectName(u"comboBox_6")
        sizePolicy.setHeightForWidth(self.comboBox_6.sizePolicy().hasHeightForWidth())
        self.comboBox_6.setSizePolicy(sizePolicy)
        self.comboBox_6.setMinimumSize(QSize(175, 20))

        self.horizontalLayout_19.addWidget(self.comboBox_6)

        self.lineEdit_7 = QLineEdit(self.frame_10)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        sizePolicy.setHeightForWidth(self.lineEdit_7.sizePolicy().hasHeightForWidth())
        self.lineEdit_7.setSizePolicy(sizePolicy)
        self.lineEdit_7.setMinimumSize(QSize(115, 20))
        self.lineEdit_7.setFont(font1)
        self.lineEdit_7.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_19.addWidget(self.lineEdit_7)


        self.verticalLayout_15.addWidget(self.frame_10)


        self.verticalLayout_14.addWidget(self.frame_9)


        self.verticalLayout_13.addWidget(self.widget_15, 0, Qt.AlignTop)

        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.verticalLayout_16 = QVBoxLayout(self.tab_5)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.widget_16 = QWidget(self.tab_5)
        self.widget_16.setObjectName(u"widget_16")
        self.verticalLayout_17 = QVBoxLayout(self.widget_16)
        self.verticalLayout_17.setSpacing(10)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.label_25 = QLabel(self.widget_16)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setFont(font4)

        self.verticalLayout_17.addWidget(self.label_25, 0, Qt.AlignTop)

        self.frame_11 = QFrame(self.widget_16)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_20 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(15, -1, -1, -1)
        self.label_26 = QLabel(self.frame_11)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setFont(font6)

        self.horizontalLayout_20.addWidget(self.label_26, 0, Qt.AlignLeft)

        self.comboBox_7 = QComboBox(self.frame_11)
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.setObjectName(u"comboBox_7")
        sizePolicy.setHeightForWidth(self.comboBox_7.sizePolicy().hasHeightForWidth())
        self.comboBox_7.setSizePolicy(sizePolicy)
        self.comboBox_7.setMinimumSize(QSize(84, 20))

        self.horizontalLayout_20.addWidget(self.comboBox_7)

        self.lineEdit_10 = QLineEdit(self.frame_11)
        self.lineEdit_10.setObjectName(u"lineEdit_10")
        sizePolicy.setHeightForWidth(self.lineEdit_10.sizePolicy().hasHeightForWidth())
        self.lineEdit_10.setSizePolicy(sizePolicy)
        self.lineEdit_10.setMinimumSize(QSize(115, 19))
        self.lineEdit_10.setFont(font1)
        self.lineEdit_10.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_20.addWidget(self.lineEdit_10)


        self.verticalLayout_17.addWidget(self.frame_11)


        self.verticalLayout_16.addWidget(self.widget_16, 0, Qt.AlignTop)

        self.tabWidget.addTab(self.tab_5, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.verticalLayout_19 = QVBoxLayout(self.tab_6)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.widget_17 = QWidget(self.tab_6)
        self.widget_17.setObjectName(u"widget_17")
        self.verticalLayout_18 = QVBoxLayout(self.widget_17)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.label_27 = QLabel(self.widget_17)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setFont(font4)

        self.verticalLayout_18.addWidget(self.label_27, 0, Qt.AlignTop)

        self.frame_12 = QFrame(self.widget_17)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setFrameShape(QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_21 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(15, -1, -1, -1)
        self.label_28 = QLabel(self.frame_12)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setFont(font6)

        self.horizontalLayout_21.addWidget(self.label_28, 0, Qt.AlignLeft)

        self.comboBox_8 = QComboBox(self.frame_12)
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.setObjectName(u"comboBox_8")
        sizePolicy.setHeightForWidth(self.comboBox_8.sizePolicy().hasHeightForWidth())
        self.comboBox_8.setSizePolicy(sizePolicy)
        self.comboBox_8.setMinimumSize(QSize(84, 20))

        self.horizontalLayout_21.addWidget(self.comboBox_8)

        self.lineEdit_11 = QLineEdit(self.frame_12)
        self.lineEdit_11.setObjectName(u"lineEdit_11")
        sizePolicy.setHeightForWidth(self.lineEdit_11.sizePolicy().hasHeightForWidth())
        self.lineEdit_11.setSizePolicy(sizePolicy)
        self.lineEdit_11.setMinimumSize(QSize(115, 19))
        self.lineEdit_11.setFont(font1)
        self.lineEdit_11.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_21.addWidget(self.lineEdit_11)


        self.verticalLayout_18.addWidget(self.frame_12)


        self.verticalLayout_19.addWidget(self.widget_17, 0, Qt.AlignTop)

        self.tabWidget.addTab(self.tab_6, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_21 = QVBoxLayout(self.tab_3)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.widget_18 = QWidget(self.tab_3)
        self.widget_18.setObjectName(u"widget_18")
        self.verticalLayout_20 = QVBoxLayout(self.widget_18)
        self.verticalLayout_20.setSpacing(10)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.verticalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.label_29 = QLabel(self.widget_18)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setFont(font4)

        self.verticalLayout_20.addWidget(self.label_29, 0, Qt.AlignTop)

        self.frame_16 = QFrame(self.widget_18)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setFrameShape(QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_25 = QHBoxLayout(self.frame_16)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_25.setContentsMargins(10, -1, -1, -1)
        self.label_33 = QLabel(self.frame_16)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setFont(font4)

        self.horizontalLayout_25.addWidget(self.label_33)


        self.verticalLayout_20.addWidget(self.frame_16)

        self.frame_14 = QFrame(self.widget_18)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setFrameShape(QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_23 = QHBoxLayout(self.frame_14)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(15, -1, -1, -1)
        self.label_32 = QLabel(self.frame_14)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setFont(font6)

        self.horizontalLayout_23.addWidget(self.label_32)

        self.comboBox_11 = QComboBox(self.frame_14)
        self.comboBox_11.addItem("")
        self.comboBox_11.addItem("")
        self.comboBox_11.addItem("")
        self.comboBox_11.addItem("")
        self.comboBox_11.setObjectName(u"comboBox_11")
        sizePolicy.setHeightForWidth(self.comboBox_11.sizePolicy().hasHeightForWidth())
        self.comboBox_11.setSizePolicy(sizePolicy)
        self.comboBox_11.setMinimumSize(QSize(84, 20))

        self.horizontalLayout_23.addWidget(self.comboBox_11)

        self.lineEdit_14 = QLineEdit(self.frame_14)
        self.lineEdit_14.setObjectName(u"lineEdit_14")
        sizePolicy.setHeightForWidth(self.lineEdit_14.sizePolicy().hasHeightForWidth())
        self.lineEdit_14.setSizePolicy(sizePolicy)
        self.lineEdit_14.setMinimumSize(QSize(115, 19))
        self.lineEdit_14.setFont(font1)
        self.lineEdit_14.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_23.addWidget(self.lineEdit_14)


        self.verticalLayout_20.addWidget(self.frame_14)

        self.frame_15 = QFrame(self.widget_18)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setFrameShape(QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_24 = QHBoxLayout(self.frame_15)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalLayout_24.setContentsMargins(15, -1, -1, -1)
        self.label_31 = QLabel(self.frame_15)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setFont(font1)

        self.horizontalLayout_24.addWidget(self.label_31)

        self.comboBox_10 = QComboBox(self.frame_15)
        self.comboBox_10.addItem("")
        self.comboBox_10.addItem("")
        self.comboBox_10.addItem("")
        self.comboBox_10.addItem("")
        self.comboBox_10.setObjectName(u"comboBox_10")
        sizePolicy.setHeightForWidth(self.comboBox_10.sizePolicy().hasHeightForWidth())
        self.comboBox_10.setSizePolicy(sizePolicy)
        self.comboBox_10.setMinimumSize(QSize(84, 20))

        self.horizontalLayout_24.addWidget(self.comboBox_10)

        self.lineEdit_15 = QLineEdit(self.frame_15)
        self.lineEdit_15.setObjectName(u"lineEdit_15")
        sizePolicy.setHeightForWidth(self.lineEdit_15.sizePolicy().hasHeightForWidth())
        self.lineEdit_15.setSizePolicy(sizePolicy)
        self.lineEdit_15.setMinimumSize(QSize(115, 19))
        self.lineEdit_15.setFont(font1)
        self.lineEdit_15.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_24.addWidget(self.lineEdit_15)


        self.verticalLayout_20.addWidget(self.frame_15)

        self.frame_13 = QFrame(self.widget_18)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setFont(font6)
        self.frame_13.setFrameShape(QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Raised)
        self.verticalLayout_22 = QVBoxLayout(self.frame_13)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_22.setContentsMargins(10, -1, -1, -1)
        self.label_30 = QLabel(self.frame_13)
        self.label_30.setObjectName(u"label_30")
        font8 = QFont()
        font8.setFamilies([u"Tahoma"])
        font8.setPointSize(8)
        font8.setBold(True)
        self.label_30.setFont(font8)

        self.verticalLayout_22.addWidget(self.label_30)


        self.verticalLayout_20.addWidget(self.frame_13)

        self.frame_17 = QFrame(self.widget_18)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setFrameShape(QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QFrame.Raised)
        self.verticalLayout_23 = QVBoxLayout(self.frame_17)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.verticalLayout_23.setContentsMargins(15, 0, 0, 0)
        self.label_34 = QLabel(self.frame_17)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setFont(font6)

        self.verticalLayout_23.addWidget(self.label_34)

        self.frame_18 = QFrame(self.frame_17)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setFrameShape(QFrame.StyledPanel)
        self.frame_18.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_22 = QHBoxLayout(self.frame_18)
        self.horizontalLayout_22.setSpacing(0)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.label_35 = QLabel(self.frame_18)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setFont(font6)

        self.horizontalLayout_22.addWidget(self.label_35)

        self.comboBox_9 = QComboBox(self.frame_18)
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.setObjectName(u"comboBox_9")
        sizePolicy.setHeightForWidth(self.comboBox_9.sizePolicy().hasHeightForWidth())
        self.comboBox_9.setSizePolicy(sizePolicy)
        self.comboBox_9.setMinimumSize(QSize(84, 20))

        self.horizontalLayout_22.addWidget(self.comboBox_9)

        self.lineEdit_12 = QLineEdit(self.frame_18)
        self.lineEdit_12.setObjectName(u"lineEdit_12")
        sizePolicy.setHeightForWidth(self.lineEdit_12.sizePolicy().hasHeightForWidth())
        self.lineEdit_12.setSizePolicy(sizePolicy)
        self.lineEdit_12.setMinimumSize(QSize(115, 20))
        self.lineEdit_12.setFont(font1)
        self.lineEdit_12.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_22.addWidget(self.lineEdit_12)


        self.verticalLayout_23.addWidget(self.frame_18)


        self.verticalLayout_20.addWidget(self.frame_17)


        self.verticalLayout_21.addWidget(self.widget_18, 0, Qt.AlignTop)

        self.tabWidget.addTab(self.tab_3, "")

        self.verticalLayout_10.addWidget(self.tabWidget)

        self.widget_29 = QWidget(self.widget_13)
        self.widget_29.setObjectName(u"widget_29")
        self.widget_29.setFont(font1)
        self.horizontalLayout_13 = QHBoxLayout(self.widget_29)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_10.addWidget(self.widget_29, 0, Qt.AlignTop)


        self.horizontalLayout_12.addWidget(self.widget_13)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_11.addWidget(self.scrollArea)


        self.verticalLayout_6.addWidget(self.widget_11)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_7 = QVBoxLayout(self.page_2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_14 = QLabel(self.page_2)
        self.label_14.setObjectName(u"label_14")

        self.verticalLayout_7.addWidget(self.label_14)

        self.stackedWidget.addWidget(self.page_2)

        self.verticalLayout_9.addWidget(self.stackedWidget)

        self.widget_3 = QWidget(self.scrollAreaWidgetContents_2)
        self.widget_3.setObjectName(u"widget_3")
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setMinimumSize(QSize(100, 80))
        self.widget_3.setStyleSheet(u"")
        self.verticalLayout_5 = QVBoxLayout(self.widget_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.widget_19 = QWidget(self.widget_3)
        self.widget_19.setObjectName(u"widget_19")
        self.widget_19.setStyleSheet(u"")
        self.horizontalLayout_27 = QHBoxLayout(self.widget_19)
        self.horizontalLayout_27.setSpacing(0)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_27.setContentsMargins(0, 0, 0, 0)
        self.frame_21 = QFrame(self.widget_19)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setMinimumSize(QSize(196, 41))
        self.frame_21.setFrameShape(QFrame.StyledPanel)
        self.frame_21.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_28 = QHBoxLayout(self.frame_21)
        self.horizontalLayout_28.setSpacing(5)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.horizontalLayout_28.setContentsMargins(5, 5, 5, 5)
        self.label_9 = QLabel(self.frame_21)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_28.addWidget(self.label_9, 0, Qt.AlignLeft)

        self.lineEdit_17 = QLineEdit(self.frame_21)
        self.lineEdit_17.setObjectName(u"lineEdit_17")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lineEdit_17.sizePolicy().hasHeightForWidth())
        self.lineEdit_17.setSizePolicy(sizePolicy2)
        self.lineEdit_17.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_28.addWidget(self.lineEdit_17)


        self.horizontalLayout_27.addWidget(self.frame_21)

        self.frame_22 = QFrame(self.widget_19)
        self.frame_22.setObjectName(u"frame_22")
        self.frame_22.setMinimumSize(QSize(197, 41))
        self.frame_22.setFrameShape(QFrame.StyledPanel)
        self.frame_22.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_29 = QHBoxLayout(self.frame_22)
        self.horizontalLayout_29.setSpacing(5)
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.horizontalLayout_29.setContentsMargins(5, 5, 5, 5)
        self.label_10 = QLabel(self.frame_22)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_29.addWidget(self.label_10, 0, Qt.AlignLeft)

        self.lineEdit_18 = QLineEdit(self.frame_22)
        self.lineEdit_18.setObjectName(u"lineEdit_18")
        sizePolicy2.setHeightForWidth(self.lineEdit_18.sizePolicy().hasHeightForWidth())
        self.lineEdit_18.setSizePolicy(sizePolicy2)
        self.lineEdit_18.setMinimumSize(QSize(100, 21))

        self.horizontalLayout_29.addWidget(self.lineEdit_18)


        self.horizontalLayout_27.addWidget(self.frame_22, 0, Qt.AlignRight)


        self.verticalLayout_5.addWidget(self.widget_19)

        self.widget_20 = QWidget(self.widget_3)
        self.widget_20.setObjectName(u"widget_20")
        self.widget_20.setStyleSheet(u"")
        self.horizontalLayout_26 = QHBoxLayout(self.widget_20)
        self.horizontalLayout_26.setSpacing(0)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.horizontalLayout_26.setContentsMargins(0, 0, 0, 0)
        self.frame_19 = QFrame(self.widget_20)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setMinimumSize(QSize(196, 41))
        self.frame_19.setFrameShape(QFrame.StyledPanel)
        self.frame_19.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_30 = QHBoxLayout(self.frame_19)
        self.horizontalLayout_30.setSpacing(5)
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.horizontalLayout_30.setContentsMargins(5, 5, 5, 5)
        self.label_7 = QLabel(self.frame_19)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_30.addWidget(self.label_7, 0, Qt.AlignLeft)

        self.lineEdit_13 = QLineEdit(self.frame_19)
        self.lineEdit_13.setObjectName(u"lineEdit_13")
        sizePolicy2.setHeightForWidth(self.lineEdit_13.sizePolicy().hasHeightForWidth())
        self.lineEdit_13.setSizePolicy(sizePolicy2)
        self.lineEdit_13.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_30.addWidget(self.lineEdit_13)


        self.horizontalLayout_26.addWidget(self.frame_19)

        self.frame_20 = QFrame(self.widget_20)
        self.frame_20.setObjectName(u"frame_20")
        self.frame_20.setMinimumSize(QSize(197, 41))
        self.frame_20.setFrameShape(QFrame.StyledPanel)
        self.frame_20.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_31 = QHBoxLayout(self.frame_20)
        self.horizontalLayout_31.setSpacing(5)
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.horizontalLayout_31.setContentsMargins(5, 5, 5, 5)
        self.label_8 = QLabel(self.frame_20)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_31.addWidget(self.label_8, 0, Qt.AlignLeft)

        self.lineEdit_16 = QLineEdit(self.frame_20)
        self.lineEdit_16.setObjectName(u"lineEdit_16")
        sizePolicy2.setHeightForWidth(self.lineEdit_16.sizePolicy().hasHeightForWidth())
        self.lineEdit_16.setSizePolicy(sizePolicy2)
        self.lineEdit_16.setMinimumSize(QSize(100, 21))

        self.horizontalLayout_31.addWidget(self.lineEdit_16)


        self.horizontalLayout_26.addWidget(self.frame_20, 0, Qt.AlignRight)


        self.verticalLayout_5.addWidget(self.widget_20)

        self.widget_21 = QWidget(self.widget_3)
        self.widget_21.setObjectName(u"widget_21")
        self.verticalLayout_24 = QVBoxLayout(self.widget_21)
        self.verticalLayout_24.setSpacing(0)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.verticalLayout_24.setContentsMargins(0, 0, 0, 0)
        self.save = QPushButton(self.widget_21)
        self.save.setObjectName(u"save")
        sizePolicy.setHeightForWidth(self.save.sizePolicy().hasHeightForWidth())
        self.save.setSizePolicy(sizePolicy)
        font9 = QFont()
        font9.setPointSize(10)
        font9.setBold(True)
        font9.setItalic(False)
        font9.setUnderline(False)
        self.save.setFont(font9)
        self.save.setStyleSheet(u"background-color: rgb(85, 255, 127);\n"
"border-radius: 8px;")
        icon = QIcon()
        icon.addFile(u":/feather/icons/feather/save.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.save.setIcon(icon)

        self.verticalLayout_24.addWidget(self.save)


        self.verticalLayout_5.addWidget(self.widget_21)


        self.verticalLayout_9.addWidget(self.widget_3)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_4.addWidget(self.scrollArea_2)


        self.horizontalLayout_7.addWidget(self.widget_9)


        self.verticalLayout_3.addWidget(self.widget_7)


        self.verticalLayout.addWidget(self.widget_2)

        self.widget_10 = QWidget(self.centralwidget)
        self.widget_10.setObjectName(u"widget_10")
        self.widget_10.setFont(font1)
        self.horizontalLayout_9 = QHBoxLayout(self.widget_10)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.label_11 = QLabel(self.widget_10)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font1)

        self.horizontalLayout_9.addWidget(self.label_11)

        self.label_12 = QLabel(self.widget_10)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font1)
        self.label_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_9.addWidget(self.label_12)


        self.verticalLayout.addWidget(self.widget_10)

        PM.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(PM)
        self.statusbar.setObjectName(u"statusbar")
        PM.setStatusBar(self.statusbar)

        self.retranslateUi(PM)

        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(PM)
    # setupUi

    def retranslateUi(self, PM):
        PM.setWindowTitle(QCoreApplication.translate("PM", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("PM", u"USE  RECORD P.M. FIXTURE AND TESTER", None))
        self.label_2.setText(QCoreApplication.translate("PM", u"Product name", None))
        self.label_3.setText(QCoreApplication.translate("PM", u"Tooling code", None))
        self.label_5.setText(QCoreApplication.translate("PM", u"Tooling for", None))
        self.efpc.setText(QCoreApplication.translate("PM", u"E-FPC", None))
        self.smt.setText(QCoreApplication.translate("PM", u"SMT", None))
        self.label_4.setText(QCoreApplication.translate("PM", u"Next PM.", None))
        self.label_6.setText(QCoreApplication.translate("PM", u"Lot", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("PM", u"New Column", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("PM", u"New Column", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("PM", u"New Column", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("PM", u"New Column", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("PM", u"New Column", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("PM", u"New Column", None));
        ___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("PM", u"New Column", None));
        ___qtablewidgetitem7 = self.tableWidget.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("PM", u"New Column", None));
        ___qtablewidgetitem8 = self.tableWidget.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("PM", u"New Column", None));
        ___qtablewidgetitem9 = self.tableWidget.horizontalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("PM", u"New Column", None));
        ___qtablewidgetitem10 = self.tableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("PM", u"New Row", None));
        ___qtablewidgetitem11 = self.tableWidget.verticalHeaderItem(1)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("PM", u"New Row", None));
        ___qtablewidgetitem12 = self.tableWidget.verticalHeaderItem(2)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("PM", u"New Row", None));
        ___qtablewidgetitem13 = self.tableWidget.verticalHeaderItem(3)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("PM", u"New Row", None));
        ___qtablewidgetitem14 = self.tableWidget.verticalHeaderItem(4)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("PM", u"New Row", None));
        ___qtablewidgetitem15 = self.tableWidget.verticalHeaderItem(5)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("PM", u"New Row", None));
        ___qtablewidgetitem16 = self.tableWidget.verticalHeaderItem(6)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("PM", u"New Row", None));
        ___qtablewidgetitem17 = self.tableWidget.verticalHeaderItem(7)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("PM", u"New Row", None));
        ___qtablewidgetitem18 = self.tableWidget.verticalHeaderItem(8)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("PM", u"New Row", None));
        ___qtablewidgetitem19 = self.tableWidget.verticalHeaderItem(9)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("PM", u"New Row", None));
        ___qtablewidgetitem20 = self.tableWidget.verticalHeaderItem(10)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("PM", u"New Row", None));
        ___qtablewidgetitem21 = self.tableWidget.verticalHeaderItem(11)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("PM", u"New Row", None));
        ___qtablewidgetitem22 = self.tableWidget.verticalHeaderItem(12)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("PM", u"New Row", None));
        ___qtablewidgetitem23 = self.tableWidget.verticalHeaderItem(13)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("PM", u"New Row", None));
        ___qtablewidgetitem24 = self.tableWidget.verticalHeaderItem(14)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("PM", u"New Row", None));
        ___qtablewidgetitem25 = self.tableWidget.verticalHeaderItem(15)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("PM", u"New Row", None));
        ___qtablewidgetitem26 = self.tableWidget.verticalHeaderItem(16)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("PM", u"New Row", None));
        ___qtablewidgetitem27 = self.tableWidget.verticalHeaderItem(17)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("PM", u"New Row", None));
        ___qtablewidgetitem28 = self.tableWidget.verticalHeaderItem(18)
        ___qtablewidgetitem28.setText(QCoreApplication.translate("PM", u"New Row", None));
        ___qtablewidgetitem29 = self.tableWidget.verticalHeaderItem(19)
        ___qtablewidgetitem29.setText(QCoreApplication.translate("PM", u"New Row", None));
        ___qtablewidgetitem30 = self.tableWidget.verticalHeaderItem(20)
        ___qtablewidgetitem30.setText(QCoreApplication.translate("PM", u"New Row", None));
        ___qtablewidgetitem31 = self.tableWidget.verticalHeaderItem(21)
        ___qtablewidgetitem31.setText(QCoreApplication.translate("PM", u"New Row", None));
        ___qtablewidgetitem32 = self.tableWidget.verticalHeaderItem(22)
        ___qtablewidgetitem32.setText(QCoreApplication.translate("PM", u"New Row", None));
        ___qtablewidgetitem33 = self.tableWidget.verticalHeaderItem(23)
        ___qtablewidgetitem33.setText(QCoreApplication.translate("PM", u"New Row", None));
        ___qtablewidgetitem34 = self.tableWidget.verticalHeaderItem(24)
        ___qtablewidgetitem34.setText(QCoreApplication.translate("PM", u"New Row", None));
        ___qtablewidgetitem35 = self.tableWidget.verticalHeaderItem(25)
        ___qtablewidgetitem35.setText(QCoreApplication.translate("PM", u"New Row", None));
        ___qtablewidgetitem36 = self.tableWidget.verticalHeaderItem(26)
        ___qtablewidgetitem36.setText(QCoreApplication.translate("PM", u"New Row", None));
        ___qtablewidgetitem37 = self.tableWidget.verticalHeaderItem(27)
        ___qtablewidgetitem37.setText(QCoreApplication.translate("PM", u"New Row", None));
        ___qtablewidgetitem38 = self.tableWidget.verticalHeaderItem(28)
        ___qtablewidgetitem38.setText(QCoreApplication.translate("PM", u"New Row", None));
        ___qtablewidgetitem39 = self.tableWidget.verticalHeaderItem(29)
        ___qtablewidgetitem39.setText(QCoreApplication.translate("PM", u"New Row", None));

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        ___qtablewidgetitem40 = self.tableWidget.item(0, 0)
        ___qtablewidgetitem40.setText(QCoreApplication.translate("PM", u"1", None));
        ___qtablewidgetitem41 = self.tableWidget.item(0, 1)
        ___qtablewidgetitem41.setText(QCoreApplication.translate("PM", u"2", None));
        ___qtablewidgetitem42 = self.tableWidget.item(0, 2)
        ___qtablewidgetitem42.setText(QCoreApplication.translate("PM", u"3", None));
        ___qtablewidgetitem43 = self.tableWidget.item(0, 3)
        ___qtablewidgetitem43.setText(QCoreApplication.translate("PM", u"4", None));
        ___qtablewidgetitem44 = self.tableWidget.item(0, 4)
        ___qtablewidgetitem44.setText(QCoreApplication.translate("PM", u"5", None));
        ___qtablewidgetitem45 = self.tableWidget.item(0, 5)
        ___qtablewidgetitem45.setText(QCoreApplication.translate("PM", u"6", None));
        ___qtablewidgetitem46 = self.tableWidget.item(0, 6)
        ___qtablewidgetitem46.setText(QCoreApplication.translate("PM", u"7", None));
        ___qtablewidgetitem47 = self.tableWidget.item(0, 7)
        ___qtablewidgetitem47.setText(QCoreApplication.translate("PM", u"8", None));
        ___qtablewidgetitem48 = self.tableWidget.item(0, 8)
        ___qtablewidgetitem48.setText(QCoreApplication.translate("PM", u"9", None));
        ___qtablewidgetitem49 = self.tableWidget.item(0, 9)
        ___qtablewidgetitem49.setText(QCoreApplication.translate("PM", u"10", None));
        ___qtablewidgetitem50 = self.tableWidget.item(1, 0)
        ___qtablewidgetitem50.setText(QCoreApplication.translate("PM", u"11", None));
        ___qtablewidgetitem51 = self.tableWidget.item(1, 1)
        ___qtablewidgetitem51.setText(QCoreApplication.translate("PM", u"12", None));
        ___qtablewidgetitem52 = self.tableWidget.item(1, 2)
        ___qtablewidgetitem52.setText(QCoreApplication.translate("PM", u"13", None));
        ___qtablewidgetitem53 = self.tableWidget.item(1, 3)
        ___qtablewidgetitem53.setText(QCoreApplication.translate("PM", u"14", None));
        ___qtablewidgetitem54 = self.tableWidget.item(1, 4)
        ___qtablewidgetitem54.setText(QCoreApplication.translate("PM", u"15", None));
        ___qtablewidgetitem55 = self.tableWidget.item(1, 5)
        ___qtablewidgetitem55.setText(QCoreApplication.translate("PM", u"16", None));
        ___qtablewidgetitem56 = self.tableWidget.item(1, 6)
        ___qtablewidgetitem56.setText(QCoreApplication.translate("PM", u"17", None));
        ___qtablewidgetitem57 = self.tableWidget.item(1, 7)
        ___qtablewidgetitem57.setText(QCoreApplication.translate("PM", u"18", None));
        ___qtablewidgetitem58 = self.tableWidget.item(1, 8)
        ___qtablewidgetitem58.setText(QCoreApplication.translate("PM", u"19", None));
        ___qtablewidgetitem59 = self.tableWidget.item(1, 9)
        ___qtablewidgetitem59.setText(QCoreApplication.translate("PM", u"20", None));
        ___qtablewidgetitem60 = self.tableWidget.item(2, 0)
        ___qtablewidgetitem60.setText(QCoreApplication.translate("PM", u"21", None));
        ___qtablewidgetitem61 = self.tableWidget.item(2, 1)
        ___qtablewidgetitem61.setText(QCoreApplication.translate("PM", u"22", None));
        ___qtablewidgetitem62 = self.tableWidget.item(2, 2)
        ___qtablewidgetitem62.setText(QCoreApplication.translate("PM", u"23", None));
        ___qtablewidgetitem63 = self.tableWidget.item(2, 3)
        ___qtablewidgetitem63.setText(QCoreApplication.translate("PM", u"24", None));
        ___qtablewidgetitem64 = self.tableWidget.item(2, 4)
        ___qtablewidgetitem64.setText(QCoreApplication.translate("PM", u"25", None));
        ___qtablewidgetitem65 = self.tableWidget.item(2, 5)
        ___qtablewidgetitem65.setText(QCoreApplication.translate("PM", u"26", None));
        ___qtablewidgetitem66 = self.tableWidget.item(2, 6)
        ___qtablewidgetitem66.setText(QCoreApplication.translate("PM", u"27", None));
        ___qtablewidgetitem67 = self.tableWidget.item(2, 7)
        ___qtablewidgetitem67.setText(QCoreApplication.translate("PM", u"28", None));
        ___qtablewidgetitem68 = self.tableWidget.item(2, 8)
        ___qtablewidgetitem68.setText(QCoreApplication.translate("PM", u"29", None));
        ___qtablewidgetitem69 = self.tableWidget.item(2, 9)
        ___qtablewidgetitem69.setText(QCoreApplication.translate("PM", u"30", None));
        ___qtablewidgetitem70 = self.tableWidget.item(3, 0)
        ___qtablewidgetitem70.setText(QCoreApplication.translate("PM", u"31", None));
        ___qtablewidgetitem71 = self.tableWidget.item(3, 1)
        ___qtablewidgetitem71.setText(QCoreApplication.translate("PM", u"32", None));
        ___qtablewidgetitem72 = self.tableWidget.item(3, 2)
        ___qtablewidgetitem72.setText(QCoreApplication.translate("PM", u"33", None));
        ___qtablewidgetitem73 = self.tableWidget.item(3, 3)
        ___qtablewidgetitem73.setText(QCoreApplication.translate("PM", u"34", None));
        ___qtablewidgetitem74 = self.tableWidget.item(3, 4)
        ___qtablewidgetitem74.setText(QCoreApplication.translate("PM", u"35", None));
        ___qtablewidgetitem75 = self.tableWidget.item(3, 5)
        ___qtablewidgetitem75.setText(QCoreApplication.translate("PM", u"36", None));
        ___qtablewidgetitem76 = self.tableWidget.item(3, 6)
        ___qtablewidgetitem76.setText(QCoreApplication.translate("PM", u"37", None));
        ___qtablewidgetitem77 = self.tableWidget.item(3, 7)
        ___qtablewidgetitem77.setText(QCoreApplication.translate("PM", u"38", None));
        ___qtablewidgetitem78 = self.tableWidget.item(3, 8)
        ___qtablewidgetitem78.setText(QCoreApplication.translate("PM", u"39", None));
        ___qtablewidgetitem79 = self.tableWidget.item(3, 9)
        ___qtablewidgetitem79.setText(QCoreApplication.translate("PM", u"40", None));
        ___qtablewidgetitem80 = self.tableWidget.item(4, 0)
        ___qtablewidgetitem80.setText(QCoreApplication.translate("PM", u"41", None));
        ___qtablewidgetitem81 = self.tableWidget.item(4, 1)
        ___qtablewidgetitem81.setText(QCoreApplication.translate("PM", u"42", None));
        ___qtablewidgetitem82 = self.tableWidget.item(4, 2)
        ___qtablewidgetitem82.setText(QCoreApplication.translate("PM", u"43", None));
        ___qtablewidgetitem83 = self.tableWidget.item(4, 3)
        ___qtablewidgetitem83.setText(QCoreApplication.translate("PM", u"44", None));
        ___qtablewidgetitem84 = self.tableWidget.item(4, 4)
        ___qtablewidgetitem84.setText(QCoreApplication.translate("PM", u"45", None));
        ___qtablewidgetitem85 = self.tableWidget.item(4, 5)
        ___qtablewidgetitem85.setText(QCoreApplication.translate("PM", u"46", None));
        ___qtablewidgetitem86 = self.tableWidget.item(4, 6)
        ___qtablewidgetitem86.setText(QCoreApplication.translate("PM", u"47", None));
        ___qtablewidgetitem87 = self.tableWidget.item(4, 7)
        ___qtablewidgetitem87.setText(QCoreApplication.translate("PM", u"48", None));
        ___qtablewidgetitem88 = self.tableWidget.item(4, 8)
        ___qtablewidgetitem88.setText(QCoreApplication.translate("PM", u"49", None));
        ___qtablewidgetitem89 = self.tableWidget.item(4, 9)
        ___qtablewidgetitem89.setText(QCoreApplication.translate("PM", u"50", None));
        ___qtablewidgetitem90 = self.tableWidget.item(5, 0)
        ___qtablewidgetitem90.setText(QCoreApplication.translate("PM", u"51", None));
        ___qtablewidgetitem91 = self.tableWidget.item(5, 1)
        ___qtablewidgetitem91.setText(QCoreApplication.translate("PM", u"52", None));
        ___qtablewidgetitem92 = self.tableWidget.item(5, 2)
        ___qtablewidgetitem92.setText(QCoreApplication.translate("PM", u"53", None));
        ___qtablewidgetitem93 = self.tableWidget.item(5, 3)
        ___qtablewidgetitem93.setText(QCoreApplication.translate("PM", u"54", None));
        ___qtablewidgetitem94 = self.tableWidget.item(5, 4)
        ___qtablewidgetitem94.setText(QCoreApplication.translate("PM", u"55", None));
        ___qtablewidgetitem95 = self.tableWidget.item(5, 5)
        ___qtablewidgetitem95.setText(QCoreApplication.translate("PM", u"56", None));
        ___qtablewidgetitem96 = self.tableWidget.item(5, 6)
        ___qtablewidgetitem96.setText(QCoreApplication.translate("PM", u"57", None));
        ___qtablewidgetitem97 = self.tableWidget.item(5, 7)
        ___qtablewidgetitem97.setText(QCoreApplication.translate("PM", u"58", None));
        ___qtablewidgetitem98 = self.tableWidget.item(5, 8)
        ___qtablewidgetitem98.setText(QCoreApplication.translate("PM", u"59", None));
        ___qtablewidgetitem99 = self.tableWidget.item(5, 9)
        ___qtablewidgetitem99.setText(QCoreApplication.translate("PM", u"60", None));
        ___qtablewidgetitem100 = self.tableWidget.item(6, 0)
        ___qtablewidgetitem100.setText(QCoreApplication.translate("PM", u"61", None));
        ___qtablewidgetitem101 = self.tableWidget.item(6, 1)
        ___qtablewidgetitem101.setText(QCoreApplication.translate("PM", u"62", None));
        ___qtablewidgetitem102 = self.tableWidget.item(6, 2)
        ___qtablewidgetitem102.setText(QCoreApplication.translate("PM", u"63", None));
        ___qtablewidgetitem103 = self.tableWidget.item(6, 3)
        ___qtablewidgetitem103.setText(QCoreApplication.translate("PM", u"64", None));
        ___qtablewidgetitem104 = self.tableWidget.item(6, 4)
        ___qtablewidgetitem104.setText(QCoreApplication.translate("PM", u"65", None));
        ___qtablewidgetitem105 = self.tableWidget.item(6, 5)
        ___qtablewidgetitem105.setText(QCoreApplication.translate("PM", u"66", None));
        ___qtablewidgetitem106 = self.tableWidget.item(6, 6)
        ___qtablewidgetitem106.setText(QCoreApplication.translate("PM", u"67", None));
        ___qtablewidgetitem107 = self.tableWidget.item(6, 7)
        ___qtablewidgetitem107.setText(QCoreApplication.translate("PM", u"68", None));
        ___qtablewidgetitem108 = self.tableWidget.item(6, 8)
        ___qtablewidgetitem108.setText(QCoreApplication.translate("PM", u"69", None));
        ___qtablewidgetitem109 = self.tableWidget.item(6, 9)
        ___qtablewidgetitem109.setText(QCoreApplication.translate("PM", u"70", None));
        ___qtablewidgetitem110 = self.tableWidget.item(7, 0)
        ___qtablewidgetitem110.setText(QCoreApplication.translate("PM", u"71", None));
        ___qtablewidgetitem111 = self.tableWidget.item(7, 1)
        ___qtablewidgetitem111.setText(QCoreApplication.translate("PM", u"72", None));
        ___qtablewidgetitem112 = self.tableWidget.item(7, 2)
        ___qtablewidgetitem112.setText(QCoreApplication.translate("PM", u"73", None));
        ___qtablewidgetitem113 = self.tableWidget.item(7, 3)
        ___qtablewidgetitem113.setText(QCoreApplication.translate("PM", u"74", None));
        ___qtablewidgetitem114 = self.tableWidget.item(7, 4)
        ___qtablewidgetitem114.setText(QCoreApplication.translate("PM", u"75", None));
        ___qtablewidgetitem115 = self.tableWidget.item(7, 5)
        ___qtablewidgetitem115.setText(QCoreApplication.translate("PM", u"76", None));
        ___qtablewidgetitem116 = self.tableWidget.item(7, 6)
        ___qtablewidgetitem116.setText(QCoreApplication.translate("PM", u"77", None));
        ___qtablewidgetitem117 = self.tableWidget.item(7, 7)
        ___qtablewidgetitem117.setText(QCoreApplication.translate("PM", u"78", None));
        ___qtablewidgetitem118 = self.tableWidget.item(7, 8)
        ___qtablewidgetitem118.setText(QCoreApplication.translate("PM", u"79", None));
        ___qtablewidgetitem119 = self.tableWidget.item(7, 9)
        ___qtablewidgetitem119.setText(QCoreApplication.translate("PM", u"80", None));
        ___qtablewidgetitem120 = self.tableWidget.item(8, 0)
        ___qtablewidgetitem120.setText(QCoreApplication.translate("PM", u"81", None));
        ___qtablewidgetitem121 = self.tableWidget.item(8, 1)
        ___qtablewidgetitem121.setText(QCoreApplication.translate("PM", u"82", None));
        ___qtablewidgetitem122 = self.tableWidget.item(8, 2)
        ___qtablewidgetitem122.setText(QCoreApplication.translate("PM", u"83", None));
        ___qtablewidgetitem123 = self.tableWidget.item(8, 3)
        ___qtablewidgetitem123.setText(QCoreApplication.translate("PM", u"84", None));
        ___qtablewidgetitem124 = self.tableWidget.item(8, 4)
        ___qtablewidgetitem124.setText(QCoreApplication.translate("PM", u"85", None));
        ___qtablewidgetitem125 = self.tableWidget.item(8, 5)
        ___qtablewidgetitem125.setText(QCoreApplication.translate("PM", u"86", None));
        ___qtablewidgetitem126 = self.tableWidget.item(8, 6)
        ___qtablewidgetitem126.setText(QCoreApplication.translate("PM", u"87", None));
        ___qtablewidgetitem127 = self.tableWidget.item(8, 7)
        ___qtablewidgetitem127.setText(QCoreApplication.translate("PM", u"88", None));
        ___qtablewidgetitem128 = self.tableWidget.item(8, 8)
        ___qtablewidgetitem128.setText(QCoreApplication.translate("PM", u"89", None));
        ___qtablewidgetitem129 = self.tableWidget.item(8, 9)
        ___qtablewidgetitem129.setText(QCoreApplication.translate("PM", u"90", None));
        ___qtablewidgetitem130 = self.tableWidget.item(9, 0)
        ___qtablewidgetitem130.setText(QCoreApplication.translate("PM", u"91", None));
        ___qtablewidgetitem131 = self.tableWidget.item(9, 1)
        ___qtablewidgetitem131.setText(QCoreApplication.translate("PM", u"92", None));
        ___qtablewidgetitem132 = self.tableWidget.item(9, 2)
        ___qtablewidgetitem132.setText(QCoreApplication.translate("PM", u"93", None));
        ___qtablewidgetitem133 = self.tableWidget.item(9, 3)
        ___qtablewidgetitem133.setText(QCoreApplication.translate("PM", u"94", None));
        ___qtablewidgetitem134 = self.tableWidget.item(9, 4)
        ___qtablewidgetitem134.setText(QCoreApplication.translate("PM", u"95", None));
        ___qtablewidgetitem135 = self.tableWidget.item(9, 5)
        ___qtablewidgetitem135.setText(QCoreApplication.translate("PM", u"96", None));
        ___qtablewidgetitem136 = self.tableWidget.item(9, 6)
        ___qtablewidgetitem136.setText(QCoreApplication.translate("PM", u"97", None));
        ___qtablewidgetitem137 = self.tableWidget.item(9, 7)
        ___qtablewidgetitem137.setText(QCoreApplication.translate("PM", u"98", None));
        ___qtablewidgetitem138 = self.tableWidget.item(9, 8)
        ___qtablewidgetitem138.setText(QCoreApplication.translate("PM", u"99", None));
        ___qtablewidgetitem139 = self.tableWidget.item(9, 9)
        ___qtablewidgetitem139.setText(QCoreApplication.translate("PM", u"100", None));
        ___qtablewidgetitem140 = self.tableWidget.item(10, 0)
        ___qtablewidgetitem140.setText(QCoreApplication.translate("PM", u"101", None));
        ___qtablewidgetitem141 = self.tableWidget.item(10, 1)
        ___qtablewidgetitem141.setText(QCoreApplication.translate("PM", u"102", None));
        ___qtablewidgetitem142 = self.tableWidget.item(10, 2)
        ___qtablewidgetitem142.setText(QCoreApplication.translate("PM", u"103", None));
        ___qtablewidgetitem143 = self.tableWidget.item(10, 3)
        ___qtablewidgetitem143.setText(QCoreApplication.translate("PM", u"104", None));
        ___qtablewidgetitem144 = self.tableWidget.item(10, 4)
        ___qtablewidgetitem144.setText(QCoreApplication.translate("PM", u"105", None));
        ___qtablewidgetitem145 = self.tableWidget.item(10, 5)
        ___qtablewidgetitem145.setText(QCoreApplication.translate("PM", u"106", None));
        ___qtablewidgetitem146 = self.tableWidget.item(10, 6)
        ___qtablewidgetitem146.setText(QCoreApplication.translate("PM", u"107", None));
        ___qtablewidgetitem147 = self.tableWidget.item(10, 7)
        ___qtablewidgetitem147.setText(QCoreApplication.translate("PM", u"108", None));
        ___qtablewidgetitem148 = self.tableWidget.item(10, 8)
        ___qtablewidgetitem148.setText(QCoreApplication.translate("PM", u"109", None));
        ___qtablewidgetitem149 = self.tableWidget.item(10, 9)
        ___qtablewidgetitem149.setText(QCoreApplication.translate("PM", u"110", None));
        ___qtablewidgetitem150 = self.tableWidget.item(11, 0)
        ___qtablewidgetitem150.setText(QCoreApplication.translate("PM", u"111", None));
        ___qtablewidgetitem151 = self.tableWidget.item(11, 1)
        ___qtablewidgetitem151.setText(QCoreApplication.translate("PM", u"112", None));
        ___qtablewidgetitem152 = self.tableWidget.item(11, 2)
        ___qtablewidgetitem152.setText(QCoreApplication.translate("PM", u"113", None));
        ___qtablewidgetitem153 = self.tableWidget.item(11, 3)
        ___qtablewidgetitem153.setText(QCoreApplication.translate("PM", u"114", None));
        ___qtablewidgetitem154 = self.tableWidget.item(11, 4)
        ___qtablewidgetitem154.setText(QCoreApplication.translate("PM", u"115", None));
        ___qtablewidgetitem155 = self.tableWidget.item(11, 5)
        ___qtablewidgetitem155.setText(QCoreApplication.translate("PM", u"116", None));
        ___qtablewidgetitem156 = self.tableWidget.item(11, 6)
        ___qtablewidgetitem156.setText(QCoreApplication.translate("PM", u"117", None));
        ___qtablewidgetitem157 = self.tableWidget.item(11, 7)
        ___qtablewidgetitem157.setText(QCoreApplication.translate("PM", u"118", None));
        ___qtablewidgetitem158 = self.tableWidget.item(11, 8)
        ___qtablewidgetitem158.setText(QCoreApplication.translate("PM", u"119", None));
        ___qtablewidgetitem159 = self.tableWidget.item(11, 9)
        ___qtablewidgetitem159.setText(QCoreApplication.translate("PM", u"120", None));
        ___qtablewidgetitem160 = self.tableWidget.item(12, 0)
        ___qtablewidgetitem160.setText(QCoreApplication.translate("PM", u"121", None));
        ___qtablewidgetitem161 = self.tableWidget.item(12, 1)
        ___qtablewidgetitem161.setText(QCoreApplication.translate("PM", u"122", None));
        ___qtablewidgetitem162 = self.tableWidget.item(12, 2)
        ___qtablewidgetitem162.setText(QCoreApplication.translate("PM", u"123", None));
        ___qtablewidgetitem163 = self.tableWidget.item(12, 3)
        ___qtablewidgetitem163.setText(QCoreApplication.translate("PM", u"124", None));
        ___qtablewidgetitem164 = self.tableWidget.item(12, 4)
        ___qtablewidgetitem164.setText(QCoreApplication.translate("PM", u"125", None));
        ___qtablewidgetitem165 = self.tableWidget.item(12, 5)
        ___qtablewidgetitem165.setText(QCoreApplication.translate("PM", u"126", None));
        ___qtablewidgetitem166 = self.tableWidget.item(12, 6)
        ___qtablewidgetitem166.setText(QCoreApplication.translate("PM", u"127", None));
        ___qtablewidgetitem167 = self.tableWidget.item(12, 7)
        ___qtablewidgetitem167.setText(QCoreApplication.translate("PM", u"128", None));
        ___qtablewidgetitem168 = self.tableWidget.item(12, 8)
        ___qtablewidgetitem168.setText(QCoreApplication.translate("PM", u"129", None));
        ___qtablewidgetitem169 = self.tableWidget.item(12, 9)
        ___qtablewidgetitem169.setText(QCoreApplication.translate("PM", u"130", None));
        ___qtablewidgetitem170 = self.tableWidget.item(13, 0)
        ___qtablewidgetitem170.setText(QCoreApplication.translate("PM", u"131", None));
        ___qtablewidgetitem171 = self.tableWidget.item(13, 1)
        ___qtablewidgetitem171.setText(QCoreApplication.translate("PM", u"132", None));
        ___qtablewidgetitem172 = self.tableWidget.item(13, 2)
        ___qtablewidgetitem172.setText(QCoreApplication.translate("PM", u"133", None));
        ___qtablewidgetitem173 = self.tableWidget.item(13, 3)
        ___qtablewidgetitem173.setText(QCoreApplication.translate("PM", u"134", None));
        ___qtablewidgetitem174 = self.tableWidget.item(13, 4)
        ___qtablewidgetitem174.setText(QCoreApplication.translate("PM", u"135", None));
        ___qtablewidgetitem175 = self.tableWidget.item(13, 5)
        ___qtablewidgetitem175.setText(QCoreApplication.translate("PM", u"136", None));
        ___qtablewidgetitem176 = self.tableWidget.item(13, 6)
        ___qtablewidgetitem176.setText(QCoreApplication.translate("PM", u"137", None));
        ___qtablewidgetitem177 = self.tableWidget.item(13, 7)
        ___qtablewidgetitem177.setText(QCoreApplication.translate("PM", u"138", None));
        ___qtablewidgetitem178 = self.tableWidget.item(13, 8)
        ___qtablewidgetitem178.setText(QCoreApplication.translate("PM", u"139", None));
        ___qtablewidgetitem179 = self.tableWidget.item(13, 9)
        ___qtablewidgetitem179.setText(QCoreApplication.translate("PM", u"140", None));
        ___qtablewidgetitem180 = self.tableWidget.item(14, 0)
        ___qtablewidgetitem180.setText(QCoreApplication.translate("PM", u"141", None));
        ___qtablewidgetitem181 = self.tableWidget.item(14, 1)
        ___qtablewidgetitem181.setText(QCoreApplication.translate("PM", u"142", None));
        ___qtablewidgetitem182 = self.tableWidget.item(14, 2)
        ___qtablewidgetitem182.setText(QCoreApplication.translate("PM", u"143", None));
        ___qtablewidgetitem183 = self.tableWidget.item(14, 3)
        ___qtablewidgetitem183.setText(QCoreApplication.translate("PM", u"144", None));
        ___qtablewidgetitem184 = self.tableWidget.item(14, 4)
        ___qtablewidgetitem184.setText(QCoreApplication.translate("PM", u"145", None));
        ___qtablewidgetitem185 = self.tableWidget.item(14, 5)
        ___qtablewidgetitem185.setText(QCoreApplication.translate("PM", u"146", None));
        ___qtablewidgetitem186 = self.tableWidget.item(14, 6)
        ___qtablewidgetitem186.setText(QCoreApplication.translate("PM", u"147", None));
        ___qtablewidgetitem187 = self.tableWidget.item(14, 7)
        ___qtablewidgetitem187.setText(QCoreApplication.translate("PM", u"148", None));
        ___qtablewidgetitem188 = self.tableWidget.item(14, 8)
        ___qtablewidgetitem188.setText(QCoreApplication.translate("PM", u"148", None));
        ___qtablewidgetitem189 = self.tableWidget.item(14, 9)
        ___qtablewidgetitem189.setText(QCoreApplication.translate("PM", u"150", None));
        ___qtablewidgetitem190 = self.tableWidget.item(15, 0)
        ___qtablewidgetitem190.setText(QCoreApplication.translate("PM", u"151", None));
        ___qtablewidgetitem191 = self.tableWidget.item(15, 1)
        ___qtablewidgetitem191.setText(QCoreApplication.translate("PM", u"152", None));
        ___qtablewidgetitem192 = self.tableWidget.item(15, 2)
        ___qtablewidgetitem192.setText(QCoreApplication.translate("PM", u"153", None));
        ___qtablewidgetitem193 = self.tableWidget.item(15, 3)
        ___qtablewidgetitem193.setText(QCoreApplication.translate("PM", u"154", None));
        ___qtablewidgetitem194 = self.tableWidget.item(15, 4)
        ___qtablewidgetitem194.setText(QCoreApplication.translate("PM", u"155", None));
        ___qtablewidgetitem195 = self.tableWidget.item(15, 5)
        ___qtablewidgetitem195.setText(QCoreApplication.translate("PM", u"156", None));
        ___qtablewidgetitem196 = self.tableWidget.item(15, 6)
        ___qtablewidgetitem196.setText(QCoreApplication.translate("PM", u"157", None));
        ___qtablewidgetitem197 = self.tableWidget.item(15, 7)
        ___qtablewidgetitem197.setText(QCoreApplication.translate("PM", u"158", None));
        ___qtablewidgetitem198 = self.tableWidget.item(15, 8)
        ___qtablewidgetitem198.setText(QCoreApplication.translate("PM", u"159", None));
        ___qtablewidgetitem199 = self.tableWidget.item(15, 9)
        ___qtablewidgetitem199.setText(QCoreApplication.translate("PM", u"160", None));
        ___qtablewidgetitem200 = self.tableWidget.item(16, 0)
        ___qtablewidgetitem200.setText(QCoreApplication.translate("PM", u"161", None));
        ___qtablewidgetitem201 = self.tableWidget.item(16, 1)
        ___qtablewidgetitem201.setText(QCoreApplication.translate("PM", u"162", None));
        ___qtablewidgetitem202 = self.tableWidget.item(16, 2)
        ___qtablewidgetitem202.setText(QCoreApplication.translate("PM", u"163", None));
        ___qtablewidgetitem203 = self.tableWidget.item(16, 3)
        ___qtablewidgetitem203.setText(QCoreApplication.translate("PM", u"164", None));
        ___qtablewidgetitem204 = self.tableWidget.item(16, 4)
        ___qtablewidgetitem204.setText(QCoreApplication.translate("PM", u"165", None));
        ___qtablewidgetitem205 = self.tableWidget.item(16, 5)
        ___qtablewidgetitem205.setText(QCoreApplication.translate("PM", u"166", None));
        ___qtablewidgetitem206 = self.tableWidget.item(16, 6)
        ___qtablewidgetitem206.setText(QCoreApplication.translate("PM", u"167", None));
        ___qtablewidgetitem207 = self.tableWidget.item(16, 7)
        ___qtablewidgetitem207.setText(QCoreApplication.translate("PM", u"168", None));
        ___qtablewidgetitem208 = self.tableWidget.item(16, 8)
        ___qtablewidgetitem208.setText(QCoreApplication.translate("PM", u"169", None));
        ___qtablewidgetitem209 = self.tableWidget.item(16, 9)
        ___qtablewidgetitem209.setText(QCoreApplication.translate("PM", u"170", None));
        ___qtablewidgetitem210 = self.tableWidget.item(17, 0)
        ___qtablewidgetitem210.setText(QCoreApplication.translate("PM", u"171", None));
        ___qtablewidgetitem211 = self.tableWidget.item(17, 1)
        ___qtablewidgetitem211.setText(QCoreApplication.translate("PM", u"172", None));
        ___qtablewidgetitem212 = self.tableWidget.item(17, 2)
        ___qtablewidgetitem212.setText(QCoreApplication.translate("PM", u"173", None));
        ___qtablewidgetitem213 = self.tableWidget.item(17, 3)
        ___qtablewidgetitem213.setText(QCoreApplication.translate("PM", u"174", None));
        ___qtablewidgetitem214 = self.tableWidget.item(17, 4)
        ___qtablewidgetitem214.setText(QCoreApplication.translate("PM", u"174", None));
        ___qtablewidgetitem215 = self.tableWidget.item(17, 5)
        ___qtablewidgetitem215.setText(QCoreApplication.translate("PM", u"176", None));
        ___qtablewidgetitem216 = self.tableWidget.item(17, 6)
        ___qtablewidgetitem216.setText(QCoreApplication.translate("PM", u"177", None));
        ___qtablewidgetitem217 = self.tableWidget.item(17, 7)
        ___qtablewidgetitem217.setText(QCoreApplication.translate("PM", u"178", None));
        ___qtablewidgetitem218 = self.tableWidget.item(17, 8)
        ___qtablewidgetitem218.setText(QCoreApplication.translate("PM", u"179", None));
        ___qtablewidgetitem219 = self.tableWidget.item(17, 9)
        ___qtablewidgetitem219.setText(QCoreApplication.translate("PM", u"180", None));
        ___qtablewidgetitem220 = self.tableWidget.item(18, 0)
        ___qtablewidgetitem220.setText(QCoreApplication.translate("PM", u"181", None));
        ___qtablewidgetitem221 = self.tableWidget.item(18, 1)
        ___qtablewidgetitem221.setText(QCoreApplication.translate("PM", u"182", None));
        ___qtablewidgetitem222 = self.tableWidget.item(18, 2)
        ___qtablewidgetitem222.setText(QCoreApplication.translate("PM", u"183", None));
        ___qtablewidgetitem223 = self.tableWidget.item(18, 3)
        ___qtablewidgetitem223.setText(QCoreApplication.translate("PM", u"184", None));
        ___qtablewidgetitem224 = self.tableWidget.item(18, 4)
        ___qtablewidgetitem224.setText(QCoreApplication.translate("PM", u"185", None));
        ___qtablewidgetitem225 = self.tableWidget.item(18, 5)
        ___qtablewidgetitem225.setText(QCoreApplication.translate("PM", u"186", None));
        ___qtablewidgetitem226 = self.tableWidget.item(18, 6)
        ___qtablewidgetitem226.setText(QCoreApplication.translate("PM", u"187", None));
        ___qtablewidgetitem227 = self.tableWidget.item(18, 7)
        ___qtablewidgetitem227.setText(QCoreApplication.translate("PM", u"188", None));
        ___qtablewidgetitem228 = self.tableWidget.item(18, 8)
        ___qtablewidgetitem228.setText(QCoreApplication.translate("PM", u"189", None));
        ___qtablewidgetitem229 = self.tableWidget.item(18, 9)
        ___qtablewidgetitem229.setText(QCoreApplication.translate("PM", u"190", None));
        ___qtablewidgetitem230 = self.tableWidget.item(19, 0)
        ___qtablewidgetitem230.setText(QCoreApplication.translate("PM", u"191", None));
        ___qtablewidgetitem231 = self.tableWidget.item(19, 1)
        ___qtablewidgetitem231.setText(QCoreApplication.translate("PM", u"192", None));
        ___qtablewidgetitem232 = self.tableWidget.item(19, 2)
        ___qtablewidgetitem232.setText(QCoreApplication.translate("PM", u"193", None));
        ___qtablewidgetitem233 = self.tableWidget.item(19, 3)
        ___qtablewidgetitem233.setText(QCoreApplication.translate("PM", u"194", None));
        ___qtablewidgetitem234 = self.tableWidget.item(19, 4)
        ___qtablewidgetitem234.setText(QCoreApplication.translate("PM", u"195", None));
        ___qtablewidgetitem235 = self.tableWidget.item(19, 5)
        ___qtablewidgetitem235.setText(QCoreApplication.translate("PM", u"196", None));
        ___qtablewidgetitem236 = self.tableWidget.item(19, 6)
        ___qtablewidgetitem236.setText(QCoreApplication.translate("PM", u"197", None));
        ___qtablewidgetitem237 = self.tableWidget.item(19, 7)
        ___qtablewidgetitem237.setText(QCoreApplication.translate("PM", u"198", None));
        ___qtablewidgetitem238 = self.tableWidget.item(19, 8)
        ___qtablewidgetitem238.setText(QCoreApplication.translate("PM", u"199", None));
        ___qtablewidgetitem239 = self.tableWidget.item(19, 9)
        ___qtablewidgetitem239.setText(QCoreApplication.translate("PM", u"200", None));
        ___qtablewidgetitem240 = self.tableWidget.item(20, 0)
        ___qtablewidgetitem240.setText(QCoreApplication.translate("PM", u"201", None));
        ___qtablewidgetitem241 = self.tableWidget.item(20, 1)
        ___qtablewidgetitem241.setText(QCoreApplication.translate("PM", u"202", None));
        ___qtablewidgetitem242 = self.tableWidget.item(20, 2)
        ___qtablewidgetitem242.setText(QCoreApplication.translate("PM", u"203", None));
        ___qtablewidgetitem243 = self.tableWidget.item(20, 3)
        ___qtablewidgetitem243.setText(QCoreApplication.translate("PM", u"204", None));
        ___qtablewidgetitem244 = self.tableWidget.item(20, 4)
        ___qtablewidgetitem244.setText(QCoreApplication.translate("PM", u"205", None));
        ___qtablewidgetitem245 = self.tableWidget.item(20, 5)
        ___qtablewidgetitem245.setText(QCoreApplication.translate("PM", u"206", None));
        ___qtablewidgetitem246 = self.tableWidget.item(20, 6)
        ___qtablewidgetitem246.setText(QCoreApplication.translate("PM", u"207", None));
        ___qtablewidgetitem247 = self.tableWidget.item(20, 7)
        ___qtablewidgetitem247.setText(QCoreApplication.translate("PM", u"208", None));
        ___qtablewidgetitem248 = self.tableWidget.item(20, 8)
        ___qtablewidgetitem248.setText(QCoreApplication.translate("PM", u"209", None));
        ___qtablewidgetitem249 = self.tableWidget.item(20, 9)
        ___qtablewidgetitem249.setText(QCoreApplication.translate("PM", u"210", None));
        ___qtablewidgetitem250 = self.tableWidget.item(21, 0)
        ___qtablewidgetitem250.setText(QCoreApplication.translate("PM", u"211", None));
        ___qtablewidgetitem251 = self.tableWidget.item(21, 1)
        ___qtablewidgetitem251.setText(QCoreApplication.translate("PM", u"212", None));
        ___qtablewidgetitem252 = self.tableWidget.item(21, 2)
        ___qtablewidgetitem252.setText(QCoreApplication.translate("PM", u"213", None));
        ___qtablewidgetitem253 = self.tableWidget.item(21, 3)
        ___qtablewidgetitem253.setText(QCoreApplication.translate("PM", u"214", None));
        ___qtablewidgetitem254 = self.tableWidget.item(21, 4)
        ___qtablewidgetitem254.setText(QCoreApplication.translate("PM", u"215", None));
        ___qtablewidgetitem255 = self.tableWidget.item(21, 5)
        ___qtablewidgetitem255.setText(QCoreApplication.translate("PM", u"216", None));
        ___qtablewidgetitem256 = self.tableWidget.item(21, 6)
        ___qtablewidgetitem256.setText(QCoreApplication.translate("PM", u"217", None));
        ___qtablewidgetitem257 = self.tableWidget.item(21, 7)
        ___qtablewidgetitem257.setText(QCoreApplication.translate("PM", u"218", None));
        ___qtablewidgetitem258 = self.tableWidget.item(21, 8)
        ___qtablewidgetitem258.setText(QCoreApplication.translate("PM", u"219", None));
        ___qtablewidgetitem259 = self.tableWidget.item(21, 9)
        ___qtablewidgetitem259.setText(QCoreApplication.translate("PM", u"220", None));
        ___qtablewidgetitem260 = self.tableWidget.item(22, 0)
        ___qtablewidgetitem260.setText(QCoreApplication.translate("PM", u"221", None));
        ___qtablewidgetitem261 = self.tableWidget.item(22, 1)
        ___qtablewidgetitem261.setText(QCoreApplication.translate("PM", u"222", None));
        ___qtablewidgetitem262 = self.tableWidget.item(22, 2)
        ___qtablewidgetitem262.setText(QCoreApplication.translate("PM", u"223", None));
        ___qtablewidgetitem263 = self.tableWidget.item(22, 3)
        ___qtablewidgetitem263.setText(QCoreApplication.translate("PM", u"224", None));
        ___qtablewidgetitem264 = self.tableWidget.item(22, 4)
        ___qtablewidgetitem264.setText(QCoreApplication.translate("PM", u"225", None));
        ___qtablewidgetitem265 = self.tableWidget.item(22, 5)
        ___qtablewidgetitem265.setText(QCoreApplication.translate("PM", u"226", None));
        ___qtablewidgetitem266 = self.tableWidget.item(22, 6)
        ___qtablewidgetitem266.setText(QCoreApplication.translate("PM", u"227", None));
        ___qtablewidgetitem267 = self.tableWidget.item(22, 7)
        ___qtablewidgetitem267.setText(QCoreApplication.translate("PM", u"228", None));
        ___qtablewidgetitem268 = self.tableWidget.item(22, 8)
        ___qtablewidgetitem268.setText(QCoreApplication.translate("PM", u"229", None));
        ___qtablewidgetitem269 = self.tableWidget.item(22, 9)
        ___qtablewidgetitem269.setText(QCoreApplication.translate("PM", u"230", None));
        ___qtablewidgetitem270 = self.tableWidget.item(23, 0)
        ___qtablewidgetitem270.setText(QCoreApplication.translate("PM", u"231", None));
        ___qtablewidgetitem271 = self.tableWidget.item(23, 1)
        ___qtablewidgetitem271.setText(QCoreApplication.translate("PM", u"232", None));
        ___qtablewidgetitem272 = self.tableWidget.item(23, 2)
        ___qtablewidgetitem272.setText(QCoreApplication.translate("PM", u"233", None));
        ___qtablewidgetitem273 = self.tableWidget.item(23, 3)
        ___qtablewidgetitem273.setText(QCoreApplication.translate("PM", u"234", None));
        ___qtablewidgetitem274 = self.tableWidget.item(23, 4)
        ___qtablewidgetitem274.setText(QCoreApplication.translate("PM", u"235", None));
        ___qtablewidgetitem275 = self.tableWidget.item(23, 5)
        ___qtablewidgetitem275.setText(QCoreApplication.translate("PM", u"236", None));
        ___qtablewidgetitem276 = self.tableWidget.item(23, 6)
        ___qtablewidgetitem276.setText(QCoreApplication.translate("PM", u"237", None));
        ___qtablewidgetitem277 = self.tableWidget.item(23, 7)
        ___qtablewidgetitem277.setText(QCoreApplication.translate("PM", u"238", None));
        ___qtablewidgetitem278 = self.tableWidget.item(23, 8)
        ___qtablewidgetitem278.setText(QCoreApplication.translate("PM", u"239", None));
        ___qtablewidgetitem279 = self.tableWidget.item(23, 9)
        ___qtablewidgetitem279.setText(QCoreApplication.translate("PM", u"240", None));
        ___qtablewidgetitem280 = self.tableWidget.item(24, 0)
        ___qtablewidgetitem280.setText(QCoreApplication.translate("PM", u"241", None));
        ___qtablewidgetitem281 = self.tableWidget.item(24, 1)
        ___qtablewidgetitem281.setText(QCoreApplication.translate("PM", u"242", None));
        ___qtablewidgetitem282 = self.tableWidget.item(24, 2)
        ___qtablewidgetitem282.setText(QCoreApplication.translate("PM", u"243", None));
        ___qtablewidgetitem283 = self.tableWidget.item(24, 3)
        ___qtablewidgetitem283.setText(QCoreApplication.translate("PM", u"244", None));
        ___qtablewidgetitem284 = self.tableWidget.item(24, 4)
        ___qtablewidgetitem284.setText(QCoreApplication.translate("PM", u"245", None));
        ___qtablewidgetitem285 = self.tableWidget.item(24, 5)
        ___qtablewidgetitem285.setText(QCoreApplication.translate("PM", u"246", None));
        ___qtablewidgetitem286 = self.tableWidget.item(24, 6)
        ___qtablewidgetitem286.setText(QCoreApplication.translate("PM", u"247", None));
        ___qtablewidgetitem287 = self.tableWidget.item(24, 7)
        ___qtablewidgetitem287.setText(QCoreApplication.translate("PM", u"248", None));
        ___qtablewidgetitem288 = self.tableWidget.item(24, 8)
        ___qtablewidgetitem288.setText(QCoreApplication.translate("PM", u"249", None));
        ___qtablewidgetitem289 = self.tableWidget.item(24, 9)
        ___qtablewidgetitem289.setText(QCoreApplication.translate("PM", u"250", None));
        ___qtablewidgetitem290 = self.tableWidget.item(25, 0)
        ___qtablewidgetitem290.setText(QCoreApplication.translate("PM", u"251", None));
        ___qtablewidgetitem291 = self.tableWidget.item(25, 1)
        ___qtablewidgetitem291.setText(QCoreApplication.translate("PM", u"252", None));
        ___qtablewidgetitem292 = self.tableWidget.item(25, 2)
        ___qtablewidgetitem292.setText(QCoreApplication.translate("PM", u"253", None));
        ___qtablewidgetitem293 = self.tableWidget.item(25, 3)
        ___qtablewidgetitem293.setText(QCoreApplication.translate("PM", u"254", None));
        ___qtablewidgetitem294 = self.tableWidget.item(25, 4)
        ___qtablewidgetitem294.setText(QCoreApplication.translate("PM", u"255", None));
        ___qtablewidgetitem295 = self.tableWidget.item(25, 5)
        ___qtablewidgetitem295.setText(QCoreApplication.translate("PM", u"256", None));
        ___qtablewidgetitem296 = self.tableWidget.item(25, 6)
        ___qtablewidgetitem296.setText(QCoreApplication.translate("PM", u"257", None));
        ___qtablewidgetitem297 = self.tableWidget.item(25, 7)
        ___qtablewidgetitem297.setText(QCoreApplication.translate("PM", u"258", None));
        ___qtablewidgetitem298 = self.tableWidget.item(25, 8)
        ___qtablewidgetitem298.setText(QCoreApplication.translate("PM", u"259", None));
        ___qtablewidgetitem299 = self.tableWidget.item(25, 9)
        ___qtablewidgetitem299.setText(QCoreApplication.translate("PM", u"260", None));
        ___qtablewidgetitem300 = self.tableWidget.item(26, 0)
        ___qtablewidgetitem300.setText(QCoreApplication.translate("PM", u"261", None));
        ___qtablewidgetitem301 = self.tableWidget.item(26, 1)
        ___qtablewidgetitem301.setText(QCoreApplication.translate("PM", u"262", None));
        ___qtablewidgetitem302 = self.tableWidget.item(26, 2)
        ___qtablewidgetitem302.setText(QCoreApplication.translate("PM", u"263", None));
        ___qtablewidgetitem303 = self.tableWidget.item(26, 3)
        ___qtablewidgetitem303.setText(QCoreApplication.translate("PM", u"264", None));
        ___qtablewidgetitem304 = self.tableWidget.item(26, 4)
        ___qtablewidgetitem304.setText(QCoreApplication.translate("PM", u"265", None));
        ___qtablewidgetitem305 = self.tableWidget.item(26, 5)
        ___qtablewidgetitem305.setText(QCoreApplication.translate("PM", u"266", None));
        ___qtablewidgetitem306 = self.tableWidget.item(26, 6)
        ___qtablewidgetitem306.setText(QCoreApplication.translate("PM", u"267", None));
        ___qtablewidgetitem307 = self.tableWidget.item(26, 7)
        ___qtablewidgetitem307.setText(QCoreApplication.translate("PM", u"268", None));
        ___qtablewidgetitem308 = self.tableWidget.item(26, 8)
        ___qtablewidgetitem308.setText(QCoreApplication.translate("PM", u"269", None));
        ___qtablewidgetitem309 = self.tableWidget.item(26, 9)
        ___qtablewidgetitem309.setText(QCoreApplication.translate("PM", u"270", None));
        ___qtablewidgetitem310 = self.tableWidget.item(27, 0)
        ___qtablewidgetitem310.setText(QCoreApplication.translate("PM", u"271", None));
        ___qtablewidgetitem311 = self.tableWidget.item(27, 1)
        ___qtablewidgetitem311.setText(QCoreApplication.translate("PM", u"272", None));
        ___qtablewidgetitem312 = self.tableWidget.item(27, 2)
        ___qtablewidgetitem312.setText(QCoreApplication.translate("PM", u"273", None));
        ___qtablewidgetitem313 = self.tableWidget.item(27, 3)
        ___qtablewidgetitem313.setText(QCoreApplication.translate("PM", u"274", None));
        ___qtablewidgetitem314 = self.tableWidget.item(27, 4)
        ___qtablewidgetitem314.setText(QCoreApplication.translate("PM", u"275", None));
        ___qtablewidgetitem315 = self.tableWidget.item(27, 5)
        ___qtablewidgetitem315.setText(QCoreApplication.translate("PM", u"276", None));
        ___qtablewidgetitem316 = self.tableWidget.item(27, 6)
        ___qtablewidgetitem316.setText(QCoreApplication.translate("PM", u"277", None));
        ___qtablewidgetitem317 = self.tableWidget.item(27, 7)
        ___qtablewidgetitem317.setText(QCoreApplication.translate("PM", u"278", None));
        ___qtablewidgetitem318 = self.tableWidget.item(27, 8)
        ___qtablewidgetitem318.setText(QCoreApplication.translate("PM", u"279", None));
        ___qtablewidgetitem319 = self.tableWidget.item(27, 9)
        ___qtablewidgetitem319.setText(QCoreApplication.translate("PM", u"280", None));
        ___qtablewidgetitem320 = self.tableWidget.item(28, 0)
        ___qtablewidgetitem320.setText(QCoreApplication.translate("PM", u"281", None));
        ___qtablewidgetitem321 = self.tableWidget.item(28, 1)
        ___qtablewidgetitem321.setText(QCoreApplication.translate("PM", u"282", None));
        ___qtablewidgetitem322 = self.tableWidget.item(28, 2)
        ___qtablewidgetitem322.setText(QCoreApplication.translate("PM", u"283", None));
        ___qtablewidgetitem323 = self.tableWidget.item(28, 3)
        ___qtablewidgetitem323.setText(QCoreApplication.translate("PM", u"284", None));
        ___qtablewidgetitem324 = self.tableWidget.item(28, 4)
        ___qtablewidgetitem324.setText(QCoreApplication.translate("PM", u"285", None));
        ___qtablewidgetitem325 = self.tableWidget.item(28, 5)
        ___qtablewidgetitem325.setText(QCoreApplication.translate("PM", u"286", None));
        ___qtablewidgetitem326 = self.tableWidget.item(28, 6)
        ___qtablewidgetitem326.setText(QCoreApplication.translate("PM", u"287", None));
        ___qtablewidgetitem327 = self.tableWidget.item(28, 7)
        ___qtablewidgetitem327.setText(QCoreApplication.translate("PM", u"288", None));
        ___qtablewidgetitem328 = self.tableWidget.item(28, 8)
        ___qtablewidgetitem328.setText(QCoreApplication.translate("PM", u"289", None));
        ___qtablewidgetitem329 = self.tableWidget.item(28, 9)
        ___qtablewidgetitem329.setText(QCoreApplication.translate("PM", u"290", None));
        ___qtablewidgetitem330 = self.tableWidget.item(29, 0)
        ___qtablewidgetitem330.setText(QCoreApplication.translate("PM", u"291", None));
        ___qtablewidgetitem331 = self.tableWidget.item(29, 1)
        ___qtablewidgetitem331.setText(QCoreApplication.translate("PM", u"292", None));
        ___qtablewidgetitem332 = self.tableWidget.item(29, 2)
        ___qtablewidgetitem332.setText(QCoreApplication.translate("PM", u"293", None));
        ___qtablewidgetitem333 = self.tableWidget.item(29, 3)
        ___qtablewidgetitem333.setText(QCoreApplication.translate("PM", u"294", None));
        ___qtablewidgetitem334 = self.tableWidget.item(29, 4)
        ___qtablewidgetitem334.setText(QCoreApplication.translate("PM", u"295", None));
        ___qtablewidgetitem335 = self.tableWidget.item(29, 5)
        ___qtablewidgetitem335.setText(QCoreApplication.translate("PM", u"296", None));
        ___qtablewidgetitem336 = self.tableWidget.item(29, 6)
        ___qtablewidgetitem336.setText(QCoreApplication.translate("PM", u"297", None));
        ___qtablewidgetitem337 = self.tableWidget.item(29, 7)
        ___qtablewidgetitem337.setText(QCoreApplication.translate("PM", u"298", None));
        ___qtablewidgetitem338 = self.tableWidget.item(29, 8)
        ___qtablewidgetitem338.setText(QCoreApplication.translate("PM", u"299", None));
        ___qtablewidgetitem339 = self.tableWidget.item(29, 9)
        ___qtablewidgetitem339.setText(QCoreApplication.translate("PM", u"300", None));
        self.tableWidget.setSortingEnabled(__sortingEnabled)

        self.label_16.setText(QCoreApplication.translate("PM", u" Fixture(E-FPC) check point  ", None))
        self.label_13.setText(QCoreApplication.translate("PM", u"Item check : 1. Check Tag", None))
        self.label_17.setText(QCoreApplication.translate("PM", u"Code tooling \u0e16\u0e39\u0e01\u0e15\u0e49\u0e2d\u0e07", None))
        self.comboBox.setItemText(0, "")
        self.comboBox.setItemText(1, QCoreApplication.translate("PM", u"Pass", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("PM", u"Not pass", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("PM", u"Not check", None))

        self.comboBox.setPlaceholderText("")
        self.lineEdit_4.setPlaceholderText(QCoreApplication.translate("PM", u"\u0e2b\u0e21\u0e32\u0e22\u0e40\u0e2b\u0e15\u0e38", None))
        self.label_18.setText(QCoreApplication.translate("PM", u"\u0e1b\u0e49\u0e32\u0e22\u0e0a\u0e37\u0e48\u0e2d\u0e44\u0e21\u0e48\u0e25\u0e1a\u0e40\u0e25\u0e37\u0e2d\u0e19, \u0e0a\u0e33\u0e23\u0e38\u0e14", None))
        self.comboBox_2.setItemText(0, "")
        self.comboBox_2.setItemText(1, QCoreApplication.translate("PM", u"Pass", None))
        self.comboBox_2.setItemText(2, QCoreApplication.translate("PM", u"Not pass", None))
        self.comboBox_2.setItemText(3, QCoreApplication.translate("PM", u"Not check", None))

        self.lineEdit_5.setPlaceholderText(QCoreApplication.translate("PM", u"\u0e2b\u0e21\u0e32\u0e22\u0e40\u0e2b\u0e15\u0e38", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("PM", u"1.Check Tag", None))
        self.label_19.setText(QCoreApplication.translate("PM", u"Item check :  2. Program", None))
        self.label_15.setText(QCoreApplication.translate("PM", u"\u0e15\u0e23\u0e07\u0e15\u0e32\u0e21\u0e0a\u0e37\u0e48\u0e2d Product", None))
        self.comboBox_3.setItemText(0, "")
        self.comboBox_3.setItemText(1, QCoreApplication.translate("PM", u"Pass", None))
        self.comboBox_3.setItemText(2, QCoreApplication.translate("PM", u"Not pass", None))
        self.comboBox_3.setItemText(3, QCoreApplication.translate("PM", u"Not check", None))

        self.lineEdit_6.setPlaceholderText(QCoreApplication.translate("PM", u"\u0e2b\u0e21\u0e32\u0e22\u0e40\u0e2b\u0e15\u0e38", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("PM", u"2.Program", None))
        self.label_20.setText(QCoreApplication.translate("PM", u"Item check :  3. Check probe pin", None))
        self.label_21.setText(QCoreApplication.translate("PM", u"\u0e44\u0e21\u0e48\u0e2b\u0e31\u0e01,\u0e44\u0e21\u0e48\u0e22\u0e38\u0e1a,\u0e44\u0e21\u0e48\u0e42\u0e04\u0e49\u0e07\u0e07\u0e2d", None))
        self.comboBox_4.setItemText(0, "")
        self.comboBox_4.setItemText(1, QCoreApplication.translate("PM", u"Pass", None))
        self.comboBox_4.setItemText(2, QCoreApplication.translate("PM", u"Not pass", None))
        self.comboBox_4.setItemText(3, QCoreApplication.translate("PM", u"Not check", None))

        self.lineEdit_9.setPlaceholderText(QCoreApplication.translate("PM", u"\u0e2b\u0e21\u0e32\u0e22\u0e40\u0e2b\u0e15\u0e38", None))
        self.label_22.setText(QCoreApplication.translate("PM", u"\u0e21\u0e35\u0e04\u0e23\u0e1a\u0e17\u0e38\u0e01\u0e15\u0e33\u0e41\u0e2b\u0e19\u0e48\u0e07", None))
        self.comboBox_5.setItemText(0, "")
        self.comboBox_5.setItemText(1, QCoreApplication.translate("PM", u"Pass", None))
        self.comboBox_5.setItemText(2, QCoreApplication.translate("PM", u"Not pass", None))
        self.comboBox_5.setItemText(3, QCoreApplication.translate("PM", u"Not check", None))

        self.lineEdit_8.setPlaceholderText(QCoreApplication.translate("PM", u"\u0e2b\u0e21\u0e32\u0e22\u0e40\u0e2b\u0e15\u0e38", None))
        self.label_23.setText(QCoreApplication.translate("PM", u"\u25ba \u0e2a\u0e33\u0e2b\u0e23\u0e31\u0e1a Wire pin OST & Wire pin Tester \u0e16\u0e2d\u0e14\u0e0a\u0e38\u0e14 Enamel wire", None))
        self.label_24.setText(QCoreApplication.translate("PM", u"\u0e15\u0e23\u0e27\u0e08\u0e2a\u0e2d\u0e1a\u0e43\u0e15\u0e49\u0e01\u0e25\u0e49\u0e2d\u0e07 Microscope Enamel wire \u0e08\u0e30\u0e15\u0e49\u0e2d\u0e07\u0e44\u0e21\u0e48\u0e22\u0e38\u0e1a\u0e15\u0e31\u0e27 \u0e2b\u0e23\u0e37\u0e2d\u0e21\u0e35\u0e04\u0e23\u0e32\u0e1a\u0e2a\u0e19\u0e34\u0e21", None))
        self.comboBox_6.setItemText(0, "")
        self.comboBox_6.setItemText(1, QCoreApplication.translate("PM", u"Pass", None))
        self.comboBox_6.setItemText(2, QCoreApplication.translate("PM", u"Not pass", None))
        self.comboBox_6.setItemText(3, QCoreApplication.translate("PM", u"Not check", None))

        self.lineEdit_7.setPlaceholderText(QCoreApplication.translate("PM", u"\u0e2b\u0e21\u0e32\u0e22\u0e40\u0e2b\u0e15\u0e38", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("PM", u"3.Check Probe pin", None))
        self.label_25.setText(QCoreApplication.translate("PM", u"Item check :  4. Check pin lock product", None))
        self.label_26.setText(QCoreApplication.translate("PM", u"\u0e21\u0e35\u0e04\u0e23\u0e1a\u0e17\u0e38\u0e01\u0e15\u0e33\u0e41\u0e2b\u0e19\u0e48\u0e07", None))
        self.comboBox_7.setItemText(0, "")
        self.comboBox_7.setItemText(1, QCoreApplication.translate("PM", u"Pass", None))
        self.comboBox_7.setItemText(2, QCoreApplication.translate("PM", u"Not pass", None))
        self.comboBox_7.setItemText(3, QCoreApplication.translate("PM", u"Not check", None))

        self.lineEdit_10.setPlaceholderText(QCoreApplication.translate("PM", u"\u0e2b\u0e21\u0e32\u0e22\u0e40\u0e2b\u0e15\u0e38", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("PM", u"4.Check pin lock product", None))
        self.label_27.setText(QCoreApplication.translate("PM", u"Item check :  5. Check \u0e42\u0e04\u0e23\u0e07\u0e2a\u0e23\u0e49\u0e32\u0e07\u0e17\u0e31\u0e48\u0e27\u0e44\u0e1b", None))
        self.label_28.setText(QCoreApplication.translate("PM", u"\u0e2a\u0e20\u0e32\u0e1e\u0e19\u0e4a\u0e2d\u0e15\u0e2a\u0e21\u0e1a\u0e39\u0e23\u0e13\u0e4c\u0e44\u0e21\u0e48\u0e2b\u0e25\u0e27\u0e21\u0e2b\u0e25\u0e38\u0e14", None))
        self.comboBox_8.setItemText(0, "")
        self.comboBox_8.setItemText(1, QCoreApplication.translate("PM", u"Pass", None))
        self.comboBox_8.setItemText(2, QCoreApplication.translate("PM", u"Not pass", None))
        self.comboBox_8.setItemText(3, QCoreApplication.translate("PM", u"Not check", None))

        self.lineEdit_11.setPlaceholderText(QCoreApplication.translate("PM", u"\u0e2b\u0e21\u0e32\u0e22\u0e40\u0e2b\u0e15\u0e38", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), QCoreApplication.translate("PM", u"5. Check \u0e42\u0e04\u0e23\u0e07\u0e2a\u0e23\u0e49\u0e32\u0e07\u0e17\u0e31\u0e48\u0e27\u0e44\u0e1b", None))
        self.label_29.setText(QCoreApplication.translate("PM", u"Item check :  6. Check Master", None))
        self.label_33.setText(QCoreApplication.translate("PM", u"Master Good  \u0e15\u0e49\u0e2d\u0e07 Pass ", None))
        self.label_32.setText(QCoreApplication.translate("PM", u" - Product \u0e15\u0e49\u0e2d\u0e07\u0e44\u0e21\u0e48\u0e09\u0e35\u0e01\u0e02\u0e32\u0e14 ", None))
        self.comboBox_11.setItemText(0, "")
        self.comboBox_11.setItemText(1, QCoreApplication.translate("PM", u"Pass", None))
        self.comboBox_11.setItemText(2, QCoreApplication.translate("PM", u"Not pass", None))
        self.comboBox_11.setItemText(3, QCoreApplication.translate("PM", u"Not check", None))

        self.lineEdit_14.setPlaceholderText(QCoreApplication.translate("PM", u"\u0e2b\u0e21\u0e32\u0e22\u0e40\u0e2b\u0e15\u0e38", None))
        self.label_31.setText(QCoreApplication.translate("PM", u" - Master good \u0e15\u0e49\u0e2d\u0e07 Test  Pass \u0e43\u0e19 shot \u0e19\u0e31\u0e49\u0e19\u0e46", None))
        self.comboBox_10.setItemText(0, "")
        self.comboBox_10.setItemText(1, QCoreApplication.translate("PM", u"Pass", None))
        self.comboBox_10.setItemText(2, QCoreApplication.translate("PM", u"Not pass", None))
        self.comboBox_10.setItemText(3, QCoreApplication.translate("PM", u"Not check", None))

        self.lineEdit_15.setPlaceholderText(QCoreApplication.translate("PM", u"\u0e2b\u0e21\u0e32\u0e22\u0e40\u0e2b\u0e15\u0e38", None))
        self.label_30.setText(QCoreApplication.translate("PM", u"Master Good  \u0e15\u0e49\u0e2d\u0e07 Pass ", None))
        self.label_34.setText(QCoreApplication.translate("PM", u"-\u0e2d\u0e49\u0e32\u0e07\u0e2d\u0e34\u0e07\u0e40\u0e2d\u0e01\u0e2a\u0e32\u0e23 FIXTURE SPECIFICATION  (Master check item) ", None))
        self.label_35.setText(QCoreApplication.translate("PM", u"QF-P1-PRE-2069", None))
        self.comboBox_9.setItemText(0, "")
        self.comboBox_9.setItemText(1, QCoreApplication.translate("PM", u"Pass", None))
        self.comboBox_9.setItemText(2, QCoreApplication.translate("PM", u"Not pass", None))
        self.comboBox_9.setItemText(3, QCoreApplication.translate("PM", u"Not check", None))

        self.lineEdit_12.setPlaceholderText(QCoreApplication.translate("PM", u"\u0e2b\u0e21\u0e32\u0e22\u0e40\u0e2b\u0e15\u0e38", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("PM", u"6.Check Master", None))
        self.label_14.setText(QCoreApplication.translate("PM", u"SMT", None))
        self.label_9.setText(QCoreApplication.translate("PM", u"Check by Fixture room:", None))
        self.label_10.setText(QCoreApplication.translate("PM", u"Date:", None))
        self.label_7.setText(QCoreApplication.translate("PM", u"Approve by production (Leader up):", None))
        self.label_8.setText(QCoreApplication.translate("PM", u"Date:", None))
        self.save.setText(QCoreApplication.translate("PM", u"PM RECORD", None))
        self.label_11.setText(QCoreApplication.translate("PM", u"Ref : QAI-P1-PRE-060-0031", None))
        self.label_12.setText(QCoreApplication.translate("PM", u"QF-P1-PRE-2023 Rev.5", None))
    # retranslateUi


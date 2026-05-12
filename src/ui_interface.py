# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_interface.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLayout, QMainWindow,
    QProgressBar, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomQStackedWidget import QCustomQStackedWidget
from Custom_Widgets.QCustomSlideMenu import QCustomSlideMenu
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1067, 656)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1067, 656))
        font = QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        MainWindow.setLayoutDirection(Qt.LeftToRight)
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.centralwidget.setMinimumSize(QSize(0, 0))
        self.centralwidget.setStyleSheet(u"")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.leftMenu = QCustomSlideMenu(self.centralwidget)
        self.leftMenu.setObjectName(u"leftMenu")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.leftMenu.sizePolicy().hasHeightForWidth())
        self.leftMenu.setSizePolicy(sizePolicy2)
        self.leftMenu.setMinimumSize(QSize(0, 0))
        self.leftMenu.setMaximumSize(QSize(140, 16777214))
        self.verticalLayout = QVBoxLayout(self.leftMenu)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.leftSubMenuTop = QWidget(self.leftMenu)
        self.leftSubMenuTop.setObjectName(u"leftSubMenuTop")
        self.leftSubMenuTop.setMinimumSize(QSize(40, 42))
        self.verticalLayout_2 = QVBoxLayout(self.leftSubMenuTop)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 0, 5)
        self.menuBtn = QPushButton(self.leftSubMenuTop)
        self.menuBtn.setObjectName(u"menuBtn")
        icon = QIcon()
        icon.addFile(u":/feather/icons/feather/menu.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menuBtn.setIcon(icon)

        self.verticalLayout_2.addWidget(self.menuBtn, 0, Qt.AlignLeft|Qt.AlignTop)


        self.verticalLayout.addWidget(self.leftSubMenuTop)

        self.leftSubMenuCenter = QWidget(self.leftMenu)
        self.leftSubMenuCenter.setObjectName(u"leftSubMenuCenter")
        self.leftSubMenuCenter.setMinimumSize(QSize(150, 138))
        self.verticalLayout_3 = QVBoxLayout(self.leftSubMenuCenter)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 5, 0, 5)
        self.dashboardBtn = QPushButton(self.leftSubMenuCenter)
        self.dashboardBtn.setObjectName(u"dashboardBtn")
        icon1 = QIcon()
        icon1.addFile(u":/feather/icons/feather/pie-chart.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.dashboardBtn.setIcon(icon1)

        self.verticalLayout_3.addWidget(self.dashboardBtn)

        self.dataBtn = QPushButton(self.leftSubMenuCenter)
        self.dataBtn.setObjectName(u"dataBtn")
        icon2 = QIcon()
        icon2.addFile(u":/feather/icons/feather/database.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.dataBtn.setIcon(icon2)

        self.verticalLayout_3.addWidget(self.dataBtn)

        self.operatorBtn = QPushButton(self.leftSubMenuCenter)
        self.operatorBtn.setObjectName(u"operatorBtn")
        icon3 = QIcon()
        icon3.addFile(u":/feather/icons/feather/user.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.operatorBtn.setIcon(icon3)

        self.verticalLayout_3.addWidget(self.operatorBtn)

        self.moreBtn = QPushButton(self.leftSubMenuCenter)
        self.moreBtn.setObjectName(u"moreBtn")
        icon4 = QIcon()
        icon4.addFile(u":/feather/icons/feather/more-horizontal.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.moreBtn.setIcon(icon4)

        self.verticalLayout_3.addWidget(self.moreBtn)


        self.verticalLayout.addWidget(self.leftSubMenuCenter)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.leftSubMenuBottom = QWidget(self.leftMenu)
        self.leftSubMenuBottom.setObjectName(u"leftSubMenuBottom")
        self.leftSubMenuBottom.setMinimumSize(QSize(150, 108))
        self.verticalLayout_4 = QVBoxLayout(self.leftSubMenuBottom)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.repairBtn = QPushButton(self.leftSubMenuBottom)
        self.repairBtn.setObjectName(u"repairBtn")
        icon5 = QIcon()
        icon5.addFile(u":/feather/icons/feather/tool.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.repairBtn.setIcon(icon5)

        self.verticalLayout_4.addWidget(self.repairBtn)

        self.informationBtn = QPushButton(self.leftSubMenuBottom)
        self.informationBtn.setObjectName(u"informationBtn")
        icon6 = QIcon()
        icon6.addFile(u":/feather/icons/feather/alert-circle.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.informationBtn.setIcon(icon6)

        self.verticalLayout_4.addWidget(self.informationBtn)

        self.settingsBtn = QPushButton(self.leftSubMenuBottom)
        self.settingsBtn.setObjectName(u"settingsBtn")
        icon7 = QIcon()
        icon7.addFile(u":/feather/icons/feather/settings.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.settingsBtn.setIcon(icon7)

        self.verticalLayout_4.addWidget(self.settingsBtn)


        self.verticalLayout.addWidget(self.leftSubMenuBottom)


        self.horizontalLayout.addWidget(self.leftMenu)

        self.centerMenu = QCustomSlideMenu(self.centralwidget)
        self.centerMenu.setObjectName(u"centerMenu")
        sizePolicy2.setHeightForWidth(self.centerMenu.sizePolicy().hasHeightForWidth())
        self.centerMenu.setSizePolicy(sizePolicy2)
        self.centerMenu.setMinimumSize(QSize(0, 0))
        self.centerMenu.setMaximumSize(QSize(200, 16777215))
        self.verticalLayout_5 = QVBoxLayout(self.centerMenu)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(6, 6, 6, 6)
        self.centerMenPages = QWidget(self.centerMenu)
        self.centerMenPages.setObjectName(u"centerMenPages")
        self.horizontalLayout_2 = QHBoxLayout(self.centerMenPages)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.center = QLabel(self.centerMenPages)
        self.center.setObjectName(u"center")

        self.horizontalLayout_2.addWidget(self.center)

        self.closeCenterMenuBtn = QPushButton(self.centerMenPages)
        self.closeCenterMenuBtn.setObjectName(u"closeCenterMenuBtn")
        icon8 = QIcon()
        icon8.addFile(u":/feather/icons/feather/x-circle.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.closeCenterMenuBtn.setIcon(icon8)

        self.horizontalLayout_2.addWidget(self.closeCenterMenuBtn, 0, Qt.AlignRight)


        self.verticalLayout_5.addWidget(self.centerMenPages, 0, Qt.AlignTop)

        self.stackedWidget = QCustomQStackedWidget(self.centerMenu)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy2.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy2)
        self.settingsPage = QWidget()
        self.settingsPage.setObjectName(u"settingsPage")
        self.verticalLayout_7 = QVBoxLayout(self.settingsPage)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_2)

        self.settings = QWidget(self.settingsPage)
        self.settings.setObjectName(u"settings")
        self.verticalLayout_6 = QVBoxLayout(self.settings)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_2 = QLabel(self.settings)
        self.label_2.setObjectName(u"label_2")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_6.addWidget(self.label_2)

        self.frame = QFrame(self.settings)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)

        self.horizontalLayout_3.addWidget(self.label_3, 0, Qt.AlignLeft)

        self.themeList = QComboBox(self.frame)
        self.themeList.setObjectName(u"themeList")
        sizePolicy.setHeightForWidth(self.themeList.sizePolicy().hasHeightForWidth())
        self.themeList.setSizePolicy(sizePolicy)
        self.themeList.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_3.addWidget(self.themeList)


        self.verticalLayout_6.addWidget(self.frame)


        self.verticalLayout_7.addWidget(self.settings, 0, Qt.AlignVCenter)

        self.commu = QWidget(self.settingsPage)
        self.commu.setObjectName(u"commu")
        self.verticalLayout_20 = QVBoxLayout(self.commu)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.communication = QPushButton(self.commu)
        self.communication.setObjectName(u"communication")
        self.communication.setFont(font1)

        self.verticalLayout_20.addWidget(self.communication)


        self.verticalLayout_7.addWidget(self.commu)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_3)

        self.stackedWidget.addWidget(self.settingsPage)
        self.information = QWidget()
        self.information.setObjectName(u"information")
        self.verticalLayout_8 = QVBoxLayout(self.information)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_4 = QLabel(self.information)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.label_4, 0, Qt.AlignVCenter)

        self.stackedWidget.addWidget(self.information)
        self.Repair = QWidget()
        self.Repair.setObjectName(u"Repair")
        self.verticalLayout_9 = QVBoxLayout(self.Repair)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label_5 = QLabel(self.Repair)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignCenter)

        self.verticalLayout_9.addWidget(self.label_5, 0, Qt.AlignVCenter)

        self.stackedWidget.addWidget(self.Repair)

        self.verticalLayout_5.addWidget(self.stackedWidget)


        self.horizontalLayout.addWidget(self.centerMenu)

        self.mainBody = QWidget(self.centralwidget)
        self.mainBody.setObjectName(u"mainBody")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.mainBody.sizePolicy().hasHeightForWidth())
        self.mainBody.setSizePolicy(sizePolicy3)
        self.mainBody.setMinimumSize(QSize(0, 0))
        self.verticalLayout_10 = QVBoxLayout(self.mainBody)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(5, 0, 0, 0)
        self.header = QWidget(self.mainBody)
        self.header.setObjectName(u"header")
        self.header.setMinimumSize(QSize(0, 0))
        self.horizontalLayout_7 = QHBoxLayout(self.header)
        self.horizontalLayout_7.setSpacing(5)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(5, 0, 0, 0)
        self.titleTxt = QLabel(self.header)
        self.titleTxt.setObjectName(u"titleTxt")
        self.titleTxt.setMaximumSize(QSize(230, 16777215))
        font2 = QFont()
        font2.setPointSize(13)
        font2.setBold(True)
        self.titleTxt.setFont(font2)

        self.horizontalLayout_7.addWidget(self.titleTxt, 0, Qt.AlignLeft)

        self.window = QFrame(self.header)
        self.window.setObjectName(u"window")
        self.window.setMaximumSize(QSize(150, 16777215))
        self.window.setFrameShape(QFrame.StyledPanel)
        self.window.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.window)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 2, 2, 0)
        self.minimizeBtn = QPushButton(self.window)
        self.minimizeBtn.setObjectName(u"minimizeBtn")
        icon9 = QIcon()
        icon9.addFile(u":/feather/icons/feather/minus.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.minimizeBtn.setIcon(icon9)

        self.horizontalLayout_8.addWidget(self.minimizeBtn)

        self.restoreBtn = QPushButton(self.window)
        self.restoreBtn.setObjectName(u"restoreBtn")
        self.restoreBtn.setMaximumSize(QSize(16777215, 16777215))
        icon10 = QIcon()
        icon10.addFile(u":/feather/icons/feather/square.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.restoreBtn.setIcon(icon10)

        self.horizontalLayout_8.addWidget(self.restoreBtn)

        self.closeBtn = QPushButton(self.window)
        self.closeBtn.setObjectName(u"closeBtn")
        icon11 = QIcon()
        icon11.addFile(u":/feather/icons/feather/window_close.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.closeBtn.setIcon(icon11)

        self.horizontalLayout_8.addWidget(self.closeBtn)


        self.horizontalLayout_7.addWidget(self.window, 0, Qt.AlignRight|Qt.AlignTop)


        self.verticalLayout_10.addWidget(self.header)

        self.mainCenter = QWidget(self.mainBody)
        self.mainCenter.setObjectName(u"mainCenter")
        sizePolicy1.setHeightForWidth(self.mainCenter.sizePolicy().hasHeightForWidth())
        self.mainCenter.setSizePolicy(sizePolicy1)
        self.horizontalLayout_9 = QHBoxLayout(self.mainCenter)
        self.horizontalLayout_9.setSpacing(2)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(2, 2, 2, 2)
        self.widget = QWidget(self.mainCenter)
        self.widget.setObjectName(u"widget")
        sizePolicy1.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy1)
        self.verticalLayout_11 = QVBoxLayout(self.widget)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.mainPages = QCustomQStackedWidget(self.widget)
        self.mainPages.setObjectName(u"mainPages")
        self.dashboardPage = QWidget()
        self.dashboardPage.setObjectName(u"dashboardPage")
        self.verticalLayout_12 = QVBoxLayout(self.dashboardPage)
        self.verticalLayout_12.setSpacing(5)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.widget_3 = QWidget(self.dashboardPage)
        self.widget_3.setObjectName(u"widget_3")
        self.gridLayout = QGridLayout(self.widget_3)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_5 = QWidget(self.widget_3)
        self.widget_5.setObjectName(u"widget_5")
        sizePolicy2.setHeightForWidth(self.widget_5.sizePolicy().hasHeightForWidth())
        self.widget_5.setSizePolicy(sizePolicy2)
        self.widget_5.setMinimumSize(QSize(0, 281))
        self.widget_5.setMaximumSize(QSize(16777215, 16777215))
        font3 = QFont()
        font3.setPointSize(8)
        self.widget_5.setFont(font3)
        self.widget_5.setLayoutDirection(Qt.LeftToRight)
        self.widget_5.setStyleSheet(u"\n"
"border-radius: 10px;")
        self.gridLayout_3 = QGridLayout(self.widget_5)
        self.gridLayout_3.setSpacing(3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(3, 3, 3, 3)
        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setSpacing(0)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.frame_6 = QFrame(self.widget_5)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(0, 0))
        self.frame_6.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.gridLayout_13 = QGridLayout(self.frame_6)
        self.gridLayout_13.setSpacing(0)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(0, 0, 0, 0)
        self.label_12 = QLabel(self.frame_6)
        self.label_12.setObjectName(u"label_12")
        sizePolicy2.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy2)
        self.label_12.setMinimumSize(QSize(116, 16))
        self.label_12.setFont(font1)
        self.label_12.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.label_12.setScaledContents(False)
        self.label_12.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_12, 0, 0, 1, 1)

        self.operator_name = QLabel(self.frame_6)
        self.operator_name.setObjectName(u"operator_name")
        sizePolicy2.setHeightForWidth(self.operator_name.sizePolicy().hasHeightForWidth())
        self.operator_name.setSizePolicy(sizePolicy2)
        self.operator_name.setMinimumSize(QSize(0, 0))
        self.operator_name.setFont(font1)
        self.operator_name.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.gridLayout_13.addWidget(self.operator_name, 1, 0, 1, 1)


        self.gridLayout_9.addWidget(self.frame_6, 0, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_9, 1, 4, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_5 = QFrame(self.widget_5)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 0))
        self.frame_5.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_5)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setHorizontalSpacing(0)
        self.gridLayout_14.setContentsMargins(0, 0, 0, 0)
        self.label_9 = QLabel(self.frame_5)
        self.label_9.setObjectName(u"label_9")
        sizePolicy2.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy2)
        self.label_9.setMinimumSize(QSize(0, 0))
        self.label_9.setFont(font1)
        self.label_9.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.label_9.setScaledContents(False)
        self.label_9.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_9, 0, 0, 1, 1)

        self.tooling_code = QLabel(self.frame_5)
        self.tooling_code.setObjectName(u"tooling_code")
        sizePolicy2.setHeightForWidth(self.tooling_code.sizePolicy().hasHeightForWidth())
        self.tooling_code.setSizePolicy(sizePolicy2)
        self.tooling_code.setMinimumSize(QSize(0, 0))
        self.tooling_code.setFont(font1)
        self.tooling_code.setAutoFillBackground(False)
        self.tooling_code.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.tooling_code.setScaledContents(False)

        self.gridLayout_14.addWidget(self.tooling_code, 1, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_5, 0, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_2, 1, 3, 1, 1)

        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.widget_5)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 0))
        self.frame_3.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_3)
        self.gridLayout_11.setSpacing(0)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame_3)
        self.label.setObjectName(u"label")
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)
        self.label.setMinimumSize(QSize(0, 0))
        self.label.setFont(font1)
        self.label.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.label.setFrameShape(QFrame.NoFrame)
        self.label.setFrameShadow(QFrame.Plain)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setScaledContents(False)
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_11.addWidget(self.label, 0, 0, 1, 1)

        self.product_name = QLabel(self.frame_3)
        self.product_name.setObjectName(u"product_name")
        sizePolicy2.setHeightForWidth(self.product_name.sizePolicy().hasHeightForWidth())
        self.product_name.setSizePolicy(sizePolicy2)
        self.product_name.setMinimumSize(QSize(0, 0))
        self.product_name.setFont(font1)
        self.product_name.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.product_name.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_11.addWidget(self.product_name, 1, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_3, 1, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_6, 0, 3, 1, 1)

        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.widget_5)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 0))
        self.frame_4.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_4)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setHorizontalSpacing(0)
        self.gridLayout_12.setVerticalSpacing(2)
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.label_10 = QLabel(self.frame_4)
        self.label_10.setObjectName(u"label_10")
        sizePolicy2.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy2)
        self.label_10.setMinimumSize(QSize(0, 0))
        self.label_10.setFont(font1)
        self.label_10.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.label_10.setScaledContents(False)
        self.label_10.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_12.addWidget(self.label_10, 0, 0, 1, 1)

        self.lot_number = QLabel(self.frame_4)
        self.lot_number.setObjectName(u"lot_number")
        sizePolicy2.setHeightForWidth(self.lot_number.sizePolicy().hasHeightForWidth())
        self.lot_number.setSizePolicy(sizePolicy2)
        self.lot_number.setMinimumSize(QSize(0, 0))
        self.lot_number.setFont(font1)
        self.lot_number.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.gridLayout_12.addWidget(self.lot_number, 1, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame_4, 0, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_7, 0, 4, 1, 1)

        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setSpacing(0)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.frame_7 = QFrame(self.widget_5)
        self.frame_7.setObjectName(u"frame_7")
        sizePolicy2.setHeightForWidth(self.frame_7.sizePolicy().hasHeightForWidth())
        self.frame_7.setSizePolicy(sizePolicy2)
        self.frame_7.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.verticalLayout_17 = QVBoxLayout(self.frame_7)
        self.verticalLayout_17.setSpacing(4)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(5, 5, 5, 3)
        self.widget_2 = QWidget(self.frame_7)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_11 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 3)
        self.label_11 = QLabel(self.widget_2)
        self.label_11.setObjectName(u"label_11")
        sizePolicy1.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy1)
        self.label_11.setMaximumSize(QSize(16777215, 16777215))
        self.label_11.setFont(font1)
        self.label_11.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.label_11.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_11.addWidget(self.label_11, 0, Qt.AlignLeft)

        self.shot_cnt = QLabel(self.widget_2)
        self.shot_cnt.setObjectName(u"shot_cnt")
        sizePolicy2.setHeightForWidth(self.shot_cnt.sizePolicy().hasHeightForWidth())
        self.shot_cnt.setSizePolicy(sizePolicy2)
        self.shot_cnt.setFont(font1)
        self.shot_cnt.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_11.addWidget(self.shot_cnt)

        self.pushButton_2 = QPushButton(self.widget_2)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy2.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy2)
        self.pushButton_2.setMinimumSize(QSize(101, 35))
        self.pushButton_2.setMaximumSize(QSize(170, 16777215))
        self.pushButton_2.setFont(font1)
        self.pushButton_2.setStyleSheet(u"background-color: rgb(240, 240, 240);\n"
"color: rgb(0, 0, 0);")
        icon12 = QIcon()
        icon12.addFile(u":/feather/icons/feather/refresh-ccw.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_2.setIcon(icon12)

        self.horizontalLayout_11.addWidget(self.pushButton_2)


        self.verticalLayout_17.addWidget(self.widget_2)

        self.widget_4 = QWidget(self.frame_7)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_10 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.finish_lot = QPushButton(self.widget_4)
        self.finish_lot.setObjectName(u"finish_lot")
        sizePolicy2.setHeightForWidth(self.finish_lot.sizePolicy().hasHeightForWidth())
        self.finish_lot.setSizePolicy(sizePolicy2)
        font4 = QFont()
        font4.setPointSize(12)
        font4.setBold(True)
        self.finish_lot.setFont(font4)
        self.finish_lot.setStyleSheet(u"background-color: rgb(0, 167, 93);")
        icon13 = QIcon()
        icon13.addFile(u":/feather/icons/feather/save.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.finish_lot.setIcon(icon13)
        self.finish_lot.setIconSize(QSize(24, 24))

        self.horizontalLayout_10.addWidget(self.finish_lot)


        self.verticalLayout_17.addWidget(self.widget_4)


        self.gridLayout_10.addWidget(self.frame_7, 0, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_10, 2, 3, 1, 2)

        self.widget_9 = QWidget(self.widget_5)
        self.widget_9.setObjectName(u"widget_9")
        sizePolicy2.setHeightForWidth(self.widget_9.sizePolicy().hasHeightForWidth())
        self.widget_9.setSizePolicy(sizePolicy2)
        self.widget_9.setStyleSheet(u"background-color: rgb(255, 106, 0);")
        self.verticalLayout_22 = QVBoxLayout(self.widget_9)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.label_sheet_per_ht = QLabel(self.widget_9)
        self.label_sheet_per_ht.setObjectName(u"label_sheet_per_ht")
        self.label_sheet_per_ht.setFont(font1)
        self.label_sheet_per_ht.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.verticalLayout_22.addWidget(self.label_sheet_per_ht, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.sheet_per_ht = QLabel(self.widget_9)
        self.sheet_per_ht.setObjectName(u"sheet_per_ht")
        self.sheet_per_ht.setFont(font1)

        self.verticalLayout_22.addWidget(self.sheet_per_ht)


        self.gridLayout_3.addWidget(self.widget_9, 0, 0, 1, 1)

        self.widget_10 = QWidget(self.widget_5)
        self.widget_10.setObjectName(u"widget_10")
        sizePolicy2.setHeightForWidth(self.widget_10.sizePolicy().hasHeightForWidth())
        self.widget_10.setSizePolicy(sizePolicy2)
        self.widget_10.setStyleSheet(u"background-color: rgb(93, 139, 255);")
        self.verticalLayout_23 = QVBoxLayout(self.widget_10)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.label_pcs_per_hr = QLabel(self.widget_10)
        self.label_pcs_per_hr.setObjectName(u"label_pcs_per_hr")
        self.label_pcs_per_hr.setFont(font1)
        self.label_pcs_per_hr.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.verticalLayout_23.addWidget(self.label_pcs_per_hr, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.pcs_per_hr = QLabel(self.widget_10)
        self.pcs_per_hr.setObjectName(u"pcs_per_hr")
        self.pcs_per_hr.setFont(font1)

        self.verticalLayout_23.addWidget(self.pcs_per_hr)


        self.gridLayout_3.addWidget(self.widget_10, 1, 0, 1, 1)

        self.widget_11 = QWidget(self.widget_5)
        self.widget_11.setObjectName(u"widget_11")
        sizePolicy2.setHeightForWidth(self.widget_11.sizePolicy().hasHeightForWidth())
        self.widget_11.setSizePolicy(sizePolicy2)
        self.widget_11.setStyleSheet(u"background-color: rgb(175, 200, 255);")
        self.verticalLayout_24 = QVBoxLayout(self.widget_11)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.shot_per_hr_2 = QLabel(self.widget_11)
        self.shot_per_hr_2.setObjectName(u"shot_per_hr_2")
        self.shot_per_hr_2.setFont(font1)
        self.shot_per_hr_2.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.verticalLayout_24.addWidget(self.shot_per_hr_2, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.shot_per_hr = QLabel(self.widget_11)
        self.shot_per_hr.setObjectName(u"shot_per_hr")
        self.shot_per_hr.setFont(font1)

        self.verticalLayout_24.addWidget(self.shot_per_hr)


        self.gridLayout_3.addWidget(self.widget_11, 2, 0, 1, 1)


        self.gridLayout.addWidget(self.widget_5, 2, 2, 1, 1)

        self.widget_7 = QWidget(self.widget_3)
        self.widget_7.setObjectName(u"widget_7")
        sizePolicy2.setHeightForWidth(self.widget_7.sizePolicy().hasHeightForWidth())
        self.widget_7.setSizePolicy(sizePolicy2)
        self.widget_7.setMinimumSize(QSize(265, 280))
        self.horizontalLayout_12 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_12.setSpacing(3)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(3, 3, 3, 3)
        self.scrollAreaWidgetContents = QWidget(self.widget_7)
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        sizePolicy1.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy1)
        self.scrollAreaWidgetContents.setMinimumSize(QSize(149, 274))
        self.scrollAreaWidgetContents.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius: 10px;")
        self.verticalLayout_16 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_16.setSpacing(3)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(3, 3, 3, 3)

        self.horizontalLayout_12.addWidget(self.scrollAreaWidgetContents)

        self.heat_map = QWidget(self.widget_7)
        self.heat_map.setObjectName(u"heat_map")
        sizePolicy1.setHeightForWidth(self.heat_map.sizePolicy().hasHeightForWidth())
        self.heat_map.setSizePolicy(sizePolicy1)
        self.heat_map.setMinimumSize(QSize(149, 274))
        self.heat_map.setLayoutDirection(Qt.RightToLeft)
        self.heat_map.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius: 10px;")
        self.verticalLayout_18 = QVBoxLayout(self.heat_map)
        self.verticalLayout_18.setSpacing(3)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(3, 3, 3, 3)

        self.horizontalLayout_12.addWidget(self.heat_map)


        self.gridLayout.addWidget(self.widget_7, 3, 1, 1, 1)

        self.widget_8 = QWidget(self.widget_3)
        self.widget_8.setObjectName(u"widget_8")
        sizePolicy2.setHeightForWidth(self.widget_8.sizePolicy().hasHeightForWidth())
        self.widget_8.setSizePolicy(sizePolicy2)
        self.widget_8.setMinimumSize(QSize(0, 281))
        self.gridLayout_5 = QGridLayout(self.widget_8)
        self.gridLayout_5.setSpacing(3)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(3, 3, 3, 3)
        self.widget_chart_area = QWidget(self.widget_8)
        self.widget_chart_area.setObjectName(u"widget_chart_area")
        sizePolicy1.setHeightForWidth(self.widget_chart_area.sizePolicy().hasHeightForWidth())
        self.widget_chart_area.setSizePolicy(sizePolicy1)
        self.widget_chart_area.setMinimumSize(QSize(259, 275))
        self.widget_chart_area.setMaximumSize(QSize(16777215, 16777215))
        self.widget_chart_area.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius: 10px;")
        self.verticalLayout_21 = QVBoxLayout(self.widget_chart_area)
        self.verticalLayout_21.setSpacing(3)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.verticalLayout_21.setContentsMargins(3, 3, 3, 3)

        self.gridLayout_5.addWidget(self.widget_chart_area, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.widget_8, 2, 1, 1, 1)

        self.widget_6 = QWidget(self.widget_3)
        self.widget_6.setObjectName(u"widget_6")
        sizePolicy2.setHeightForWidth(self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy2)
        self.widget_6.setMinimumSize(QSize(343, 280))
        self.widget_6.setMaximumSize(QSize(16777215, 16777215))
        self.widget_6.setStyleSheet(u"")
        self.gridLayout_4 = QGridLayout(self.widget_6)
        self.gridLayout_4.setSpacing(3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(3, 3, 3, 3)
        self.scrollArea = QScrollArea(self.widget_6)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy3.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy3)
        self.scrollArea.setMinimumSize(QSize(0, 0))
        self.scrollArea.setLayoutDirection(Qt.LeftToRight)
        self.scrollArea.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius: 10px;\n"
"color: rgb(0, 0, 0);")
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 385, 274))
        sizePolicy2.setHeightForWidth(self.scrollAreaWidgetContents_2.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_2.setSizePolicy(sizePolicy2)
        self.scrollAreaWidgetContents_2.setStyleSheet(u"border-radius: 10px;")
        self.verticalLayout_19 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_19.setSpacing(3)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.verticalLayout_19.setContentsMargins(3, 3, 3, 3)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.gridLayout_4.addWidget(self.scrollArea, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.widget_6, 3, 2, 1, 1)


        self.verticalLayout_12.addWidget(self.widget_3)

        self.mainPages.addWidget(self.dashboardPage)
        self.operator_2 = QWidget()
        self.operator_2.setObjectName(u"operator_2")
        self.verticalLayout_14 = QVBoxLayout(self.operator_2)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.textoperatorPage = QLabel(self.operator_2)
        self.textoperatorPage.setObjectName(u"textoperatorPage")
        self.textoperatorPage.setAlignment(Qt.AlignCenter)

        self.verticalLayout_14.addWidget(self.textoperatorPage)

        self.mainPages.addWidget(self.operator_2)
        self.morePage = QWidget()
        self.morePage.setObjectName(u"morePage")
        self.verticalLayout_15 = QVBoxLayout(self.morePage)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.textmore = QLabel(self.morePage)
        self.textmore.setObjectName(u"textmore")
        self.textmore.setAlignment(Qt.AlignCenter)

        self.verticalLayout_15.addWidget(self.textmore)

        self.mainPages.addWidget(self.morePage)
        self.dataPage = QWidget()
        self.dataPage.setObjectName(u"dataPage")
        self.verticalLayout_13 = QVBoxLayout(self.dataPage)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.textdata = QLabel(self.dataPage)
        self.textdata.setObjectName(u"textdata")
        self.textdata.setAlignment(Qt.AlignCenter)

        self.verticalLayout_13.addWidget(self.textdata)

        self.mainPages.addWidget(self.dataPage)

        self.verticalLayout_11.addWidget(self.mainPages)


        self.horizontalLayout_9.addWidget(self.widget)


        self.verticalLayout_10.addWidget(self.mainCenter)

        self.footer = QWidget(self.mainBody)
        self.footer.setObjectName(u"footer")
        self.footer.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_4 = QHBoxLayout(self.footer)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(20, 0, 0, 5)
        self.label_6 = QLabel(self.footer)
        self.label_6.setObjectName(u"label_6")
        font5 = QFont()
        font5.setFamilies([u"Segoe UI"])
        font5.setPointSize(10)
        font5.setBold(False)
        font5.setItalic(False)
        font5.setUnderline(False)
        font5.setStrikeOut(False)
        self.label_6.setFont(font5)

        self.horizontalLayout_4.addWidget(self.label_6, 0, Qt.AlignLeft|Qt.AlignBottom)

        self.frame_2 = QFrame(self.footer)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_5.setSpacing(5)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(5, 5, 5, 5)
        self.theme = QLabel(self.frame_2)
        self.theme.setObjectName(u"theme")

        self.horizontalLayout_5.addWidget(self.theme)

        self.activityProgress = QProgressBar(self.frame_2)
        self.activityProgress.setObjectName(u"activityProgress")
        self.activityProgress.setMinimumSize(QSize(0, 0))
        self.activityProgress.setMaximumSize(QSize(16777215, 10))
        font6 = QFont()
        font6.setPointSize(20)
        self.activityProgress.setFont(font6)
        self.activityProgress.setMaximum(100)
        self.activityProgress.setValue(24)
        self.activityProgress.setTextVisible(False)

        self.horizontalLayout_5.addWidget(self.activityProgress)


        self.horizontalLayout_4.addWidget(self.frame_2, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.sizeGrip = QFrame(self.footer)
        self.sizeGrip.setObjectName(u"sizeGrip")
        self.sizeGrip.setMinimumSize(QSize(15, 15))
        self.sizeGrip.setMaximumSize(QSize(15, 15))
        self.sizeGrip.setFrameShape(QFrame.NoFrame)
        self.sizeGrip.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_4.addWidget(self.sizeGrip, 0, Qt.AlignBottom)


        self.verticalLayout_10.addWidget(self.footer)


        self.horizontalLayout.addWidget(self.mainBody)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)
        self.mainPages.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(tooltip)
        self.menuBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Slide menu", None))
#endif // QT_CONFIG(tooltip)
        self.menuBtn.setText("")
#if QT_CONFIG(tooltip)
        self.dashboardBtn.setToolTip(QCoreApplication.translate("MainWindow", u"View Dashboard", None))
#endif // QT_CONFIG(tooltip)
        self.dashboardBtn.setText(QCoreApplication.translate("MainWindow", u"  Dashboard", None))
#if QT_CONFIG(tooltip)
        self.dataBtn.setToolTip(QCoreApplication.translate("MainWindow", u"View Data", None))
#endif // QT_CONFIG(tooltip)
        self.dataBtn.setText(QCoreApplication.translate("MainWindow", u"  Data Analysis", None))
#if QT_CONFIG(tooltip)
        self.operatorBtn.setToolTip(QCoreApplication.translate("MainWindow", u"View profile", None))
#endif // QT_CONFIG(tooltip)
        self.operatorBtn.setText(QCoreApplication.translate("MainWindow", u"  Operator", None))
#if QT_CONFIG(tooltip)
        self.moreBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Other", None))
#endif // QT_CONFIG(tooltip)
        self.moreBtn.setText("")
#if QT_CONFIG(tooltip)
        self.repairBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Manual repair", None))
#endif // QT_CONFIG(tooltip)
        self.repairBtn.setText(QCoreApplication.translate("MainWindow", u"  Repair", None))
#if QT_CONFIG(tooltip)
        self.informationBtn.setToolTip(QCoreApplication.translate("MainWindow", u"View Information", None))
#endif // QT_CONFIG(tooltip)
        self.informationBtn.setText(QCoreApplication.translate("MainWindow", u"  Information", None))
#if QT_CONFIG(tooltip)
        self.settingsBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Settings", None))
#endif // QT_CONFIG(tooltip)
        self.settingsBtn.setText(QCoreApplication.translate("MainWindow", u"  Settings", None))
        self.center.setText(QCoreApplication.translate("MainWindow", u"Center Menu", None))
#if QT_CONFIG(tooltip)
        self.closeCenterMenuBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close Menu", None))
#endif // QT_CONFIG(tooltip)
        self.closeCenterMenuBtn.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Theme Settings ", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Theme", None))
        self.communication.setText(QCoreApplication.translate("MainWindow", u"Configs Setting", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Information", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Pepair OST", None))
        self.titleTxt.setText(QCoreApplication.translate("MainWindow", u"SMART OST PROCESS", None))
#if QT_CONFIG(tooltip)
        self.minimizeBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Minimize window", None))
#endif // QT_CONFIG(tooltip)
        self.minimizeBtn.setText("")
#if QT_CONFIG(tooltip)
        self.restoreBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Restore window", None))
#endif // QT_CONFIG(tooltip)
        self.restoreBtn.setText("")
#if QT_CONFIG(tooltip)
        self.closeBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close window", None))
#endif // QT_CONFIG(tooltip)
        self.closeBtn.setText("")
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Operator Name", None))
        self.operator_name.setText("")
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Tooling Code", None))
        self.tooling_code.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Product Name", None))
        self.product_name.setText("")
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Lot Number", None))
        self.lot_number.setText("")
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"SHOT COUNT :", None))
        self.shot_cnt.setText("")
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"MANUAL PM", None))
        self.finish_lot.setText(QCoreApplication.translate("MainWindow", u"FINISH LOT", None))
        self.label_sheet_per_ht.setText(QCoreApplication.translate("MainWindow", u"Sheets/hr", None))
        self.sheet_per_ht.setText("")
        self.label_pcs_per_hr.setText(QCoreApplication.translate("MainWindow", u"PCS/hr", None))
        self.pcs_per_hr.setText("")
        self.shot_per_hr_2.setText(QCoreApplication.translate("MainWindow", u"Shots/hr", None))
        self.shot_per_hr.setText("")
        self.textoperatorPage.setText(QCoreApplication.translate("MainWindow", u"Profile", None))
        self.textmore.setText(QCoreApplication.translate("MainWindow", u"More...", None))
        self.textdata.setText(QCoreApplication.translate("MainWindow", u"Data analysis", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Developed by Fixture Room (FETL)", None))
        self.theme.setText(QCoreApplication.translate("MainWindow", u"Theme progress", None))
    # retranslateUi


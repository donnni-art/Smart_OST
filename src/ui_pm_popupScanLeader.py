# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_pm_popupScanLeader.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)
class Ui_Scanleader(object):
    def setupUi(self, Scanleader):
        if not Scanleader.objectName():
            Scanleader.setObjectName(u"Scanleader")
        Scanleader.resize(280, 364)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Scanleader.sizePolicy().hasHeightForWidth())
        Scanleader.setSizePolicy(sizePolicy)
        Scanleader.setMinimumSize(QSize(280, 364))
        Scanleader.setMaximumSize(QSize(280, 364))
        self.verticalLayout_3 = QVBoxLayout(Scanleader)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.widget_6 = QWidget(Scanleader)
        self.widget_6.setObjectName(u"widget_6")
        self.verticalLayout = QVBoxLayout(self.widget_6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.widget_6)
        self.widget.setObjectName(u"widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy1)
        self.widget.setMinimumSize(QSize(0, 0))
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.icon = QLabel(self.widget)
        self.icon.setObjectName(u"icon")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.icon.sizePolicy().hasHeightForWidth())
        self.icon.setSizePolicy(sizePolicy2)
        self.icon.setMinimumSize(QSize(80, 80))
        self.icon.setMaximumSize(QSize(80, 80))
        self.icon.setPixmap(QPixmap(u":/feather/icons/feather/user-check.png"))
        self.icon.setScaledContents(True)

        self.verticalLayout_2.addWidget(self.icon, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.verticalSpacer = QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.labelname = QLabel(self.widget)
        self.labelname.setObjectName(u"labelname")
        sizePolicy2.setHeightForWidth(self.labelname.sizePolicy().hasHeightForWidth())
        self.labelname.setSizePolicy(sizePolicy2)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.labelname.setFont(font)

        self.verticalLayout_2.addWidget(self.labelname, 0, Qt.AlignHCenter)

        self.verticalSpacer_2 = QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.widget_4 = QWidget(self.widget)
        self.widget_4.setObjectName(u"widget_4")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy3)
        self.horizontalLayout_2 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.lineEdit = QLineEdit(self.widget_4)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMinimumSize(QSize(200, 30))
        self.lineEdit.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.Refresh_scanleader = QPushButton(self.widget_4)
        self.Refresh_scanleader.setObjectName(u"Refresh_scanleader")
        self.Refresh_scanleader.setEnabled(True)
        sizePolicy.setHeightForWidth(self.Refresh_scanleader.sizePolicy().hasHeightForWidth())
        self.Refresh_scanleader.setSizePolicy(sizePolicy)
        self.Refresh_scanleader.setMinimumSize(QSize(37, 30))
        self.Refresh_scanleader.setMaximumSize(QSize(37, 30))
        self.Refresh_scanleader.setSizeIncrement(QSize(18, 20))
        self.Refresh_scanleader.setStyleSheet(u"border-radius: 10px;\n"
"background-color: rgb(85, 170, 255);\n"
"border: 1px solid black;")
        icon1 = QIcon()
        icon1.addFile(u":/feather/icons/feather/refresh-ccw.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.Refresh_scanleader.setIcon(icon1)
        self.Refresh_scanleader.setIconSize(QSize(16, 16))

        self.horizontalLayout_2.addWidget(self.Refresh_scanleader)


        self.verticalLayout_2.addWidget(self.widget_4)


        self.verticalLayout.addWidget(self.widget)

        self.widget_2 = QWidget(self.widget_6)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy3.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy3)
        self.horizontalLayout_3 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.label_name = QLabel(self.widget_2)
        self.label_name.setObjectName(u"label_name")
        sizePolicy2.setHeightForWidth(self.label_name.sizePolicy().hasHeightForWidth())
        self.label_name.setSizePolicy(sizePolicy2)
        font1 = QFont()
        font1.setBold(True)
        self.label_name.setFont(font1)

        self.horizontalLayout_3.addWidget(self.label_name)

        self.scan_leader = QLineEdit(self.widget_2)
        self.scan_leader.setObjectName(u"scan_leader")
        sizePolicy1.setHeightForWidth(self.scan_leader.sizePolicy().hasHeightForWidth())
        self.scan_leader.setSizePolicy(sizePolicy1)
        self.scan_leader.setMinimumSize(QSize(0, 30))
        self.scan_leader.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_3.addWidget(self.scan_leader)


        self.verticalLayout.addWidget(self.widget_2)

        self.widget_3 = QWidget(self.widget_6)
        self.widget_3.setObjectName(u"widget_3")
        sizePolicy3.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy3)
        self.horizontalLayout = QHBoxLayout(self.widget_3)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.label_Level = QLabel(self.widget_3)
        self.label_Level.setObjectName(u"label_Level")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_Level.sizePolicy().hasHeightForWidth())
        self.label_Level.setSizePolicy(sizePolicy4)
        font2 = QFont()
        font2.setPointSize(9)
        font2.setBold(True)
        self.label_Level.setFont(font2)

        self.horizontalLayout.addWidget(self.label_Level)

        self.comboBox = QComboBox(self.widget_3)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(100, 30))
        font3 = QFont()
        font3.setBold(False)
        font3.setKerning(True)
        self.comboBox.setFont(font3)
        self.comboBox.setLayoutDirection(Qt.LeftToRight)
        self.comboBox.setAutoFillBackground(False)
        self.comboBox.setStyleSheet(u"")
        self.comboBox.setEditable(False)
        self.comboBox.setInsertPolicy(QComboBox.InsertAtCurrent)

        self.horizontalLayout.addWidget(self.comboBox, 0, Qt.AlignVCenter)


        self.verticalLayout.addWidget(self.widget_3)

        self.widget_5 = QWidget(self.widget_6)
        self.widget_5.setObjectName(u"widget_5")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_4.setSpacing(5)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.confirmID = QPushButton(self.widget_5)
        self.confirmID.setObjectName(u"confirmID")
        sizePolicy.setHeightForWidth(self.confirmID.sizePolicy().hasHeightForWidth())
        self.confirmID.setSizePolicy(sizePolicy)
        self.confirmID.setMinimumSize(QSize(0, 30))
        self.confirmID.setMaximumSize(QSize(16777215, 31))
        self.confirmID.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/feather/icons/feather/check.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.confirmID.setIcon(icon2)

        self.horizontalLayout_4.addWidget(self.confirmID)

        self.pushButton_D = QPushButton(self.widget_5)
        self.pushButton_D.setObjectName(u"pushButton_D")
        self.pushButton_D.setMinimumSize(QSize(0, 30))
        icon3 = QIcon()
        icon3.addFile(u":/feather/icons/feather/x-circle.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_D.setIcon(icon3)

        self.horizontalLayout_4.addWidget(self.pushButton_D)


        self.verticalLayout.addWidget(self.widget_5)


        self.verticalLayout_3.addWidget(self.widget_6)


        self.retranslateUi(Scanleader)

        QMetaObject.connectSlotsByName(Scanleader)
    # setupUi

    def retranslateUi(self, Scanleader):
        Scanleader.setWindowTitle(QCoreApplication.translate("Scanleader", u"Dialog", None))
        self.icon.setText("")
        self.labelname.setText(QCoreApplication.translate("Scanleader", u"LOGIN LEADER", None))
        self.lineEdit.setText("")
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("Scanleader", u"Leader Scan ID", None))
        self.Refresh_scanleader.setText("")
        self.label_name.setText(QCoreApplication.translate("Scanleader", u"Name:", None))
        self.scan_leader.setInputMask("")
        self.scan_leader.setText("")
        self.scan_leader.setPlaceholderText(QCoreApplication.translate("Scanleader", u"Name and Surname", None))
        self.label_Level.setText(QCoreApplication.translate("Scanleader", u"Position Level: ", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Scanleader", u"Leader", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Scanleader", u"Supervisor", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Scanleader", u"Engineer", None))

        self.confirmID.setText(QCoreApplication.translate("Scanleader", u"Complete", None))
        self.pushButton_D.setText(QCoreApplication.translate("Scanleader", u"Close", None))
    # retranslateUi


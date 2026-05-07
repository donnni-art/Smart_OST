# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_pm_popupScanRepair.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)
class Ui_Scanrepair(object):
    def setupUi(self, Scanrepair):
        if not Scanrepair.objectName():
            Scanrepair.setObjectName(u"Scanrepair")
        Scanrepair.resize(245, 288)
        self.verticalLayout = QVBoxLayout(Scanrepair)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(Scanrepair)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.widget_4 = QWidget(self.widget)
        self.widget_4.setObjectName(u"widget_4")
        self.verticalLayout_4 = QVBoxLayout(self.widget_4)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.icon = QLabel(self.widget_4)
        self.icon.setObjectName(u"icon")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.icon.sizePolicy().hasHeightForWidth())
        self.icon.setSizePolicy(sizePolicy)
        self.icon.setPixmap(QPixmap(u":/material_design/icons/material_design/people_outline.png"))
        self.icon.setScaledContents(True)
        self.icon.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.icon, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.labelname = QLabel(self.widget_4)
        self.labelname.setObjectName(u"labelname")
        sizePolicy.setHeightForWidth(self.labelname.sizePolicy().hasHeightForWidth())
        self.labelname.setSizePolicy(sizePolicy)
        self.labelname.setMinimumSize(QSize(0, 0))
        self.labelname.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.labelname.setFont(font)

        self.verticalLayout_4.addWidget(self.labelname, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.verticalSpacer = QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)


        self.verticalLayout_2.addWidget(self.widget_4)

        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName(u"widget_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy1)
        self.horizontalLayout_2 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.scan_repair = QLineEdit(self.widget_3)
        self.scan_repair.setObjectName(u"scan_repair")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.scan_repair.sizePolicy().hasHeightForWidth())
        self.scan_repair.setSizePolicy(sizePolicy2)
        self.scan_repair.setMinimumSize(QSize(170, 30))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        self.scan_repair.setFont(font1)
        self.scan_repair.setInputMask(u"")

        self.horizontalLayout_2.addWidget(self.scan_repair)

        self.Refresh_scan = QPushButton(self.widget_3)
        self.Refresh_scan.setObjectName(u"Refresh_scan")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.Refresh_scan.sizePolicy().hasHeightForWidth())
        self.Refresh_scan.setSizePolicy(sizePolicy3)
        self.Refresh_scan.setMinimumSize(QSize(33, 30))
        self.Refresh_scan.setMaximumSize(QSize(33, 30))
        self.Refresh_scan.setSizeIncrement(QSize(0, 0))
        font2 = QFont()
        font2.setPointSize(7)
        font2.setBold(False)
        font2.setItalic(True)
        self.Refresh_scan.setFont(font2)
        self.Refresh_scan.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Refresh_scan.setStyleSheet(u"border-radius: 10px;\n"
"background-color: rgb(85, 170, 255);\n"
"border: 1px solid black;")
        icon1 = QIcon()
        icon1.addFile(u":/feather/icons/feather/refresh-ccw.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.Refresh_scan.setIcon(icon1)

        self.horizontalLayout_2.addWidget(self.Refresh_scan)


        self.verticalLayout_2.addWidget(self.widget_3)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy1.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy1)
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.confirmID = QPushButton(self.widget_2)
        self.confirmID.setObjectName(u"confirmID")
        sizePolicy1.setHeightForWidth(self.confirmID.sizePolicy().hasHeightForWidth())
        self.confirmID.setSizePolicy(sizePolicy1)
        self.confirmID.setMinimumSize(QSize(0, 30))
        font3 = QFont()
        font3.setPointSize(10)
        self.confirmID.setFont(font3)
        self.confirmID.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/feather/icons/feather/check.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.confirmID.setIcon(icon2)

        self.horizontalLayout.addWidget(self.confirmID)

        self.pushButton_D = QPushButton(self.widget_2)
        self.pushButton_D.setObjectName(u"pushButton_D")
        self.pushButton_D.setMinimumSize(QSize(0, 30))
        icon3 = QIcon()
        icon3.addFile(u":/feather/icons/feather/x-circle.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_D.setIcon(icon3)

        self.horizontalLayout.addWidget(self.pushButton_D)


        self.verticalLayout_2.addWidget(self.widget_2)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(Scanrepair)

        QMetaObject.connectSlotsByName(Scanrepair)
    # setupUi

    def retranslateUi(self, Scanrepair):
        Scanrepair.setWindowTitle(QCoreApplication.translate("Scanrepair", u"Dialog", None))
        self.icon.setText("")
        self.labelname.setText(QCoreApplication.translate("Scanrepair", u"LOGIN  REPAIRRING STAFF", None))
        self.scan_repair.setText("")
        self.scan_repair.setPlaceholderText(QCoreApplication.translate("Scanrepair", u"Maintenance staff scans ID", None))
        self.Refresh_scan.setText("")
        self.confirmID.setText(QCoreApplication.translate("Scanrepair", u"Complete", None))
        self.pushButton_D.setText(QCoreApplication.translate("Scanrepair", u"Close", None))
    # retranslateUi


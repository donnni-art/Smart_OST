# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_PopupScan.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)
class Ui_Scan(object):
    def setupUi(self, Scan):
        if not Scan.objectName():
            Scan.setObjectName(u"Scan")
        Scan.resize(356, 54)
        icon = QIcon()
        icon.addFile(u":/feather/icons/feather/user.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Scan.setWindowIcon(icon)
        self.UserID = QLineEdit(Scan)
        self.UserID.setObjectName(u"UserID")
        self.UserID.setGeometry(QRect(30, 20, 221, 21))
        self.confirm = QPushButton(Scan)
        self.confirm.setObjectName(u"confirm")
        self.confirm.setGeometry(QRect(290, 20, 61, 21))
        self.confirm.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Refresh_scan = QPushButton(Scan)
        self.Refresh_scan.setObjectName(u"Refresh_scan")
        self.Refresh_scan.setGeometry(QRect(260, 20, 20, 20))
        font = QFont()
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(True)
        self.Refresh_scan.setFont(font)
        self.Refresh_scan.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Refresh_scan.setStyleSheet(u"border-radius: 10px;\n"
"background-color: rgb(85, 170, 255);\n"
"border: 1px solid black;")
        icon1 = QIcon()
        icon1.addFile(u":/feather/icons/feather/refresh-ccw.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.Refresh_scan.setIcon(icon1)

        self.retranslateUi(Scan)

        QMetaObject.connectSlotsByName(Scan)
    # setupUi

    def retranslateUi(self, Scan):
        Scan.setWindowTitle(QCoreApplication.translate("Scan", u"Dialog", None))
        self.UserID.setText("")
        self.confirm.setText(QCoreApplication.translate("Scan", u"Complete", None))
        self.Refresh_scan.setText("")
    # retranslateUi


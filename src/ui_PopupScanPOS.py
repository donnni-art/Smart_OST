# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_PopupScanPOS.ui'
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
class Ui_ScanPOS(object):
    def setupUi(self, ScanPOS):
        if not ScanPOS.objectName():
            ScanPOS.setObjectName(u"ScanPOS")
        ScanPOS.resize(356, 54)
        icon = QIcon()
        icon.addFile(u":/feather/icons/feather/book.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        ScanPOS.setWindowIcon(icon)
        self.NumberPOS = QLineEdit(ScanPOS)
        self.NumberPOS.setObjectName(u"NumberPOS")
        self.NumberPOS.setGeometry(QRect(30, 20, 221, 21))
        self.confirmPOS = QPushButton(ScanPOS)
        self.confirmPOS.setObjectName(u"confirmPOS")
        self.confirmPOS.setGeometry(QRect(290, 20, 61, 21))
        self.confirmPOS.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Refresh_scanPOS = QPushButton(ScanPOS)
        self.Refresh_scanPOS.setObjectName(u"Refresh_scanPOS")
        self.Refresh_scanPOS.setGeometry(QRect(260, 20, 20, 20))
        font = QFont()
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(True)
        self.Refresh_scanPOS.setFont(font)
        self.Refresh_scanPOS.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Refresh_scanPOS.setStyleSheet(u"border-radius: 10px;\n"
"background-color: rgb(85, 170, 255);\n"
"border: 1px solid black;")
        icon1 = QIcon()
        icon1.addFile(u":/feather/icons/feather/refresh-ccw.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.Refresh_scanPOS.setIcon(icon1)

        self.retranslateUi(ScanPOS)

        QMetaObject.connectSlotsByName(ScanPOS)
    # setupUi

    def retranslateUi(self, ScanPOS):
        ScanPOS.setWindowTitle(QCoreApplication.translate("ScanPOS", u"Dialog", None))
        self.NumberPOS.setText("")
        self.confirmPOS.setText(QCoreApplication.translate("ScanPOS", u"Complete", None))
        self.Refresh_scanPOS.setText("")
    # retranslateUi


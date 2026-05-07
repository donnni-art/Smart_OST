# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_PopupScanCodeFixture.ui'
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
class Ui_ScanCode(object):
    def setupUi(self, ScanCode):
        if not ScanCode.objectName():
            ScanCode.setObjectName(u"ScanCode")
        ScanCode.resize(356, 54)
        icon = QIcon()
        icon.addFile(u":/feather/icons/feather/tool.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        ScanCode.setWindowIcon(icon)
        self.codeFixture = QLineEdit(ScanCode)
        self.codeFixture.setObjectName(u"codeFixture")
        self.codeFixture.setGeometry(QRect(30, 20, 221, 21))
        self.confirmFixture = QPushButton(ScanCode)
        self.confirmFixture.setObjectName(u"confirmFixture")
        self.confirmFixture.setGeometry(QRect(290, 20, 61, 21))
        self.confirmFixture.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Refresh_scanCodeFixture = QPushButton(ScanCode)
        self.Refresh_scanCodeFixture.setObjectName(u"Refresh_scanCodeFixture")
        self.Refresh_scanCodeFixture.setGeometry(QRect(260, 20, 20, 20))
        font = QFont()
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(True)
        self.Refresh_scanCodeFixture.setFont(font)
        self.Refresh_scanCodeFixture.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Refresh_scanCodeFixture.setStyleSheet(u"border-radius: 10px;\n"
"background-color: rgb(85, 170, 255);\n"
"border: 1px solid black;\n"
"color: rgb(0, 0, 0);")
        icon1 = QIcon()
        icon1.addFile(u":/feather/icons/feather/refresh-cw.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.Refresh_scanCodeFixture.setIcon(icon1)

        self.retranslateUi(ScanCode)

        QMetaObject.connectSlotsByName(ScanCode)
    # setupUi

    def retranslateUi(self, ScanCode):
        ScanCode.setWindowTitle(QCoreApplication.translate("ScanCode", u"Dialog", None))
        self.codeFixture.setText("")
        self.confirmFixture.setText(QCoreApplication.translate("ScanCode", u"Complete", None))
        self.Refresh_scanCodeFixture.setText("")
    # retranslateUi


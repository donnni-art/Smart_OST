# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_Demo2.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QLineEdit, QPushButton, QRadioButton,
    QSizePolicy, QWidget)
class Ui_Demo1(object):
    def setupUi(self, Demo1):
        if not Demo1.objectName():
            Demo1.setObjectName(u"Demo1")
        Demo1.resize(528, 183)
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setBold(False)
        Demo1.setFont(font)
        Demo1.setMouseTracking(False)
        icon = QIcon()
        icon.addFile(u":/material_design/icons/material_design/login.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Demo1.setWindowIcon(icon)
        Demo1.setAutoFillBackground(False)
        Demo1.setStyleSheet(u"")
        self.buttonBox = QDialogButtonBox(Demo1)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(440, 20, 71, 91))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(9)
        font1.setBold(False)
        font1.setKerning(False)
        self.buttonBox.setFont(font1)
        self.buttonBox.setOrientation(Qt.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close|QDialogButtonBox.Reset|QDialogButtonBox.Save)
        self.IDoperator = QPushButton(Demo1)
        self.IDoperator.setObjectName(u"IDoperator")
        self.IDoperator.setGeometry(QRect(30, 60, 241, 24))
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setBold(False)
        self.IDoperator.setFont(font2)
        self.CodeFixture = QPushButton(Demo1)
        self.CodeFixture.setObjectName(u"CodeFixture")
        self.CodeFixture.setGeometry(QRect(30, 100, 241, 24))
        self.NumberPOS = QPushButton(Demo1)
        self.NumberPOS.setObjectName(u"NumberPOS")
        self.NumberPOS.setGeometry(QRect(30, 20, 241, 24))
        self.NumberPOS.setText(u"Click to scan Qr code POS")
        self.LicenseUser = QLabel(Demo1)
        self.LicenseUser.setObjectName(u"LicenseUser")
        self.LicenseUser.setGeometry(QRect(300, 60, 121, 21))
        self.LicenseUser.setStyleSheet(u"background-color: rgb(218, 218, 218);\n"
"border-radius: 4px;")
        self.checkPOS = QLabel(Demo1)
        self.checkPOS.setObjectName(u"checkPOS")
        self.checkPOS.setGeometry(QRect(300, 20, 121, 21))
        self.checkPOS.setStyleSheet(u"background-color: rgb(218, 218, 218);\n"
"border-radius: 4px;")
        self.Status_confirm_fixture = QLabel(Demo1)
        self.Status_confirm_fixture.setObjectName(u"Status_confirm_fixture")
        self.Status_confirm_fixture.setGeometry(QRect(300, 100, 121, 21))
        self.Status_confirm_fixture.setStyleSheet(u"background-color: rgb(218, 218, 218);\n"
"border-radius: 4px;")
        self.FOST = QRadioButton(Demo1)
        self.FOST.setObjectName(u"FOST")
        self.FOST.setGeometry(QRect(40, 140, 71, 41))
        self.FOST2 = QRadioButton(Demo1)
        self.FOST2.setObjectName(u"FOST2")
        self.FOST2.setGeometry(QRect(120, 140, 71, 41))
        self.FOST3 = QRadioButton(Demo1)
        self.FOST3.setObjectName(u"FOST3")
        self.FOST3.setGeometry(QRect(200, 140, 71, 41))
        self.lineEdit = QLineEdit(Demo1)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(350, 150, 111, 21))
        self.label = QLabel(Demo1)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(280, 140, 71, 41))
        font3 = QFont()
        font3.setFamilies([u"Segoe UI"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        font3.setUnderline(False)
        font3.setStrikeOut(False)
        font3.setKerning(True)
        self.label.setFont(font3)
        self.label.setStyleSheet(u"font: 10pt \"Segoe UI\";")
        self.label_2 = QLabel(Demo1)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(470, 140, 41, 41))
        font4 = QFont()
        font4.setFamilies([u"Segoe UI"])
        font4.setPointSize(10)
        font4.setBold(False)
        font4.setItalic(False)
        self.label_2.setFont(font4)
        self.label_2.setStyleSheet(u"font: 10pt \"Segoe UI\";")
        self.fa = QRadioButton(Demo1)
        self.fa.setObjectName(u"fa")
        self.fa.setGeometry(QRect(440, 120, 95, 21))
        font5 = QFont()
        font5.setBold(False)
        self.fa.setFont(font5)
        self.mass = QRadioButton(Demo1)
        self.mass.setObjectName(u"mass")
        self.mass.setGeometry(QRect(480, 120, 95, 20))
        self.mass.setFont(font5)

        self.retranslateUi(Demo1)
        self.buttonBox.accepted.connect(Demo1.accept)
        self.buttonBox.rejected.connect(Demo1.reject)

        QMetaObject.connectSlotsByName(Demo1)
    # setupUi

    def retranslateUi(self, Demo1):
        Demo1.setWindowTitle(QCoreApplication.translate("Demo1", u"Dialog", None))
        self.IDoperator.setText(QCoreApplication.translate("Demo1", u"Click to scan user ID", None))
        self.CodeFixture.setText(QCoreApplication.translate("Demo1", u"Click to scan Qr code Fixture", None))
        self.LicenseUser.setText("")
        self.checkPOS.setText("")
        self.Status_confirm_fixture.setText("")
        self.FOST.setText(QCoreApplication.translate("Demo1", u"FOST", None))
        self.FOST2.setText(QCoreApplication.translate("Demo1", u"FOST2", None))
        self.FOST3.setText(QCoreApplication.translate("Demo1", u"FOST3", None))
        self.lineEdit.setText("")
        self.label.setText(QCoreApplication.translate("Demo1", u"Lot size : ", None))
        self.label_2.setText(QCoreApplication.translate("Demo1", u"pcs.", None))
        self.fa.setText(QCoreApplication.translate("Demo1", u"F.", None))
        self.mass.setText(QCoreApplication.translate("Demo1", u"M.", None))
    # retranslateUi


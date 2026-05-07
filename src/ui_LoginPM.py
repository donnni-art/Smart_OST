# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_LoginPM.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)
class Ui_PM_SYSTEM(object):
    def setupUi(self, PM_SYSTEM):
        if not PM_SYSTEM.objectName():
            PM_SYSTEM.setObjectName(u"PM_SYSTEM")
        PM_SYSTEM.resize(321, 382)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PM_SYSTEM.sizePolicy().hasHeightForWidth())
        PM_SYSTEM.setSizePolicy(sizePolicy)
        PM_SYSTEM.setMinimumSize(QSize(0, 0))
        PM_SYSTEM.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(PM_SYSTEM)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.LoginPM = QWidget(PM_SYSTEM)
        self.LoginPM.setObjectName(u"LoginPM")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.LoginPM.sizePolicy().hasHeightForWidth())
        self.LoginPM.setSizePolicy(sizePolicy1)
        self.LoginPM.setMinimumSize(QSize(0, 0))
        self.LoginPM.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.LoginPM)
        self.verticalLayout_2.setSpacing(9)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(9, 10, 9, 9)
        self.icon = QLabel(self.LoginPM)
        self.icon.setObjectName(u"icon")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.icon.sizePolicy().hasHeightForWidth())
        self.icon.setSizePolicy(sizePolicy2)
        self.icon.setMinimumSize(QSize(80, 80))
        self.icon.setMaximumSize(QSize(80, 80))
        self.icon.setPixmap(QPixmap(u":/feather/icons/feather/check-square.png"))
        self.icon.setScaledContents(True)

        self.verticalLayout_2.addWidget(self.icon, 0, Qt.AlignHCenter)

        self.verticalSpacer_4 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_4)

        self.labelname = QLabel(self.LoginPM)
        self.labelname.setObjectName(u"labelname")
        sizePolicy2.setHeightForWidth(self.labelname.sizePolicy().hasHeightForWidth())
        self.labelname.setSizePolicy(sizePolicy2)
        self.labelname.setMinimumSize(QSize(113, 31))
        font = QFont()
        font.setPointSize(17)
        font.setBold(True)
        self.labelname.setFont(font)

        self.verticalLayout_2.addWidget(self.labelname, 0, Qt.AlignHCenter)

        self.labelimform = QLabel(self.LoginPM)
        self.labelimform.setObjectName(u"labelimform")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.labelimform.sizePolicy().hasHeightForWidth())
        self.labelimform.setSizePolicy(sizePolicy3)
        font1 = QFont()
        font1.setBold(False)
        self.labelimform.setFont(font1)

        self.verticalLayout_2.addWidget(self.labelimform, 0, Qt.AlignHCenter)

        self.id_repair = QPushButton(self.LoginPM)
        self.id_repair.setObjectName(u"id_repair")
        self.id_repair.setMinimumSize(QSize(285, 41))
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(12)
        font2.setBold(True)
        font2.setItalic(False)
        font2.setUnderline(False)
        font2.setStrikeOut(False)
        font2.setKerning(True)
        self.id_repair.setFont(font2)
        self.id_repair.setAcceptDrops(False)
        self.id_repair.setLayoutDirection(Qt.LeftToRight)
        self.id_repair.setAutoFillBackground(False)
        self.id_repair.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u":/font_awesome_solid/icons/font_awesome/solid/screwdriver-wrench.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.id_repair.setIcon(icon1)
        self.id_repair.setIconSize(QSize(30, 30))
        self.id_repair.setAutoExclusive(False)
        self.id_repair.setAutoDefault(False)
        self.id_repair.setFlat(False)

        self.verticalLayout_2.addWidget(self.id_repair)

        self.id_leader = QPushButton(self.LoginPM)
        self.id_leader.setObjectName(u"id_leader")
        self.id_leader.setMinimumSize(QSize(285, 41))
        self.id_leader.setFont(font2)
        self.id_leader.setAcceptDrops(True)
        self.id_leader.setLayoutDirection(Qt.LeftToRight)
        self.id_leader.setAutoFillBackground(False)
        self.id_leader.setStyleSheet(u"")
        icon2 = QIcon()
        icon2.addFile(u":/feather/icons/feather/user.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.id_leader.setIcon(icon2)
        self.id_leader.setIconSize(QSize(30, 30))
        self.id_leader.setAutoDefault(False)

        self.verticalLayout_2.addWidget(self.id_leader)

        self.id_pm = QPushButton(self.LoginPM)
        self.id_pm.setObjectName(u"id_pm")
        sizePolicy.setHeightForWidth(self.id_pm.sizePolicy().hasHeightForWidth())
        self.id_pm.setSizePolicy(sizePolicy)
        self.id_pm.setMinimumSize(QSize(200, 38))
        self.id_pm.setMaximumSize(QSize(200, 38))
        self.id_pm.setFont(font2)
        self.id_pm.setAcceptDrops(True)
        self.id_pm.setLayoutDirection(Qt.LeftToRight)
        self.id_pm.setAutoFillBackground(False)
        self.id_pm.setStyleSheet(u"")
        icon3 = QIcon()
        icon3.addFile(u":/feather/icons/feather/log-in.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.id_pm.setIcon(icon3)
        self.id_pm.setIconSize(QSize(30, 30))
        self.id_pm.setAutoDefault(False)

        self.verticalLayout_2.addWidget(self.id_pm, 0, Qt.AlignHCenter)

        self.pushButton_D = QPushButton(self.LoginPM)
        self.pushButton_D.setObjectName(u"pushButton_D")
        sizePolicy1.setHeightForWidth(self.pushButton_D.sizePolicy().hasHeightForWidth())
        self.pushButton_D.setSizePolicy(sizePolicy1)
        self.pushButton_D.setMinimumSize(QSize(0, 0))
        self.pushButton_D.setMaximumSize(QSize(16777215, 16777215))
        font3 = QFont()
        font3.setPointSize(8)
        font3.setBold(True)
        self.pushButton_D.setFont(font3)
        icon4 = QIcon()
        icon4.addFile(u":/feather/icons/feather/x-circle.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_D.setIcon(icon4)
        self.pushButton_D.setAutoDefault(False)

        self.verticalLayout_2.addWidget(self.pushButton_D, 0, Qt.AlignRight|Qt.AlignVCenter)


        self.verticalLayout.addWidget(self.LoginPM)


        self.retranslateUi(PM_SYSTEM)

        self.id_repair.setDefault(False)


        QMetaObject.connectSlotsByName(PM_SYSTEM)
    # setupUi

    def retranslateUi(self, PM_SYSTEM):
        PM_SYSTEM.setWindowTitle(QCoreApplication.translate("PM_SYSTEM", u"Dialog", None))
        self.icon.setText("")
        self.labelname.setText(QCoreApplication.translate("PM_SYSTEM", u"LOGIN PM", None))
        self.labelimform.setText(QCoreApplication.translate("PM_SYSTEM", u"The fixture is due for preventive maintenance.", None))
        self.id_repair.setText(QCoreApplication.translate("PM_SYSTEM", u"    Repairing Staff", None))
        self.id_leader.setText(QCoreApplication.translate("PM_SYSTEM", u"    Leader up", None))
        self.id_pm.setText(QCoreApplication.translate("PM_SYSTEM", u" PM", None))
        self.pushButton_D.setText(QCoreApplication.translate("PM_SYSTEM", u" Close", None))
    # retranslateUi


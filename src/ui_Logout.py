# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_Logout.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)
class Ui_Finish(object):
    def setupUi(self, Finish):
        if not Finish.objectName():
            Finish.setObjectName(u"Finish")
        Finish.resize(366, 478)
        self.centralwidget = QWidget(Finish)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.Logout = QWidget(self.centralwidget)
        self.Logout.setObjectName(u"Logout")
        self.verticalLayout_2 = QVBoxLayout(self.Logout)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.icon_logout = QLabel(self.Logout)
        self.icon_logout.setObjectName(u"icon_logout")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.icon_logout.sizePolicy().hasHeightForWidth())
        self.icon_logout.setSizePolicy(sizePolicy)
        self.icon_logout.setPixmap(QPixmap(u":/feather/icons/feather/log-out.png"))

        self.verticalLayout_2.addWidget(self.icon_logout, 0, Qt.AlignHCenter)

        self.label_logout = QLabel(self.Logout)
        self.label_logout.setObjectName(u"label_logout")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_logout.sizePolicy().hasHeightForWidth())
        self.label_logout.setSizePolicy(sizePolicy1)
        self.label_logout.setMinimumSize(QSize(0, 0))
        font = QFont()
        font.setPointSize(17)
        font.setBold(True)
        self.label_logout.setFont(font)

        self.verticalLayout_2.addWidget(self.label_logout, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.label_note = QLabel(self.Logout)
        self.label_note.setObjectName(u"label_note")
        sizePolicy.setHeightForWidth(self.label_note.sizePolicy().hasHeightForWidth())
        self.label_note.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.label_note, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.scan_confirm = QWidget(self.Logout)
        self.scan_confirm.setObjectName(u"scan_confirm")
        self.horizontalLayout = QHBoxLayout(self.scan_confirm)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.widget_confirm = QWidget(self.scan_confirm)
        self.widget_confirm.setObjectName(u"widget_confirm")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_confirm)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_name = QLabel(self.widget_confirm)
        self.label_name.setObjectName(u"label_name")

        self.horizontalLayout_4.addWidget(self.label_name)

        self.lineEdit_name = QLineEdit(self.widget_confirm)
        self.lineEdit_name.setObjectName(u"lineEdit_name")

        self.horizontalLayout_4.addWidget(self.lineEdit_name)

        self.label_id = QLabel(self.widget_confirm)
        self.label_id.setObjectName(u"label_id")

        self.horizontalLayout_4.addWidget(self.label_id)

        self.lineEdit_id = QLineEdit(self.widget_confirm)
        self.lineEdit_id.setObjectName(u"lineEdit_id")

        self.horizontalLayout_4.addWidget(self.lineEdit_id)


        self.horizontalLayout.addWidget(self.widget_confirm)


        self.verticalLayout_2.addWidget(self.scan_confirm)

        self.defect_items = QLabel(self.Logout)
        self.defect_items.setObjectName(u"defect_items")
        font1 = QFont()
        font1.setPointSize(11)
        font1.setBold(True)
        self.defect_items.setFont(font1)

        self.verticalLayout_2.addWidget(self.defect_items, 0, Qt.AlignLeft|Qt.AlignBottom)

        self.total_ng = QWidget(self.Logout)
        self.total_ng.setObjectName(u"total_ng")
        self.horizontalLayout_5 = QHBoxLayout(self.total_ng)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(3, 3, 3, 3)
        self.label_ng = QLabel(self.total_ng)
        self.label_ng.setObjectName(u"label_ng")

        self.horizontalLayout_5.addWidget(self.label_ng)

        self.lineEdit_tatal = QLineEdit(self.total_ng)
        self.lineEdit_tatal.setObjectName(u"lineEdit_tatal")
        self.lineEdit_tatal.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_5.addWidget(self.lineEdit_tatal)

        self.label_pcs = QLabel(self.total_ng)
        self.label_pcs.setObjectName(u"label_pcs")

        self.horizontalLayout_5.addWidget(self.label_pcs)


        self.verticalLayout_2.addWidget(self.total_ng, 0, Qt.AlignLeft)

        self.ng_item1 = QWidget(self.Logout)
        self.ng_item1.setObjectName(u"ng_item1")
        self.horizontalLayout_2 = QHBoxLayout(self.ng_item1)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.open = QWidget(self.ng_item1)
        self.open.setObjectName(u"open")
        self.horizontalLayout_9 = QHBoxLayout(self.open)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(3, 3, 3, 3)
        self.label_open = QLabel(self.open)
        self.label_open.setObjectName(u"label_open")

        self.horizontalLayout_9.addWidget(self.label_open)

        self.lineEdit_open = QLineEdit(self.open)
        self.lineEdit_open.setObjectName(u"lineEdit_open")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lineEdit_open.sizePolicy().hasHeightForWidth())
        self.lineEdit_open.setSizePolicy(sizePolicy2)

        self.horizontalLayout_9.addWidget(self.lineEdit_open)


        self.horizontalLayout_2.addWidget(self.open)

        self.short_2 = QWidget(self.ng_item1)
        self.short_2.setObjectName(u"short_2")
        self.horizontalLayout_8 = QHBoxLayout(self.short_2)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(3, 3, 3, 3)
        self.label_short = QLabel(self.short_2)
        self.label_short.setObjectName(u"label_short")

        self.horizontalLayout_8.addWidget(self.label_short)

        self.lineEdit_short = QLineEdit(self.short_2)
        self.lineEdit_short.setObjectName(u"lineEdit_short")
        sizePolicy2.setHeightForWidth(self.lineEdit_short.sizePolicy().hasHeightForWidth())
        self.lineEdit_short.setSizePolicy(sizePolicy2)

        self.horizontalLayout_8.addWidget(self.lineEdit_short)


        self.horizontalLayout_2.addWidget(self.short_2)

        self.blkm = QWidget(self.ng_item1)
        self.blkm.setObjectName(u"blkm")
        self.horizontalLayout_7 = QHBoxLayout(self.blkm)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(3, 3, 3, 3)
        self.label_blkm = QLabel(self.blkm)
        self.label_blkm.setObjectName(u"label_blkm")

        self.horizontalLayout_7.addWidget(self.label_blkm)

        self.lineEdit_blkm = QLineEdit(self.blkm)
        self.lineEdit_blkm.setObjectName(u"lineEdit_blkm")
        sizePolicy2.setHeightForWidth(self.lineEdit_blkm.sizePolicy().hasHeightForWidth())
        self.lineEdit_blkm.setSizePolicy(sizePolicy2)

        self.horizontalLayout_7.addWidget(self.lineEdit_blkm)


        self.horizontalLayout_2.addWidget(self.blkm)


        self.verticalLayout_2.addWidget(self.ng_item1)

        self.ng_item2 = QWidget(self.Logout)
        self.ng_item2.setObjectName(u"ng_item2")
        self.horizontalLayout_3 = QHBoxLayout(self.ng_item2)
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.mat = QWidget(self.ng_item2)
        self.mat.setObjectName(u"mat")
        self.horizontalLayout_10 = QHBoxLayout(self.mat)
        self.horizontalLayout_10.setSpacing(3)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(3, 3, 3, 3)
        self.label_mat = QLabel(self.mat)
        self.label_mat.setObjectName(u"label_mat")

        self.horizontalLayout_10.addWidget(self.label_mat)

        self.lineEdit_mat = QLineEdit(self.mat)
        self.lineEdit_mat.setObjectName(u"lineEdit_mat")
        sizePolicy2.setHeightForWidth(self.lineEdit_mat.sizePolicy().hasHeightForWidth())
        self.lineEdit_mat.setSizePolicy(sizePolicy2)

        self.horizontalLayout_10.addWidget(self.lineEdit_mat)


        self.horizontalLayout_3.addWidget(self.mat)

        self.shot = QWidget(self.ng_item2)
        self.shot.setObjectName(u"shot")
        self.horizontalLayout_11 = QHBoxLayout(self.shot)
        self.horizontalLayout_11.setSpacing(3)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(3, 3, 3, 3)
        self.label_shot = QLabel(self.shot)
        self.label_shot.setObjectName(u"label_shot")

        self.horizontalLayout_11.addWidget(self.label_shot)

        self.lineEdit_shot = QLineEdit(self.shot)
        self.lineEdit_shot.setObjectName(u"lineEdit_shot")
        sizePolicy2.setHeightForWidth(self.lineEdit_shot.sizePolicy().hasHeightForWidth())
        self.lineEdit_shot.setSizePolicy(sizePolicy2)

        self.horizontalLayout_11.addWidget(self.lineEdit_shot)


        self.horizontalLayout_3.addWidget(self.shot)

        self.note = QWidget(self.ng_item2)
        self.note.setObjectName(u"note")
        self.horizontalLayout_12 = QHBoxLayout(self.note)
        self.horizontalLayout_12.setSpacing(3)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(3, 3, 3, 3)
        self.label = QLabel(self.note)
        self.label.setObjectName(u"label")

        self.horizontalLayout_12.addWidget(self.label)

        self.lineEdit_note = QLineEdit(self.note)
        self.lineEdit_note.setObjectName(u"lineEdit_note")
        sizePolicy2.setHeightForWidth(self.lineEdit_note.sizePolicy().hasHeightForWidth())
        self.lineEdit_note.setSizePolicy(sizePolicy2)

        self.horizontalLayout_12.addWidget(self.lineEdit_note)


        self.horizontalLayout_3.addWidget(self.note)


        self.verticalLayout_2.addWidget(self.ng_item2)

        self.confirm_finish = QWidget(self.Logout)
        self.confirm_finish.setObjectName(u"confirm_finish")
        self.horizontalLayout_6 = QHBoxLayout(self.confirm_finish)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.save_finish = QPushButton(self.confirm_finish)
        self.save_finish.setObjectName(u"save_finish")
        icon = QIcon()
        icon.addFile(u":/feather/icons/feather/save.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.save_finish.setIcon(icon)

        self.horizontalLayout_6.addWidget(self.save_finish)

        self.close_finish = QPushButton(self.confirm_finish)
        self.close_finish.setObjectName(u"close_finish")
        icon1 = QIcon()
        icon1.addFile(u":/feather/icons/feather/x-circle.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.close_finish.setIcon(icon1)

        self.horizontalLayout_6.addWidget(self.close_finish)


        self.verticalLayout_2.addWidget(self.confirm_finish)


        self.verticalLayout.addWidget(self.Logout)

        Finish.setCentralWidget(self.centralwidget)

        self.retranslateUi(Finish)

        QMetaObject.connectSlotsByName(Finish)
    # setupUi

    def retranslateUi(self, Finish):
        Finish.setWindowTitle(QCoreApplication.translate("Finish", u"MainWindow", None))
        self.icon_logout.setText("")
        self.label_logout.setText(QCoreApplication.translate("Finish", u"Log Out", None))
        self.label_note.setText(QCoreApplication.translate("Finish", u"Confirm the results after the test is completed.", None))
        self.label_name.setText(QCoreApplication.translate("Finish", u"Confirmed by", None))
        self.label_id.setText(QCoreApplication.translate("Finish", u"ID", None))
        self.defect_items.setText(QCoreApplication.translate("Finish", u"Defect Items.", None))
        self.label_ng.setText(QCoreApplication.translate("Finish", u"TOTAL NG :", None))
        self.lineEdit_tatal.setText("")
        self.label_pcs.setText(QCoreApplication.translate("Finish", u"pcs.", None))
        self.label_open.setText(QCoreApplication.translate("Finish", u"OPEN", None))
        self.label_short.setText(QCoreApplication.translate("Finish", u"SHORT", None))
        self.label_blkm.setText(QCoreApplication.translate("Finish", u"BLKM", None))
        self.label_mat.setText(QCoreApplication.translate("Finish", u"MAT", None))
        self.label_shot.setText(QCoreApplication.translate("Finish", u"SHOT", None))
        self.label.setText(QCoreApplication.translate("Finish", u"Note", None))
        self.lineEdit_note.setPlaceholderText(QCoreApplication.translate("Finish", u"note", None))
        self.save_finish.setText(QCoreApplication.translate("Finish", u"    SAVE", None))
        self.close_finish.setText(QCoreApplication.translate("Finish", u" CLOES", None))
    # retranslateUi


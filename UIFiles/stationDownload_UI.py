# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'stationDownloadUI.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)
import assets_rc

class Ui_stationdownloadMainUI(object):
    def setupUi(self, stationdownloadMainUI):
        if not stationdownloadMainUI.objectName():
            stationdownloadMainUI.setObjectName(u"stationdownloadMainUI")
        stationdownloadMainUI.resize(716, 300)
        stationdownloadMainUI.setStyleSheet(u"#stationdownloadMainUI{\n"
"	background-color:transparent;\n"
"}\n"
"\n"
"#main_frame{\n"
"background: #413B47;\n"
"border: 2px solid rgb(36, 32, 39);\n"
"}\n"
"\n"
"QLabel[styleClass=\"titleInfo\"]{\n"
"	color: #fff;\n"
"}\n"
"\n"
"QLabel[styleClass=\"info\"]{\n"
"	color: #fff;\n"
"	font-size:15px;\n"
"	font-weight:bold;\n"
"}\n"
"\n"
"*[styleClass=\"hide\"]{\n"
"	background-color:transparent;\n"
"}\n"
"")
        self.verticalLayout = QVBoxLayout(stationdownloadMainUI)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.main_frame = QFrame(stationdownloadMainUI)
        self.main_frame.setObjectName(u"main_frame")
        self.main_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.main_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.main_frame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.info_frame = QFrame(self.main_frame)
        self.info_frame.setObjectName(u"info_frame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.info_frame.sizePolicy().hasHeightForWidth())
        self.info_frame.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self.info_frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label20_3 = QLabel(self.info_frame)
        self.label20_3.setObjectName(u"label20_3")

        self.gridLayout.addWidget(self.label20_3, 0, 6, 1, 1)

        self.date_lbl = QLabel(self.info_frame)
        self.date_lbl.setObjectName(u"date_lbl")

        self.gridLayout.addWidget(self.date_lbl, 0, 10, 1, 1)

        self.train_lbl = QLabel(self.info_frame)
        self.train_lbl.setObjectName(u"train_lbl")

        self.gridLayout.addWidget(self.train_lbl, 0, 4, 1, 1)

        self.camera_lbl = QLabel(self.info_frame)
        self.camera_lbl.setObjectName(u"camera_lbl")

        self.gridLayout.addWidget(self.camera_lbl, 0, 7, 1, 1)

        self.station_lbl = QLabel(self.info_frame)
        self.station_lbl.setObjectName(u"station_lbl")

        self.gridLayout.addWidget(self.station_lbl, 0, 1, 1, 1)

        self.label20_2 = QLabel(self.info_frame)
        self.label20_2.setObjectName(u"label20_2")

        self.gridLayout.addWidget(self.label20_2, 0, 3, 1, 1)

        self.label20 = QLabel(self.info_frame)
        self.label20.setObjectName(u"label20")

        self.gridLayout.addWidget(self.label20, 0, 9, 1, 1)

        self.label = QLabel(self.info_frame)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 0, 5, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 8, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_5, 0, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 11, 1, 1)

        self.close_btn = QPushButton(self.info_frame)
        self.close_btn.setObjectName(u"close_btn")
        self.close_btn.setStyleSheet(u"QPushButton{\n"
"	background-color:transparent;\n"
"	icon: url(:/icons/icons/icons8-close-48.png);\n"
"	border:none;\n"
"\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	icon: url(:/icons/icons/icons8-close-48-hover.png);\n"
"\n"
"}\n"
"\n"
"")

        self.gridLayout.addWidget(self.close_btn, 0, 12, 1, 1)


        self.verticalLayout_4.addWidget(self.info_frame)

        self.line = QFrame(self.main_frame)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_4.addWidget(self.line)

        self.frame_2 = QFrame(self.main_frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.download_filter_am_lock_wgt = QWidget(self.frame_3)
        self.download_filter_am_lock_wgt.setObjectName(u"download_filter_am_lock_wgt")
        self.horizontalLayout_8 = QHBoxLayout(self.download_filter_am_lock_wgt)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")

        self.verticalLayout_2.addWidget(self.download_filter_am_lock_wgt)


        self.horizontalLayout_3.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.download_filter_pm_lock_wgt = QWidget(self.frame_4)
        self.download_filter_pm_lock_wgt.setObjectName(u"download_filter_pm_lock_wgt")
        self.horizontalLayout_7 = QHBoxLayout(self.download_filter_pm_lock_wgt)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")

        self.verticalLayout_3.addWidget(self.download_filter_pm_lock_wgt)


        self.horizontalLayout_3.addWidget(self.frame_4)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.verticalLayout_4.addWidget(self.frame_2)

        self.msg_lbl = QLabel(self.main_frame)
        self.msg_lbl.setObjectName(u"msg_lbl")
        self.msg_lbl.setMinimumSize(QSize(0, 0))
        self.msg_lbl.setMaximumSize(QSize(16777215, 50))
        self.msg_lbl.setStyleSheet(u"color: rgb(64, 150, 255);")
        self.msg_lbl.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.msg_lbl)

        self.frame = QFrame(self.main_frame)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 50))
        self.frame.setMaximumSize(QSize(16777215, 50))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.prograssbar = QProgressBar(self.frame)
        self.prograssbar.setObjectName(u"prograssbar")
        self.prograssbar.setStyleSheet(u"QProgressBar {\n"
"    border: 1px solid #444; /* \u062d\u0627\u0634\u06cc\u0647 \u0638\u0631\u06cc\u0641 \u0628\u0631\u0627\u06cc \u06a9\u0644 \u067e\u0631\u0648\u06af\u0631\u0633 \u0628\u0627\u0631 */\n"
"    background-color: rgba(30,30,30,60); /* \u067e\u0633\u200c\u0632\u0645\u06cc\u0646\u0647 \u062a\u06cc\u0631\u0647 */\n"
"    border-radius: 5px; /* \u06af\u0648\u0634\u0647\u200c\u0647\u0627\u06cc \u06af\u0631\u062f */\n"
"    height: 10px; /* \u0627\u0631\u062a\u0641\u0627\u0639 \u06a9\u0644\u06cc \u067e\u0631\u0648\u06af\u0631\u0633 \u0628\u0627\u0631 */\n"
"    text-align: right; /* \u0645\u062a\u0646 \u0633\u0645\u062a \u0631\u0627\u0633\u062a \u0642\u0631\u0627\u0631 \u06af\u06cc\u0631\u062f */\n"
"    color: white; /* \u0631\u0646\u06af \u0645\u062a\u0646 \u0633\u0641\u06cc\u062f */\n"
"    padding: 0px;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.534, x2:1, y2:0.483, stop:0 rgba(39, 83, 237, 255), stop:0.516484 rgba(118, 22, 228, 255));\n"
""
                        "    border-radius: 5px; /* \u06af\u0648\u0634\u0647\u200c\u0647\u0627\u06cc \u06af\u0631\u062f \u0628\u0631\u0627\u06cc \u0628\u062e\u0634 \u067e\u0631 \u0634\u062f\u0647 */\n"
"    margin: 1px; /* \u0641\u0627\u0635\u0644\u0647\u200c\u0627\u06cc \u06a9\u0648\u0686\u06a9 \u0628\u06cc\u0646 \u0642\u0633\u0645\u062a \u067e\u0631 \u0634\u062f\u0647 \u0648 \u062d\u0627\u0634\u06cc\u0647 */\n"
"}")
        self.prograssbar.setValue(24)

        self.horizontalLayout_2.addWidget(self.prograssbar, 0, Qt.AlignmentFlag.AlignVCenter)

        self.download_btn = QPushButton(self.frame)
        self.download_btn.setObjectName(u"download_btn")
        self.download_btn.setMinimumSize(QSize(30, 30))
        self.download_btn.setStyleSheet(u"QPushButton{\n"
"	background-color:transparent;\n"
"	icon:url(:/icons/icons/download2_disable.png);\n"
"	border:none;\n"
"\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	icon: url(:/icons/icons/download2_hover.png);\n"
"\n"
"}\n"
"\n"
"")
        self.download_btn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.download_btn, 0, Qt.AlignmentFlag.AlignVCenter)


        self.verticalLayout_4.addWidget(self.frame)


        self.verticalLayout.addWidget(self.main_frame)


        self.retranslateUi(stationdownloadMainUI)

        QMetaObject.connectSlotsByName(stationdownloadMainUI)
    # setupUi

    def retranslateUi(self, stationdownloadMainUI):
        stationdownloadMainUI.setWindowTitle(QCoreApplication.translate("stationdownloadMainUI", u"Form", None))
        self.label20_3.setText(QCoreApplication.translate("stationdownloadMainUI", u"Camera:", None))
        self.label20_3.setProperty("styleClass", QCoreApplication.translate("stationdownloadMainUI", u"titleInfo", None))
        self.date_lbl.setText(QCoreApplication.translate("stationdownloadMainUI", u"TextLabel", None))
        self.date_lbl.setProperty("styleClass", QCoreApplication.translate("stationdownloadMainUI", u"info", None))
        self.train_lbl.setText(QCoreApplication.translate("stationdownloadMainUI", u"TextLabel", None))
        self.train_lbl.setProperty("styleClass", QCoreApplication.translate("stationdownloadMainUI", u"info", None))
        self.camera_lbl.setText(QCoreApplication.translate("stationdownloadMainUI", u"TextLabel", None))
        self.camera_lbl.setProperty("styleClass", QCoreApplication.translate("stationdownloadMainUI", u"info", None))
        self.station_lbl.setText(QCoreApplication.translate("stationdownloadMainUI", u"TextLabel", None))
        self.station_lbl.setProperty("styleClass", QCoreApplication.translate("stationdownloadMainUI", u"info", None))
        self.label20_2.setText(QCoreApplication.translate("stationdownloadMainUI", u"Train", None))
        self.label20_2.setProperty("styleClass", QCoreApplication.translate("stationdownloadMainUI", u"titleInfo", None))
        self.label20.setText(QCoreApplication.translate("stationdownloadMainUI", u"Date:", None))
        self.label20.setProperty("styleClass", QCoreApplication.translate("stationdownloadMainUI", u"titleInfo", None))
        self.label.setText(QCoreApplication.translate("stationdownloadMainUI", u"Station:", None))
        self.label.setProperty("styleClass", QCoreApplication.translate("stationdownloadMainUI", u"titleInfo", None))
        self.close_btn.setText("")
        self.frame_2.setProperty("styleClass", QCoreApplication.translate("stationdownloadMainUI", u"hide", None))
        self.frame_3.setProperty("styleClass", QCoreApplication.translate("stationdownloadMainUI", u"hide", None))
        self.frame_4.setProperty("styleClass", QCoreApplication.translate("stationdownloadMainUI", u"hide", None))
        self.msg_lbl.setText(QCoreApplication.translate("stationdownloadMainUI", u"-", None))
        self.frame.setProperty("styleClass", QCoreApplication.translate("stationdownloadMainUI", u"hide", None))
        self.download_btn.setText("")
    # retranslateUi


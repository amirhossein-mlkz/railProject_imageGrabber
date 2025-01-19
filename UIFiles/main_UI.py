# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_UI.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QStackedWidget, QStatusBar,
    QVBoxLayout, QWidget)
import assets_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1120, 845)
        MainWindow.setMinimumSize(QSize(1000, 700))
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        self.centralwidget.setStyleSheet(u"QLabel{\n"
"	color: #e0e0e0;\n"
"	font-size:14px;\n"
"}\n"
"\n"
"\n"
"*[styleClass=\"page\"]{\n"
"	background-color:rgb(36, 32, 39);\n"
"}\n"
"\n"
"*[styleClass=\"page-light\"]{\n"
"	background-color:rgb(65, 59, 71);\n"
"}\n"
"\n"
"\n"
"*[styleClass=\"hide\"]{\n"
"	background-color:transparent;\n"
"}\n"
"\n"
"/*****************QSpinBox, QDoubleSpinBox*******************/\n"
"\n"
"QSpinBox, QDoubleSpinBox\n"
"{\n"
"	background-color: transparent;\n"
"	border-bottom: 2px solid #D7D7D9;\n"
"	color:#fff;\n"
"	border-radius: None;\n"
"	font-size: 16px;\n"
"	min-height: 25px;\n"
"	min-width: 70px;\n"
"	qproperty-alignment: AlignCenter;\n"
"}\n"
"\n"
"QSpinBox:disabled ,\n"
"QDoubleSpinBox:disabled\n"
"{\n"
"	border-bottom: 2px solid #F0F0F2;\n"
"	color: rgb(120, 120, 120);\n"
"}\n"
"\n"
"QSpinBox::up-arrow, \n"
"QDoubleSpinBox::up-arrow\n"
"{   \n"
"	image: url(:/icons/icons/icons8-plus-36.png);\n"
"	width: 16px;\n"
"	height: 16px;\n"
"}\n"
"\n"
"QSpinBox::down-arrow,  \n"
"QDoubleSpinBox::down-arrow\n"
"{   \n"
"	i"
                        "mage: url(:/icons/icons/icons8-minus-36.png);\n"
"	width: 16px;\n"
"	height: 16px;\n"
"}\n"
"\n"
"QSpinBox::up-arrow:hover, \n"
"QDoubleSpinBox::up-arrow:hover\n"
"{   \n"
"	image: url(:/icons/icons/icons8-plus-36-hover.png);\n"
"	width: 16px;\n"
"	height: 16px;\n"
"}\n"
"\n"
"QSpinBox::down-arrow:hover,  \n"
"QDoubleSpinBox::down-arrow:hover\n"
"{   \n"
"	image: url(:/icons/icons/icons8-minus-36-hover.png);\n"
"	width: 16px;\n"
"	height: 16px;\n"
"}\n"
"\n"
"\n"
"\n"
"QSpinBox::up-arrow:disabled, \n"
"QDoubleSpinBox::up-arrow:disabled\n"
"{   \n"
"	image: url(:/icons/icons/plus_icon_gray.png);\n"
"	width: 16px;\n"
"	height: 16px;\n"
"}\n"
"\n"
"QSpinBox::down-arrow:disabled ,  \n"
"QDoubleSpinBox::down-arrow:disabled\n"
"{   \n"
"	image: url(:/icons/icons/minus_icon_gray.png);\n"
"	width: 16px;\n"
"	height: 16px;\n"
"}\n"
"\n"
"QSpinBox::up-button,\n"
"QDoubleSpinBox::up-button\n"
"{\n"
"	border:none;\n"
"    min-width:30px;\n"
"    min-height: 29px;\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-posit"
                        "ion: right;\n"
"    top: 0px;\n"
"    right: 0px;\n"
"}\n"
"\n"
"QSpinBox::down-button,\n"
"QDoubleSpinBox::down-button\n"
"{\n"
"    min-width:30px;\n"
"    min-height: 29px;\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: left;\n"
"    top: 0px;\n"
"    right: 0px;\n"
"}\n"
"\n"
"QSpinBox::up-button,\n"
"QSpinBox::down-button,\n"
"QDoubleSpinBox::up-button,\n"
"QDoubleSpinBox::down-button\n"
"{\n"
"	background-color: transparent;\n"
"}\n"
"\n"
"QSpinBox::up-button:disabled ,\n"
"QSpinBox::down-button:disabled ,\n"
"QDoubleSpinBox::up-button:disabled ,\n"
"QDoubleSpinBox::down-button:disabled\n"
"{\n"
"    subcontrol-origin: border;\n"
"}\n"
"\n"
"QSpinBox:focus, QDoubleSpinBox:focus\n"
"{\n"
"	border-bottom: 2px solid #7892DF;\n"
"}\n"
"\n"
"\n"
"/****************************************************************************/\n"
"/****************************************************************************/\n"
"QComboBox {\n"
"    background-color:  transparent;\n"
"    border: 2px solid white;"
                        "\n"
"    border-radius: 5px;\n"
"    padding: 6px 10px;\n"
"	color: white;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid #5e81ac;\n"
"}\n"
"\n"
"QComboBox::drop-down { /*\u062f\u06a9\u0645\u0647 \u0641\u0644\u0634*/\n"
"    background-color: #fff;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"        background-color: rgb(65, 59, 71);\n"
"        color: #fff;\n"
"        /*selection-background-color: #ff5722; /* \u0631\u0646\u06af \u0622\u06cc\u062a\u0645 \u0627\u0646\u062a\u062e\u0627\u0628\u200c\u0634\u062f\u0647 */\n"
"    }\n"
"QComboBox QAbstractItemView::item {\n"
"        min-height: 25px; /* \u0627\u0631\u062a\u0641\u0627\u0639 \u0647\u0631 \u0622\u06cc\u062a\u0645 */\n"
"        padding: 7px; /* \u0641\u0627\u0635\u0644\u0647 \u062f\u0627\u062e\u0644\u06cc \u0622\u06cc\u062a\u0645\u200c\u0647\u0627 */\n"
"\n"
" }\n"
"QComboBox QAbstractItemView::item:hover {\n"
"        background-color: rgb(96, 99, 234);\n"
"        color: #ffffff; \n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"QComboBox::down-arrow "
                        "{\n"
"    image: url(:/icons/icons/icons8-drop-down-80.png);\n"
"\n"
"    width: 12px;\n"
"    height: 12px;\n"
"}\n"
"/****************************************************************************/\n"
"/****************************************************************************/\n"
"QPushButton[styleClass=\"fill_gradient_purple_btn\"]{\n"
"border-radius:15px;\n"
"padding:5px 10px;\n"
"font-weight:bold;\n"
"color:#fff;\n"
"\n"
"background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(39, 83, 237, 255), stop:1 rgba(118, 22, 228, 255));\n"
"\n"
"\n"
"}\n"
"\n"
"QPushButton[styleClass=\"fill_gradient_purple_btn\"]:hover{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(39, 83, 237, 255), stop:0.516484 rgba(118, 22, 228, 255));\n"
"}\n"
"\n"
"QPushButton[styleClass=\"fill_gradient_purple_btn\"]:disabled{\n"
"background-color: rgb(170,170,170);\n"
"}\n"
"/****************************************************************************/\n"
"/******************"
                        "**********************************************************/\n"
"QPushButton[styleClass=\"border_gradient_purple_btn\"]{\n"
"border-radius:15px;\n"
"padding:5px 10px;\n"
"font-weight:bold;\n"
"color:#fff;\n"
"\n"
"border: 3px solid qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(39, 83, 237, 255), stop:1 rgba(118, 22, 228, 255));\n"
"\n"
"}\n"
"\n"
"QPushButton[styleClass=\"border_gradient_purple_btn\"]:hover{\n"
"border: 5px solid qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(39, 83, 237, 255), stop:1 rgba(118, 22, 228, 255));\n"
"border: 3px solid rgba(118, 22, 228, 255);\n"
"}\n"
"\n"
"/****************************************************************************/\n"
"/****************************************************************************/\n"
"\n"
" QTabWidget::pane { \n"
"        border: 1px solid #444; /* \u0631\u0646\u06af \u062d\u0627\u0634\u06cc\u0647 \u062f\u0648\u0631 TabWidget */\n"
"        background-color: #2b2b2b; /* \u0631\u0646\u06af \u067e\u0633\u200c\u0632"
                        "\u0645\u06cc\u0646\u0647 \u06a9\u0644 TabWidget */\n"
"    }\n"
"\n"
"    QTabBar::tab {\n"
"        background-color: rgb(65, 59, 71); /* \u0631\u0646\u06af \u067e\u0633\u200c\u0632\u0645\u06cc\u0646\u0647 \u062a\u0628\u200c\u0647\u0627 \u062f\u0631 \u062d\u0627\u0644\u062a \u0639\u0627\u062f\u06cc */\n"
"        color: #ffffff;  /* \u0631\u0646\u06af \u0645\u062a\u0646 \u062a\u0628\u200c\u0647\u0627 */\n"
"        padding: 10px;  /* \u0641\u0636\u0627\u06cc \u062f\u0627\u062e\u0644\u06cc \u062a\u0628\u200c\u0647\u0627 */\n"
"        border: 1px solid #444; /* \u0631\u0646\u06af \u062d\u0627\u0634\u06cc\u0647 \u062f\u0648\u0631 \u062a\u0628\u200c\u0647\u0627 */\n"
"        border-bottom-color: #2b2b2b; /* \u0647\u0645\u200c\u0631\u0627\u0633\u062a\u0627\u06cc\u06cc \u062a\u0628\u200c\u0647\u0627 \u0628\u0627 \u067e\u0646\u0644 */\n"
"    }\n"
"\n"
"    QTabBar::tab:selected {\n"
"        background-color: #6327E8; /* \u0631\u0646\u06af \u062a\u0628 \u0627\u0646\u062a\u062e\u0627\u0628 \u0634\u062f\u0647 */\n"
""
                        "        color: #ffffff;  /* \u0631\u0646\u06af \u0645\u062a\u0646 \u062a\u0628 \u0627\u0646\u062a\u062e\u0627\u0628 \u0634\u062f\u0647 */\n"
"        border-bottom-color: #2b2b2b; /* \u0628\u062f\u0648\u0646 \u062d\u0627\u0634\u06cc\u0647 \u062f\u0631 \u067e\u0627\u06cc\u06cc\u0646 \u062a\u0628 \u0627\u0646\u062a\u062e\u0627\u0628 \u0634\u062f\u0647 */\n"
"    }\n"
"\n"
"    QTabBar::tab:hover {\n"
"        background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(39, 83, 237, 			255), stop:0.516484 rgba(118, 22, 228, 255));\n"
"    }\n"
"\n"
"    QTabWidget::tab-bar {\n"
"        left: 5px; /* \u0641\u0627\u0635\u0644\u0647\u200c\u06cc \u062a\u0628\u200c\u0647\u0627 \u0627\u0632 \u067e\u0646\u0644 */\n"
"    }\n"
"/****************************************************************************/\n"
"/****************************************************************************/\n"
"QLineEdit{\n"
"	background-color: transparent;\n"
"	border:1px solid rgba(255, 255, 255, 50);\n"
"	border-botto"
                        "m: 2px solid rgb(247, 240, 255);\n"
"	min-height: 25px;\n"
"	color: #f0e0e0;\n"
"	font-size: 14px;\n"
"	padding: 2px 10px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"        border-bottom: 2px solid qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(39, 83, 237, 255), stop:0.516484 rgba(118, 22, 228, 255));\n"
"        \n"
"    }\n"
"\n"
"QLineEdit:disabled{\n"
"	border-bottom: 2px solid #a0a0a0;\n"
"	color: #a0a0a0;\n"
"}\n"
"\n"
"/****************************************************************************/\n"
"/****************************************************************************/\n"
"   QTableWidget, QTableView {\n"
"       \n"
"	background-color: rgba(74, 74, 74, 50);\n"
"\n"
"    text-align:centre;\n"
"        \n"
"	color: rgb(220, 220, 220);\n"
"	border: 1px solid #444444;  /* \u062d\u0627\u0634\u06cc\u0647 \u062f\u0648\u0631 \u062c\u062f\u0648\u0644 */\n"
"	gridline-color: #555555;  /* \u0631\u0646\u06af \u062e\u0637\u0648\u0637 \u0634\u0628\u06a9\u0647 \u0628\u06cc\u0646 \u0633\u0644\u0648"
                        "\u0644\u200c\u0647\u0627 */\n"
"	font-size: 14px;  /* \u0627\u0646\u062f\u0627\u0632\u0647 \u0641\u0648\u0646\u062a */\n"
"    }\n"
"\n"
"    QHeaderView {\n"
"        background-color: qlineargradient(spread:pad, x1:0.454, y1:0, x2:0.514495, y2:1, stop:0 rgba(77, 77, 104, 255), stop:1 rgba(77, 77, 104, 128));\n"
"        border-top-left-radius: 10px;   /* \u0634\u0639\u0627\u0639 \u06af\u0648\u0634\u0647 \u0628\u0627\u0644\u0627 \u0633\u0645\u062a \u0686\u067e */\n"
"        border-top-right-radius: 10px;  /* \u0634\u0639\u0627\u0639 \u06af\u0648\u0634\u0647 \u0628\u0627\u0644\u0627 \u0633\u0645\u062a \u0631\u0627\u0633\u062a */\n"
"        border: none;  /* \u062d\u0627\u0634\u06cc\u0647 \u0647\u062f\u0631 */\n"
"    }\n"
"\n"
"    QHeaderView::section {\n"
"        background-color: transparent;  /* \u0631\u0646\u06af \u067e\u0633\u200c\u0632\u0645\u06cc\u0646\u0647 \u0633\u0631\u0633\u062a\u0648\u0646\u200c\u0647\u0627 */\n"
"        color: #ffffff;  /* \u0631\u0646\u06af \u0645\u062a\u0646 \u0633\u0631\u0633"
                        "\u062a\u0648\u0646\u200c\u0647\u0627 */\n"
"        padding: 5px;  /* \u0641\u0636\u0627\u06cc \u062f\u0627\u062e\u0644\u06cc \u0633\u0631\u0633\u062a\u0648\u0646\u200c\u0647\u0627 */\n"
"        border: none;  /* \u062d\u0630\u0641 \u062d\u0627\u0634\u06cc\u0647 \u0633\u0631\u0633\u062a\u0648\u0646\u200c\u0647\u0627 */\n"
"        font-weight: bold;  /* \u0628\u0648\u0644\u062f \u06a9\u0631\u062f\u0646 \u0641\u0648\u0646\u062a \u0633\u0631\u0633\u062a\u0648\u0646\u200c\u0647\u0627 */\n"
"    }\n"
"\n"
"QTableView::item:alternate {\n"
"        background-color: rgba(83, 83, 105,50)\n"
"    }\n"
"/****************************************************************************/\n"
"/****************************************************************************/\n"
"\n"
"QCheckBox {\n"
"        spacing: 5px;  /* \u0641\u0627\u0635\u0644\u0647 \u0628\u06cc\u0646 \u062a\u06cc\u06a9 \u0648 \u0645\u062a\u0646 */\n"
"        font-size: 16px;  /* \u0627\u0646\u062f\u0627\u0632\u0647 \u0641\u0648\u0646\u062a */\n"
"        c"
                        "olor: #ffffff;  /* \u0631\u0646\u06af \u0645\u062a\u0646 */\n"
"    }\n"
"\n"
"    QCheckBox::indicator {\n"
"        width: 18px;  /* \u0639\u0631\u0636 \u0686\u06a9 \u0628\u0627\u06a9\u0633 */\n"
"        height: 18px;  /* \u0627\u0631\u062a\u0641\u0627\u0639 \u0686\u06a9 \u0628\u0627\u06a9\u0633 */\n"
"        border: 2px solid rgb(192, 197, 217);  /* \u062d\u0627\u0634\u06cc\u0647 \u0686\u06a9 \u0628\u0627\u06a9\u0633 */\n"
"        border-radius: 0px;  /* \u0634\u0639\u0627\u0639 \u06af\u0648\u0634\u0647 \u0686\u06a9 \u0628\u0627\u06a9\u0633 */\n"
"        background-color: transparent;  /* \u0631\u0646\u06af \u067e\u0633\u200c\u0632\u0645\u06cc\u0646\u0647 \u0686\u06a9 \u0628\u0627\u06a9\u0633 */\n"
"    }\n"
"\n"
"    QCheckBox::indicator:checked {\n"
"        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(39, 83, 237, 255), stop:0.516484 rgba(118, 22, 228, 255));  /* \u0631\u0646\u06af \u067e\u0633\u200c\u0632\u0645\u06cc\u0646\u0647 \u0686\u06a9 \u0628\u0627\u06a9\u0633"
                        " \u062f\u0631 \u062d\u0627\u0644\u062a \u062a\u06cc\u06a9 \u062e\u0648\u0631\u062f\u0647 */\n"
"        border: 2px solid rgb(192, 197, 217);  /* \u062d\u0627\u0634\u06cc\u0647 \u0686\u06a9 \u0628\u0627\u06a9\u0633 \u062f\u0631 \u062d\u0627\u0644\u062a \u062a\u06cc\u06a9 \u062e\u0648\u0631\u062f\u0647 */\n"
"\n"
"		background-image: url(:/icons/icons/check-wight-24.png);  /* \u0645\u0633\u06cc\u0631 \u0622\u06cc\u06a9\u0648\u0646 \u0686\u06a9 */\n"
"        background-repeat: no-repeat;  /* \u062c\u0644\u0648\u06af\u06cc\u0631\u06cc \u0627\u0632 \u062a\u06a9\u0631\u0627\u0631 \u0622\u06cc\u06a9\u0648\u0646 */\n"
"        background-position: center;  /* \u062a\u0631\u0627\u0632 \u06a9\u0631\u062f\u0646 \u0622\u06cc\u06a9\u0648\u0646 \u062f\u0631 \u0648\u0633\u0637 */\n"
"		border: 2px solid qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(39, 83, 237, 255), stop:0.516484 rgba(118, 22, 228, 255));\n"
"    }\n"
"\n"
"    QCheckBox::indicator:unchecked:hover {\n"
"        border: 2px solid rgb(99, "
                        "39, 232);  /* \u062d\u0627\u0634\u06cc\u0647 \u0686\u06a9 \u0628\u0627\u06a9\u0633 \u062f\u0631 \u062d\u0627\u0644\u062a \u063a\u06cc\u0631\u0641\u0639\u0627\u0644 \u0648 \u0647\u0646\u06af\u0627\u0645\u06cc \u06a9\u0647 \u0645\u0627\u0648\u0633 \u0631\u0648\u06cc \u0622\u0646 \u0627\u0633\u062a */\n"
"    }\n"
"\n"
"    QCheckBox::indicator:checked:hover {\n"
"          /* \u0631\u0646\u06af \u067e\u0633\u200c\u0632\u0645\u06cc\u0646\u0647 \u0686\u06a9 \u0628\u0627\u06a9\u0633 \u062f\u0631 \u062d\u0627\u0644\u062a \u062a\u06cc\u06a9 \u062e\u0648\u0631\u062f\u0647 \u0648 \u0645\u0627\u0648\u0633 \u0631\u0648\u06cc \u0622\u0646 \u0627\u0633\u062a */\n"
"    }\n"
"\n"
"/****************************************************************************/\n"
"/****************************************************************************/\n"
"\n"
"#playback_bottom_frame{\n"
"	\n"
"background-color: rgb(30, 27, 33);\n"
"}\n"
"\n"
"#playback_filter_frame{\n"
"background-color:rgb(49, 44, 53);\n"
"}")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.softeware_top_frame = QFrame(self.centralwidget)
        self.softeware_top_frame.setObjectName(u"softeware_top_frame")
        self.softeware_top_frame.setMaximumSize(QSize(16777215, 35))
        self.softeware_top_frame.setStyleSheet(u"\n"
"background-color: #262632")
        self.softeware_top_frame.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_22 = QHBoxLayout(self.softeware_top_frame)
        self.horizontalLayout_22.setSpacing(0)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.softeware_top_frame)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(120, 16777215))
        self.frame.setFrameShape(QFrame.NoFrame)

        self.horizontalLayout_22.addWidget(self.frame)

        self.label_32 = QLabel(self.softeware_top_frame)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setMinimumSize(QSize(0, 37))
        font = QFont()
        font.setFamilies([u"Mongolian Baiti"])
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        self.label_32.setFont(font)
        self.label_32.setStyleSheet(u"color: #f0f0f0;\n"
"font: 16pt ;")

        self.horizontalLayout_22.addWidget(self.label_32)

        self.frame_2 = QFrame(self.softeware_top_frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMaximumSize(QSize(120, 16777215))
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.minimize_btn = QPushButton(self.frame_2)
        self.minimize_btn.setObjectName(u"minimize_btn")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.minimize_btn.sizePolicy().hasHeightForWidth())
        self.minimize_btn.setSizePolicy(sizePolicy)
        self.minimize_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.minimize_btn.setStyleSheet(u"background-color:none;\n"
"border:none;")
        icon = QIcon()
        icon.addFile(u":/icons/icons/icons8-minimize-100 (1).png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.minimize_btn.setIcon(icon)
        self.minimize_btn.setIconSize(QSize(17, 17))

        self.horizontalLayout_2.addWidget(self.minimize_btn)

        self.maximize_btn = QPushButton(self.frame_2)
        self.maximize_btn.setObjectName(u"maximize_btn")
        sizePolicy.setHeightForWidth(self.maximize_btn.sizePolicy().hasHeightForWidth())
        self.maximize_btn.setSizePolicy(sizePolicy)
        self.maximize_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.maximize_btn.setStyleSheet(u"background-color:none;\n"
"border:none;")
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/icons8-maximize-100.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.maximize_btn.setIcon(icon1)
        self.maximize_btn.setIconSize(QSize(17, 17))

        self.horizontalLayout_2.addWidget(self.maximize_btn)

        self.close_btn = QPushButton(self.frame_2)
        self.close_btn.setObjectName(u"close_btn")
        self.close_btn.setEnabled(False)
        sizePolicy.setHeightForWidth(self.close_btn.sizePolicy().hasHeightForWidth())
        self.close_btn.setSizePolicy(sizePolicy)
        self.close_btn.setCursor(QCursor(Qt.CursorShape.ForbiddenCursor))
        self.close_btn.setStyleSheet(u"border:none;")
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/icons8-close-80.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.close_btn.setIcon(icon2)
        self.close_btn.setIconSize(QSize(18, 18))

        self.horizontalLayout_2.addWidget(self.close_btn)


        self.horizontalLayout_22.addWidget(self.frame_2)


        self.verticalLayout.addWidget(self.softeware_top_frame)

        self.line_9 = QFrame(self.centralwidget)
        self.line_9.setObjectName(u"line_9")
        self.line_9.setMinimumSize(QSize(0, 1))
        self.line_9.setMaximumSize(QSize(16777215, 1))
        self.line_9.setStyleSheet(u"background-color: rgb(175, 175, 175);")
        self.line_9.setFrameShape(QFrame.Shape.VLine)
        self.line_9.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_9)

        self.middle = QFrame(self.centralwidget)
        self.middle.setObjectName(u"middle")
        self.middle.setMaximumSize(QSize(16777215, 16777215))
        self.middle.setStyleSheet(u"")
        self.middle.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_27 = QHBoxLayout(self.middle)
        self.horizontalLayout_27.setSpacing(0)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_27.setContentsMargins(0, 0, 0, 0)
        self.toggle_frame = QFrame(self.middle)
        self.toggle_frame.setObjectName(u"toggle_frame")
        self.toggle_frame.setMinimumSize(QSize(130, 0))
        self.toggle_frame.setMaximumSize(QSize(130, 16777215))
        self.toggle_frame.setStyleSheet(u"QFrame{\n"
"	background: #413B47;\n"
"	padding:0px;\n"
"\n"
"}\n"
"\n"
"\n"
"QPushButton{\n"
"	color: #fff;\n"
"	background-color:transparent;\n"
"	padding: 0px;\n"
"	font-size: 10pt;\n"
"	font-weight: normal;\n"
"	border-radius:0px;\n"
"	min-width:120px;\n"
"	text-align: left; \n"
"	padding-left:10px;\n"
"}\n"
"\n"
"QPushButton::icon {\n"
"        subcontrol-position: left center;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background: #D43D41;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    color: #8D8D8D;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background: rgb(0, 0, 0);\n"
"}")
        self.toggle_frame.setFrameShape(QFrame.NoFrame)
        self.toggle_frame.setLineWidth(3)
        self.verticalLayout_36 = QVBoxLayout(self.toggle_frame)
        self.verticalLayout_36.setSpacing(0)
        self.verticalLayout_36.setObjectName(u"verticalLayout_36")
        self.verticalLayout_36.setContentsMargins(0, 0, 0, 0)
        self.frame_7 = QFrame(self.toggle_frame)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(0, 82))
        self.frame_7.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_2 = QVBoxLayout(self.frame_7)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.side_menu_frame = QFrame(self.frame_7)
        self.side_menu_frame.setObjectName(u"side_menu_frame")
        self.side_menu_frame.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_20 = QVBoxLayout(self.side_menu_frame)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.verticalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.btn_side_playback = QPushButton(self.side_menu_frame)
        self.btn_side_playback.setObjectName(u"btn_side_playback")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_side_playback.sizePolicy().hasHeightForWidth())
        self.btn_side_playback.setSizePolicy(sizePolicy1)
        self.btn_side_playback.setMinimumSize(QSize(130, 50))
        self.btn_side_playback.setMaximumSize(QSize(120, 50))
        self.btn_side_playback.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_side_playback.setStyleSheet(u"\n"
"    icon: url(:/icons/icons/playback-white.png);\n"
"")
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/icons8-playback-24.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_side_playback.setIcon(icon3)
        self.btn_side_playback.setIconSize(QSize(28, 28))

        self.verticalLayout_20.addWidget(self.btn_side_playback)

        self.btn_side_settings = QPushButton(self.side_menu_frame)
        self.btn_side_settings.setObjectName(u"btn_side_settings")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.btn_side_settings.sizePolicy().hasHeightForWidth())
        self.btn_side_settings.setSizePolicy(sizePolicy2)
        self.btn_side_settings.setMinimumSize(QSize(130, 50))
        self.btn_side_settings.setMaximumSize(QSize(120, 50))
        self.btn_side_settings.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_side_settings.setStyleSheet(u"icon: url(:/icons/icons/setting-white.png);\n"
"")
        icon4 = QIcon()
        icon4.addFile(u":/icons/icons/icons8-settings-80.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_side_settings.setIcon(icon4)
        self.btn_side_settings.setIconSize(QSize(28, 28))

        self.verticalLayout_20.addWidget(self.btn_side_settings)


        self.verticalLayout_2.addWidget(self.side_menu_frame, 0, Qt.AlignTop)


        self.verticalLayout_36.addWidget(self.frame_7)

        self.label_5 = QLabel(self.toggle_frame)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(80, 80))
        self.label_5.setPixmap(QPixmap(u":/icons/icons/rahahan-logo.png"))
        self.label_5.setScaledContents(True)

        self.verticalLayout_36.addWidget(self.label_5, 0, Qt.AlignHCenter)

        self.label_2 = QLabel(self.toggle_frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(80, 70))
        self.label_2.setTextFormat(Qt.PlainText)
        self.label_2.setPixmap(QPixmap(u":/icons/icons/logo_aryan.png"))
        self.label_2.setScaledContents(True)

        self.verticalLayout_36.addWidget(self.label_2, 0, Qt.AlignHCenter)

        self.verticalSpacer_3 = QSpacerItem(20, 97, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_36.addItem(self.verticalSpacer_3)


        self.horizontalLayout_27.addWidget(self.toggle_frame)

        self.line_3 = QFrame(self.middle)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setMinimumSize(QSize(0, 0))
        self.line_3.setMaximumSize(QSize(1, 16777215))
        self.line_3.setStyleSheet(u"background-color: rgb(175, 175, 175);")
        self.line_3.setFrameShape(QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_27.addWidget(self.line_3)

        self.main_frame = QFrame(self.middle)
        self.main_frame.setObjectName(u"main_frame")
        self.main_frame.setMinimumSize(QSize(1, 1))
        self.main_frame.setMaximumSize(QSize(16777215, 16777215))
        self.main_frame.setStyleSheet(u"")
        self.main_frame.setFrameShape(QFrame.NoFrame)
        self.main_frame.setLineWidth(0)
        self.verticalLayout_3 = QVBoxLayout(self.main_frame)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.pages_stackwidget = QStackedWidget(self.main_frame)
        self.pages_stackwidget.setObjectName(u"pages_stackwidget")
        self.pages_stackwidget.setStyleSheet(u"")
        self.pages_stackwidget.setFrameShape(QFrame.NoFrame)
        self.pages_stackwidget.setLineWidth(2)
        self.page_playback = QWidget()
        self.page_playback.setObjectName(u"page_playback")
        self.page_playback.setStyleSheet(u"")
        self.verticalLayout_9 = QVBoxLayout(self.page_playback)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, -1, -1, -1)
        self.frame_18 = QFrame(self.page_playback)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setMinimumSize(QSize(0, 60))
        self.frame_18.setStyleSheet(u"")
        self.frame_18.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_18)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.line_5 = QFrame(self.frame_18)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setMaximumSize(QSize(2, 16777215))
        self.line_5.setStyleSheet(u"background-color: rgb(175, 175, 175);")
        self.line_5.setFrameShape(QFrame.Shape.VLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_12.addWidget(self.line_5)

        self.frame_4 = QFrame(self.frame_18)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setStyleSheet(u"background: #413B47;")
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setLineWidth(6)
        self.verticalLayout_15 = QVBoxLayout(self.frame_4)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.lbl_camera_1 = QLabel(self.frame_4)
        self.lbl_camera_1.setObjectName(u"lbl_camera_1")
        self.lbl_camera_1.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.lbl_camera_1.setScaledContents(True)

        self.gridLayout_3.addWidget(self.lbl_camera_1, 0, 0, 1, 1, Qt.AlignHCenter)

        self.lbl_camera_4 = QLabel(self.frame_4)
        self.lbl_camera_4.setObjectName(u"lbl_camera_4")
        self.lbl_camera_4.setScaledContents(True)

        self.gridLayout_3.addWidget(self.lbl_camera_4, 2, 2, 1, 1, Qt.AlignHCenter)

        self.line = QFrame(self.frame_4)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_3.addWidget(self.line, 1, 0, 1, 1)

        self.lbl_camera_3 = QLabel(self.frame_4)
        self.lbl_camera_3.setObjectName(u"lbl_camera_3")
        self.lbl_camera_3.setScaledContents(True)

        self.gridLayout_3.addWidget(self.lbl_camera_3, 2, 0, 1, 1, Qt.AlignHCenter)

        self.lbl_camera_2 = QLabel(self.frame_4)
        self.lbl_camera_2.setObjectName(u"lbl_camera_2")
        self.lbl_camera_2.setScaledContents(True)

        self.gridLayout_3.addWidget(self.lbl_camera_2, 0, 2, 1, 1, Qt.AlignHCenter)

        self.line_2 = QFrame(self.frame_4)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_3.addWidget(self.line_2, 1, 2, 1, 1)

        self.line_4 = QFrame(self.frame_4)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.VLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_3.addWidget(self.line_4, 0, 1, 1, 1)

        self.line_6 = QFrame(self.frame_4)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.Shape.VLine)
        self.line_6.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_3.addWidget(self.line_6, 2, 1, 1, 1)


        self.verticalLayout_15.addLayout(self.gridLayout_3)


        self.horizontalLayout_12.addWidget(self.frame_4)

        self.line_14 = QFrame(self.frame_18)
        self.line_14.setObjectName(u"line_14")
        self.line_14.setMaximumSize(QSize(1, 16777215))
        self.line_14.setStyleSheet(u"background-color: rgb(175, 175, 175);")
        self.line_14.setFrameShape(QFrame.Shape.VLine)
        self.line_14.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_12.addWidget(self.line_14)


        self.horizontalLayout.addWidget(self.frame_18)


        self.verticalLayout_9.addLayout(self.horizontalLayout)

        self.playback_bottom_frame = QFrame(self.page_playback)
        self.playback_bottom_frame.setObjectName(u"playback_bottom_frame")
        self.playback_bottom_frame.setMinimumSize(QSize(0, 100))
        self.playback_bottom_frame.setMaximumSize(QSize(16777215, 100))
        self.playback_bottom_frame.setStyleSheet(u"")
        self.playback_bottom_frame.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_4 = QHBoxLayout(self.playback_bottom_frame)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 42, 0)
        self.frame_3 = QFrame(self.playback_bottom_frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_8 = QLabel(self.frame_3)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_3.addWidget(self.label_8)

        self.lbl_status = QLabel(self.frame_3)
        self.lbl_status.setObjectName(u"lbl_status")
        font1 = QFont()
        font1.setPointSize(32)
        font1.setBold(False)
        font1.setItalic(False)
        self.lbl_status.setFont(font1)
        self.lbl_status.setStyleSheet(u"color: rgb(0, 255, 0);\n"
"font: 32pt;")

        self.horizontalLayout_3.addWidget(self.lbl_status)


        self.horizontalLayout_4.addWidget(self.frame_3, 0, Qt.AlignLeft)

        self.frame_6 = QFrame(self.playback_bottom_frame)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.btn_show_live = QPushButton(self.frame_6)
        self.btn_show_live.setObjectName(u"btn_show_live")
        self.btn_show_live.setMinimumSize(QSize(0, 50))
        self.btn_show_live.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_show_live.setStyleSheet(u"QPushButton {\n"
"    background-color: #2E2A3D; /* Background color similar to top bar */\n"
"    color: white;\n"
"    font-size: 14px;\n"
"    padding: 0px 20px;\n"
"    border-radius: 5px;\n"
"    border: 1px solid #D43D41; /* Red border */\n"
"\n"
"    icon: url(:/icons/icons/icons8-video-100.png);\n"
"\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #D43D41; /* Red hover color */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #1F1B2C; /* Darker version of the top bar color on press */\n"
"}\n"
"QPushButton:disabled {\n"
"\n"
"	background-color: rgb(118, 118, 118);\n"
"	color: rgb(59, 59, 59);\n"
"}\n"
"")

        self.horizontalLayout_5.addWidget(self.btn_show_live)


        self.horizontalLayout_4.addWidget(self.frame_6)


        self.verticalLayout_9.addWidget(self.playback_bottom_frame)

        self.pages_stackwidget.addWidget(self.page_playback)
        self.page_settings = QWidget()
        self.page_settings.setObjectName(u"page_settings")
        self.page_settings.setStyleSheet(u"")
        self.verticalLayout_4 = QVBoxLayout(self.page_settings)
        self.verticalLayout_4.setSpacing(3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, -1)
        self.frame_5 = QFrame(self.page_settings)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setStyleSheet(u"background: #413B47;")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.frame_8 = QFrame(self.frame_5)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label = QLabel(self.frame_8)
        self.label.setObjectName(u"label")

        self.horizontalLayout_6.addWidget(self.label)

        self.spinBox = QSpinBox(self.frame_8)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimum(5)
        self.spinBox.setMaximum(120)

        self.horizontalLayout_6.addWidget(self.spinBox)

        self.label_3 = QLabel(self.frame_8)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_6.addWidget(self.label_3)


        self.verticalLayout_5.addWidget(self.frame_8, 0, Qt.AlignLeft|Qt.AlignTop)


        self.verticalLayout_4.addWidget(self.frame_5)

        self.pages_stackwidget.addWidget(self.page_settings)

        self.verticalLayout_3.addWidget(self.pages_stackwidget)


        self.horizontalLayout_27.addWidget(self.main_frame)


        self.verticalLayout.addWidget(self.middle)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)

        self.pages_stackwidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"IRAN RailWay Monitor Software - Arian Shabake", None))
        self.minimize_btn.setText("")
        self.maximize_btn.setText("")
        self.close_btn.setText("")
#if QT_CONFIG(tooltip)
        self.btn_side_playback.setToolTip(QCoreApplication.translate("MainWindow", u"Live View", None))
#endif // QT_CONFIG(tooltip)
        self.btn_side_playback.setText(QCoreApplication.translate("MainWindow", u"   Live", None))
#if QT_CONFIG(tooltip)
        self.btn_side_settings.setToolTip(QCoreApplication.translate("MainWindow", u"Defect Parameters", None))
#endif // QT_CONFIG(tooltip)
        self.btn_side_settings.setText(QCoreApplication.translate("MainWindow", u"   Settings", None))
        self.label_5.setText("")
        self.label_2.setText("")
#if QT_CONFIG(tooltip)
        self.pages_stackwidget.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lbl_camera_1.setText(QCoreApplication.translate("MainWindow", u"Camera 1", None))
        self.lbl_camera_4.setText(QCoreApplication.translate("MainWindow", u"Camera 4", None))
        self.lbl_camera_3.setText(QCoreApplication.translate("MainWindow", u"Camera 3", None))
        self.lbl_camera_2.setText(QCoreApplication.translate("MainWindow", u"Camera 2", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Status : ", None))
        self.lbl_status.setText(QCoreApplication.translate("MainWindow", u"INITIALIZING", None))
        self.btn_show_live.setText(QCoreApplication.translate("MainWindow", u"Show Live ", None))
        self.page_settings.setProperty(u"styleClass", QCoreApplication.translate("MainWindow", u"page", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Live Time", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Second", None))
    # retranslateUi


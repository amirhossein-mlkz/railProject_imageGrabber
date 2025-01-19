import time
import datetime

import re
import cv2
#from persiantools.jdatetime import JalaliDateTime, JalaliDate
from datetime import datetime, date

from PySide6.QtWidgets import QApplication, QToolButton
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QComboBox, QGridLayout, QLabel, QDialog,QDialogButtonBox,QPushButton

from uiUtils.guiBackend import GUIBackend
from UIFiles.calendar import Ui_CalendarDialog
from PySide6.QtCore import QDate
from PySide6 import QtCore as sQtCore

from persiantools.jdatetime import JalaliDateTime, timedelta
from persiantools import jdatetime
import jdatetime





DAY_BUTTON_STYLE = """QPushButton {

    background-color:transparent;
    color: #EAE4F5;
    width:16px;
    height:16px;


    }
    """





DAY_BUTTON_EXIST_STYLE ="""QPushButton{
    max-width:20px;
    max-height:20px;
    min-width:20px;
    min-height:20px;
    border-radius:12px;
    font-weight:bold;
    color:#fff;
    padding:2px;
    background-color: rgb(99, 39, 232);
}

QPushButton:hover{
    max-width:24px;
    max-height:24px;
    min-width:24px;
    min-height:24px;
}
"""




DAY_BUTTON_SELECTED_STYLE ="""
QPushButton {
    background-color: #2b8c67;
    max-width:20px;
    max-height:20px;
    min-width:20px;
    min-height:20px;
    border-radius:12px;
    font-weight:bold;
    color:#fff;
    padding:2px;
}

"""





MAIN_STYLE = """
QComboBox {
    background-color: #3b4252;
	background-color: rgb(180, 180, 180);
    border: 1px solid #4c566a;
    border-radius: 5px;
    padding: 6px 10px;

	color: rgb(0, 0, 0);
}

QComboBox:hover {
    border: 1px solid #5e81ac;
}

QComboBox::drop-down {
    border: none;
}

QComboBox::down-arrow {
    image: url(:/icons/icons/icons8-drop-down-80.png);

    width: 12px;
    height: 12px;
}

QDialogButtonBox{
color:red;
}







QComboBox {
    background-color: #3b4252;
	background-color: rgb(180, 180, 180);
    border: 1px solid #4c566a;
    border-radius: 5px;
    padding: 6px 10px;

	color: rgb(0, 0, 0);
}

QComboBox:hover {
    border: 1px solid #5e81ac;
}

QComboBox::drop-down {
    border: none;
}

QComboBox::down-arrow {
    image: url(:/icons/icons/icons8-drop-down-80.png);

    width: 12px;
    height: 12px;
}


QPushButton{
	color: black;
    background-color:#0C356A;
	padding: 5px;
	font-size:12px;
	font-weight: bold;
	border-radius:7px;
	background-color: rgb(0, 17, 255);

}

QPushButton:hover{
	background-color: rgb(18, 3, 104);
}

QPushButton:disabled {
    color: #8D8D8D;
}

QPushButton:pressed {
	background: rgb(0, 0, 0);
}







"""

        



class JalaliCalendarDialog(QWidget):
   
    def __init__(self, input_field: QtWidgets, date=None,maimumwidth:int = 300,maximumheight:int = 180):
        super().__init__()

        self.setWindowTitle("Jalali Calendar Dialog")


        flags = sQtCore.Qt.WindowFlags(
            sQtCore.Qt.FramelessWindowHint
        )  # remove the windows frame of ui
        self.pos_ = self.pos()
        self.setWindowFlags(flags)
        self._old_pos = None

        self.selected_day = None
        self.input_field = input_field
        self.avaiable_dates = []
        self.path_selected_date = None
        self.parent_func = None
        self.external_calender_event_func = None

        # if date is None:
            # date = JalaliDateTime.now()
        


        self.date:datetime = date
        self.select_day_btn = None

        # Set up the layout
        layout = QVBoxLayout()


        self.yearCombo = QComboBox()
        self.monthCombo = QComboBox()

        # Add years to the year combo box
        current_jalali_year = JalaliDateTime.now().year
        for year in range(current_jalali_year, current_jalali_year-10, -1):
            self.yearCombo.addItem(str(year))

        # Add months to the month combo box
        jalali_months = [
            "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
            "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
        ]
        for month in jalali_months:
            self.monthCombo.addItem(month)

        self.yearCombo.setCurrentText(str(current_jalali_year))
        self.monthCombo.setCurrentIndex(JalaliDateTime.now().month - 1)

        self.yearCombo.currentTextChanged.connect(self.updateCalendar)
        self.monthCombo.currentIndexChanged.connect(self.updateCalendar)

        self.calendarGrid = QGridLayout()
        self.selected_button = None
        self.updateCalendar()

        layout.addWidget(self.yearCombo)
        layout.addWidget(self.monthCombo)

        calendar_widget = QWidget()
        calendar_widget.setLayout(self.calendarGrid)
        layout.addWidget(calendar_widget)

        # Add buttons
        # buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        # buttonBox.accepted.connect(self.selected_date)
        # buttonBox.rejected.connect(self.reject)
        # layout.addWidget(buttonBox)

        self.setLayout(layout)
        self.setStyleSheet(MAIN_STYLE)

        self.__set_date_into_field()
        # self.show()

        calendar_widget.setMaximumWidth(maimumwidth)
        calendar_widget.setMaximumHeight(maximumheight)
        calendar_widget.setMinimumWidth(maimumwidth)
        calendar_widget.setMinimumHeight(maximumheight)



        self.yearCombo.setMaximumWidth(maimumwidth-20)
        self.yearCombo.setMinimumWidth(maimumwidth-20)
        self.monthCombo.setMinimumWidth(maimumwidth-20)
        self.monthCombo.setMaximumWidth(maimumwidth-20)



    def reject(self):
        self.close()

    def updateCalendar(self):
        self.path_selected_date = None
        # Clear previous widgets in the calendar grid
        while self.calendarGrid.count():
            item = self.calendarGrid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        year = int(self.yearCombo.currentText())
        month = self.monthCombo.currentIndex() + 1

        first_day_of_month = JalaliDateTime(year, month, 1)
        first_day_of_week = first_day_of_month.weekday()

        days_in_month = self.days_in_jalali_month(year, month)

        self.btns_status = []
        

        day = 1
        for week in range(6):
            for weekday in range(7):
                if week == 0 and weekday < first_day_of_week:
                    label = QLabel("")
                    self.calendarGrid.addWidget(label, week, weekday)
                elif day > days_in_month:
                    label = QLabel("")
                    self.calendarGrid.addWidget(label, week, weekday)
                else:
                    day_btn = QPushButton(str(day))
                    date_of_btn = JalaliDateTime(year=year, month=month, day=day).jdate()
                    GUIBackend.button_connector_argument_pass(day_btn, self.date_click, args=(date_of_btn, day_btn))

                    if date_of_btn in self.avaiable_dates:
                        GUIBackend.set_style(day_btn, DAY_BUTTON_EXIST_STYLE)
                    else:
                        GUIBackend.set_style(day_btn, DAY_BUTTON_STYLE)
                        day_btn.setDisabled(True)
                    
                    if self.date:
                        if date_of_btn == self.date:
                            GUIBackend.set_style(day_btn, DAY_BUTTON_SELECTED_STYLE)


                    self.calendarGrid.addWidget(day_btn, week, weekday)
                    day += 1
                    continue
                    ############################################

    def set_calender_event(self, func):
        self.external_calender_event_func = func

    def date_click(self, date, btn):
        if self.select_day_btn :
            try:
                GUIBackend.set_style(self.select_day_btn , DAY_BUTTON_EXIST_STYLE)
            except:
                pass
        
        self.date = date
        self.select_day_btn = btn
        GUIBackend.set_style(self.select_day_btn , DAY_BUTTON_SELECTED_STYLE)
        self.__set_date_into_field()
        self.external_calender_event_func(date)
    
    def set_date(self, date):
        self.date = date
        self.updateCalendar()
        self.__set_date_into_field()

    @staticmethod
    def days_in_jalali_month(year, month):
        if month <= 6:
            return 31
        elif month <= 11:
            return 30
        else:
            # Check for leap year
            return 30 if JalaliDateTime.is_leap(year) else 29


    def select_day(self):
        try:
            if self.selected_button:
                day = int(self.selected_button.text())
                if self.btns_status[day-1]:
                    GUIBackend.set_style(self.selected_button, DAY_BUTTON_EXIST_STYLE)
                else:
                    GUIBackend.set_style(self.selected_button, DAY_BUTTON_STYLE)



        except RuntimeError as e:
            print("Button has been deleted.")


        self.selected_button = self.sender()
        self.selected_day = int(self.selected_button.text())
        GUIBackend.set_style(self.selected_button, DAY_BUTTON_EXIST_STYLE)



    




    
    def __set_date_into_field(self,):
        if self.date:
            str_date = self.date.strftime("%Y/%m/%d")
            self.str_date = str_date
            self.input_field.setText(str_date)

            if self.parent_func is not None:
                self.parent_func(self.date)
        else:
            self.input_field.setText('-')

        # GUIBackend.set_input(self.input_field, str_date)



    def set_input_field(self,input_field:QtWidgets):

        self.input_field = input_field



    def set_avaiable_date_ranges(self, avaiable_dates:list[ JalaliDateTime]):
        self.avaiable_dates = avaiable_dates
        self.date = None
        self.updateCalendar()

            







    def set_parent_function(self,func):
        self.parent_func = func






if __name__ == "__main__":

    from PySide6.QtWidgets import QApplication as sQApplication

    app = sQApplication()
    win = JalaliCalendarDialog()

    win.show()

    import sys
    sys.exit(app.exec())
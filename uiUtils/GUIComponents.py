from PySide6.QtWidgets import QWidget, QFrame, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy,QPushButton, QMessageBox,QCheckBox, QSpinBox
from PySide6.QtWidgets import QSlider, QProgressBar
from PySide6.QtCore import QTimer, Qt, Signal, QRect, QLine, QPoint
from PySide6.QtGui import QPixmap, QIcon, QColor, QPen, QPainter, QPalette
from persiantools.jdatetime import JalaliDateTime, timedelta

TABEL_BUTTON_STYLE = """
    QPushButton{ 
        background-color: transparent;
        border: none;
        min-height:0px; min-width:0px; 
        width:auto;
        qproperty-iconSize: 24px;
        } 
    """


CONFIRMBOX_STYLESHEET = """
   QMessageBox{ 
        background-color: #ffffff;

    }
    
    QPushButton{
        border: none;
        font-weight: bold;
        color: #ffffff;
        background-color:rgb(6, 76, 130);
        min-height: 25px;
        border-radius: 5px;
        min-width:100px;
        font-size:12px;
	
        }

    QPushButton:hover{
	    background-color:rgb(22, 38, 76);
    }
"""

class MessageWidget(QWidget):
    # Constants for border colors
    SUCCESS_COLOR = "#00CB51"  # Green
    ERROR_COLOR = "#ff4444"    # Red
    INFO_COLOR = "#33B5E5"     # Blue
    BORDER_RADIUS = "10px"     # Border radius for the frame

    def __init__(self, parent=None):
        super().__init__(parent)

        # Main frame for the message
        self.frame = QFrame(self)
        # self.frame.setFixedHeight(80)
        # self.frame.setFixedWidth(280)

        # Set a unique object name (ID) for the frame to target it in the stylesheet
        self.frame.setObjectName("messageFrame")
        # Set border-radius and transparency for the frame
        self.frame.setStyleSheet(f"#{self.frame.objectName()} {{ border-radius: {self.BORDER_RADIUS}; background: transparent; }}")

        # Horizontal layout for icon and message text
        self.layout = QHBoxLayout(self.frame)

        # Icon label for message type
        self.icon_label = QLabel(self)
        self.icon_label.setFixedSize(30, 30)
        self.icon_label.setScaledContents(True)
        # Make icon label transparent
        self.icon_label.setStyleSheet("background: transparent;")

        # Text label for the message
        self.text_label = QLabel(self)
        self.text_label.setWordWrap(True)
        self.text_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # Align text to the left and vertically centered
        # Make text label transparent
        self.text_label.setStyleSheet("background: transparent;")

        # Adding widgets to the layout (icon and text label without spacer)
        self.layout.addWidget(self.icon_label)
        self.layout.addWidget(self.text_label)

        # Main layout for the widget
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.frame)
        self.setLayout(main_layout)

        # Timer to hide the widget after a certain period
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.hide)

    def show_message(self, message: str, msg_type="info", display_time=3000):
        """
        Shows the message widget with the specified message and type.

        :param message: The message to display.
        :param msg_type: The type of the message ("success", "error", "info").
        :param display_time: The time in milliseconds to display the message before hiding it.
        """
        if not message:
            self.hide()
            return

        # Set message text
        self.text_label.setText(message)

        # Set the corresponding icon and border color based on message type
        if msg_type == "success":
            self.icon_label.setPixmap(QPixmap(":/icons/icons/success.png"))  # Use success icon from resources
            self.frame.setStyleSheet(f"#{self.frame.objectName()} {{ border: 2px solid {self.SUCCESS_COLOR}; border-radius: {self.BORDER_RADIUS}; background: transparent; }}")
        elif msg_type == "error":
            self.icon_label.setPixmap(QPixmap(":/icons/icons/error.png"))  # Use error icon from resources
            self.frame.setStyleSheet(f"#{self.frame.objectName()} {{ border: 2px solid {self.ERROR_COLOR}; border-radius: {self.BORDER_RADIUS}; background: transparent; }}")
        else:  # Default is "info"
            self.icon_label.setPixmap(QPixmap(":/icons/icons/info.png"))  # Use info icon from resources
            self.frame.setStyleSheet(f"#{self.frame.objectName()} {{ border: 2px solid {self.INFO_COLOR}; border-radius: {self.BORDER_RADIUS}; background: transparent; }}")

        # Show the widget
        self.show()
        if display_time>0:
            # Start the timer to hide the message after 'display_time' milliseconds
            self.timer.start(display_time)

    def hide(self):
        """
        Hides the message widget.
        """
        self.timer.stop()  # Stop the timer if it's running
        super().hide()     # Call the parent class's hide method



    



class deleteButton(QPushButton):

    def __init__(self, *a, **kw):
        super(deleteButton, self).__init__(*a, **kw)
        self._icon_normal = QIcon(':/icons/icons/icons8-remove-table-50.png')
        self._icon_over = QIcon(':/icons/icons/icons8-remove-hover-table-50.png')
        self.setStyleSheet(TABEL_BUTTON_STYLE)
        self.setIcon(self._icon_normal)

    def enterEvent(self, event):
        self.setIcon(self._icon_over)
        #return super(deleteButton, self).enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(self._icon_normal)
        #return super(deleteButton, self).enterEvent(event)


class editButton(QPushButton):

    def __init__(self, *a, **kw):
        super(editButton, self).__init__(*a, **kw)
        self._icon_normal = QIcon(':/icons/icons/icons8-edit-table-50.png')
        self._icon_over = QIcon(':/icons/icons/icons8-edit-hover-table-50.png')
        self.setStyleSheet(TABEL_BUTTON_STYLE)
        self.setIcon(self._icon_normal)

    def enterEvent(self, event):
        self.setIcon(self._icon_over)
        #return super(editButton, self).enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(self._icon_normal)
        #return super(editButton, self).enterEvent(event)




class confirmMessageBox:
    def __init__(self, title, text, buttons, min_height=300, min_width=400, parent=None ):
        self.STANDARD_BUTTONS = {
            'yes': QMessageBox.Yes,
            'no': QMessageBox.No,
            'cancel': QMessageBox.Cancel,
            'save': QMessageBox.Save,
            'ok': QMessageBox.Ok,
            'ignore': QMessageBox.Ignore,
            

        }

        self.icon = QIcon(':/assets/icons/icons8-question-blue-50.png')
        self.buttons = buttons

        text = text + " " * 100 + "\n"

        self.msg = QMessageBox( text=text, parent=parent)
        self.msg.setWindowTitle(title)
        self.msg.setStyleSheet(CONFIRMBOX_STYLESHEET)
        self.msg.setWindowIcon(self.icon)
        #self.msg.setMinimumHeight(min_height)
        #self.msg.setStyleSheet("QLabel{ min-width:" + str(min_width) + " px; }" )
        #self.msg.setMinimumWidth(min_width)

        
        #---------------------------------------------------
        selected_buttons_obj = []
        for btn_name in buttons:
            btn = self.STANDARD_BUTTONS[btn_name]
            if isinstance(selected_buttons_obj, list):
                selected_buttons_obj = btn
            else:
                selected_buttons_obj = selected_buttons_obj | btn
        self.msg.setStandardButtons(selected_buttons_obj)
        #---------------------------------------------------

    def render(self) -> str:
        retval = self.msg.exec_()
        for btn_name in self.buttons:
            if self.STANDARD_BUTTONS[btn_name] == retval:
                return btn_name
            



class tabelCheckbox(QCheckBox):

    def __init__(self, *a, **kw):
        super(tabelCheckbox, self).__init__(*a, **kw)
        

    def set_size(self, w, h):
        self.setStyleSheet(f"""QCheckBox::indicator 
                                {{
                                    
                               width :{w}px;
                               height :{h}px;
                               }}
                            
                            QCheckBox::indicator:checked
                                {{
                               width :{w+4}px;
                               height :{h+4}px;
                               }}

                               """ )

        #self.setMaximumWidth(h+5)
        #self.setMaximumWidth(w+5)

class timeSpinBox(QSpinBox):
    def textFromValue(self, value):
        # این تابع اعداد را همیشه با دو رقم نمایش می‌دهد
        return f"{value:02d}"  # دو رقم با پر کردن صفر



class timeLineSlider(QSlider):
    timeSelected = Signal(JalaliDateTime)  # Signal to emit selected time

    def __init__(self, start_time, end_time, active_color=(90, 150, 100), deactive_color=(100,100,100), time_label=None, parent=None):
        super().__init__(Qt.Horizontal, parent)
        
        self.time_label = time_label
        self.active_color = active_color
        self.deactive_color = deactive_color
        self.green_sections = []
        self.dragging = False  # Track if dragging is happening
        self.sliderMoved.connect(self.update_time_from_slider)
        self.valueChanged.connect(self.update_time_from_slider)

    
    def set_min_max(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

        diff: timedelta = self.end_time - self.start_time
        self.duration = diff.total_seconds()
        
        self.setMinimum(0)
        self.setMaximum(self.duration)  # Set the slider's range based on the duration

        

    def set_avaiable_segments(self, green_sections):
        """Set sections that should be green, and redraw the slider."""
        self.green_sections = green_sections
        self.update()  # Force the slider to repaint

    def update_time_from_slider(self):
        """Update the time label when the slider is moved."""
        slider_value = self.value()
        time_fraction = slider_value / self.maximum()
        current_time = self.start_time + timedelta(seconds=self.duration * time_fraction)
        if self.time_label:
            self.time_label.setText(current_time.strftime("%H:%M:%S"))

    def set_time_by_jdatetime(self, time):
        """Set the slider's position based on a given JalaliDateTime time."""
        time_offset = (time - self.start_time).total_seconds()
        slider_value = int((time_offset / self.duration) * self.maximum())
        self.setValue(slider_value)

    def is_in_green_section(self, time):
        """Check if the given time falls within one of the green sections."""
        for start, end in self.green_sections:
            if start <= time <= end:
                return True
        return False

    def mousePressEvent(self, event):
        """Handle mouse press event to ensure only green sections are clickable."""
        if event.button() == Qt.LeftButton:
            slider_value = event.position().x() / self.width() * self.maximum()
            time_fraction = slider_value / self.maximum()
            clicked_time = self.start_time + timedelta(seconds=self.duration * time_fraction)

            # If clicked time is in a green section, allow moving the slider
            if self.is_in_green_section(clicked_time):
                self.setValue(int(slider_value))
                self.timeSelected.emit(clicked_time)  # Emit the clicked time as a signal
                self.update_time_from_slider()
                self.dragging = True  # Enable dragging after clicking on a green section

    def mouseMoveEvent(self, event):
        """Allow dragging the slider while the mouse is held down, but only in green sections."""
        if self.dragging:
            slider_value = event.position().x() / self.width() * self.maximum()
            time_fraction = slider_value / self.maximum()
            current_time = self.start_time + timedelta(seconds=self.duration * time_fraction)

            # Only allow movement in green sections
            if self.is_in_green_section(current_time):
                self.setValue(int(slider_value))
                self.update_time_from_slider()

    def mouseReleaseEvent(self, event):
        """Stop dragging when the mouse is released."""
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def paintEvent(self, event):
        """Custom paint to show green and red sections and handle the slider handle design."""
        painter = QPainter(self)
        slider_width = self.width()
        groove_rect = QRect(0, (self.height() - 20) // 2, slider_width, 20)  # Create the groove rectangle
        groove_height = groove_rect.height()

        # Paint red background for the whole slider
        painter.setBrush(QColor(*self.deactive_color))
        painter.drawRect(groove_rect)

        # Paint green sections
        for start, end in self.green_sections:
            start_fraction = (start - self.start_time).total_seconds() / self.duration
            end_fraction = (end - self.start_time).total_seconds() / self.duration

            start_x = int(slider_width * start_fraction)
            end_x = int(slider_width * end_fraction)

            green_rect = QRect(start_x, (self.height() - groove_height) // 2, end_x - start_x, groove_height)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(*self.active_color))
            painter.drawRect(green_rect)

        # Custom handle (pointer)
        handle_pos = self.value() / self.maximum() * slider_width
        # handle_size = 10
        handle_size = int(groove_height * 0.6)

        handle_line = QLine(handle_pos, (self.height() - groove_height) // 2, handle_pos, groove_height)
        painter.setPen(QPen(QColor(Qt.black), 2))
        painter.drawLine(handle_line)

        handle_rect = QRect(int(handle_pos - handle_size / 2), (self.height() - handle_size) // 2, handle_size, handle_size)

        painter.setBrush(QColor(Qt.white))
        painter.setPen(QPen(QColor(50,50,50), 1))
        painter.drawEllipse(handle_rect)







class trainLoading(QWidget):
    def __init__(self,min, max, parent=None):
        
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # No window title or border, always on top

        self.setAttribute(Qt.WA_TranslucentBackground)  # Transparent background

        # Set window size and initial position
        self.setFixedSize(500, 100)

        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setRange(min, max)
        self.progress_bar.setFixedHeight(10)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: rgba(200, 200, 200, 150);
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: #3b5998;
                border-radius: 5px;
            }
        """)

        # Train image
        self.train_pixmap = QPixmap("icons/icons8-railway-50.png")
        self.train_position = 0  # Initial train position

        # Percentage label
        self.percent_label = QLabel("0%", self)
        self.percent_label.setAlignment(Qt.AlignCenter)
        self.percent_label.setStyleSheet("font-size: 18px; font-weight: bold; color: black;")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.percent_label)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

        # Set background color (optional)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0, 0))  # Fully transparent
        self.setPalette(palette)

        # Initialize loading process
        self.progress = 0
        self.center_on_parent(parent)

    def center_on_parent(self, parent):
        if parent is not None:
            # Calculate the center position
            parent_geometry = parent.geometry()
            x = parent_geometry.x() + (parent_geometry.width() - self.width()) // 2
            y = parent_geometry.y() + (parent_geometry.height() - self.height()) // 2
            self.move(x, y)




    def set_value(self, value):
        self.progress_bar.setValue(value)
        percent = round(value/self.progress_bar.maximum() * 100,1)
        self.percent_label.setText(f"{percent}%")

        # Update the train's position based on progress
        bar_width = self.progress_bar.width()
        max_train_x = bar_width - self.train_pixmap.width()
        self.train_position = max_train_x * value / self.progress_bar.maximum()

        self.update()  # Trigger the paintEvent to redraw the train

        if value >= self.progress_bar.maximum():
            self.close()  # Close the loading screen when complete

    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Draw the train above the progress bar
        # Ensure that the train image is fully visible above the progress bar
        train_y_position = self.progress_bar.y() - self.train_pixmap.height() +5  # Adjust vertical offset as needed
        painter.drawPixmap(QPoint(int(self.train_position), train_y_position), self.train_pixmap)  
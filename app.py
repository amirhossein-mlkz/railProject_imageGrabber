import os,sys
from PySide6.QtWidgets import QApplication as sQApplication
from PySide6.QtWidgets import QStyleFactory
from Pysidemain import ImageDisplayApp

BUILD_UI = False

if BUILD_UI:

    os.system('pyside6-uic {} -o {}'.format(os.path.join('UIFiles', 'main_UI.ui'), os.path.join('UIFiles', 'main_UI.py')))
    os.system('CMD /C pyside6-rcc assets.qrc -o assets.py')#PySide
    # os.system('pyside6-rcc {} -o {}'.format(os.path.join(r'login_qt\uiFiles\resources', 'resource.qrc'), os.path.join(r'', 'resource_rc.py')))




if __name__ == "__main__":


    app = sQApplication()

    app.setStyle(QStyleFactory.create("Fusion"))  # Enforces a consistent style


    win = ImageDisplayApp()
    win.show()
    sys.exit(app.exec())
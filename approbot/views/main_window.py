from PyQt6.QtWidgets import QMainWindow, QStackedWidget

import config  
from controllers.robot_controller import RobotController  

from .connexion_view import ConnexionView
from .robot_view import RobotView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(config.WINDOW_TITLE)
        self.setStyleSheet(config.BACKGROUND_STYLE)
        self.resize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

        self.marty = RobotController()
        self.client = None
        self.ref_connected = False

        self.window_stack = QStackedWidget()
        self.setCentralWidget(self.window_stack)

        self.connexion_page = ConnexionView(self)
        self.robot_page = RobotView(self)

        self.window_stack.addWidget(self.connexion_page)
        self.window_stack.addWidget(self.robot_page)

        self.window_stack.setCurrentIndex(0)
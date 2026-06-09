from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6.QtGui import QIcon
import config  
from controllers.robot_controller import RobotController  

from .connexion_view import ConnexionView
from .robot_view import RobotView
from .calibration_view import CalibrationView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(config.WINDOW_TITLE)
        self.setStyleSheet(config.BACKGROUND_STYLE)
        self.resize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        self.setWindowIcon(QIcon(config.WINDOW_ICON_PATH))

        self.marty = RobotController()
        self.client = None
        self.ref_connected = False

        self.window_stack = QStackedWidget()
        self.setCentralWidget(self.window_stack)

        self.connexion_page = ConnexionView(self)
        self.robot_page = RobotView(self)
        self.calibration_page = CalibrationView(self)

        self.window_stack.addWidget(self.connexion_page)
        self.window_stack.addWidget(self.robot_page)
        self.window_stack.addWidget(self.calibration_page)

        self.window_stack.setCurrentIndex(0)
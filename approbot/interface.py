import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout,QPushButton,QLineEdit,QLabel,QStackedWidget
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap

import robot_controller

class ConnexionWorker(QThread):
    is_connected = pyqtSignal(bool)
    def __init__(self, marty_controller, ip):
        super().__init__()
        self.marty = marty_controller
        self.ip = ip
    
    def run(self):
            self.is_connected.emit(self.marty.connect(self.ip))

class MovementWorker(QThread):
    def __init__(self, marty_controller, action_code, nbr_action=1):
        super().__init__()
        self.marty=marty_controller
        self.action_code = action_code
        self.nbr_action = nbr_action
    
    def run(self):
        self.marty.execute_action(self.action_code,self.nbr_action)

class Interface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MartyApp")
        self.setStyleSheet("background-color:#98d7d6;")
        self.resize(500,480)

        self.marty = robot_controller.RobotController()

        self.window_stack = QStackedWidget()
        self.setCentralWidget(self.window_stack)

        self.create_connexion_page()
        self.create_robot_page()

        self.window_stack.setCurrentIndex(0)

    def create_connexion_page(self):
        window = QWidget()
        layout = QVBoxLayout()
        layout.addStretch()
        title_label = QLabel("Marty Dance Battle")
        title_label.setStyleSheet("font-size:24px; font-weight:bold; color: #2C3E50; qproperty-alignment: 'AlignCenter';")
        layout.addWidget(title_label)
        layout.addSpacing(40)

        image_label = QLabel()
        pixmap = QPixmap("approbot/Logo.png")
        pixmap_2=pixmap.scaledToWidth(150,Qt.TransformationMode.SmoothTransformation)
        image_label.setPixmap(pixmap_2)
        layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(100)
        
        info_label = QLabel("Pls enter Marty's IP address :")
        info_label.setStyleSheet("font-size: 14px; color: #7F8C8D; qproperty-alignment: 'AlignCenter';")
        layout.addWidget(info_label)
        layout.addSpacing(15)

        self.text_field = QLineEdit()
        self.text_field.setPlaceholderText("Ex:192.168.1.4")
        self.text_field.setMinimumWidth(250)
        self.text_field.setStyleSheet("""
            QLineEdit 
            {
                padding:8px;
                font-size:14px;
                border: 2px solid #3498DB;
                border-radius: 6px;
                color: #000000;
                background-color: #45c2e8;
            }
            QLineEdit:focus 
            {
                border : 2px solid #3498DB;
            }
        """)
        layout.addWidget(self.text_field, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(25)
        connexion_button = QPushButton("Try connexion")
        connexion_button.setMinimumWidth(150)
        connexion_button.setStyleSheet("""
            QPushButton
            {
                padding : 8px;
                background-color: #45c2e8;
                color: black;
                border: 2px solid #3498DB;
                border-radius: 15px;
                
            }
            """)
        connexion_button.clicked.connect(self.connexion_button_action)
        layout.addWidget(connexion_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        self.label_status = QLabel("")
        layout.addWidget(self.label_status,alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        window.setLayout(layout)
        self.window_stack.addWidget(window)
    
    def create_robot_page(self):
        window = QWidget()
        layout = QVBoxLayout()
        title=QLabel("Manual Control")
        title.setStyleSheet("font-size:20px; font-weight:bold;color:#2C3E50;")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(30)
        window.setLayout(layout)
        self.window_stack.addWidget(window)

    def connexion_button_action(self):
        ip_entered = self.text_field.text()
        self.label_status.setStyleSheet("color:green;")
        self.label_status.setText("Connecting...")

        self.worker = ConnexionWorker(self.marty, ip_entered)
        self.worker.is_connected.connect(self.connexion_action)
        
        self.worker.start()
    
    def connexion_action(self, is_connected):
        if is_connected:
            self.window_stack.setCurrentIndex(1)
        else:
            self.label_status.setStyleSheet("color:red;")
            self.label_status.setText("Error, please enter a valid IP address")
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    interface = Interface()
    interface.showMaximized()
    sys.exit(app.exec())
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout,QPushButton,QLineEdit,QLabel,QStackedWidget, QGridLayout
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap

import robot_controller
import robot_client

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
        self.ref_connected = False

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
        self.color_list = ["Black","Purple","Dark Blue","Yellow","Cyan", "Green", "Red"]
        self.index_color = 0
        window = QWidget()
        layout = QVBoxLayout()
        title=QLabel("Manual Control")
        title.setStyleSheet("font-size:20px; font-weight:bold;color:#2C3E50;")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(30)

        grid_layout = QGridLayout()
        btn_up = QPushButton("UP")
        btn_back = QPushButton("DOWN")
        btn_left = QPushButton("LEFT")
        btn_right = QPushButton("RIGHT")
        btn_reset = QPushButton("RESET")

        btn_style = """
            QPushButton 
            {
                padding: 15px;
                background-color: #3498DB;
                color: white;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {background-color: #2980B9;}
            """
        btn_up.setStyleSheet(btn_style)
        btn_back.setStyleSheet(btn_style)
        btn_left.setStyleSheet(btn_style) 
        btn_right.setStyleSheet(btn_style)
        btn_reset.setStyleSheet(btn_style)

        grid_layout.addWidget(btn_up, 0,1)
        grid_layout.addWidget(btn_reset,1,1)
        grid_layout.addWidget(btn_left,2,0)
        grid_layout.addWidget(btn_back,2,1)
        grid_layout.addWidget(btn_right,2,2)

        btn_up.clicked.connect(lambda: self.movement_button_action("U")) 
        btn_left.clicked.connect(lambda: self.movement_button_action("L")) 
        btn_right.clicked.connect(lambda: self.movement_button_action("R")) 
        btn_back.clicked.connect(lambda: self.movement_button_action("B")) 
        btn_reset.clicked.connect(lambda: self.movement_button_action("RESET"))
        layout.addLayout(grid_layout)
        

        self.label_order = QLabel(f"Place Marty's left foot on the {self.color_list[0]}")
        self.label_order.setStyleSheet("font-size:16px; font-weight: bold; color: #E67E22;")
        self.label_order.hide()
        layout.addWidget(self.label_order, alignment=Qt.AlignmentFlag.AlignCenter)
        self.calibrate_btn= QPushButton("Calibrate")
        self.calibrate_btn.clicked.connect(self.calibrate_button_action)
        layout.addWidget(self.calibrate_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(20)

        self.input_ref_ip = QLineEdit()
        self.input_ref_ip.setPlaceholderText("Pls enter ref IP")
        self.input_ref_ip.setMinimumWidth(250)
        self.input_ref_ip.setStyleSheet("""
            QLineEdit
            {
                color: black;
                padding:8px;
                font-size: 14px;
                border: 2px solid #E74C3C;
                border-radius: 6px;
                background-color: blue;
            }
            QLineEdit:focus {border: 2px solid #C0392B;}
                                        """)
        layout.addWidget(self.input_ref_ip, alignment=Qt.AlignmentFlag.AlignCenter)
        self.ref_connexion_button = QPushButton("Ref : Deconnected")
        self.ref_connexion_button.setStyleSheet("""
            padding:10px;
            background-color: #E74C3C;
            color:white;
            font-weight:bold;
            border-radius:8px
                                                """)
        self.ref_connexion_button.clicked.connect(self.ref_connexion_button_action)
        layout.addWidget(self.ref_connexion_button, alignment=Qt.AlignmentFlag.AlignCenter)


        layout.addStretch()
        window.setLayout(layout)
        self.window_stack.addWidget(window)

        self.calibration_started = False

    def movement_button_action(self, action_code):
        self.movement_worker = MovementWorker(self.marty,action_code=action_code)
        self.movement_worker.start()

    def calibrate_button_action(self):

        if not self.calibration_started:
            self.calibration_started=True
            self.label_order.show()
            return
        actual_color = self.color_list[self.index_color]
        success = self.marty.calibrate_color(actual_color)

        if success:
            self.index_color+=1

            if self.index_color<len(self.color_list):
                next_color = self.color_list[self.index_color]
                self.label_order.setText(f"Place Marty's left foot ont the {next_color}")

            else:
                self.label_order.setText("Calibration Succeed!")
                self.label_order.setStyleSheet("font-size: 16px; font-weight: bold; color: green;")
                self.calibration_started = False
                self.index_color=0
        else:
            self.label_order.setText(f"Error on {actual_color}, try again")

    def connexion_button_action(self):
        ip_entered = self.text_field.text()
        self.label_status.setStyleSheet("color:green;")
        self.label_status.setText("Connecting...")

        self.worker = ConnexionWorker(self.marty, ip_entered)
        self.worker.is_connected.connect(self.connexion_action)
        
        self.worker.start()
    
    def ref_connexion_button_action(self):
        if not self.ref_connected:

            ip_entered = self.input_ref_ip.text()

            self.client = robot_client.RobotClient(host=ip_entered)
            self.ref_connexion_button.setText("Ref research...")
            self.ref_connexion_button.setStyleSheet("padding: 10px; background-color: #F39C12; color: white; font-weight: bold; border-radius: 8px;")
            QApplication.processEvents()

            if self.client.connect():
                self.ref_connected=True
                self.ref_connexion_button.setText("Ref Connected")
                self.ref_connexion_button.setStyleSheet("padding: 10px; background-color: #2ECC71; color: white; font-weight: bold; border-radius: 8px;")
                self.input_ref_ip.setEnabled(False)
            else:
                self.ref_connexion_button.setText("Error, couldn't find the ref")
                self.ref_connexion_button.setStyleSheet("padding: 10px; background-color: #E74C3C; color: white; font-weight: bold; border-radius: 8px;")
        else:
            self.client.disconnect()
            self.ref_connected=False
            self.ref_connexion_button.setText("Ref : Disconnected")
            self.ref_connexion_button.setStyleSheet("padding: 10px; background-color: #E74C3C; color: white; font-weight: bold; border-radius: 8px;")
            self.input_ref_ip.setEnabled(True)

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
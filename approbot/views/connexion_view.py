from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

import config  
from workers.connexion_worker import ConnexionWorker  

class ConnexionView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.marty = main_window.marty
        
        layout = QVBoxLayout()
        layout.addStretch()
        
        title_label = QLabel("Marty Dance Battle")
        title_label.setStyleSheet("font-size:24px; font-weight:bold; color: #2C3E50; qproperty-alignment: 'AlignCenter';")
        layout.addWidget(title_label)
        layout.addSpacing(40)

        image_label = QLabel()
        pixmap = QPixmap(config.WINDOW_ICON_PATH)
        pixmap_2 = pixmap.scaledToWidth(150, Qt.TransformationMode.SmoothTransformation)
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
        self.text_field.setStyleSheet(config.INPUT_MARTY_IP_STYLE)  
        layout.addWidget(self.text_field, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(25)
        
        connexion_button = QPushButton("Try connexion")
        connexion_button.setMinimumWidth(150)
        connexion_button.setStyleSheet(config.BTN_PRIMARY_STYLE) 
        connexion_button.clicked.connect(self.connexion_button_action)
        layout.addWidget(connexion_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        
        self.label_status = QLabel("")
        layout.addWidget(self.label_status, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        
        self.setLayout(layout)

    def connexion_button_action(self):
        ip_entered = self.text_field.text()
        self.label_status.setStyleSheet("color:green;")
        self.label_status.setText("Connecting...")

        self.worker = ConnexionWorker(self.marty, ip_entered)
        self.worker.is_connected.connect(self.connexion_action)
        self.worker.start()
    
    def connexion_action(self, is_connected):
        if is_connected:
            self.main_window.window_stack.setCurrentIndex(1)
        else:
            self.label_status.setStyleSheet("color:red;")
            self.label_status.setText("Error, please enter a valid IP address")
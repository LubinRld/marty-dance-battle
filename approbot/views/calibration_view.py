from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QFrame
from PyQt6.QtCore import Qt

from workers.calibration_worker import CalibrationWorker

import config

class CalibrationView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.marty = main_window.marty

        main_layout = QVBoxLayout()
        
        self.back_btn = QPushButton("Back to Controls")
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #34495E;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2C3E50; }
        """)
        self.back_btn.clicked.connect(lambda: self.main_window.window_stack.setCurrentIndex(1))
        main_layout.addWidget(self.back_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        main_layout.addSpacing(10)

        title = QLabel("CALIBRATION PAGE")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2C3E50;")
        main_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addSpacing(20)

        card = QFrame()
        card.setStyleSheet(config.CARD_STYLE)
        card.setFixedWidth(420)  
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(15)

        dropdown_label = QLabel("COLOR CHOICE")
        dropdown_label.setStyleSheet("font-weight: bold; color: #34495E; font-size: 12px;")
        card_layout.addWidget(dropdown_label)

        self.color_dropdown = QComboBox()
        self.color_dropdown.addItems(["Black", "Purple", "Dark Blue", "Yellow", "Cyan", "Green", "Red"])
        self.color_dropdown.setStyleSheet(config.INPUT_STYLE)
        card_layout.addWidget(self.color_dropdown)

        self.instruction_label = QLabel("INSTRUCTION\nPlace Marty's foot on the color.")
        self.instruction_label.setStyleSheet("color: #7F8C8D; font-style: italic; qproperty-alignment: 'AlignCenter';")
        card_layout.addWidget(self.instruction_label)
        card_layout.addSpacing(5)

        self.run_btn = QPushButton("CALIBRATE")
        self.run_btn.setStyleSheet(config.BTN_LAUNCH_STYLE)
        self.run_btn.clicked.connect(self.run_calibration_action)
        card_layout.addWidget(self.run_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        card_layout.addSpacing(5)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet("font-weight: bold; qproperty-alignment: 'AlignCenter';")
        card_layout.addWidget(self.status_label)

        main_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def run_calibration_action(self):
        
        selected_color = self.color_dropdown.currentText()
        self.status_label.setStyleSheet("color: #F39C12;")
        self.status_label.setText(f"Calibrating {selected_color}...")

        self.back_btn.setEnabled(False)
        self.run_btn.setEnabled(False)
        self.color_dropdown.setEnabled(False)

        self.calibration_worker = CalibrationWorker(self.marty, selected_color)
        self.calibration_worker.is_calibration_done.connect(self.calibration_action)
        self.calibration_worker.start()


    def calibration_action(self, is_calibration_done):

        self.back_btn.setEnabled(True)
        self.run_btn.setEnabled(True)
        self.color_dropdown.setEnabled(True)

        if is_calibration_done:
            self.status_label.setStyleSheet("color: #2ECC71;")
            self.status_label.setText("Calibrating Done!")
        else:
            self.status_label.setStyleSheet("color: #E74C3C;")
            self.status_label.setText("Calibrating failed, please try again.")
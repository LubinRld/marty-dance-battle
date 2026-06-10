from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel, QLineEdit, QFileDialog,QHBoxLayout
from PyQt6.QtCore import Qt

import config  
from models.read_dance import ReadDance
from models.game_manager import GameManager
from workers.movement_worker import MovementWorker
from workers.connexion_ref_worker import ConnexionRefWorker
from workers.game_worker import GameWorker
from models import robot_client

class RobotView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.marty = main_window.marty
        
        self.color_list = ["Black", "Purple", "Dark Blue", "Yellow", "Cyan", "Green", "Red"]
        self.index_color = 0
        self.calibration_started = False
        self.file_path_danse = None

        layout = QVBoxLayout()
        
        title = QLabel("Manual Control")
        title.setStyleSheet("font-size:20px; font-weight:bold; color:#2C3E50;")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(30)

        grid_step_layout = QGridLayout()
        btn_up = QPushButton("UP")
        btn_back = QPushButton("DOWN")
        btn_left = QPushButton("LEFT")
        btn_right = QPushButton("RIGHT")
        btn_reset = QPushButton("RESET")

        grid_arm_layout= QGridLayout()
        btn_left_arm_down = QPushButton("ALB")
        btn_left_arm_up = QPushButton("ALU")
        btn_right_arm_down = QPushButton("ARB")
        btn_right_arm_up = QPushButton("ARU")

        btn_up.setStyleSheet(config.BTN_MOVEMENT_STYLE)
        btn_back.setStyleSheet(config.BTN_MOVEMENT_STYLE)
        btn_left.setStyleSheet(config.BTN_MOVEMENT_STYLE) 
        btn_right.setStyleSheet(config.BTN_MOVEMENT_STYLE)
        btn_reset.setStyleSheet(config.BTN_MOVEMENT_STYLE)
        btn_left_arm_down.setStyleSheet(config.BTN_MOVEMENT_STYLE)
        btn_left_arm_up.setStyleSheet(config.BTN_MOVEMENT_STYLE)
        btn_right_arm_down.setStyleSheet(config.BTN_MOVEMENT_STYLE)
        btn_right_arm_up.setStyleSheet(config.BTN_MOVEMENT_STYLE)

        grid_step_layout.addWidget(btn_up, 0, 1)
        grid_step_layout.addWidget(btn_reset, 1, 1)
        grid_step_layout.addWidget(btn_left, 1, 0)
        grid_step_layout.addWidget(btn_right, 1, 2)
        grid_step_layout.addWidget(btn_back, 2, 1)

        grid_arm_layout.addWidget(btn_left_arm_up, 0,0)
        grid_arm_layout.addWidget(btn_right_arm_up, 0,1)
        grid_arm_layout.addWidget(btn_left_arm_down, 1,0)
        grid_arm_layout.addWidget(btn_right_arm_down, 1,1)

        btn_up.clicked.connect(lambda: self.movement_button_action("U")) 
        btn_left.clicked.connect(lambda: self.movement_button_action("L")) 
        btn_right.clicked.connect(lambda: self.movement_button_action("R")) 
        btn_back.clicked.connect(lambda: self.movement_button_action("B")) 
        btn_reset.clicked.connect(lambda: self.movement_button_action("RESET"))

        btn_left_arm_down.clicked.connect(lambda: self.movement_button_action("ALB"))
        btn_left_arm_up.clicked.connect(lambda: self.movement_button_action("ALU"))
        btn_right_arm_down.clicked.connect(lambda: self.movement_button_action("ARB"))
        btn_right_arm_up.clicked.connect(lambda: self.movement_button_action("ARU"))

        layout.addLayout(grid_step_layout)
        layout.addSpacing(20)

        layout.addLayout(grid_arm_layout)
        layout.addSpacing(20)

        self.calibrate_btn = QPushButton("Calibrate")
        self.calibrate_btn.clicked.connect(lambda: self.main_window.window_stack.setCurrentIndex(2))
        layout.addWidget(self.calibrate_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(20)

        self.input_ref_ip = QLineEdit()
        self.input_ref_ip.setPlaceholderText("Pls enter ref IP")
        self.input_ref_ip.setMinimumWidth(250)
        self.input_ref_ip.setStyleSheet(config.INPUT_REF_IP_STYLE)
        layout.addWidget(self.input_ref_ip, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.ref_connexion_button = QPushButton("Ref : Deconnected")
        self.ref_connexion_button.setStyleSheet("""
            padding:10px;
            background-color: #E74C3C;
            color:white;
            font-weight:bold;
            border-radius:8px;
        """)
        self.ref_connexion_button.clicked.connect(self.ref_connexion_button_action)
        layout.addWidget(self.ref_connexion_button, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(30)
        
        self.label_file_path = QLabel("Pls select a .dance file")
        self.label_file_path.setStyleSheet("color: #7F8C8D; font-style: italic;")
        layout.addWidget(self.label_file_path, alignment=Qt.AlignmentFlag.AlignCenter)

        self.choose_file_btn = QPushButton("Choose a .dance file")
        self.choose_file_btn.setStyleSheet("padding: 8px; background-color: #34495E; color: white; border-radius: 5px;")  
        self.choose_file_btn.clicked.connect(self.choose_file_action)
        layout.addWidget(self.choose_file_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)

        self.start_battle_btn = QPushButton("Start Battle")
        self.start_battle_btn.setEnabled(False)
        self.start_battle_btn.setStyleSheet("""
            QPushButton { padding: 12px; background-color: #2ECC71; color: white; font-weight: bold; border-radius: 8px; min-width: 180px; }
            QPushButton:disabled { background-color: #BDC3C7; color: #7F8C8D; }
        """)
        self.start_battle_btn.clicked.connect(self.start_game_action)
        layout.addWidget(self.start_battle_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()
        self.setLayout(layout)



    def movement_button_action(self, action_code):
        self.movement_worker = MovementWorker(self.marty, action_code=action_code)
        self.movement_worker.start()

    def ref_connexion_button_action(self):
        if not self.main_window.ref_connected:
            ip_entered = self.input_ref_ip.text()
            
            self.main_window.client = robot_client.RobotClient(host=ip_entered)
            self.ref_connexion_button.setText("Ref research...")
            self.ref_connexion_button.setStyleSheet("padding: 10px; background-color: #F39C12; color: white; font-weight: bold; border-radius: 8px;")
            self.ref_connexion_button.setEnabled(False)

            
            self.connexion_ref_worker = ConnexionRefWorker(self.main_window.client)

            self.connexion_ref_worker.is_connected.connect(self.connexion_ref_action)
            self.connexion_ref_worker.start()

        else:
            self.main_window.client.disconnect()
            self.main_window.ref_connected = False
            self.ref_connexion_button.setText("Ref : Disconnected")
            self.ref_connexion_button.setStyleSheet("padding: 10px; background-color: #E74C3C; color: white; font-weight: bold; border-radius: 8px;")
            self.input_ref_ip.setEnabled(True)
        
    def connexion_ref_action(self, is_connected):
        self.ref_connexion_button.setEnabled(True)

        if is_connected:
                self.main_window.ref_connected = True
                self.ref_connexion_button.setText("Ref Connected")
                self.ref_connexion_button.setStyleSheet("padding: 10px; background-color: #2ECC71; color: white; font-weight: bold; border-radius: 8px;")
                self.input_ref_ip.setEnabled(False)
        else:
            self.ref_connexion_button.setText("Error, couldn't find the ref")
            self.ref_connexion_button.setStyleSheet("padding: 10px; background-color: #E74C3C; color: white; font-weight: bold; border-radius: 8px;")

        self.update_battle_button_state()


    def choose_file_action(self):
        fichier, _ = QFileDialog.getOpenFileName(
            self, 
            "Sélectionner ton fichier de danse", 
            "", 
            "Fichiers Danse (*.dance);;Tous les fichiers (*)"
        )
        if fichier:
            self.file_path_danse = fichier
            self.label_file_path.setText(f"File loaded: {self.file_path_danse}")
            self.label_file_path.setStyleSheet("color: #27AE60; font-weight: bold;")
            self.update_battle_button_state()        

    def update_battle_button_state(self):
        has_file = self.file_path_danse is not None
        is_ref_connected = self.main_window.ref_connected

        self.start_battle_btn.setEnabled(has_file and is_ref_connected)

    def start_game_action(self):
        if not self.file_path_danse:
            return
        
        self.start_battle_btn.setEnabled(False)
        self.start_battle_btn.setText("Ref connexion verification...")

        self.check_live_worker = ConnexionRefWorker(self.main_window.client, True)
        self.check_live_worker.is_live.connect(self.start_game_check)
        self.check_live_worker.start()
            
    def start_game_check(self, is_live):
        if not is_live:
            self.main_window.ref_connected = False
            self.ref_connexion_button.setText("Ref : Disconnected")
            self.ref_connexion_button.setStyleSheet("padding: 10px; background-color: #E74C3C; color: white; font-weight: bold; border-radius: 8px;")
            self.input_ref_ip.setEnabled(True)
            self.start_battle_btn.setText("Start Battle")
            self.update_battle_button_state()
            return
        
        reader = ReadDance(self.file_path_danse)
        self.manager = GameManager(self.marty, self.main_window.client, reader)

        self.manager.moves = reader.getMovement()
        self.manager.acts = reader.getAct()

        self.start_battle_btn.setEnabled(False)
        self.start_battle_btn.setText("Battle en cours...")

        self.game_worker = GameWorker(self.manager)
        self.game_worker.game_over_signal.connect(self.battle_end_action)
        self.game_worker.start()

    def battle_end_action(self):
        self.start_battle_btn.setEnabled(True)
        self.start_battle_btn.setText("Start Battle")
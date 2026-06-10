from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel, QLineEdit, QFileDialog,QHBoxLayout, QFrame
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt

import config  
from models.read_dance import ReadDance
from models.game_manager import GameManager
from workers.movement_worker import MovementWorker
from workers.connexion_ref_worker import ConnexionRefWorker
from workers.game_worker import GameWorker
from workers.read_color_worker import ReadColorWorker
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

        #Creation of titles

        page_title = QLabel("MARTY DANCE BATTLE")
        page_title.setStyleSheet("font-size:20px; font-weight:bold; color:#2C3E50;")
        page_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        manual_field_title = QLabel("MANUAL CONTROL")
        manual_field_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        battle_setup_field_title = QLabel("BATTLE SETUP")
        battle_setup_field_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #Creation of movements buttons

        btn_up = QPushButton()
        btn_back = QPushButton()
        btn_left = QPushButton()
        btn_right = QPushButton()
        btn_reset = QPushButton()

        btn_up.setIcon(QIcon("assets/Up-arrow.png"))
        btn_back.setIcon(QIcon("assets/Down-arrow.png"))
        btn_left.setIcon(QIcon("assets/Left-arrow.png"))
        btn_right.setIcon(QIcon("assets/Right-arrow.png"))
        btn_reset.setIcon(QIcon("assets/Reset-button.png"))
        

        btn_up.setIconSize(QSize(64,64))
        btn_back.setIconSize(QSize(64,64))
        btn_left.setIconSize(QSize(64,64))
        btn_right.setIconSize(QSize(64,64))
        btn_reset.setIconSize(QSize(64,64))

        btn_up.setFixedSize(70,70)
        btn_back.setFixedSize(70,70)
        btn_left.setFixedSize(70,70)
        btn_right.setFixedSize(70,70)
        btn_reset.setFixedSize(70,70)

        btn_up.setStyleSheet(config.BTN_MOVEMENT_STYLE)
        btn_back.setStyleSheet(config.BTN_MOVEMENT_STYLE)
        btn_left.setStyleSheet(config.BTN_MOVEMENT_STYLE) 
        btn_right.setStyleSheet(config.BTN_MOVEMENT_STYLE)
        btn_reset.setStyleSheet(config.BTN_MOVEMENT_STYLE)

        btn_up.clicked.connect(lambda: self.movement_button_action("U")) 
        btn_left.clicked.connect(lambda: self.movement_button_action("L")) 
        btn_right.clicked.connect(lambda: self.movement_button_action("R")) 
        btn_back.clicked.connect(lambda: self.movement_button_action("B")) 
        btn_reset.clicked.connect(lambda: self.movement_button_action("RESET"))

        grid_step_layout = QGridLayout()
        grid_step_layout.addWidget(btn_up, 0, 1)
        grid_step_layout.addWidget(btn_reset, 1, 1)
        grid_step_layout.addWidget(btn_left, 1, 0)
        grid_step_layout.addWidget(btn_right, 1, 2)
        grid_step_layout.addWidget(btn_back, 2, 1)

        #Creation of color square widgets

        self.color_indicator_square = QFrame()
        self.color_name_label = QLabel("Unknown")
        self.btn_read_color = QPushButton("Read Color")

        self.color_indicator_square.setFixedSize(60,60)
        self.color_indicator_square.setStyleSheet("background-color: #BDC3C7; border: 1px solid #7F8C8D; border-radius: 10px;")

        self.color_name_label.setStyleSheet("font-weight: bold; color: #2C3E50;")

        self.btn_read_color.setStyleSheet(config.BTN_MOVEMENT_STYLE)
        self.btn_read_color.clicked.connect(self.refresh_color_action)

        color_square_layout = QVBoxLayout()
        color_square_layout.addWidget(self.color_indicator_square)
        color_square_layout.addWidget(self.color_name_label)
        color_square_layout.addWidget(self.btn_read_color)

        #Creation of arms movement buttons

        btn_left_arm_down = QPushButton()
        btn_left_arm_up = QPushButton()
        btn_right_arm_down = QPushButton()
        btn_right_arm_up = QPushButton()

        btn_left_arm_down.setIcon(QIcon("assets/Marty_LB.png"))
        btn_left_arm_up.setIcon(QIcon("assets/Marty_LU.png"))
        btn_right_arm_down.setIcon(QIcon("assets/Marty_RB.png"))
        btn_right_arm_up.setIcon(QIcon("assets/Marty_RU.png"))

        btn_left_arm_down.setIconSize(QSize(80,80))
        btn_left_arm_up.setIconSize(QSize(80,80))
        btn_right_arm_down.setIconSize(QSize(80,80))
        btn_right_arm_up.setIconSize(QSize(80,80))
        
        btn_left_arm_down.setFixedSize(95,95)
        btn_left_arm_up.setFixedSize(95,95)
        btn_right_arm_down.setFixedSize(95,95)
        btn_right_arm_up.setFixedSize(95,95)

        btn_left_arm_down.setStyleSheet(config.BTN_MOVEMENT_STYLE)
        btn_left_arm_up.setStyleSheet(config.BTN_MOVEMENT_STYLE)
        btn_right_arm_down.setStyleSheet(config.BTN_MOVEMENT_STYLE)
        btn_right_arm_up.setStyleSheet(config.BTN_MOVEMENT_STYLE)

        btn_left_arm_down.clicked.connect(lambda: self.movement_button_action("ALB"))
        btn_left_arm_up.clicked.connect(lambda: self.movement_button_action("ALU"))
        btn_right_arm_down.clicked.connect(lambda: self.movement_button_action("ARB"))
        btn_right_arm_up.clicked.connect(lambda: self.movement_button_action("ARU"))

        grid_arm_layout= QGridLayout()
    
        grid_arm_layout.addWidget(btn_left_arm_up, 0,0)
        grid_arm_layout.addWidget(btn_right_arm_up, 0,1)
        grid_arm_layout.addWidget(btn_left_arm_down, 1,0)
        grid_arm_layout.addWidget(btn_right_arm_down, 1,1)


        #Creation of emotions buttons

        btn_emotion_sad = QPushButton()
        btn_emotion_angry = QPushButton()
        btn_emotion_happy = QPushButton()
        btn_emotion_excited = QPushButton()

        btn_emotion_sad.setIcon(QIcon("assets/Marty_sad.png"))
        btn_emotion_angry.setIcon(QIcon("assets/Marty_angry.png"))
        btn_emotion_happy.setIcon(QIcon("assets/Marty_happy.png"))
        btn_emotion_excited.setIcon(QIcon("assets/Marty_joyful.png"))

        btn_emotion_sad.setIconSize(QSize(80,80))
        btn_emotion_angry.setIconSize(QSize(80,80))
        btn_emotion_happy.setIconSize(QSize(80,80))
        btn_emotion_excited.setIconSize(QSize(80,80))

        btn_emotion_sad.setFixedSize(95,95)
        btn_emotion_angry.setFixedSize(95,95)
        btn_emotion_happy.setFixedSize(95,95)
        btn_emotion_excited.setFixedSize(95,95)

        btn_emotion_sad.setStyleSheet(config.BTN_MOVEMENT_STYLE)
        btn_emotion_angry.setStyleSheet(config.BTN_MOVEMENT_STYLE)
        btn_emotion_happy.setStyleSheet(config.BTN_MOVEMENT_STYLE)
        btn_emotion_excited.setStyleSheet(config.BTN_MOVEMENT_STYLE)

        btn_emotion_sad.clicked.connect(lambda: self.movement_button_action("XSD"))
        btn_emotion_angry.clicked.connect(lambda: self.movement_button_action("XNG"))
        btn_emotion_happy.clicked.connect(lambda: self.movement_button_action("XHP"))
        btn_emotion_excited.clicked.connect(lambda: self.movement_button_action("XDN"))

        emotion_layout = QHBoxLayout()

        emotion_layout.addWidget(btn_emotion_sad)
        emotion_layout.addWidget(btn_emotion_angry)
        emotion_layout.addWidget(btn_emotion_happy)
        emotion_layout.addWidget(btn_emotion_excited)

        #Creation of Calibration Page button 

        self.calibrate_btn = QPushButton("Calibrate Colors")

        self.calibrate_btn.setStyleSheet(config.BTN_MOVEMENT_STYLE)

        self.calibrate_btn.clicked.connect(lambda: self.main_window.window_stack.setCurrentIndex(2))

        calibration_layout = QVBoxLayout()
        calibration_layout.addWidget(self.calibrate_btn)


        #Referee connexion field 
        ref_connexion_label = QLabel ("REF CONNEXION")
        self.input_ref_ip = QLineEdit()
        self.ref_connexion_button = QPushButton("Ref : Deconnected")


        self.input_ref_ip.setPlaceholderText("Pls enter ref IP")
        self.input_ref_ip.setMinimumWidth(250)
        self.input_ref_ip.setStyleSheet(config.INPUT_REF_IP_STYLE)

        self.ref_connexion_button.setStyleSheet("""
            padding:10px;
            background-color: #E74C3C;
            color:white;
            font-weight:bold;
            border-radius:8px;
        """)

        ref_connexion_layout = QVBoxLayout()
        ref_connexion_layout.addWidget(ref_connexion_label)
        ref_connexion_layout.addWidget(self.input_ref_ip)
        ref_connexion_layout.addWidget(self.ref_connexion_button)


        self.ref_connexion_button.clicked.connect(self.ref_connexion_button_action)

        #Dance Configuration field

        dance_file_label = QLabel("DANCE CONFIGURATION")
        self.choose_file_btn = QPushButton("Choose a .dance file")
        self.label_file_path = QLabel("Pls select a .dance file")



        self.label_file_path.setStyleSheet("color: #7F8C8D; font-style: italic;")
        self.choose_file_btn.setStyleSheet("padding: 8px; background-color: #34495E; color: white; border-radius: 5px;")  


        self.choose_file_btn.clicked.connect(self.choose_file_action)

        dance_file_layout = QVBoxLayout()
        dance_file_layout.addWidget(dance_file_label)
        dance_file_layout.addWidget(self.choose_file_btn)
        dance_file_layout.addWidget(self.label_file_path)


        #Start Battle button
        self.start_battle_btn = QPushButton("Start Battle")

        self.start_battle_btn.setStyleSheet("""
            QPushButton { padding: 12px; background-color: #2ECC71; color: white; font-weight: bold; border-radius: 8px; min-width: 180px; }
            QPushButton:disabled { background-color: #BDC3C7; color: #7F8C8D; }
        """)

        self.start_battle_btn.setEnabled(False)
        self.start_battle_btn.clicked.connect(self.start_game_action)


       

        
        #layout adgencement: 
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 30, 40, 40)
        main_layout.setSpacing(20)
    
        page_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2C3E50; margin-bottom: 20px;")
        main_layout.addWidget(page_title, alignment=Qt.AlignmentFlag.AlignCenter)

   
        page_layout = QHBoxLayout()
        page_layout.setSpacing(80)

        manual_control_container = QFrame()
        manual_control_container.setStyleSheet("background: transparent; border: none;")
        manual_control_layout = QVBoxLayout(manual_control_container)
        manual_control_layout.setSpacing(25)
        manual_control_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        manual_field_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2C3E50;")
        manual_control_layout.addWidget(manual_field_title, alignment=Qt.AlignmentFlag.AlignCenter)
        

        moving_and_square_layout = QHBoxLayout()
        moving_and_square_layout.setSpacing(30) 
        moving_and_square_layout.addLayout(grid_step_layout)
        
        color_square_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        color_square_layout.setSpacing(5)
        moving_and_square_layout.addLayout(color_square_layout)

        manual_control_layout.addLayout(moving_and_square_layout)
        

        arm_section_label = QLabel("ARMS CONTROL")
        arm_section_label.setStyleSheet("font-weight: bold; color: #34495E; font-size: 11px; margin-top: 10px;")
        manual_control_layout.addWidget(arm_section_label, alignment=Qt.AlignmentFlag.AlignCenter)
        manual_control_layout.addLayout(grid_arm_layout)

        emotion_section_label = QLabel("EMOTIONS / EXPRESSIONS")
        emotion_section_label.setStyleSheet("font-weight: bold; color: #34495E; font-size: 11px; margin-top: 10px;")
        manual_control_layout.addWidget(emotion_section_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        emotion_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        manual_control_layout.addLayout(emotion_layout)
        
        self.calibrate_btn.setStyleSheet("""
            QPushButton { padding: 8px 15px; background-color: #34495E; color: white; font-weight: bold; border-radius: 5px; }
            QPushButton:hover { background-color: #2C3E50; }
        """)
        manual_control_layout.addSpacing(10)
        manual_control_layout.addLayout(calibration_layout)

   
        battle_setup_container = QFrame()
        battle_setup_container.setStyleSheet("background: transparent; border: none;")

        battle_setup_container.setFixedWidth(320) 
        
        battle_setup_layout = QVBoxLayout(battle_setup_container)
        battle_setup_layout.setSpacing(25)
        battle_setup_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        battle_setup_field_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2C3E50;")
        battle_setup_layout.addWidget(battle_setup_field_title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        ref_connexion_label.setStyleSheet("font-weight: bold; color: #34495E; font-size: 11px;")
        dance_file_label.setStyleSheet("font-weight: bold; color: #34495E; font-size: 11px;")
        
        ref_connexion_layout.setSpacing(8)
        dance_file_layout.setSpacing(8)
        
        battle_setup_layout.addLayout(ref_connexion_layout)
        battle_setup_layout.addLayout(dance_file_layout)
        
        battle_setup_layout.addSpacing(10)
        battle_setup_layout.addWidget(self.start_battle_btn)


        page_layout.addStretch(1) 
        page_layout.addWidget(manual_control_container, alignment=Qt.AlignmentFlag.AlignCenter)
        page_layout.addWidget(battle_setup_container, alignment=Qt.AlignmentFlag.AlignCenter)
        page_layout.addStretch(1)

        main_layout.addLayout(page_layout)
        main_layout.addStretch(1) 
        
        self.setLayout(main_layout)



    def refresh_color_action(self):

        self.color_name_label.setText("Reading...")
        self.btn_read_color.setEnabled(False)

        self.read_color_worker = ReadColorWorker(self.marty)
        self.read_color_worker.color_read_signal.connect(self.update_color)
        self.read_color_worker.start()

    def update_color(self, color):
        css_colors = config.REAL_COLOR_RGB
        self.btn_read_color.setEnabled(True)
        if color in css_colors:
            self.color_indicator_square.setStyleSheet(f"background-color : {css_colors[color]};border: 1px solid #1C2833;border-radius: 10px;")
            self.color_name_label.setText(color)
        else:
            self.color_indicator_square.setStyleSheet("background-color: #BDC3C7; border: 1px solid #7F8C8D; border-radius: 10px;border-color: red")
            self.color_name_label.setText("Error")





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
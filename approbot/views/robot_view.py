from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel, QLineEdit, QFileDialog,QHBoxLayout, QFrame
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PyQt6.QtCore import QSize, Qt

import config  
from models.read_dance import ReadDance
from models.game_manager import GameManager
from workers.movement_worker import MovementWorker
from workers.connexion_ref_worker import ConnexionRefWorker
from workers.game_worker import GameWorker
from workers.refresh_status_worker import RefreshStatusWorker
from workers.ref_disconnexion_worker import RefDisconnexionWorker
from models import robot_client

class RobotView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.marty = main_window.marty
    
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

        self.btn_up = QPushButton()
        self.btn_back = QPushButton()
        self.btn_left = QPushButton()
        self.btn_right = QPushButton()
        self.btn_reset = QPushButton()

        self.btn_up.setIcon(QIcon("assets/Up-arrow.png"))
        self.btn_back.setIcon(QIcon("assets/Down-arrow.png"))
        self.btn_left.setIcon(QIcon("assets/Left-arrow.png"))
        self.btn_right.setIcon(QIcon("assets/Right-arrow.png"))
        self.btn_reset.setIcon(QIcon("assets/Reset-button.png"))
        

        self.btn_up.setIconSize(QSize(64,64))
        self.btn_back.setIconSize(QSize(64,64))
        self.btn_left.setIconSize(QSize(64,64))
        self.btn_right.setIconSize(QSize(64,64))
        self.btn_reset.setIconSize(QSize(64,64))

        self.btn_up.setFixedSize(70,70)
        self.btn_back.setFixedSize(70,70)
        self.btn_left.setFixedSize(70,70)
        self.btn_right.setFixedSize(70,70)
        self.btn_reset.setFixedSize(70,70)

        self.btn_up.setStyleSheet(config.BTN_MOVEMENT_STYLE)
        self.btn_back.setStyleSheet(config.BTN_MOVEMENT_STYLE)
        self.btn_left.setStyleSheet(config.BTN_MOVEMENT_STYLE) 
        self.btn_right.setStyleSheet(config.BTN_MOVEMENT_STYLE)
        self.btn_reset.setStyleSheet(config.BTN_MOVEMENT_STYLE)

        self.btn_up.clicked.connect(lambda: self.movement_button_action("U")) 
        self.btn_left.clicked.connect(lambda: self.movement_button_action("L")) 
        self.btn_right.clicked.connect(lambda: self.movement_button_action("R")) 
        self.btn_back.clicked.connect(lambda: self.movement_button_action("B")) 
        self.btn_reset.clicked.connect(lambda: self.movement_button_action("RESET"))

        grid_step_layout = QGridLayout()
        grid_step_layout.addWidget(self.btn_up, 0, 1)
        grid_step_layout.addWidget(self.btn_reset, 1, 1)
        grid_step_layout.addWidget(self.btn_left, 1, 0)
        grid_step_layout.addWidget(self.btn_right, 1, 2)
        grid_step_layout.addWidget(self.btn_back, 2, 1)

        #Creation of color square and battery widgets

        self.battery_icon_label =QLabel()
        self.battery_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.battery_icon_label.setPixmap(self.create_battery_icon(100))

        self.color_indicator_square = QFrame()
        self.color_name_label = QLabel("Unknown")
        self.btn_refresh_status = QPushButton("Refresh Status")

        self.color_indicator_square.setFixedSize(60,60)
        self.color_indicator_square.setStyleSheet("background-color: #BDC3C7; border: 1px solid #7F8C8D; border-radius: 10px;")

        self.color_name_label.setStyleSheet("font-weight: bold; color: #2C3E50;")

        self.btn_refresh_status.setStyleSheet(config.BTN_SECONDARY_STYLE)

        self.btn_refresh_status.clicked.connect(self.refresh_status_action)

        color_square_layout = QVBoxLayout()
        color_square_layout.setSpacing(8) 
        
        color_square_layout.addWidget(self.color_indicator_square, alignment=Qt.AlignmentFlag.AlignCenter)
        color_square_layout.addWidget(self.color_name_label, alignment=Qt.AlignmentFlag.AlignCenter)
        color_square_layout.addWidget(self.battery_icon_label, alignment=Qt.AlignmentFlag.AlignCenter)
        color_square_layout.addWidget(self.btn_refresh_status, alignment=Qt.AlignmentFlag.AlignCenter)

        #Creation of arms movement buttons

        self.btn_left_arm_down = QPushButton()
        self.btn_left_arm_up = QPushButton()
        self.btn_right_arm_down = QPushButton()
        self.btn_right_arm_up = QPushButton()

        self.btn_left_arm_down.setIcon(QIcon("assets/Marty_LB.png"))
        self.btn_left_arm_up.setIcon(QIcon("assets/Marty_LU.png"))
        self.btn_right_arm_down.setIcon(QIcon("assets/Marty_RB.png"))
        self.btn_right_arm_up.setIcon(QIcon("assets/Marty_RU.png"))

        self.btn_left_arm_down.setIconSize(QSize(80,80))
        self.btn_left_arm_up.setIconSize(QSize(80,80))
        self.btn_right_arm_down.setIconSize(QSize(80,80))
        self.btn_right_arm_up.setIconSize(QSize(80,80))
        
        self.btn_left_arm_down.setFixedSize(95,95)
        self.btn_left_arm_up.setFixedSize(95,95)
        self.btn_right_arm_down.setFixedSize(95,95)
        self.btn_right_arm_up.setFixedSize(95,95)

        self.btn_left_arm_down.setStyleSheet(config.BTN_MOVEMENT_STYLE)
        self.btn_left_arm_up.setStyleSheet(config.BTN_MOVEMENT_STYLE)
        self.btn_right_arm_down.setStyleSheet(config.BTN_MOVEMENT_STYLE)
        self.btn_right_arm_up.setStyleSheet(config.BTN_MOVEMENT_STYLE)

        self.btn_left_arm_down.clicked.connect(lambda: self.movement_button_action("ALB"))
        self.btn_left_arm_up.clicked.connect(lambda: self.movement_button_action("ALU"))
        self.btn_right_arm_down.clicked.connect(lambda: self.movement_button_action("ARB"))
        self.btn_right_arm_up.clicked.connect(lambda: self.movement_button_action("ARU"))

        grid_arm_layout= QGridLayout()
    
        grid_arm_layout.addWidget(self.btn_left_arm_up, 0,0)
        grid_arm_layout.addWidget(self.btn_right_arm_up, 0,1)
        grid_arm_layout.addWidget(self.btn_left_arm_down, 1,0)
        grid_arm_layout.addWidget(self.btn_right_arm_down, 1,1)


        #Creation of emotions buttons

        self.btn_emotion_sad = QPushButton()
        self.btn_emotion_angry = QPushButton()
        self.btn_emotion_happy = QPushButton()
        self.btn_emotion_excited = QPushButton()

        self.btn_emotion_sad.setIcon(QIcon("assets/Marty_sad.png"))
        self.btn_emotion_angry.setIcon(QIcon("assets/Marty_angry.png"))
        self.btn_emotion_happy.setIcon(QIcon("assets/Marty_happy.png"))
        self.btn_emotion_excited.setIcon(QIcon("assets/Marty_joyful.png"))

        self.btn_emotion_sad.setIconSize(QSize(80,80))
        self.btn_emotion_angry.setIconSize(QSize(80,80))
        self.btn_emotion_happy.setIconSize(QSize(80,80))
        self.btn_emotion_excited.setIconSize(QSize(80,80))

        self.btn_emotion_sad.setFixedSize(95,95)
        self.btn_emotion_angry.setFixedSize(95,95)
        self.btn_emotion_happy.setFixedSize(95,95)
        self.btn_emotion_excited.setFixedSize(95,95)

        self.btn_emotion_sad.setStyleSheet(config.BTN_MOVEMENT_STYLE)
        self.btn_emotion_angry.setStyleSheet(config.BTN_MOVEMENT_STYLE)
        self.btn_emotion_happy.setStyleSheet(config.BTN_MOVEMENT_STYLE)
        self.btn_emotion_excited.setStyleSheet(config.BTN_MOVEMENT_STYLE)

        self.btn_emotion_sad.clicked.connect(lambda: self.movement_button_action("XSD"))
        self.btn_emotion_angry.clicked.connect(lambda: self.movement_button_action("XNG"))
        self.btn_emotion_happy.clicked.connect(lambda: self.movement_button_action("XHP"))
        self.btn_emotion_excited.clicked.connect(lambda: self.movement_button_action("XDN"))

        emotion_layout = QHBoxLayout()

        emotion_layout.addWidget(self.btn_emotion_sad)
        emotion_layout.addWidget(self.btn_emotion_angry)
        emotion_layout.addWidget(self.btn_emotion_happy)
        emotion_layout.addWidget(self.btn_emotion_excited)

        #Creation of Calibration Page button 

        self.calibrate_btn = QPushButton("Calibrate Colors")

        self.calibrate_btn.setStyleSheet(config.BTN_SECONDARY_STYLE)

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
        self.input_ref_ip.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        self.ref_connexion_button.setStyleSheet(config.BTN_REF_DISCONNECTED_STYLE)

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
        self.choose_file_btn.setStyleSheet(config.BTN_SECONDARY_STYLE)  


        self.choose_file_btn.clicked.connect(self.choose_file_action)

        dance_file_layout = QVBoxLayout()
        dance_file_layout.addWidget(dance_file_label)
        dance_file_layout.addWidget(self.choose_file_btn)
        dance_file_layout.addWidget(self.label_file_path)


        #Start Battle button
        self.start_battle_btn = QPushButton("Start Battle")

        self.start_battle_btn.setStyleSheet(config.BTN_PRIMARY_STYLE)

        self.start_battle_btn.setEnabled(False)
        self.start_battle_btn.clicked.connect(self.start_game_action)

        #securisation button for keyboard
        self.btn_refresh_status.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.calibrate_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.choose_file_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.start_battle_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.ref_connexion_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
       

        
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
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocus()



    def refresh_status_action(self):

        self.color_name_label.setText("Reading...")
        self.btn_refresh_status.setEnabled(False)
        self.btn_refresh_status.setText("Reading...")

        self.status_worker = RefreshStatusWorker(self.marty)
        self.status_worker.status_updated_signal.connect(self.update_status)
        self.status_worker.start()

    def update_status(self, status_data):

        css_colors = config.REAL_COLOR_RGB
        self.btn_refresh_status.setEnabled(True)
        self.btn_refresh_status.setText("Refresh Status")
        color, battery = status_data

        self.battery_icon_label.setPixmap(self.create_battery_icon(battery))
        if color in css_colors:
            self.color_indicator_square.setStyleSheet(f"background-color : {css_colors[color]};border: 1px solid #1C2833;border-radius: 10px;")
            self.color_name_label.setText(color)
        else:
            self.color_indicator_square.setStyleSheet("background-color: #BDC3C7; border: 1px solid #7F8C8D; border-radius: 10px;border-color: red")
            self.color_name_label.setText("Error")

    def movement_button_action(self, action_code):
        self.set_manual_controls_enabled(False)
        self.movement_worker = MovementWorker(self.marty, action_code=action_code)
        self.movement_worker.finished.connect(self.on_movement_finished)
        self.movement_worker.start()

    def on_movement_finished(self):
        self.set_manual_controls_enabled(True)

    def ref_connexion_button_action(self):
        if not self.main_window.ref_connected:
            self.input_ref_ip.clearFocus()
            ip_entered = self.input_ref_ip.text()
            
            self.main_window.client = robot_client.RobotClient(host=ip_entered)
            self.ref_connexion_button.setText("Ref research...")
            self.ref_connexion_button.setStyleSheet(config.BTN_REF_WAITING_STYLE)
            self.ref_connexion_button.setEnabled(False)

            self.connexion_ref_worker = ConnexionRefWorker(self.main_window.client)
            self.connexion_ref_worker.is_connected.connect(self.connexion_ref_action)
            self.connexion_ref_worker.start()

        else:
            self.input_ref_ip.clearFocus()
            self.ref_connexion_button.setText("Disconnecting...")
            self.ref_connexion_button.setStyleSheet(config.BTN_REF_WAITING_STYLE)
            self.ref_connexion_button.setEnabled(False)

            self.disconnexion_worker = RefDisconnexionWorker(self.main_window.client)
            self.disconnexion_worker.is_disconnected.connect(self.ref_disconnexion_action)
            self.disconnexion_worker.start()
            

    def ref_disconnexion_action(self, is_disconnected):
            self.ref_connexion_button.setEnabled(True)
            if is_disconnected:
                self.main_window.ref_connected = False
                self.ref_connexion_button.setText("Ref : Disconnected")
                self.ref_connexion_button.setStyleSheet(config.BTN_REF_DISCONNECTED_STYLE)
                self.input_ref_ip.setEnabled(True)
                self.update_battle_button_state()
            else:
                self.ref_connexion_button.setText("Error, couldn't disconnect the ref")
        
    def connexion_ref_action(self, is_connected):
        self.ref_connexion_button.setEnabled(True)

        if is_connected:
                self.main_window.ref_connected = True
                self.ref_connexion_button.setText("Ref Connected")
                self.ref_connexion_button.setStyleSheet(config.BTN_REF_CONNECTED_STYLE)
                self.input_ref_ip.setEnabled(False)
        else:
            self.ref_connexion_button.setText("Error, couldn't find the ref")
            self.ref_connexion_button.setStyleSheet("padding: 10px; background-color: #E74C3C; color: white; font-weight: bold; border-radius: 6px;")

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
            self.ref_connexion_button.setStyleSheet("padding: 10px; background-color: #E74C3C; color: white; font-weight: bold; border-radius: 6px;")
            self.input_ref_ip.setEnabled(True)
            self.start_battle_btn.setText("Start Battle")
            self.update_battle_button_state()
            return
        
        reader = ReadDance(self.file_path_danse)
        self.manager = GameManager(self.marty, self.main_window.client, reader)
        self.set_manual_controls_enabled(False)
        self.start_battle_btn.setEnabled(False)
        self.choose_file_btn.setEnabled(False)
        self.ref_connexion_button.setEnabled(False)
        self.start_battle_btn.setText("Battle en cours...")

        self.game_worker = GameWorker(self.manager)
        self.game_worker.game_over_signal.connect(self.battle_end_action)
        self.game_worker.start()

    def battle_end_action(self):
        self.start_battle_btn.setEnabled(True)
        self.set_manual_controls_enabled(True)
        self.choose_file_btn.setEnabled(True)
        self.ref_connexion_button.setEnabled(True)
        self.start_battle_btn.setText("Start Battle")

    def create_battery_icon(self, percentage):
        pixmap = QPixmap(56, 28)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if percentage > 50:
            fill_color = QColor("#2ECC71") 
        elif percentage > 20:
            fill_color = QColor("#F39C12") 
        else:
            fill_color = QColor("#E74C3C") 

        painter.setPen(QColor("#34495E"))
        painter.setBrush(QColor("#BDC3C7"))
        painter.drawRoundedRect(3, 3, 44, 22, 4, 4)

        painter.setBrush(QColor("#34495E"))
        painter.drawRoundedRect(47, 9, 4, 10, 1, 1)

        if percentage > 0:
            max_width = 38
            current_width = int((percentage / 100.0) * max_width)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(fill_color)
            painter.drawRoundedRect(6, 6, current_width, 16, 2, 2)

        painter.setPen(QColor("#FFFFFF" if percentage > 35 else "#34495E"))
        font = QFont("Arial", 8, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(3, 3, 44, 22, Qt.AlignmentFlag.AlignCenter, f"{percentage}%")

        painter.end()
        return pixmap
    
    def keyPressEvent(self, event):

        if self.input_ref_ip.hasFocus():
            super().keyPressEvent(event)
            return

        key = event.key()

        if key == Qt.Key.Key_Up or key == Qt.Key.Key_Z:
            self.btn_up.animateClick() 
        elif key == Qt.Key.Key_Down or key == Qt.Key.Key_S:
            self.btn_back.animateClick()
        elif key == Qt.Key.Key_Left or key == Qt.Key.Key_Q:
            self.btn_left.animateClick()
        elif key == Qt.Key.Key_Right or key == Qt.Key.Key_D:
            self.btn_right.animateClick()
        elif key == Qt.Key.Key_Space:
            self.btn_reset.animateClick()
        else:
            super().keyPressEvent(event)

    def set_manual_controls_enabled(self, enabled):

        self.btn_up.setEnabled(enabled)
        self.btn_back.setEnabled(enabled)
        self.btn_left.setEnabled(enabled)
        self.btn_right.setEnabled(enabled)
        self.btn_reset.setEnabled(enabled)

        self.btn_left_arm_up.setEnabled(enabled)
        self.btn_left_arm_down.setEnabled(enabled)
        self.btn_right_arm_up.setEnabled(enabled)
        self.btn_right_arm_down.setEnabled(enabled)

        self.btn_emotion_sad.setEnabled(enabled)
        self.btn_emotion_angry.setEnabled(enabled)
        self.btn_emotion_happy.setEnabled(enabled)
        self.btn_emotion_excited.setEnabled(enabled)

        self.btn_refresh_status.setEnabled(enabled)
        self.calibrate_btn.setEnabled(enabled)
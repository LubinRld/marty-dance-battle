import server
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QTextEdit,
    QListWidget,
    QFrame,
    QGridLayout,
    QVBoxLayout
)

from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QThread, pyqtSignal

HOST = "0.0.0.0"
PORT = 8000

BACKG_COLOR = "#98d7d6"
FRAME_COLOR = "#fed55a"

class ServerThread(QThread):
    log_signal = pyqtSignal(str)

    def run(self):
        server.log_callback = self.log_signal.emit
        self.myserver = server.ThreadedHTTPServer((HOST, PORT), server.RequestHandler)
        server.add_log(f"Server running on {HOST}:{PORT}")
        server.battle.print_rules()
        self.myserver.serve_forever()

    def stop_server(self):
        if hasattr(self, "myserver") and self.myserver:
            self.myserver.shutdown()
            self.myserver.server_close()
    

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.server_thread = None
        self.setWindowTitle("Serveur Robot")
        self.resize(1200, 700)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet(f"background-color: {BACKG_COLOR};")

        grid = QGridLayout()
        central_widget.setLayout(grid)
        
        self.logo = QLabel()
        pixmap = QPixmap("./appserver/martygrise.png")
        if pixmap.isNull():
            self.logo.setText("Logo not found")
        else:
            pixmap = pixmap.scaled(180,180,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
            self.logo.setPixmap(pixmap)

        self.logo.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.robot_count = QLabel("Registered robots : 12")
        self.robot_count.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
        """)

        self.robot_selector = QListWidget()

        robots = [
            "Marty",
            "Atlas",
            "Wall-E",
            "R2D2",
            "Terminator",
            "Optimus Prime"
        ]

        for robot in robots:
            self.robot_selector.addItem(robot)

        robot_frame = QFrame()
        robot_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {FRAME_COLOR};
                border-radius: 10px;
            }}
        """)

        robot_layout = QVBoxLayout()
        robot_title = QLabel("Robots available")

        robot_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        robot_layout.addWidget(robot_title)
        robot_layout.addWidget(self.robot_selector)
        robot_frame.setLayout(robot_layout)
        self.server_running = False

        self.server_button = QPushButton("Start the server")

        self.server_button.clicked.connect(self.toggle_server)

        self.server_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {FRAME_COLOR};
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }}

            QPushButton:hover {{
                background-color: #ffd96f;
            }}
        """)

        self.server_ip = QLabel("IP : 192.168.1.42")

        self.server_ip.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
        """)

        fight_frame = QFrame()

        fight_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {FRAME_COLOR};
                border-radius: 10px;
            }}
        """)

        fight_layout = QVBoxLayout()
        fight_title = QLabel("Ongoing Fight")
        fight_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fight_label = QLabel("Marty  VS  Atlas")
        self.fight_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fight_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
        """)

        fight_layout.addWidget(fight_title)
        fight_layout.addWidget(self.fight_label)
        fight_frame.setLayout(fight_layout)
        logs_frame = QFrame()
        logs_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {FRAME_COLOR};
                border-radius: 10px;
            }}
        """)

        logs_layout = QVBoxLayout()
        logs_title = QLabel("Logs")
        self.logs = QTextEdit()
        self.logs.setReadOnly(True)
        self.logs.setStyleSheet("""
            background-color: black;
            border: none;
        """)

        self.logs.append("[INFO] Interface started")

        logs_layout.addWidget(logs_title)
        logs_layout.addWidget(self.logs)
        logs_frame.setLayout(logs_layout)

        grid.addWidget(self.logo, 0, 0)
        grid.addWidget(self.server_button, 0, 1)

        grid.addWidget(self.robot_count, 1, 0)
        grid.addWidget(self.server_ip, 1, 1)

        grid.addWidget(
            robot_frame,
            2, 0,
            2, 1
        )

        grid.addWidget(
            fight_frame,
            2, 1
        )

        grid.addWidget(
            logs_frame,
            3, 1
        )

        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        grid.setRowStretch(2, 1)
        grid.setRowStretch(3, 2)

    def add_log(self, message):
        self.logs.append(message)

    def toggle_server(self):
            self.server_running = not self.server_running
            if self.server_running:
                self.server_button.setText("Stop the server")
                self.server_thread = ServerThread()
                self.server_thread.log_signal.connect(self.add_log)
                self.server_thread.start()
            else:
                self.server_button.setText("Start the server")
                if self.server_thread:
                    self.server_thread.stop_server()
                    self.server_thread.wait()
                self.logs.append("[INFO] Server stopped")
            
app = QApplication([])
window = MainWindow()


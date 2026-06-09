from PyQt6.QtCore import QThread, pyqtSignal

class ConnexionRefWorker(QThread):
    is_connected = pyqtSignal(bool)

    def __init__(self, robot_client):
        super().__init__()
        self.client = robot_client

    def run(self):
        self.is_connected.emit(self.client.connect())
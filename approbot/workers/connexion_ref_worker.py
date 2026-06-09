from PyQt6.QtCore import QThread, pyqtSignal

class ConnexionRefWorker(QThread):
    is_connected = pyqtSignal(bool)
    is_live = pyqtSignal(bool)

    def __init__(self, robot_client, check_live = False):
        super().__init__()
        self.client = robot_client
        self.check_live = check_live

    def run(self):

        if self.check_live:
            self.is_live.emit(self.client.is_server_live())
        else:
            self.is_connected.emit(self.client.connect())
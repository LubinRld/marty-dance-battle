from PyQt6.QtCore import QThread, pyqtSignal

class RefDisconnexionWorker(QThread):
    is_disconnected = pyqtSignal(bool)

    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):
        self.is_disconnected.emit(self.client.disconnect())
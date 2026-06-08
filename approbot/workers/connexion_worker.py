from PyQt6.QtCore import QThread, pyqtSignal

class ConnexionWorker(QThread):
    is_connected = pyqtSignal(bool)
    def __init__(self, marty_controller, ip):
        super().__init__()
        self.marty = marty_controller
        self.ip = ip
    
    def run(self):
            self.is_connected.emit(self.marty.connect(self.ip))
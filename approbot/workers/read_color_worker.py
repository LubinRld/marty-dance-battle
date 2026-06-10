from PyQt6.QtCore import QThread, pyqtSignal

class ReadColorWorker(QThread):
    color_read_signal = pyqtSignal(str)

    def __init__(self, marty_controller):
        super().__init__()
        self.marty = marty_controller

    def run(self):
        self.color_read_signal.emit(self.marty.get_actual_color_name())
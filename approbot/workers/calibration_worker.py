from PyQt6.QtCore import QThread, pyqtSignal

class CalibrationWorker(QThread):

    is_calibration_done = pyqtSignal(bool)

    def __init__(self, marty_controller, color_name):
        super().__init__()
        self.marty = marty_controller
        self.color_name = color_name

    def run(self):
        self.is_calibration_done.emit(self.marty.calibrate_color(self.color_name))
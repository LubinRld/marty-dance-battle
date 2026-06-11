from PyQt6.QtCore import QThread, pyqtSignal

class RefreshStatusWorker(QThread):
    status_updated_signal = pyqtSignal(tuple)

    def __init__(self, marty_controller):
        super().__init__()
        self.marty = marty_controller

    def run(self):
        color = self.marty.get_actual_color_name()
        if not color:
            color = None
        
        battery_percentage = self.marty.get_battery_level()
        if battery_percentage is None:
            battery_percentage = 0
        
        self.status_updated_signal.emit((color, battery_percentage))
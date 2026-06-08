from PyQt6.QtCore import QThread, pyqtSignal

class MovementWorker(QThread):
    def __init__(self, marty_controller, action_code, nbr_action=1):
        super().__init__()
        self.marty=marty_controller
        self.action_code = action_code
        self.nbr_action = nbr_action
    
    def run(self):
        self.marty.execute_action(self.action_code,self.nbr_action)
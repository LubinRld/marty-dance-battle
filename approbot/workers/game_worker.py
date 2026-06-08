from PyQt6.QtCore import QThread, pyqtSignal

class GameWorker(QThread):
    game_over_signal = pyqtSignal()

    def __init__(self, manager):
        super().__init__()
        self.manager = manager
    def run(self):
        self.manager.play_game()
        self.game_over_signal.emit()


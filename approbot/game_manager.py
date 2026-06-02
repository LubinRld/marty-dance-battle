import robot_controller
import robot_client
import read_dance

class GameManager:
    def __init__(self, robot_controller:robot_controller.RobotController, robot_client:robot_client.RobotClient, dance_reader:read_dance.ReadDance):
        self.robot = robot_controller
        self.client=  robot_client
        self.reader = dance_reader
        self.moves = []
        self.acts = {}

    def prepare_game(self, ip_adress):
        self.robot.connect(ip_adress)
        self.moves = self.reader.getMovement()
        self.acts = self.reader.getAct()
        if(self.robot.is_connected and self.client.connect()):
            return True
        else:
            return False


        
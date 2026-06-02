import robot_controller
import robot_client
import read_dance
import time

class GameManager:
    def __init__(self, robot_controller:robot_controller.RobotController, robot_client:robot_client.RobotClient, dance_reader:read_dance.ReadDance):
        self.robot = robot_controller
        self.client=  robot_client
        self.reader = dance_reader
        self.moves = []
        self.acts = {}
        self.color_traduction = {
            "Black" : "N",
            "Purple" : "P",
            "Dark Blue" : "B",
            "Yellow" : "Y",
            "Cyan" : "C",
            "Green" : "G",
            "Red":"R"
            }

    def prepare_game(self, ip_adress):
        self.robot.connect(ip_adress)
        self.moves = self.reader.getMovement()
        self.acts = self.reader.getAct()
        if(self.robot.is_connected and self.client.connect()):
            return True
        else:
            return False
        
    def play_game(self):
        max_moves = self.client.start()
        given_moves = len(self.moves)
        for i in range(max_moves):
            index_move = i%given_moves
            nbr_action, action_code = self.moves[index_move]
            self.robot.execute_action(action_code,nbr_action)
            time.sleep(2.5)
            arm_action = None
            exp_action = None
            color = self.robot.get_actual_color_name()
            color_translated = self.color_traduction.get(color, color)
            if color_translated in self.acts:
                for act in self.acts[color_translated]:
                    self.robot.execute_action(act)
                    if "AL" in act or "AR" in act:
                        arm_action=act
                    elif "X" in act:
                        exp_action=act
            points = self.client.step(color_translated,arm_action,exp_action)
            print(f"This step gave {points} points")
        total_points = self.client.get_score()
        print(f"Congrats, you won a total of {total_points} points!")

    def end_game(self):
        self.client.disconnect()
        self.robot.disconnect()
        
        

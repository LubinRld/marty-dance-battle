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
        #self.robot.calibrate_color()
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
            self.robot._reset_position()
            self.robot.execute_action(action_code,nbr_action)
            time.sleep(2.5)
            arm_action = []
            exp_action = "None"
            color = self.robot.get_actual_color_name()
            color_translated = self.color_traduction.get(color, color)
            if color_translated in self.acts:
                arms_to_do = []
                exp_to_do = None

                for act in self.acts[color_translated]:
                    if "AL" in act or "AR" in act:
                        arm_action.append(act)
                        arms_to_do.append(act)
                    elif "X" in act:
                        exp_action=act
                        exp_to_do = act
                for act in arms_to_do:
                    self.robot.execute_action(act)

                if len(arms_to_do)>0:
                    time.sleep(1.2)
                    self.robot._reset_position()
                if exp_to_do is not None:
                    self.robot.execute_action(exp_to_do)

            if(len(arm_action)==0):
                arm_action_translated="None"
            elif(len(arm_action)==1):
                arm_action_translated = arm_action[0]
            elif(len(arm_action)==2):
                arm_action_translated = arm_action[0] + "+" + arm_action[1]
            points = self.client.step(color_translated,arm_action_translated,exp_action)
            print(f"This step gave {points} points")
        total_points = self.client.get_score()
        print(f"Congrats, you won a total of {total_points} points!")

    def end_game(self):
        self.client.disconnect()
        self.robot.disconnect()
        
        

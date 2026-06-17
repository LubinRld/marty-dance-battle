import config
import time

class GameManager:
    def __init__(self, robot_controller, robot_client, dance_reader):
        self.robot = robot_controller
        self.client=  robot_client
        self.reader = dance_reader
        self.moves = self.reader.getMovement()
        self.acts = self.reader.getAct()
        self.color_traduction = config.COLOR_TRANSLATION.copy()

    def play_game(self):
        try:
            max_moves = self.client.start()
        except Exception as ref_error:
            print("Connexion lost with ref")
            return
        given_moves = len(self.moves)
        for i in range(max_moves):
            index_move = i%given_moves
            nbr_action, action_code = self.moves[index_move]
            try:
                self.robot._reset_position()
                self.robot.execute_action(action_code,nbr_action)
                time.sleep(2.5)
                arm_action = []
                exp_action = "None"
                color = self.robot.get_actual_color_name()
                color_translated = self.color_traduction.get(color, color)#si il connait pas color, il renvoie par défaut color
                if color_translated in self.acts:
                    for act in self.acts[color_translated]:
                        if "AL" in act or "AR" in act:
                            arm_action.append(act)
                        elif "X" in act:
                            exp_action=act
                    for act in arm_action:
                        self.robot.execute_action(act)

                    if len(arm_action)>0:
                        time.sleep(1.2)
                        self.robot._reset_position()
                    if exp_action != "None":
                        self.robot.execute_action(exp_action)
            except Exception as robot_error:
                print("Connexion lost with Marty")
                break

            if(len(arm_action)==0):
                arm_action_translated="None"
            elif(len(arm_action)==1):
                arm_action_translated = arm_action[0]
            elif(len(arm_action)==2):
                arm_action_translated = arm_action[0] + "+" + arm_action[1]

            try:
                points = self.client.step(color_translated,arm_action_translated,exp_action)
                print(f"This step gave {points} points")
            except Exception as ref_error:
                print("Connexion lost with ref")
                break
        try:
            total_points = self.client.get_score()
            print(f"Congrats, you won a total of {total_points} points!")
        except Exception as ref_error:
            print("Connexion lost with ref")


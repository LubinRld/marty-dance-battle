from martypy import Marty

class RobotController:

    def __init__(self):
        self.robot = None
        self.is_connected=False

    def connect(self, ip_address):
        try:
            self.robot=Marty("wifi", ip_address)
            self.is_connected=True
            print("The robot is connected")
            print(Marty.JOINT_IDS)
        except Exception as e:
            print(f"Connection failed : {e}")
            self.is_connected=False
    
    def execute_action(self, actionCode, nbrAction=None):
        if self.is_connected==False or self.robot is None:
            print(f"The robot is not connected, you can't do the movement code : {actionCode}")
            return False
        if actionCode == "U":
            self._reset_position()
            self._step("forward", nbrAction)
        elif actionCode == "B":
            self._reset_position()
            self._step("backward", nbrAction)
        elif actionCode == "L":
            self._reset_position()
            self._step("left", nbrAction)
        elif actionCode == "R":
            self._reset_position()
            self._step("right", nbrAction)
        elif actionCode == "ARU":
            self._move_arm("right", 100)
        elif actionCode == "ARB":
            self._move_arm("right", -100)
        elif actionCode == "ALU":
            self._move_arm("left", 100)
        elif actionCode == "ALB":
            self._move_arm("left", -100)
        elif actionCode == "XNG":
            self._eye_expression("angry")
        elif actionCode == "XNT":
            self._eye_expression("normal")
        else:
            print(f"the action code you filled : {actionCode} doesn't exist")
            return False

    def disconnect(self):
        if self.is_connected and self.robot != None:
            self.robot.close()
            self.is_connected=False
            print("The robot is disconnected")

    def _move_arm(self, side, angle, _move_time=1500):
        if side == "left":
            self.robot.move_joint("left arm",angle, _move_time)
        elif side == "right":
            self.robot.move_joint("right arm", angle, _move_time)
        else:
            print(f"move_arm: the only direction known is left or right, or, you indicated {side}")
        
    def _step(self, direction, step_number, _move_time=1500):
        if direction == "forward":
            self.robot.walk(step_number, move_time=_move_time)
        elif direction == "backward":
            self.robot.walk(step_number, step_length=-25, move_time=_move_time)
        elif direction == "left" or direction == "right":
            self.robot.sidestep(direction,step_number,move_time= _move_time)
        else:
            print(f"step: the only direction known is forward, backward, left or right or, you indicated {direction}")

    def _eye_expression(self, emotion):
        valid_emotion = {"angry", "excited", "normal", "wide", "wiggle"}
        if emotion in valid_emotion:
            self.robot.eyes(emotion)
        else:
            print(f"eye_expression: the only valid expressions are {valid_emotion} or you indicated {emotion}")
        
    def _reset_position(self):
        self.robot.stand_straight()



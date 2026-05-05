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
        except Exception:
            print(f"Connection failed : {Exception}")
            self.is_connected=False
    

    def deconnect(self):
        if(self.is_connected and self.robot != None):
            self.robot.close()
            self.is_connected=False
            print("The robot is disconnected")

    def move_arm(self, side, angle):
        if side == "left":
            self.robot.arms(angle, 0, 500)
        elif side == "right":
            self.robot.arms(0, angle, 500)
        
    def step(self, direction, step_number):
        if direction == "forward":
            self.robot.walk(step_number)
        elif direction == "backward":
            self.robot.walk(step_number, step_length=-25)
        elif direction == "left" or direction == "right":
            self.robot.sidestep(direction,step_number)
        else:
            print("the only direction known is forward, backward, left or righ")

    

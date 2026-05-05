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

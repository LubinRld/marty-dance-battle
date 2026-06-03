from martypy import Marty
import time

class RobotController:

    def __init__(self):
        self.robot = None
        self.is_connected=False
        self.color_references = {"Black" : (122,22,32), 
                                 "Purple" : (47,45,41),
                                 "Dark Blue" : (75,80,108),
                                 "Yellow" : (278,113,81),
                                 "Cyan" : (141,32,55),
                                 "Green" : (255,255,255),
                                 "Red" : (255,0,0)}

    def connect(self, ip_address):
        try:
            self.robot=Marty("wifi", ip_address)
            self.is_connected=True
            print("The robot is connected")
            #print(Marty.JOINT_IDS)
            #print(self.robot.get_add_ons_status())
        except Exception as e:
            print(f"Connection failed : {e}")
            self.is_connected=False
    
    def _check_connexion(self):
        if self.is_connected==False or self.robot is None:
            return False
        return True

    def get_battery_level(self):
        if not self._check_connexion():
             print("Cannot get battery level : the robot is not connected")
             return None
        try:
            battery_level = self.robot.get_battery_remaining()
            return battery_level
        except Exception as e:
            print(f"Error reading battery : {e}")
            return None

    def _read_RGB_color(self, sensor_name = 'left'):
        if not self._check_connexion():
            print("Cannot read color, robot is not connected")
            return None
        
        red = self.robot.get_color_sensor_value_by_channel(sensor_name, "red")
        green = self.robot.get_color_sensor_value_by_channel(sensor_name, "green")
        blue = self.robot.get_color_sensor_value_by_channel(sensor_name, "blue")

        if red is not None and green is not None and blue is not None:
            print(f"Colors read : Red:{red}, Green:{green}, Blue:{blue}")
            return (red,green,blue)
        else:
            print("The sensor didn't work")
            return None
    
    def get_actual_color_name(self):
        RGB_measure = self._read_RGB_color()
        if RGB_measure is None:
            return "Sensor didn't work"
        
        def distance(color_ref):
            distance = ((color_ref[0]-RGB_measure[0])**2+
                        (color_ref[1]-RGB_measure[1])**2+
                        (color_ref[2]-RGB_measure[2])**2)
            return distance
        color_name = min(self.color_references.keys(), key=lambda color: distance(self.color_references[color]))
        return color_name

    def calibrate_color(self, sensor_name="left"):
        if not self._check_connexion():
            print("Cannot calibrate: the robot is not connected")
            return

        colors_to_calibrate = ["Black","Purple","Dark Blue","Yellow","Cyan", "Green", "Red"] #A REMPLIR
        
        print("====Calibrating colors====\n")

        for color in colors_to_calibrate:
            input(f"Place Marty's left foot on the {color}, then press entry")
            red_measures = []
            green_measures = []
            blue_measures = []

            print(f"Color :{color} acquisition...")
            for i in range(10):
                measure = self._read_RGB_color(sensor_name=sensor_name)
                if measure is not None:
                    red_measures.append(measure[0])
                    green_measures.append(measure[1])
                    blue_measures.append(measure[2])
                time.sleep(0.1)
            measure_number=len(red_measures)
            if measure_number>0:
                red_mean=sum(red_measures)//measure_number
                green_mean=sum(green_measures)//measure_number
                blue_mean=sum(blue_measures)//measure_number
                self.color_references[color]=(red_mean, green_mean, blue_mean)
                print(f"{color} updated : {self.color_references[color]}")
            else:
                print(f"Error, A problem happenned while calibrating the color : {color}. Please try again")


    def execute_action(self, actionCode, nbrAction=None):
        if not self._check_connexion():
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
        return True

    def disconnect(self):
        if self._check_connexion():
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

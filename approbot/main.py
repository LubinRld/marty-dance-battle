import robot_controller
import robot_client
import time
def main():

    
    my_robot_client = robot_client.RobotClient()
    my_robot_client.connect()

    """"
    ip_adress_1 = "192.168.0.105"

    my_robot = robot_controller.RobotController()
    my_robot.connect(ip_adress_1)
    my_robot.calibrate_color()
    my_robot.execute_action("U",2)
    time.sleep(2)
    
    if(my_robot.get_actual_color_name() == "Blue"):
        my_robot.execute_action("ARU")
        my_robot.execute_action("ALB")
        my_robot.execute_action("XNG")

    my_robot.execute_action("L",2)
    time.sleep(2)

    if(my_robot.get_actual_color_name() == "Black"):
        my_robot.execute_action("ARB")
        my_robot.execute_action("ALU")
        my_robot.execute_action("XNT")

    print(my_robot.get_battery_level())
    my_robot.disconnect()
    """
if __name__ == "__main__":
    main()
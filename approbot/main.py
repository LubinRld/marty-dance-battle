import robot_controller

def main():

    ip_adress_1 = "192.168.0.103"

    my_robot = robot_controller.RobotController()

    my_robot.connect(ip_adress_1)

    my_robot.execute_action("U",2)
    my_robot.execute_action("ARU")
    my_robot.execute_action("ALB")
    my_robot.execute_action("XNG")
    my_robot.execute_action("L",2)
    my_robot.execute_action("ARB")
    my_robot.execute_action("ALU")
    my_robot.execute_action("XNT")


    my_robot.disconnect()

if __name__ == "__main__":
    main()
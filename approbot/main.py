import robot_controller

def main():

    ip_adress_1 = "192.168.1.1"
    ip_address_2 = "192.168.1.2"

    my_robot = robot_controller.RobotController()
    my_second_robot = robot_controller.RobotController()

    my_robot.connect(ip_adress_1)
    my_second_robot.connect(ip_address_2)

    my_robot.move_arm("left", 100)
    my_robot.move_arm("right", -100)
    my_robot.step("forward", 2)
    my_robot.step("left", 1)

if __name__ == "__main__":
    main()
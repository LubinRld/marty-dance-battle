import robot_controller
import robot_client
import read_dance
import game_manager
def main():

    my_client = robot_client.RobotClient()
    my_robot = robot_controller.RobotController()
    my_reader = read_dance.ReadDance("approbot/example.dance")

    my_manager = game_manager.GameManager(my_robot,my_client,my_reader)
    my_manager.prepare_game("192.168.1.5")
    my_manager.play_game()
    my_manager.end_game()
    
    
if __name__ == "__main__":
    main()
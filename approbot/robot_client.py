import time
import requests

class RobotClient:
    def __init__(self, host="localhost", port=8000):
        self.url = f"http://{host}:{port}"
        self.rid = None
    
    def connect(self):
        url = f"{self.url}/hello"
        try:
            response = requests.post(url)
            if response.status_code == 200:
                self.rid = response.json()
                print(f"Robot connected! ID is {self.rid}")
                return True
            else:
                print(f"Connexion error : {response.status_code}")
                return False
        except Exception as e:
            print("Can't connect to the server")
            return False
        
    
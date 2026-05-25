import time
import requests

class RobotClient:
    def __init__(self, host="localhost", port=8000):
        self.url = f"http://{host}:{port}"
        self.rid = None
    
    def connect(self):
        url_hello = f"{self.url}/hello"
        try:
            response = requests.post(url_hello)
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
        
    def disconnect(self):
        url_bye = f"{self.url}/bye"
        payload  = {"rid": self.rid}
        try:
            response = requests.post(url_bye, json = payload)
            if response.status_code == 200:
                print("Robot successfully disconnected")
            else:
                print("A problem occured during disconnection")
        except Exception as e:
            print (f"Can't connect to the server : {e}")    
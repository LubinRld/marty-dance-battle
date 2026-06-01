import time
import requests

ping = "10.113.26.100"

class RobotClient:
    def __init__(self, host="localhost", port=8000):
        self.url = f"http://{host}:{port}"
        self.rid = None
    
    def is_server_live(self):
        url_server_live = f"{self.url}/"
        try:
            response = requests.get(url_server_live)
            if(response.json() == "1.2"):
                return True
            else:
                return False
        except Exception as e:
            print(f"An error occured: {e}")
            return False



    def connect(self):
        url_hello = f"{self.url}/hello"
        try:
            request = requests.post(url_hello)
            if request.status_code == 200:
                self.rid = request.json()
                print(f"Robot connected! ID is {self.rid}")
                return True
            else:
                print(f"Connexion error : {request.status_code}")
                return False
        except Exception as e:
            print("Can't connect to the server")
            return False
        
    def disconnect(self):
        url_bye = f"{self.url}/bye"
        payload  = {"rid": self.rid}
        try:
            request = requests.post(url_bye, json = payload)
            if request.status_code == 200:
                print("Robot successfully disconnected")
            else:
                print("A problem occured during disconnection")
        except Exception as e:
            print (f"Can't connect to the server : {e}")    

    def start(self):
        url_start = f"{self.url}/start"
        payload = {"rid":self.rid}
        try:
            request = requests.post(url_start, json=payload)
            if request.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            print (f"can't connect to the server : {e}")

    def get_score(self):
        url_score = f"{self.url}/score"
        payload = {"rid":self.rid}
        try:
            response = requests.get(url_score, params=payload)
            if response.status_code == 200 and response.json is not None:
                return response.json()
            else:
                print(f"didn't work : {response.json()}")
        except Exception as e:
            print (f"Can't connect to the server : {e}")

    def step(self, col, arm, exp):
        url_step = f"{self.url}/step"
        payload = {"rid":self.rid,
                   "col":col,
                   "arm":arm,
                   "exp":exp}
        try:
            request = requests.post(url_step, json=payload)
            if(request.status_code == 200 and request.json() is not None):
                return request.json()
            else:
                print(f"didn't work: {request.json()}")
        except Exception as e:
            print(f"Error : {e}")


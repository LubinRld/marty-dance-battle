from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import uuid
from urllib.parse import urlparse, parse_qs
from battle import Battle


SERVER_VERSION = "1.2"
MAX_MOVES = 10

battle = Battle()
battle.load_file("appserver/example.battle")
log_callback = None
robots = {}
scores = {}

def add_log(message):
    print(message)

    if log_callback:
        log_callback(message)

class RequestHandler(BaseHTTPRequestHandler):

    def send_json(self, data, status=200):

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def read_json(self):

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        return json.loads(body.decode("utf-8"))

    def do_GET(self):

        parsed = urlparse(self.path)
    
        if parsed.path == "/":
            self.send_json(SERVER_VERSION)

        elif parsed.path == "/score":
            params = parse_qs(parsed.query)
            rid = params.get("rid", [None])[0]
            if rid not in scores:
                self.send_json({"error": "unknown robot"},404)
                return

            self.send_json(scores[rid])

        else:

            self.send_json({"error": "unknown way"},404)


    def do_POST(self):

        if self.path == "/hello":
            rid = str(uuid.uuid4())[:6].upper()
            robots[rid] = {"connected": True}
            scores[rid] = 0
            add_log(f"[HELLO] {rid}")
            self.send_json(rid)

        elif self.path == "/start":
            data = self.read_json()
            rid = data.get("rid")
            if rid not in robots:
                self.send_json({"error": "unknown robot"},404)
                return

            moves = battle.max_moves
            add_log(f"[START] {rid} -> {moves}")
            self.send_json(moves)

        elif self.path == "/step":
            data = self.read_json()
            rid = data.get("rid")
            col = data.get("col")
            arm = data.get("arm")
            exp = data.get("exp")

            if rid not in robots:
                self.send_json({"error": "unknown robot"},404)
                return

            points = battle.compute_points(col,arm,exp)
            scores[rid] += points
            add_log(
                f"[STEP] {rid} "
                f"col={col} "
                f"arm={arm} "
                f"exp={exp} "
                f"=> {points}"
            )

            self.send_json(points)

        elif self.path == "/bye":
            data = self.read_json()
            rid = data.get("rid")
            if rid in robots:
                robots[rid]["connected"] = False

            add_log(f"[BYE] {rid}")
            self.send_json({"status": "ok"})

        else:
            self.send_json({"error": "unknown route"},404)
    
        


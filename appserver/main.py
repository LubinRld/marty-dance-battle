import server 

HOST = "0.0.0.0"
PORT = 8000

myserver = None

def run():

    global myserver

    myserver = server.HTTPServer((HOST, PORT),server.RequestHandler)
    print(f"Server running on {HOST}:{PORT}")
    server.battle.print_rules()
    myserver.serve_forever()


def stop():
    global myserver
    if myserver:
        myserver.shutdown()
        myserver.server_close()
        myserver = None
import server 

HOST = "0.0.0.0"
PORT = 8000

def run():

    myserver = server.HTTPServer((HOST, PORT),server.RequestHandler)
    print(f"Server running on {HOST}:{PORT}")
    server.battle.print_rules()
    myserver.serve_forever()


if __name__ == "__main__":
    run()
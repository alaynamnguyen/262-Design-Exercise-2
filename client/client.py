import socket
import configparser
from controller import client_login, accounts
import json

# Load config
config = configparser.ConfigParser()
config.read("config.ini")

HOST = config["network"]["host"]
PORT = int(config["network"]["port"])

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        client_login.login_user(sock)
        print("Connected to the server. Type 'count <words>' or 'translate <word>'")
        
        while True:
            message = input("> ")
            if message.lower() == "exit":
                break
            elif message.startswith("list-accounts"):
                _, *wildcard = message.split()
                wildcard = wildcard[0] if wildcard else "*"
                print("Wildcard:", wildcard)
                accounts.list_accounts(sock, wildcard)
                # request = {"task": "list-accounts", "wildcard": wildcard}
                # sock.sendall(json.dumps(request).encode("utf-8"))
            else:
                sock.sendall(message.encode("utf-8"))
            # TODO modify this part to send back task structured messages
            # sock.sendall(message.encode("utf-8"))
            # response = sock.recv(1024).decode("utf-8")
            # print("Server response:", response)

if __name__ == "__main__":
    main()

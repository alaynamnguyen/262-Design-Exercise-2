import socket
import configparser
from controller import communication, login

# Load config
config = configparser.ConfigParser()
config.read("config.ini")

HOST = config["network"]["host"]
PORT = int(config["network"]["port"])

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        login.login_user(sock)
        print("Connected to the server. Type 'count <words>' or 'translate <word>'")
        
        while True:
            message = input("> ")
            if message.lower() == "exit":
                break
            # TODO modify this part to send back task structured messages
            sock.sendall(message.encode("utf-8"))
            response = sock.recv(1024).decode("utf-8")
            print("Server response:", response)

if __name__ == "__main__":
    main()

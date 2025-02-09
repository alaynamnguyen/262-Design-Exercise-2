import socket
import configparser
from controller import client_login, accounts, communication, client_messages
from datetime import datetime

# Load config
config = configparser.ConfigParser()
config.read("config.ini")

HOST = config["network"]["host"]
PORT = int(config["network"]["port"])

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        client_uid = client_login.login_user(sock)
        print(f"{client_uid} connected to the server. Type 'count <words>' or 'translate <word>'")
        
        while True:
            message = input("> ")
            if message.lower() == "exit":
                break
            elif message.startswith("list-accounts"):
                _, *wildcard = message.split()
                wildcard = wildcard[0] if wildcard else "*"
                accounts.list_accounts(sock, wildcard)
            elif message.startswith("send-message"):
                _, receiver, *text = message.split()
                text = " ".join(text)
                print("Sending message:", text)
                communication.build_and_send_task(sock, "send-message", sender=client_uid, receiver=receiver, text=text, timestamp=str(datetime.now()))
                # TODO: Receiver show "Received page" and call list-messages, sender return back to "Received page".
            elif message.startswith("get-sent-messages"):
                communication.build_and_send_task(sock, "get-sent-messages", sender=client_uid)
            elif message.startswith("get-received-messages"):
                communication.build_and_send_task(sock, "get-received-messages", sender=client_uid)
            elif message.startswith("delete-messages"):
                _, *mids = message.split()
                mids = [int(mid) for mid in mids] # TODO: later sub this with mids of selected messages from UI
                client_messages.delete_messages(sock, mids)
            elif message.startswith("delete-account"):
                success = accounts.delete_account(sock, client_uid)
                if success:
                    print("Account successfully deleted.")
                    break
            else:
                print("Invalid command. Please try again.")
                # sock.sendall(message.encode("utf-8"))

if __name__ == "__main__":
    main()

# send-message alayna helloooooooo
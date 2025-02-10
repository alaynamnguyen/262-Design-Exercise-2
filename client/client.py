import socket
import configparser
from controller import client_login, accounts, communication, client_messages
from datetime import datetime

# Load config
config = configparser.ConfigParser()
config.read("config.ini")

HOST = config["network"]["host"]
PORT = int(config["network"]["port"])

def print_help():
    """
    Prints a list of available commands and their descriptions.
    """
    help_text = """
Available Commands:
-------------------
help                        - Show this help message
exit                        - Disconnect from the server and exit
list-accounts [wildcard]    - List all accounts (optionally filtered by wildcard)
send-message <user> <text>  - Send a message to a user
get-sent-messages           - Retrieve messages you have sent
get-received-messages       - Retrieve messages you have received
delete-messages <ids>       - Delete messages by message IDs
delete-account              - Delete your account and exit
"""
    print(help_text)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        client_uid = client_login.cli_login(sock)
        print(f"{client_uid} connected to the server. Type 'help' for a list of commands.")
        
        while True:
            message = input("> ")
            if message.lower() == "exit":
                break
            elif message.lower() == "help":
                print_help()
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
                # TODO: restrict sending messages to only active users (UI side)
            elif message.startswith("get-sent-messages"):
                communication.build_and_send_task(sock, "get-sent-messages", sender=client_uid)
            elif message.startswith("get-received-messages"):
                communication.build_and_send_task(sock, "get-received-messages", sender=client_uid)
            elif message.startswith("get-message-by-mid"):
                _, mid = message.split()
                communication.build_and_send_task(sock, "get-message-by-mid", mid=mid)
            elif message.startswith("mark-message-read"):
                _, mid = message.split()
                client_messages.mark_message_read(sock, mid)
            elif message.startswith("delete-messages"):
                _, *mids = message.split() # TODO: later sub this with mids of selected messages from UI
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
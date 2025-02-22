import grpc
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import chat_pb2
import chat_pb2_grpc
from concurrent import futures
import json
import hashlib
import configparser
from controller.login import check_username_exists, check_username_password, create_account
from controller.accounts import list_accounts, delete_account
from model import User, Message
from utils import dict_to_object_recursive, object_to_dict_recursive, parse_request, send_response

# Load config
config = configparser.ConfigParser()
config.read("config.ini")

HOST = config["network"]["host"]
PORT = int(config["network"]["port"])

# Message dict
# TODO stick into function later
messages_dict = dict()
with open("server/test/message.json", "r") as f:
    messages = json.load(f)
for k, v in messages.items():
    message = dict_to_object_recursive(v, Message)
    messages_dict[message.mid] = message

def load_users():
    """Loads user data from the JSON file."""
    # User dict
    users_dict = dict()
    with open("server/test/user.json", "r") as f:
            users = json.load(f)
    for k, v in users.items():
        user = dict_to_object_recursive(v, User)
        users_dict[user.uid] = user
    return users_dict

def save_users(users_dict):
    """Saves user data to the JSON file."""
    with open("server/test/user.json", "w") as f:
        json.dump(users_dict, f, default=object_to_dict_recursive, indent=4)

def hash_password(password):
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

class ChatService(chat_pb2_grpc.ChatServiceServicer):
    
    def __init__(self):
        self.users_dict = load_users()

    def LoginUsername(self, request, context):
        """Handles username lookup to check if a user exists."""
        print("Calling LoginUsername")
        username = request.username
        user_exists = check_username_exists(username, self.users_dict) is not None
        return chat_pb2.LoginUsernameResponse(user_exists=user_exists, username=username)

    def LoginPassword(self, request, context):
        """Handles login by verifying the hashed password."""
        print("Calling LoginPassword")
        username = request.username
        password = request.password

        uid = check_username_exists(username, self.users_dict)
        if uid: # Existing account
            print(f'Existing account: {uid}')
            print("Password is correct:",check_username_password(uid, password, self.users_dict))
            if check_username_password(uid, password, self.users_dict): # Password is correct
                return chat_pb2.LoginPasswordResponse(success=True, uid=uid)
            else: # Password incorrect
                return chat_pb2.LoginPasswordResponse(success=False, uid=uid)
        else: # Create account
            print('Running create account')
            uid = create_account(username, password, self.users_dict)
            return chat_pb2.LoginPasswordResponse(success=True, uid=uid)
        
    def ListAccounts(self, request, context):
        wildcard = request.wildcard
        accounts = list_accounts(self.users_dict, wildcard=wildcard)
        return chat_pb2.LoginPasswordResponse(accounts=accounts)
    
    def SendMessage(self, request, context):
        pass
        




    
def serve():
    """Starts the gRPC server with only login flow."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    server_address = f"{HOST}:{PORT}"  # Use HOST and PORT from config.ini
    server.add_insecure_port(server_address)
    server.start()
    print(f"Server Proto started on port {PORT}...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
import json
from model import User

def check_username_exists(username: str, accounts_dict: dict):
    print("Calling check_username_exists")
    for uid, info in accounts_dict.items():
        if info["username"] == username:
            return uid
    return None

def check_username_password(uid: str, password: str, accounts_dict: dict):
    print("Calling check_username_password")
    return accounts_dict[uid]["password"] == password

def create_account(username: str, password: str, accounts_dict: dict, users: list):
    print("Calling create_account")
    if check_username_exists(username, accounts_dict):
        return None

    user = User(username, password) 
    users.append(user)
    accounts_dict[user.uid] = {
        "username": username,
        "password": password
    }
    return user.uid

def handle_login_request(data, message, accounts_dict, users):
    print("Calling handle_login_request")
    response = {}
    if message["task"] == "login-username":
        print("Handling login-username")
        uid = check_username_exists(message["username"], accounts_dict)
        response = {
            "task": "login-username-reply",
            "username": message["username"], # TODO return uid instead?
            "user_exists": uid is not None
        }
    elif message["task"] == "login-password":
        print("Handling login-password")
        
        uid = check_username_exists(message["username"], accounts_dict)
        if uid: # Username exists
            if check_username_password(uid, message["password"], accounts_dict): # Password is correct
                response = {
                    "task": "login-password-reply",
                    "uid": uid,
                    "login_success": True,
                    "unread_messages": ["hey", "hi"]  # Placeholder for unread messages
                }
            else: # Password is incorrect
                response = {
                    "task": "login-password-reply",
                    "uid": uid,
                    "login_success": False,
                    "unread_messages": []
                }
        else: # Username does not exist
            uid = create_account(message["username"], message["password"], accounts_dict, users)
            print("UID:", uid)
            response = {
                "task": "login-password-reply",
                "uid": uid,
                "login_success": True,
                "unread_messages": []
            }

    data.outb += json.dumps(response).encode("utf-8")

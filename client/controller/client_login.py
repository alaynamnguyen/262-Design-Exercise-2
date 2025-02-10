import hashlib
from .communication import build_and_send_task

def hash_password(password):
    """
    Hashes a password using SHA-256.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def check_username(sock, username):
    """
    Checks if the username exists on the server.
    """
    response = build_and_send_task(sock, "login-username", username=username)
    return response["user_exists"]

def login_user(sock, username, password):
    """
    Attempts to log in an existing user.
    """
    hashed_password = hash_password(password)
    response = build_and_send_task(sock, "login-password", username=username, password=hashed_password)
    return response

def create_account(sock, username, password):
    """
    Attempts to create a new account.
    """
    hashed_password = hash_password(password)
    response = build_and_send_task(sock, "login-password", username=username, password=hashed_password)
    return response

def cli_login(sock):
    """
    Handles command-line login.
    """
    while True:
        username = input("Username: ").strip()
        user_exists = check_username(sock, username)

        if user_exists:  # Login with existing account
            print("User exists.")
            while True:
                password = input("Password: ").strip()
                response = login_user(sock, username, password)
                if response["login_success"]:
                    print(f"Login successful. You have {len(response['unread_messages'])} unread messages.")
                    return response["uid"]
                else:
                    print("Incorrect password. Please try again.")
        else:  # Create a new account
            print("Username does not exist. Creating a new account.")
            while True:
                password = input("Create a password: ").strip()
                response = create_account(sock, username, password)
                if response["login_success"]:
                    print("Account created successfully.")
                    return response["uid"]
                else:
                    print("Failed to create account. Please try again.")

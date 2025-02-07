import hashlib
from .communication import build_and_send_task

def hash_password(password):
    """
    Hashes a password using SHA-256.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(sock):
    print("Calling login_user")
    while True:
        username = input("Username: ")
        response = build_and_send_task(sock, "login-username", username=username)

        if response["user_exists"]: # Login with existing account
            print("User exists.")
            while True:
                password = input("Password: ")
                hashed_password = hash_password(password)
                response = build_and_send_task(sock, "login-password", username=username, password=hashed_password)

                if response["login_success"]:
                    print(f"Login successful. You have {len(response['unread_messages'])} unread messages.")
                    return
                else:
                    print("Incorrect password. Please try again.")
        else: # Create a new account
            print("Username does not exist.")
            while True:
                password = input("Create a password: ")
                hashed_password = hash_password(password)
                response = build_and_send_task(sock, "login-password", username=username, password=hashed_password)

                if response["login_success"]:
                    print("Account created successfully.")
                    return
                else:
                    print("Failed to create account. Please try again.")

# def check_username(sock, username):
#     """
#     Checks if the username exists on the server.

#     Args:
#         sock (socket.socket): The socket connected to the server.
#         username (str): The username to check.

#     Returns:
#         dict: The response from the server.
#     """
#     return build_and_send_task(sock, "login-username", username=username)

# def login_user(sock, username, password):
#     """
#     Attempts to log in the user with the given username and password.

#     Args:
#         sock (socket.socket): The socket connected to the server.
#         username (str): The username of the user.
#         password (str): The password of the user.

#     Returns:
#         dict: The response from the server.
#     """
#     hashed_password = hash_password(password)
#     return build_and_send_task(sock, "login-password", username=username, password=hashed_password)

# def create_account(sock, username, password):
#     """
#     Attempts to create a new account with the given username and password.

#     Args:
#         sock (socket.socket): The socket connected to the server.
#         username (str): The username of the user.
#         password (str): The password of the user.

#     Returns:
#         dict: The response from the server.
#     """
#     hashed_password = hash_password(password)
#     return build_and_send_task(sock, "login-password", username=username, password=hashed_password)
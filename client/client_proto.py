import grpc
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import chat_pb2
import chat_pb2_grpc
import configparser
import hashlib
import tkinter as tk
from tkinter import messagebox

# Load config
config = configparser.ConfigParser()
config.read("config.ini")

HOST = config["network"]["host"]
PORT = int(config["network"]["port"])
SERVER_ADDRESS = f"{HOST}:{PORT}"  # Update if needed

def hash_password(password):
    """Hashes a password using SHA-256 before sending to the server."""
    return hashlib.sha256(password.encode()).hexdigest()

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Message App")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.user_exists = False
        self.client_uid = None

        self.create_login_screen()

    def create_login_screen(self):
        """Creates the username entry screen."""
        self.clear_screen()

        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(expand=True)

        tk.Label(self.login_frame, text="Welcome", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self.login_frame, text="Username:", font=("Arial", 12)).pack()

        self.username_entry = tk.Entry(self.login_frame, textvariable=self.username, font=("Arial", 12))
        self.username_entry.pack(pady=5)

        tk.Button(self.login_frame, text="Next", command=self.check_username, font=("Arial", 12)).pack(pady=10)

    def check_username(self):
        """Checks if username is valid and exists, then moves to password entry."""
        username = self.username.get().strip()

        if not username:
            messagebox.showerror("Error", "Username cannot be empty.")
            return
        if "," in username:
            messagebox.showerror("Error", "Username cannot contain commas.")
            return

        with grpc.insecure_channel(SERVER_ADDRESS) as channel:
            stub = chat_pb2_grpc.ChatServiceStub(channel)
            request = chat_pb2.LoginUsernameRequest(username=username)
            response = stub.LoginUsername(request)

        self.user_exists = response.user_exists
        self.create_password_screen()

    def create_password_screen(self):
        """Creates the password entry screen."""
        self.clear_screen()

        self.password_frame = tk.Frame(self.root)
        self.password_frame.pack(expand=True)

        title = "Welcome Back" if self.user_exists else "Create Account"
        tk.Label(self.password_frame, text=title, font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self.password_frame, text="Password:", font=("Arial", 12)).pack()

        self.password_entry = tk.Entry(self.password_frame, textvariable=self.password, show="*", font=("Arial", 12))
        self.password_entry.pack(pady=5)

        tk.Button(self.password_frame, text="Next", command=self.handle_password, font=("Arial", 12)).pack(pady=10)

    def handle_password(self):
        """Handles login process using gRPC."""
        password = self.password.get().strip()
        if not password:
            messagebox.showerror("Error", "Password cannot be empty.")
            return

        username = self.username.get()
        hashed_password = hash_password(password)

        with grpc.insecure_channel(SERVER_ADDRESS) as channel:
            stub = chat_pb2_grpc.ChatServiceStub(channel)
            request = chat_pb2.LoginPasswordRequest(username=username, password=hashed_password)
            
            try:
                response = stub.LoginPassword(request)
                if response.success:
                    self.client_uid = response.uid
                    messagebox.showinfo("Success", "Login successful!")
                    self.load_home_page()
                else:
                    messagebox.showerror("Error", "Incorrect password.")
            except grpc.RpcError as e:
                print(e.details())
                messagebox.showerror("Error", "Login failed. Please check your credentials.")

    def load_home_page(self):
        """Loads the main page after successful login."""
        self.clear_screen()
        tk.Label(self.root, text="Welcome to Chat!", font=("Arial", 16, "bold")).pack(pady=10)

    def clear_screen(self):
        """Clears the screen before rendering new UI elements."""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()

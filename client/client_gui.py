import tkinter as tk
from tkinter import messagebox
import socket
from controller.login import login_user
import configparser

# Load config
config = configparser.ConfigParser()
config.read("../config.ini")

HOST = config["network"]["host"]
PORT = int(config["network"]["port"])

class ClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Client Login")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))  # Adjust the host and port as needed

        self.username_label = tk.Label(root, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        response = login_user(self.sock, username, password)
        if response["login_success"]:
            messagebox.showinfo("Success", f"Welcome back, {username}!")
        else:
            messagebox.showinfo("Info", "Username does not exist. Creating a new account.")
            response = login_user(self.sock, username, password, create_account=True)
            if response["login_success"]:
                messagebox.showinfo("Success", "Account created successfully!")
            else:
                messagebox.showerror("Error", "Failed to create account. Please try again.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientGUI(root)
    root.mainloop()
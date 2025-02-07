import tkinter as tk
from tkinter import messagebox
import socket
from client.controller.client_login import check_username, login_user, create_account
import configparser

# Load config
config = configparser.ConfigParser()
config.read("config.ini")

HOST = config["network"]["host"]
PORT = int(config["network"]["port"])

class ClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Client Login")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))

        self.username_label = tk.Label(root, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        self.check_username_button = tk.Button(root, text="Next", command=self.check_username)
        self.check_username_button.pack()

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()
        self.password_entry.pack_forget()  # Hide password entry initially

        self.login_button = tk.Button(root, text="Login", command=self.prompt_password)
        self.login_button.pack()
        self.login_button.pack_forget()  # Hide login button initially

        self.username = ""

    def check_username(self):
        self.username = self.username_entry.get()
        if not self.username:
            messagebox.showerror("Error", "Please enter a username")
            return

        response = check_username(self.sock, self.username)
        if response["user_exists"]:
            messagebox.showinfo("Info", "Username exists. Please enter your password.")
            self.password_label.pack()
            self.password_entry.pack()
            self.login_button.pack()
        else:
            messagebox.showinfo("Info", "Username does not exist. Please create a password.")
            self.password_label.pack()
            self.password_entry.pack()
            self.login_button.config(text="Create Account", command=self.create_account)
            self.login_button.pack()

    def prompt_password(self):
        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Please enter a password")
            return

        response = login_user(self.sock, self.username, password)
        if response["login_success"]:
            messagebox.showinfo("Success", f"Welcome back, {self.username}! You have {len(response['unread_messages'])} unread messages.")
        else:
            messagebox.showerror("Error", "Incorrect password. Please try again.")
            self.password_entry.delete(0, tk.END)

    def create_account(self):
        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Please enter a password to create an account")
            return

        response = create_account(self.sock, self.username, password)
        if response["login_success"]:
            messagebox.showinfo("Success", "Account created successfully!")
        else:
            messagebox.showerror("Error", "Failed to create account. Please try again.")
            self.password_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientGUI(root)
    root.mainloop()
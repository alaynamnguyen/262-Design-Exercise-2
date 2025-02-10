import tkinter as tk
from tkinter import messagebox, Scrollbar, Canvas, Frame
import socket
import configparser
from controller import client_login, communication, client_messages, accounts
from datetime import datetime

# Load config
config = configparser.ConfigParser()
config.read("config.ini")

HOST = config["network"]["host"]
PORT = int(config["network"]["port"])

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Message App")
        self.root.geometry("600x400")  # Larger window for better UI
        self.root.resizable(False, False)  # Prevent resizing

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.user_exists = False
        self.client_uid = None  # Store user ID after login
        self.selected_messages = set()  # Store selected messages for deletion
        self.selected_recipient = tk.StringVar()  # Store selected recipient for new messages

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
        """Checks if username exists and moves to password entry."""
        username = self.username.get().strip()
        if not username:
            messagebox.showerror("Error", "Username cannot be empty.")
            return

        self.user_exists = client_login.check_username(self.sock, username)
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
        """Handles login or account creation based on user existence."""
        password = self.password.get().strip()
        if not password:
            messagebox.showerror("Error", "Password cannot be empty.")
            return

        username = self.username.get()
        response = client_login.login_user(self.sock, username, password) if self.user_exists else client_login.create_account(self.sock, username, password)

        if response["login_success"]:
            self.client_uid = response["uid"]  # Store user ID
            messagebox.showinfo("Success", "Login successful!" if self.user_exists else "Account created successfully!")
            self.load_home_page()
        else:
            messagebox.showerror("Error", "Incorrect password!" if self.user_exists else "Account creation failed.")

    def load_home_page(self):
        """Loads the main page after successful login."""
        self.clear_screen()
        self.create_nav_buttons()
        
        self.home_frame = tk.Frame(self.root)
        self.home_frame.pack(fill=tk.BOTH, expand=True)
        
        self.load_received_messages()  # Default page

    def create_nav_buttons(self):
        """Creates persistent navigation buttons."""
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(side=tk.TOP, pady=10)

        tk.Button(btn_frame, text="Received", command=self.load_received_messages).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Sent", command=self.load_sent_messages).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="New Message", command=self.load_new_message_page).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete Account", command=self.load_delete_account_page).pack(side=tk.LEFT, padx=5)

    def load_received_messages(self):
        """Fetch and display received messages with scrolling."""
        self.clear_screen()
        self.create_nav_buttons()

        self.home_frame = tk.Frame(self.root)
        self.home_frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas for scrolling
        canvas = Canvas(self.home_frame)
        scrollbar = Scrollbar(self.home_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        response = communication.build_and_send_task(self.sock, "get-received-messages", sender=self.client_uid)
        mids = response["mids"]

        unread_count = 0
        for mid in mids:
            msg_response = communication.build_and_send_task(self.sock, "get-message-by-mid", mid=mid)
            message = msg_response["message"]

            if not message["receiver_read"]:
                unread_count += 1

            self.display_message(scrollable_frame, message, received=True)

        tk.Label(scrollable_frame, text=f"{unread_count} unread messages", font=("Arial", 14, "bold")).pack()

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def display_message(self, parent, message, received=True):
        """Displays a single message in the UI inside a scrollable parent frame."""
        frame = tk.Frame(parent, bg="lightgray", padx=5, pady=5)
        frame.pack(fill=tk.X, pady=5)

        sender = "From" if received else "To"
        status = "🔴" if received and not message["receiver_read"] else ""

        header = f"{status} {sender} {message['sender'] if received else message['receiver']}\n{message['timestamp']}"
        tk.Label(frame, text=header, font=("Arial", 10), bg="lightgray").pack(anchor="w")

        tk.Label(frame, text=message["text"], font=("Arial", 12), bg="white", padx=5, pady=5).pack(fill=tk.X)

    def clear_screen(self):
        """Clears all widgets before switching pages."""
        for widget in self.root.winfo_children():
            widget.destroy()

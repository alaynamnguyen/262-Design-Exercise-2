import tkinter as tk
from tkinter import messagebox, Scrollbar
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

    def load_delete_account_page(self):
        """Loads the delete account confirmation page."""
        self.clear_screen()
        self.create_nav_buttons()

        tk.Button(self.root, text="Confirm Delete Account", command=self.delete_account, bg="red", fg="black", font=("Arial", 14, "bold"), padx=20, pady=10).pack(pady=100)

    def delete_account(self):
        """Deletes the user account."""
        response = accounts.delete_account(self.sock, self.client_uid)
        if response["success"]:
            messagebox.showinfo("Success", "Account successfully deleted.")
            self.create_login_screen()

    def load_new_message_page(self):
        """Loads the new message page with account selection."""
        self.clear_screen()
        self.create_nav_buttons()

        tk.Label(self.root, text="To:", font=("Arial", 12)).pack(pady=5)

        search_frame = tk.Frame(self.root)
        search_frame.pack()

        self.search_entry = tk.Entry(search_frame, font=("Arial", 12))
        self.search_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(search_frame, text="List", command=self.list_accounts).pack(side=tk.LEFT)

        self.recipient_listbox = tk.Listbox(self.root, height=5)
        self.recipient_listbox.pack(pady=5, expand=True, fill=tk.BOTH)

        scrollbar = Scrollbar(self.root)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.recipient_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.recipient_listbox.yview)

        self.message_entry = tk.Text(self.root, height=5, width=50)
        self.message_entry.pack(pady=5)

        tk.Button(self.root, text="Send", command=self.send_message).pack(pady=5)

    def list_accounts(self):
        """Fetches and displays accounts based on wildcard search."""
        wildcard = self.search_entry.get().strip() or "*"
        response = communication.build_and_send_task(self.sock, "list-accounts", wildcard=wildcard)
        self.recipient_listbox.delete(0, tk.END)
        for account in response["accounts"]:
            self.recipient_listbox.insert(tk.END, account)

    def send_message(self):
        """Sends a message to the selected recipient."""
        selected_index = self.recipient_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a recipient.")
            return

        recipient = self.recipient_listbox.get(selected_index)
        message_text = self.message_entry.get("1.0", tk.END).strip()

        if not message_text:
            messagebox.showerror("Error", "Message cannot be empty.")
            return

        communication.build_and_send_task(self.sock, "send-message", sender=self.client_uid, receiver=recipient, text=message_text, timestamp=str(datetime.now()))
        messagebox.showinfo("Success", "Message sent successfully!")
        self.load_received_messages()

    def load_received_messages(self):
        """Fetch and display received messages, but only show unread messages when requested."""
        self.clear_screen()
        self.create_nav_buttons()

        self.current_page = "received"  # Track the current page to stay on Received after deletion

        self.home_frame = tk.Frame(self.root)
        self.home_frame.pack(fill=tk.BOTH, expand=True)

        response = communication.build_and_send_task(self.sock, "get-received-messages", sender=self.client_uid)
        mids = response["mids"]

        self.unread_messages = []
        self.read_messages = []
        
        for mid in mids:
            msg_response = communication.build_and_send_task(self.sock, "get-message-by-mid", mid=mid)
            message = msg_response["message"]
            if message["receiver_read"]:
                self.read_messages.append(message)
            else:
                self.unread_messages.append(message)

        # Sort messages so newest ones appear first
        self.read_messages.sort(key=lambda x: x["timestamp"], reverse=True)
        self.unread_messages.sort(key=lambda x: x["timestamp"], reverse=True)

        unread_count = len(self.unread_messages)

        control_frame = tk.Frame(self.home_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        self.unread_label = tk.Label(control_frame, text=f"{unread_count} unread messages", font=("Arial", 14, "bold"))
        self.unread_label.pack(side=tk.LEFT, padx=5)

        self.num_messages_var = tk.IntVar(value=1)
        self.num_messages_dropdown = tk.Spinbox(control_frame, from_=1, to=unread_count if unread_count > 0 else 1, textvariable=self.num_messages_var, width=5)
        self.num_messages_dropdown.pack(side=tk.LEFT, padx=5)

        tk.Button(control_frame, text="Get N Unread", command=self.fetch_unread_messages, bg="blue", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Delete Selected", command=self.delete_selected_messages, bg="red", fg="white").pack(side=tk.RIGHT, padx=5)

        self.messages_frame = tk.Frame(self.home_frame)
        self.messages_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Display only read messages initially
        for message in self.read_messages:
            self.display_message(self.messages_frame, message, received=True)
    
    def fetch_unread_messages(self):
        """Displays the next N unread messages as requested by the user while keeping existing ones."""
        num_to_fetch = self.num_messages_var.get()

        if not self.unread_messages:
            messagebox.showinfo("Info", "No more unread messages.")
            return

        # Fetch up to the requested number of unread messages
        messages_to_display = self.unread_messages[:num_to_fetch]

        # Insert new messages at the top instead of appending at the bottom
        for message in (messages_to_display):  # Display newest unread messages first
            self.display_message(self.messages_frame, message, received=True)

        self.unread_messages = self.unread_messages[num_to_fetch:]  # Keep previously loaded unread messages

        self.unread_label.config(text=f"{len(self.unread_messages)} unread messages")
        self.num_messages_dropdown.config(to=len(self.unread_messages) if len(self.unread_messages) > 0 else 1)

    def load_sent_messages(self):
        """Fetch and display sent messages with checkboxes for deletion, newest messages on top."""
        self.clear_screen()
        self.create_nav_buttons()

        self.current_page = "sent"  # Track the current page to stay on Sent after deletion

        self.home_frame = tk.Frame(self.root)
        self.home_frame.pack(fill=tk.BOTH, expand=True)

        # "Delete Selected" button at the top
        control_frame = tk.Frame(self.home_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(control_frame, text="Delete Selected", command=self.delete_selected_messages, bg="red", fg="white").pack(side=tk.RIGHT, padx=5)

        response = communication.build_and_send_task(self.sock, "get-sent-messages", sender=self.client_uid)
        mids = response["mids"]

        self.messages_frame = tk.Frame(self.home_frame)
        self.messages_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Fetch and display messages in reverse order (newest first)
        messages = []
        for mid in mids:
            msg_response = communication.build_and_send_task(self.sock, "get-message-by-mid", mid=mid)
            messages.append(msg_response["message"])

        for message in reversed(messages):  # Newest messages first
            self.display_message(self.messages_frame, message, received=False)

    def display_message(self, parent, message, received=True):
        """Displays a single message in the UI and tracks its ID for selective updates."""
        frame = tk.Frame(parent, bg="lightgray", padx=5, pady=5)
        frame.pack(fill=tk.X, pady=5)
        frame.message_mid = message["mid"]  # Store message ID for updates

        sender = "From" if received else "To"
        status = "🔴" if received and not message["receiver_read"] else ""

        header = f"{status} {sender} {message['sender'] if received else message['receiver']}\n{message['timestamp']}"
        tk.Label(frame, text=header, font=("Arial", 10), bg="lightgray").pack(anchor="w")

        tk.Label(frame, text=message["text"], font=("Arial", 12), bg="white", padx=5, pady=5).pack(fill=tk.X)

        btn_frame = tk.Frame(frame, bg="lightgray")
        btn_frame.pack(fill=tk.X)

        if received:
            mark_read_btn = tk.Button(btn_frame, text="Mark as Read", command=lambda: self.mark_message_read(message["mid"]), bg="green", fg="white")
            mark_read_btn.pack(side=tk.RIGHT, padx=5)
            if message["receiver_read"]:
                mark_read_btn.config(state=tk.DISABLED)

        # Replace delete button with a checkbox
        delete_var = tk.BooleanVar()
        checkbox = tk.Checkbutton(btn_frame, variable=delete_var, command=lambda: self.toggle_selection(message["mid"], delete_var))
        checkbox.pack(side=tk.RIGHT, padx=5)
        tk.Label(btn_frame, text="Select to Delete", font=("Arial", 10), bg="lightgray").pack(side=tk.RIGHT, padx=5)

    def toggle_selection(self, mid, var):
        """Tracks selected messages for deletion using checkboxes."""
        if var.get():
            self.selected_messages.add(mid)
        else:
            self.selected_messages.discard(mid)


    def delete_selected_messages(self):
        """Deletes selected messages and refreshes only the current page."""
        if not self.selected_messages:
            messagebox.showerror("Error", "No messages selected for deletion.")
            return

        client_messages.delete_messages(self.sock, list(self.selected_messages), self.client_uid)
        self.selected_messages.clear()

        # Stay on the correct page after deleting
        if self.current_page == "sent":
            self.load_sent_messages()
        else:  # If it's not Sent, assume it's Received
            self.load_received_messages()

    def mark_message_read(self, mid):
        """Marks a message as read without refreshing the entire page."""
        client_messages.mark_message_read(self.sock, mid)

        # Find the message and update its status
        for widget in self.messages_frame.winfo_children():
            if hasattr(widget, "message_mid") and widget.message_mid == mid:
                for sub_widget in widget.winfo_children():
                    if isinstance(sub_widget, tk.Label) and "🔴" in sub_widget.cget("text"):
                        sub_widget.config(text=sub_widget.cget("text").replace("🔴", ""))  # Remove unread indicator
                    if isinstance(sub_widget, tk.Button) and sub_widget.cget("text") == "Mark as Read":
                        sub_widget.config(state=tk.DISABLED)  # Disable the Mark as Read button
                break

        # Update unread message count
        self.unread_messages = [msg for msg in self.unread_messages if msg["mid"] != mid]
        self.unread_label.config(text=f"{len(self.unread_messages)} unread messages")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def clear_content(self):
        """Clears content inside home_frame to prevent 'AttributeError'."""
        if hasattr(self, "home_frame") and isinstance(self.home_frame, tk.Frame):
            for widget in self.home_frame.winfo_children():
                widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()

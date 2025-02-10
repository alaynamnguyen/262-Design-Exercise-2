import tkinter as tk
from tkinter import messagebox
from controller import communication

class ClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Client GUI")
        self.sock = None  # Initialize the socket connection elsewhere
        self.client_uid = None  # Initialize the client UID elsewhere
        self.home_frame = tk.Frame(self.root)
        self.home_frame.pack(fill=tk.BOTH, expand=True)

    def load_received_messages(self):
        """Fetch and display received messages."""
        self.clear_content()
        self.create_nav_buttons()

        response = communication.build_and_send_task(self.sock, "get-received-messages", sender=self.client_uid)
        mids = response["mids"]

        self.messages_frame = tk.Frame(self.home_frame)  # Use self.home_frame
        self.messages_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        unread_count = 0

        for mid in mids:
            msg_response = communication.build_and_send_task(self.sock, "get-message-by-mid", mid=mid)
            message = msg_response["message"]

            if not message["receiver_read"]:
                unread_count += 1

            # Display the message
            msg_text = f"From: {message['sender']}\nTo: {message['receiver']}\nMessage: {message['text']}\nTimestamp: {message['timestamp']}\nRead: {message['receiver_read']}"
            tk.Label(self.messages_frame, text=msg_text, anchor="w", justify="left").pack(fill=tk.X, padx=10, pady=5)

        # Display unread count
        tk.Label(self.messages_frame, text=f"Unread messages: {unread_count}", anchor="w", justify="left").pack(fill=tk.X, padx=10, pady=5)

    def clear_content(self):
        """Clear the content of the home frame."""
        if self.home_frame:
            for widget in self.home_frame.winfo_children():
                widget.destroy()

    def create_nav_buttons(self):
        """Create navigation buttons."""
        nav_frame = tk.Frame(self.home_frame)
        nav_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(nav_frame, text="Received Messages", command=self.load_received_messages).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="Sent Messages", command=self.load_sent_messages).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="New Message", command=self.load_new_message).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="Deleted Messages", command=self.load_deleted_messages).pack(side=tk.LEFT, padx=5)

    def load_sent_messages(self):
        """Fetch and display sent messages."""
        self.clear_content()
        self.create_nav_buttons()

        response = communication.build_and_send_task(self.sock, "get-sent-messages", sender=self.client_uid)
        mids = response["mids"]

        self.messages_frame = tk.Frame(self.home_frame)  # Use self.home_frame
        self.messages_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        for mid in mids:
            msg_response = communication.build_and_send_task(self.sock, "get-message-by-mid", mid=mid)
            message = msg_response["message"]

            # Display the message
            msg_text = f"From: {message['sender']}\nTo: {message['receiver']}\nMessage: {message['text']}\nTimestamp: {message['timestamp']}\nRead: {message['receiver_read']}"
            tk.Label(self.messages_frame, text=msg_text, anchor="w", justify="left").pack(fill=tk.X, padx=10, pady=5)

    def load_new_message(self):
        """Load the new message screen."""
        self.clear_content()
        self.create_nav_buttons()
        # Add new message form here

    def load_deleted_messages(self):
        """Load the deleted messages screen."""
        self.clear_content()
        self.create_nav_buttons()
        # Add deleted messages display here

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientGUI(root)
    root.mainloop()
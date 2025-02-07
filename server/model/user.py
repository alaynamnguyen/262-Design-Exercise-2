import uuid
from server.read_write import *
import json

class User:
    """
    A class to represent a user.

    Attributes:
    ----------
    username : str
        The username of the user.
    password : str
        The password of the user.
    messages : set
        A set to store user message IDs.
    """

    def __init__(self, username, password, uid=None):
        """
        Constructs all the necessary attributes for the user object.

        Parameters:
        ----------
        username : str
            The username of the user.
        password : str
            The password of the user.
        """
        self.uid = uid if uid else str(uuid.uuid4())
        self.username = username
        self.password = password
        self.messages = list()

    def add_messages(self, message_id):
        """
        Adds a message ID to the user's messages.

        Parameters:
        ----------
        message_id : str
            The ID of the message to be added.
        """
        self.messages.add(message_id)

    def get_messages(self):
        """
        Retrieves all message IDs from the user's messages.

        Returns:
        -------
        set
            A set of all message IDs.
        """
        return self.messages

    def remove_message(self, message_id):
        """
        Removes a message ID from the user's messages.

        Parameters:
        ----------
        message_id : str
            The ID of the message to remove.
        """
        self.messages.discard(message_id)

    def __repr__(self):
        """
        Returns a string representation of the user.
        """
        return f"User(id={self.uid}, username={self.username}, messages={self.messages})"
    
if __name__ == "__main__":
    import hashlib

    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    usernames = ['yinan', 'alayna', 'jim', 'alex']
    users = dict()
    for username in usernames:
        user = User(username, hash_password(f"{username}_pass"))
        users[user.uid] = user

    with open("server/data/user.json", "w") as f:
        json.dump(users, f, default=object_to_dict_recursive, indent=4) 



import uuid
import json

# Recursive function for object to dict
def object_to_dict_recursive(obj):
    """Recursively converts objects to dictionaries."""
    if hasattr(obj, "__dict__"):
        return {key: object_to_dict_recursive(value) for key, value in vars(obj).items()}
    return obj

# Recursive function for dict to object
def dict_to_object_recursive(dct, cls):
    """Converts a dictionary back to an object of type cls."""
    obj = cls.__new__(cls)  # Create an empty instance
    for key, value in dct.items():
        setattr(obj, key, dict_to_object_recursive(value, globals().get(cls.__name__, object)) if isinstance(value, dict) else value)
    return obj

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

    def __init__(self, username, password, uid=None, active=True):
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
        self.received_messages = list()
        self.sent_messages = list()
        self.active = active

    def __repr__(self):
        """
        Returns a string representation of the user.
        """
        return f"User(uid={self.uid}, username={self.username}, password={self.password}, received_messages={self.received_messages}, sent_messages={self.sent_messages}, active={self.active})"
    
if __name__ == "__main__":
    import hashlib

    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    usernames = ['yinan', 'alayna', 'jim', 'alex']
    users = dict()
    for username in usernames:
        user = User(username, hash_password(f"{username}_pass"))
        users[user.uid] = user

    with open("server/data/message.json", "r") as f:
        messages = json.load(f)
    for user in users.values():
        for mid, message in messages.items():
            if message["sender"] == user.username:
                user.sent_messages.append(mid)
            if message["receiver"] == user.username:
                user.received_messages.append(mid)

    print(users)
    print()
    with open("server/data/user.json", "w") as f:
        json.dump(users, f, default=object_to_dict_recursive, indent=4)

    with open("server/data/user.json", "r") as f:
        users = json.load(f)

    print(users)

    users_dict = dict()
    for k, v in users.items():
        user = dict_to_object_recursive(v, User)
        users_dict[user.uid] = user
    print(users)


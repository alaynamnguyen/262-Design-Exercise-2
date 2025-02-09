from datetime import datetime
import uuid

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

class Message:
    def __init__(self, sender, receiver, text, mid=None, timestamp=None, receiver_read=False):
        """
        Initializes a new message.

        Args:
            sender (str): The sender of the message.
            receiver (str): The receiver of the message.
            text (str): The text content of the message.
            mid (int): The unique identifier of the message.
            timestamp (datetime, optional): The time the message was sent. Defaults to current time.
            receiver_read (bool, optional): Whether the receiver has read the message. Defaults to False.
        """
        self.sender = sender
        self.receiver = receiver
        self.text = text
        self.mid = mid if mid else str(uuid.uuid4())
        self.timestamp = str(timestamp if timestamp else datetime.now())  # Convert to string for JSON serialization
        self.receiver_read = receiver_read

    def mark_as_read(self):
        """
        Marks the message as read by the receiver.
        """
        self.receiver_read = True

    def __repr__(self):
        """
        Returns a string representation of the message.
        """
        return (f"Message(mid={self.mid}, sender={self.sender}, receiver={self.receiver}, "
                f"timestamp={self.timestamp}, text={self.text}, receiver_read={self.receiver_read})")
    
if __name__ == "__main__":
    import hashlib
    import json

    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    senders = ['yinan', 'alayna', 'jim', 'alex']  # NOTE: Dummy code, actual code uses uid instead of username
    receivers = ['alayna', 'yinan', 'alex', 'jim']
    texts = list()
    for sender, receiver in zip(senders, receivers):
        texts.append(f"{sender}->{receiver} hi sent at {datetime.now().replace(microsecond=0)}")

    messages_dict = dict()
    for sender, receiver, text in zip(senders, receivers, texts):
        message = Message(sender=sender, receiver=receiver, text=text)
        messages_dict[message.mid] = message
    print(messages_dict)
    print()

    with open("server/data/message.json", "w") as f:
        json.dump(messages_dict, f, default=object_to_dict_recursive, indent=4)
        
    with open("server/data/message.json", "r") as f:
        messages = json.load(f)
    print(messages)
    print()

    messages_dict = dict()
    for k, v in messages.items():
        message = dict_to_object_recursive(v, Message)
        messages_dict[message.mid] = message
    print(messages_dict)
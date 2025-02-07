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
    def __init__(self, sender, receiver, text, id, timestamp=None, receiver_read=False):
        """
        Initializes a new message.

        Args:
            sender (str): The sender of the message.
            receiver (str): The receiver of the message.
            text (str): The text content of the message.
            id (int): The unique identifier of the message.
            timestamp (datetime, optional): The time the message was sent. Defaults to current time.
            receiver_read (bool, optional): Whether the receiver has read the message. Defaults to False.
        """
        self.sender = sender
        self.receiver = receiver
        self.text = text
        self.id = id if id else str(uuid.uuid4())
        self.timestamp = timestamp if timestamp else datetime.now()
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
        return (f"Message(id={self.id}, sender={self.sender}, receiver={self.receiver}, "
                f"timestamp={self.timestamp}, text={self.text}, receiver_read={self.receiver_read})")
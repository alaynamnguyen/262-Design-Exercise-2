from datetime import datetime
import uuid

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
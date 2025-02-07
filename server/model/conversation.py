from .message import Message

class Conversation:
    """
    A class to represent a conversation between two users.

    Attributes:
    ----------
    messages : list
        A list to store messages in this conversation.
    """

    def __init__(self, conversation_id):
        """
        Initializes a new conversation.

        Args:
            conversation_id (int): The unique identifier of the conversation.
        """
        self.conversation_id = conversation_id # TODO: Add description that this is a tuple of the two users or something
        self.messages = []

    def add_message(self, message):
        """
        Adds a message to the conversation.

        Args:
            message (Message): The message to add.
        """
        if isinstance(message, Message):
            self.messages.append(message)
        else:
            raise TypeError("Expected a Message object")

    def get_messages(self):
        """
        Returns the list of messages in the conversation.

        Returns:
            list: The list of messages.
        """
        return self.messages

    def __repr__(self):
        """
        Returns a string representation of the conversation.
        """
        return f"Conversation(conversation_id={self.conversation_id}, messages={self.messages})"
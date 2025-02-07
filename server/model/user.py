import uuid

class User:
    """
    A class to represent a user.

    Attributes:
    ----------
    username : str
        The username of the user.
    password : str
        The password of the user.
    conversations : set
        A set to store user conversation IDs.
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
        self.conversations = set()

    def add_conversation(self, conversation_id):
        """
        Adds a conversation ID to the user's conversations.

        Parameters:
        ----------
        conversation_id : str
            The ID of the conversation to be added.
        """
        self.conversations.add(conversation_id)

    def get_conversations(self):
        """
        Retrieves all conversation IDs from the user's conversations.

        Returns:
        -------
        set
            A set of all conversation IDs.
        """
        return self.conversations

    def remove_conversation(self, conversation_id):
        """
        Removes a conversation ID from the user's conversations.

        Parameters:
        ----------
        conversation_id : str
            The ID of the conversation to remove.
        """
        self.conversations.discard(conversation_id)

    def __repr__(self):
        """
        Returns a string representation of the user.
        """
        return f"User(id={self.uid}, username={self.username}, conversations={self.conversations})"
    
    # def object_to_dict_recursive(obj):
    # """Recursively converts objects to dictionaries, handling nested objects."""
    # if hasattr(obj, "__dict__"):
    #     return {key: object_to_dict_recursive(value) for key, value in vars(obj).items()}
    # elif isinstance(obj, list):  # Handle lists of objects
    #     return [object_to_dict_recursive(item) for item in obj]
    # elif isinstance(obj, dict):  # Handle dictionaries with objects as values
    #     return {key: object_to_dict_recursive(value) for key, value in obj.items()}
    # else:
    #     return obj  # Return primitive types unchanged
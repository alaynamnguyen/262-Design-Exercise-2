from model import Message

def send_message(sender_uid, receiver_username, text, users_dict, messages_dict, timestamp): 
    """
    Sends a message to the server.

    Args:
        message (dict): The message to send to the server.
    """

    receiver_uid = None
    for uid, user in users_dict.items():
        if user.username == receiver_username:
            receiver_uid = uid

    if receiver_uid is None:
        print("Receiver does not exist.")
        return False

    # Create message object, receiver_read is False by default
    message = Message(sender=sender_uid, receiver=receiver_uid, text=text, timestamp=timestamp)
    
    # Update runtime storage
    messages_dict[message.mid] = message
    users_dict[sender_uid].sent_messages.append(message.mid)
    users_dict[receiver_uid].received_messages.append(message.mid)

    # TODO: Wrap with try-except?
    # TODO: Send to receiver if receiver online

    return True

def get_sent_messages_id(uid, users_dict):
    """
    Gets the message IDs of the messages sent by the user.

    Args:
        uid (str): The unique identifier of the user.
        users_dict (dict): The dictionary of users.

    Returns:
        list: The list of message IDs.
    """
    return users_dict[uid].sent_messages

def get_received_messages_id(uid, users_dict):
    """
    Gets the message IDs of the messages received by the user.

    Args:
        uid (str): The unique identifier of the user.
        users_dict (dict): The dictionary of users.

    Returns:
        list: The list of message IDs.
    """
    return users_dict[uid].received_messages

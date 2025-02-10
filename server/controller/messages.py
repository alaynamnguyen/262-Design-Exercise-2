from model import Message
from utils import dict_to_object_recursive, object_to_dict_recursive

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
    print("Message id:", message.mid)

    # Update runtime storage
    messages_dict[message.mid] = message
    users_dict[sender_uid].sent_messages.append(message.mid)
    users_dict[receiver_uid].received_messages.append(message.mid)

    # TODO: Wrap with try-except?
    # TODO: Send to receiver if receiver online

    return True

def delete_messages(users_dict, messages_dict, mids):
    deleted_mids = []
    success = True
    for mid in mids:
        if mid in messages_dict:
            message = messages_dict[mid]
            # Remove message from sender
            users_dict[message.sender].sent_messages.remove(mid)
            # Remove message from receiver
            users_dict[message.receiver].received_messages.remove(mid)
            # Remove message from messages_dict
            del messages_dict[mid]
            deleted_mids.append(mid)
        else:
            print(f"Message {mid} does not exist.")
            success = False

    return success, deleted_mids

def mark_message_read(messages_dict, mid):
    if mid in messages_dict:
        messages_dict[mid].receiver_read = True
        return True
    else:
        print(f"Failed to mark message read: message {mid} does not exist.")
        return False
    
def get_message_by_mid(mid, messages_dict):
    """
    Gets the message by its unique identifier.

    Args:
        mid (str): The unique identifier of the message.
        messages_dict (dict): The dictionary of messages.

    Returns:
        Message: The message object.
    """
    if mid in messages_dict:
        return object_to_dict_recursive(messages_dict[mid]) # Convert to dict
    else:
        print(f"Message {mid} does not exist.")
        return None  # TODO Handle missing message case
    
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

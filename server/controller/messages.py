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


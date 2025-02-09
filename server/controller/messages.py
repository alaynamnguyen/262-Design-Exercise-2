from model import Message

def send_message(sender, receiver, text, users_dict, messages_dict, timestamp): 
    """
    Sends a message to the server.

    Args:
        message (dict): The message to send to the server.
    """

    # Create message object, receiver_read is False by default
    message = Message(sender=sender, receiver=receiver, text=text, timestamp=timestamp)
    
    sender_id = None
    receiver_id = None
    for uid, user in users_dict.items():
        if user.username == sender:
            sender_id = uid
        if user.username == receiver:
            receiver_id = uid

    if sender_id is None or receiver_id is None:
        return False
    
    # Update runtime storage
    messages_dict[message.mid] = message
    users_dict[sender_id].sent_messages.append(message.mid)
    users_dict[receiver_id].received_messages.append(message.mid)

    # TODO: Wrap with try-except?
    # TODO: Send to receiver if receiver online

    return True


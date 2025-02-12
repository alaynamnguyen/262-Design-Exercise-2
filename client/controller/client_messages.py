from .communication import build_and_send_task

def delete_messages(sock, mids, client_uid, use_wire_protocol):
    """
    Sends a request to delete specified messages from the server.

    Args:
        sock (socket.socket): The active socket connection to the server.
        mids (list of str): A list of message IDs (MIDs) to be deleted.
        client_uid (str): The user ID of the client requesting the deletion.
        use_wire_protocol (bool): If True, uses the wire protocol for communication; otherwise, JSON format is used.

    Returns:
        None: Prints a success or failure message based on the server response.
    """
    print("Calling delete_messages")
    response = build_and_send_task(sock, "delete-messages", use_wire_protocol, mids=mids, uid=client_uid)

    if response["success"]:
        print("Messages successfully deleted")
        return
    else:
        print("Failed to delete messages.")
        return # UI does not change
    
def mark_message_read(sock, mid, use_wire_protocol):
    """
    Sends a request to mark a specific message as read.

    Args:
        sock (socket.socket): The active socket connection to the server.
        mid (str): The message ID (MID) of the message to mark as read.
        use_wire_protocol (bool): If True, uses the wire protocol for communication; otherwise, JSON format is used.

    Returns:
        None: Prints a confirmation message if the message is successfully marked as read.
    """
    print("Calling mark_message_read")
    response = build_and_send_task(sock, "mark-message-read", use_wire_protocol, mid=mid)

    if response["success"]:
        print("Message marked as read.")
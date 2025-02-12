from .communication import build_and_send_task

def list_accounts(sock, wildcard, use_wire_protocol):
    """
    Retrieves a list of accounts from the server that match a specified wildcard pattern.

    Args:
        sock (socket.socket): The active socket connection to the server.
        wildcard (str): A search pattern to filter accounts (e.g., "a*" to list accounts starting with "a").
        use_wire_protocol (bool): If True, uses the wire protocol for communication; otherwise, JSON format is used.

    Returns:
        None: The function prints the retrieved account list if any accounts are found.
    """
    print("Calling list_accounts")
    response = build_and_send_task(sock, "list-accounts", use_wire_protocol, wildcard=wildcard)
    
def delete_account(sock, uid, use_wire_protocol):
    """
    Requests account deletion from the server for a specified user ID.

    Args:
        sock (socket.socket): The active socket connection to the server.
        uid (str): The unique user ID of the account to be deleted.
        use_wire_protocol (bool): If True, uses the wire protocol for communication; otherwise, JSON format is used.

    Returns:
        dict: The response from the server indicating success or failure of the deletion request.
    """
    print("Calling delete_account")
    response = build_and_send_task(sock, "delete-account", use_wire_protocol, uid=uid)
    # print("Response:", response)
    return response

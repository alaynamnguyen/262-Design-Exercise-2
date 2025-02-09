import json

def send_message(sock, message):
    """
    Sends a JSON message to the server and receives a response.

    Args:
        sock (socket.socket): The socket connected to the server.
        message (dict): The message to send to the server.

    Returns:
        dict: The response from the server.
    """
    sock.sendall(json.dumps(message).encode("utf-8"))
    response = sock.recv(1024).decode("utf-8")
    print("Response from server: ", response)
    return json.loads(response)

def build_and_send_task(sock, task, **kwargs):
    """
    Builds a task message and sends it to the server.

    Args:
        sock (socket.socket): The socket connected to the server.
        task (str): The task to perform.
        kwargs: Additional keyword arguments to include in the message.

    Returns:
        dict: The response from the server.
    """
    message = {"task": task}
    message.update(kwargs)
    return send_message(sock, message)
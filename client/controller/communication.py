from utils import send_request, receive_response

def build_and_send_task(sock, task, use_wire_protocol, **kwargs):
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
    send_request(sock, message, use_wire_protocol)
    return receive_response(sock, use_wire_protocol)
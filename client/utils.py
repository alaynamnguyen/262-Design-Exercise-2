import json
import hashlib

# Define task to opcode mappings
opcode_to_task = {
    "a": "login-username",
    "b": "login-username-reply",
    "c": "login-password",
    "d": "login-password-reply",
}

task_to_opcode = {v: k for k, v in opcode_to_task.items()}

def json_to_wire_protocol(json_message):
    """Encodes JSON message into wire protocol format."""
    wire_message = task_to_opcode[json_message["task"]]

    if json_message["task"] == "login-username":
        wire_message += json_message["username"]

    elif json_message["task"] == "login-username-reply":
        user_exists = "T" if json_message["user_exists"] else "F"
        wire_message += user_exists + json_message["username"]

    elif json_message["task"] == "login-password":
        username_length = f'{len(json_message["username"]):02}'
        wire_message += username_length + json_message["username"] + json_message["password"]

    elif json_message["task"] == "login-password-reply":
        login_success = "T" if json_message["login_success"] else "F"
        wire_message += login_success + json_message["uid"]

    else:
        raise NotImplementedError(f"Unsupported task: {json_message['task']}")

    print("Wire message constructed:", wire_message)
    return wire_message.encode("utf-8")

def wire_protocol_to_json(wire_message):
    """Decodes wire protocol message into JSON format."""
    wire_message = wire_message.decode("utf-8")
    print("Wire message received:", wire_message)
    json_message = {"task": opcode_to_task[wire_message[0]]}

    if json_message["task"] == "login-username":
        json_message["username"] = wire_message[1:]

    elif json_message["task"] == "login-username-reply":
        json_message["user_exists"] = wire_message[1] == "T"
        json_message["username"] = wire_message[2:]

    elif json_message["task"] == "login-password":
        username_length = int(wire_message[1:3])
        json_message["username"] = wire_message[3 : username_length + 3]
        json_message["password"] = wire_message[username_length + 3:]

    elif json_message["task"] == "login-password-reply":
        json_message["login_success"] = wire_message[1] == "T"
        json_message["uid"] = wire_message[2:]

    else:
        raise NotImplementedError(f"Unsupported wire protocol task: {wire_message[0]}")

    return json_message

def send_request(sock, json_message, use_wire_protocol):
    print("Use wire protocol:", use_wire_protocol, type(use_wire_protocol))
    print(json_message)
    """Sends a JSON message, encoding it to wire protocol if needed."""
    if use_wire_protocol:
        print("Using wire protocol")
        encoded_message = json_to_wire_protocol(json_message)
    else:
        print("Using JSON protocol")
        encoded_message = json.dumps(json_message).encode("utf-8")
    sock.sendall(encoded_message)

def receive_response(sock, use_wire_protocol):
    """Receives a response, decoding from wire protocol if needed."""
    response_data = sock.recv(1024)
    if use_wire_protocol:
        return wire_protocol_to_json(response_data)
    return json.loads(response_data.decode("utf-8"))

def hash_password(password):
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

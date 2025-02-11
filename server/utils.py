opcode_to_task = {
    "a": "login-username",
    "b": "login-username-reply",
    "c": "login-password",
    "d": "login-password-reply",
}

task_to_opcode = dict()
for k, v in opcode_to_task.items():
    task_to_opcode[v] = k

def json_to_wire_protocol(json_message):
    wire_message = f"{task_to_opcode[json_message['task']]}"

    if json_message["task"] == "login-username":
        wire_message += json_message["username"]

    elif json_message["task"] == "login-username-reply":
        user_exists = str(json_message["user_exists"])[0]
        wire_message += user_exists + \
            str(json_message["username"])

    elif json_message["task"] == "login-password":
        username_length = f'{len(json_message["username"]):02}'
        wire_message += username_length + \
            json_message["username"] + \
            json_message["password"]
        
    elif json_message["task"] == "login-password-reply":
        login_success = str(json_message["login_success"])[0]
        # Note len(uuid) = 36
        wire_message += login_success + \
            json_message["uid"] + \
            ",".join(json_message["unread_messages"])
        
    else:
        raise NotImplementedError

    return wire_message

def wire_protocol_to_json(wire_message):
    json_message = {
        "task": opcode_to_task[wire_message[0]]
    }

    if json_message["task"] == "login-username":
        json_message["username"] = wire_message[1:]

    elif json_message["task"] == "login-username-reply":
        json_message["user_exists"] = (wire_message[1] == "T")
        json_message["username"] = wire_message[2:]

    elif json_message["task"] == "login-password":
        username_length = int(wire_message[1:3])
        json_message["username"] = wire_message[3:username_length+3]
        json_message["password"] = wire_message[username_length+3:]
    
    elif json_message["task"] == "login-password-reply":
        json_message["login_success"] = (wire_message[1] == "T")
        json_message["uid"] = wire_message[2: 2+36]
        json_message["unread_messages"] = wire_message[2+36:].split(",")

    else:
        raise NotImplementedError
    
    return json_message

# Recursive function for object to dict
def object_to_dict_recursive(obj):
    """Recursively converts objects to dictionaries."""
    if hasattr(obj, "__dict__"):
        return {key: object_to_dict_recursive(value) for key, value in vars(obj).items()}
    return obj

# Recursive function for dict to object
def dict_to_object_recursive(dct, cls):
    """Converts a dictionary back to an object of type cls."""
    obj = cls.__new__(cls)  # Create an empty instance
    for key, value in dct.items():
        setattr(obj, key, dict_to_object_recursive(value, globals().get(cls.__name__, object)) if isinstance(value, dict) else value)
    return obj

if __name__ == "__main__":
    # wire_m = json_to_wire_protocol(
    #     {
    #         "task": "login-username-reply",
    #         "username": "yinan",
    #         "user_exists": False
    #     })
    
    # wire_m = json_to_wire_protocol(
    #     {
    #         "task": "login-password",
    #         "username": "yinan",
    #         "password": "abracadabra"
    #     })

    wire_m = json_to_wire_protocol(
        {
            "task": "login-password-reply",
            "uid": "90c20039-0057-49f2-95d5-7682ba0777d3",
            "login_success": True,
            "unread_messages": ["ae3c13a9-7678-4229-9761-de29f8f85a11",
                                "6bac3754-b1ba-4381-9718-afde00234ff3"]
        })
    
    print(wire_m)
    
    json_m = wire_protocol_to_json(wire_m)
    print(json_m)
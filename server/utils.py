import json 

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

# Utility Functions for JSON/Wire Protocol Handling
def send_response(data, response, USE_WIRE_PROTOCOL):
    """Encapsulates response handling for JSON or wire protocol."""
    if USE_WIRE_PROTOCOL:
        pass
        # encoded_response = encode_to_wire_protocol(response)  # TODO update, Placeholder for wire protocol
    else:
        encoded_response = json.dumps(response).encode("utf-8")

    data.outb += encoded_response

def parse_request(data, USE_WIRE_PROTOCOL):
    """Encapsulates request handling for JSON or wire protocol."""
    if USE_WIRE_PROTOCOL:
        pass
        # return decode_wire_protocol(data.inb) # TODO update, Placeholder for wire protocol decoding
    return json.loads(data.inb.decode("utf-8"))

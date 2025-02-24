from utils import send_request, receive_response
import sys
import grpc
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import chat_pb2
import chat_pb2_grpc

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

def delete_messages(server_address, uid, mids):
    with grpc.insecure_channel(server_address) as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)
        request = chat_pb2.DeleteMessagesRequest(uid=uid, mids=mids)
        response = stub.DeleteMessages(request)

        response_dict = dict()
        response_dict["success"] = response.success

        return response_dict

def send_message(server_address, sender, receiver_username, text, timestamp):
    with grpc.insecure_channel(server_address) as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)
        request = chat_pb2.SendMessageRequest(sender=sender, receiver_username=receiver_username, text=text, timestamp=timestamp)
        response = stub.SendMessage(request)

        response_dict = dict()
        response_dict["success"] = response.success

        return response_dict

def list_accounts(server_address, wildcard):
    with grpc.insecure_channel(server_address) as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)
        request = chat_pb2.ListAccountsRequest(wildcard=wildcard)
        response = stub.ListAccounts(request)

        response_dict = dict()
        response_dict["accounts"] = response.accounts

        return response_dict
    
def delete_account(server_address, uid):
    with grpc.insecure_channel(server_address) as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)
        request = chat_pb2.DeleteAccountRequest(uid=uid)
        response = stub.DeleteAccount(request)

        response_dict = dict()
        response_dict["success"] = response.success

        return response_dict
    
def mark_message_read(server_address, mid):
    with grpc.insecure_channel(server_address) as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)
        request = chat_pb2.MarkMessageReadRequest(mid=mid)
        response = stub.MarkMessageRead(request)

        response_dict = dict()
        response_dict["success"] = response.success

        return response_dict

def get_messages(server_address, client_uid):
    with grpc.insecure_channel(server_address) as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)
        request = chat_pb2.GetMessagesRequest(uid=client_uid)
        response = stub.GetReceivedMessages(request)
        
        message = dict()
        message["mids"] = response.mids

        return message

def get_message_by_mid(server_address, mid):
    with grpc.insecure_channel(server_address) as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)
        request = chat_pb2.GetMessageRequest(mid=mid)
        response = stub.GetMessageByMid(request)

        message = dict()
        message["sender"] = response.sender_uid
        message["receiver"] = response.receiver_uid
        message["mid"] = mid
        message["timestamp"] = response.timestamp
        message["receiver_read"] = response.receiver_read
        message["sender_username"] = response.sender_username
        message["receiver_username"] = response.receiver_username
        message["text"] = response.text
        
        return message
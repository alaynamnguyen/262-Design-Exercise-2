import pytest
import os
import sys
import grpc
from concurrent import futures
import time
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import server_proto
import chat_pb2
import chat_pb2_grpc

logging.basicConfig(level=logging.INFO)

# ---------------- FIXTURES ---------------- #

@pytest.fixture(scope="module")
def grpc_server():
    """
    Fixture to set up a test gRPC server.
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(server_proto.ChatService(), server)
    
    port = "127.0.0.1:50052"
    server.add_insecure_port(port)
    server.start()
    
    time.sleep(1)
    
    yield server
    server.stop(None)


@pytest.fixture(scope="module")
def grpc_channel(grpc_server):
    """
    Fixture to set up a gRPC channel for communication.
    """
    channel = grpc.insecure_channel("127.0.0.1:50052")
    yield channel
    channel.close()


@pytest.fixture
def grpc_stub(grpc_channel):
    """
    Fixture to provide a gRPC client stub for testing.
    """
    return chat_pb2_grpc.ChatServiceStub(grpc_channel)


@pytest.fixture
def create_test_users(grpc_stub):
    """
    Fixture to ensure a sender and receiver exist before running a test.
    Returns sender UID and receiver username.
    """
    sender_username = "test_user"
    sender_password = "test_password"
    receiver_username = "receiver_user"
    receiver_password = "receiver_password"

    # Ensure sender exists and fetch the actual UID
    check_request = chat_pb2.LoginUsernameRequest(username=sender_username)
    check_response = grpc_stub.LoginUsername(check_request)

    if not check_response.user_exists:
        create_request = chat_pb2.LoginPasswordRequest(username=sender_username, password=sender_password)
        create_response = grpc_stub.LoginPassword(create_request)
        assert create_response.success
        sender_uid = create_response.uid
    else:
        login_request = chat_pb2.LoginPasswordRequest(username=sender_username, password=sender_password)
        login_response = grpc_stub.LoginPassword(login_request)
        assert login_response.success
        sender_uid = login_response.uid

    # Ensure receiver exists
    check_request_receiver = chat_pb2.LoginUsernameRequest(username=receiver_username)
    check_response_receiver = grpc_stub.LoginUsername(check_request_receiver)

    if not check_response_receiver.user_exists:
        create_request_receiver = chat_pb2.LoginPasswordRequest(username=receiver_username, password=receiver_password)
        create_response_receiver = grpc_stub.LoginPassword(create_request_receiver)
        assert create_response_receiver.success

    return sender_uid, receiver_username


# ---------------- TEST SEND MESSAGE ---------------- #

def test_send_message_valid(grpc_stub, create_test_users):
    """
    Test sending a message from one user to another.
    """
    sender_uid, receiver_username = create_test_users

    logging.info(f"Users before SendMessage call: Sender UID: {sender_uid}, Receiver: {receiver_username}")

    request = chat_pb2.SendMessageRequest(
        sender=sender_uid,
        receiver_username=receiver_username,
        text="Hello!",
        timestamp="2025-02-24 14:00:00"
    )
    response = grpc_stub.SendMessage(request)
    
    assert response.success


# ---------------- TEST ACCOUNT CREATION ---------------- #

def test_create_account_valid(grpc_stub):
    """
    Test creating a new account.
    """
    new_username = "new_user"
    new_password = "new_password"

    check_request = chat_pb2.LoginUsernameRequest(username=new_username)
    check_response = grpc_stub.LoginUsername(check_request)

    assert not check_response.user_exists

    create_request = chat_pb2.LoginPasswordRequest(username=new_username, password=new_password)
    create_response = grpc_stub.LoginPassword(create_request)

    assert create_response.success
    assert create_response.uid is not None


# ---------------- TEST LOGIN ---------------- #

def test_login_valid_password(grpc_stub):
    """
    Test logging in with the correct password.
    """
    test_username = "valid_user"
    test_password = "correct_password"

    create_request = chat_pb2.LoginPasswordRequest(username=test_username, password=test_password)
    create_response = grpc_stub.LoginPassword(create_request)
    assert create_response.success
    test_uid = create_response.uid

    login_request = chat_pb2.LoginPasswordRequest(username=test_username, password=test_password)
    login_response = grpc_stub.LoginPassword(login_request)

    assert login_response.success
    assert login_response.uid == test_uid


def test_login_wrong_password(grpc_stub):
    """
    Test logging in with an incorrect password.
    """
    test_username = "wrong_password_user"
    correct_password = "correct_password"
    wrong_password = "incorrect_password"

    create_request = chat_pb2.LoginPasswordRequest(username=test_username, password=correct_password)
    create_response = grpc_stub.LoginPassword(create_request)
    assert create_response.success

    login_request = chat_pb2.LoginPasswordRequest(username=test_username, password=wrong_password)
    login_response = grpc_stub.LoginPassword(login_request)

    assert not login_response.success


# ---------------- TEST GET SENT MESSAGES ---------------- #

def test_get_sent_messages_valid(grpc_stub, create_test_users):
    """
    Test retrieving sent messages.
    """
    sender_uid, receiver_username = create_test_users

    get_sent_request = chat_pb2.GetMessagesRequest(uid=sender_uid)
    get_sent_response = grpc_stub.GetSentMessages(get_sent_request)

    assert len(get_sent_response.mids) > 0

    message_mid = get_sent_response.mids[0]
    get_message_request = chat_pb2.GetMessageRequest(mid=message_mid)
    get_message_response = grpc_stub.GetMessageByMid(get_message_request)

    assert get_message_response.text == "Hello!"
    assert get_message_response.sender_uid == sender_uid
    assert get_message_response.receiver_username == receiver_username


